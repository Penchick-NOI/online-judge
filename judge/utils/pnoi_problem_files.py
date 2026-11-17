"""Read and check PNOI problem folders.

A problem folder looks like this (see docs/pnoi/problem-files.md):

    sumtwo/
        problem.yml      name, limits, difficulty, subtasks ...
        statement.md     the statement students read (Markdown)
        tests/           test files in pairs: 1.in + 1.out, sample.in + sample.out, ...

This module only needs Python and PyYAML, so it can also run on its own (for example in the problems
repository's GitHub check) without the rest of the site:

    python3 pnoi_problem_files.py path/to/problems
"""
import fnmatch
import io
import os
import re
import sys

import yaml

CODE_RE = re.compile(r'^[a-z0-9]{1,20}$')
ID_RE = re.compile(r'^[a-z0-9_-]{1,20}$')
CHECKERS = ('standard', 'floats', 'floatsabs', 'floatsrel', 'rstripped', 'sorted', 'identical', 'linecount')
DEFAULT_LANGUAGES = ['CPP17', 'CPP20', 'PY3']
DIFFICULTY_RANGE = (800, 3500)
KNOWN_KEYS = {
    'name', 'authors', 'group', 'types', 'time_limit', 'memory_limit', 'difficulty', 'points', 'public',
    'checker', 'checker_args', 'languages', 'subtasks', 'summary',
}
MAX_TEST_BYTES = 256 * 1024 * 1024


def natural_key(name):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r'(\d+)', name)]


class ProblemFolder:
    """One problem folder, read and checked. ``errors`` lists everything wrong with it."""

    def __init__(self, path):
        self.path = path
        self.code = os.path.basename(os.path.normpath(path))
        self.errors = []
        self.warnings = []
        self.config = {}
        self.statement = ''
        self.tests = []      # [(name, input file, output file)], in judging order
        self.batches = []    # [(points, [test names])]; empty means every test is its own case
        self._read()

    # ---------------------------------------------------------------- helpers
    def fail(self, message):
        self.errors.append(message)

    @property
    def ok(self):
        return not self.errors

    def file(self, *parts):
        return os.path.join(self.path, *parts)

    # ---------------------------------------------------------------- reading
    def _read(self):
        if not CODE_RE.match(self.code):
            self.fail('The folder name "%s" is not a valid problem code: use only lowercase letters a-z and '
                      'digits 0-9, at most 20 characters.' % self.code)

        self._read_config()
        self._read_statement()
        self._read_tests()
        if self.tests:
            self._read_subtasks()

    def _read_config(self):
        try:
            with io.open(self.file('problem.yml'), encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            self.fail('problem.yml is missing.')
            return
        except (yaml.YAMLError, UnicodeDecodeError) as e:
            self.fail('problem.yml could not be read: %s' % str(e).replace('\n', ' '))
            return
        if not isinstance(config, dict):
            self.fail('problem.yml should be a list of "key: value" lines.')
            return
        self.config = config

        for key in sorted(set(config) - KNOWN_KEYS):
            self.fail('problem.yml: unknown setting "%s" (check the spelling).' % key)

        name = config.get('name')
        if not isinstance(name, str) or not name.strip():
            self.fail('problem.yml: "name" (the problem title) is required.')
        elif len(name) > 100:
            self.fail('problem.yml: "name" is longer than 100 characters.')

        time_limit = config.get('time_limit')
        if not isinstance(time_limit, (int, float)) or isinstance(time_limit, bool) or not 0 < time_limit <= 60:
            self.fail('problem.yml: "time_limit" is required, in seconds, between 0 and 60 '
                      '(for example 1 or 2.5).')

        memory_limit = config.get('memory_limit')
        if not isinstance(memory_limit, int) or isinstance(memory_limit, bool) or not 16 <= memory_limit <= 2048:
            self.fail('problem.yml: "memory_limit" is required, in megabytes, between 16 and 2048 '
                      '(for example 256).')

        difficulty = config.get('difficulty')
        points = config.get('points')
        if difficulty is not None:
            if not isinstance(difficulty, int) or isinstance(difficulty, bool) or \
                    not DIFFICULTY_RANGE[0] <= difficulty <= DIFFICULTY_RANGE[1]:
                self.fail('problem.yml: "difficulty" must be a whole number from %d to %d.' % DIFFICULTY_RANGE)
        elif points is None:
            self.fail('problem.yml: give "difficulty" (your estimate, for example 1200); points come from it.')
        if points is not None and (not isinstance(points, (int, float)) or isinstance(points, bool) or points <= 0):
            self.fail('problem.yml: "points" must be a number above 0.')

        group = config.get('group', 'practice')
        if not isinstance(group, str) or not ID_RE.match(group):
            self.fail('problem.yml: "group" must be a short ID such as pnoi2026 '
                      '(lowercase letters, digits, - or _).')

        types = config.get('types', [])
        if isinstance(types, str):
            types = [types]
        if not isinstance(types, list) or not types or \
                not all(isinstance(t, str) and ID_RE.match(t) for t in types):
            self.fail('problem.yml: "types" must list at least one topic ID, for example [greedy, math].')
        else:
            config['types'] = types

        authors = config.get('authors', [])
        if isinstance(authors, str):
            authors = [authors]
        if not isinstance(authors, list) or not all(isinstance(a, str) for a in authors):
            self.fail('problem.yml: "authors" must list PNOI usernames, for example [juan, maria].')
        else:
            config['authors'] = authors

        if 'public' in config and not isinstance(config['public'], bool):
            self.fail('problem.yml: "public" must be true or false.')

        checker = config.get('checker', 'standard')
        if checker not in CHECKERS:
            self.fail('problem.yml: "checker" must be one of: %s.' % ', '.join(CHECKERS))
        if 'checker_args' in config and not isinstance(config['checker_args'], dict):
            self.fail('problem.yml: "checker_args" must be a list of "key: value" settings, '
                      'for example {precision: 6}.')

        languages = config.get('languages', DEFAULT_LANGUAGES)
        if not isinstance(languages, list) or not languages or not all(isinstance(x, str) for x in languages):
            self.fail('problem.yml: "languages" must list language keys, for example [CPP17, CPP20, PY3].')
        else:
            config['languages'] = languages

        if 'summary' in config and not isinstance(config['summary'], str):
            self.fail('problem.yml: "summary" must be text.')

    def _read_statement(self):
        try:
            with io.open(self.file('statement.md'), encoding='utf-8') as f:
                self.statement = f.read()
        except FileNotFoundError:
            self.fail('statement.md is missing.')
            return
        except UnicodeDecodeError:
            self.fail('statement.md is not saved as UTF-8 text.')
            return
        if not self.statement.strip():
            self.fail('statement.md is empty.')

    def _read_tests(self):
        folder = self.file('tests')
        if not os.path.isdir(folder):
            self.fail('The tests folder is missing.')
            return
        names = os.listdir(folder)
        inputs = {n[:-3] for n in names if n.endswith('.in')}
        outputs = {n[:-4] for n in names if n.endswith('.out')}
        for name in sorted(inputs - outputs, key=natural_key):
            self.fail('tests/%s.in has no matching tests/%s.out.' % (name, name))
        for name in sorted(outputs - inputs, key=natural_key):
            self.fail('tests/%s.out has no matching tests/%s.in.' % (name, name))
        for name in sorted(names, key=natural_key):
            if not name.endswith(('.in', '.out')) and not name.startswith('.'):
                self.warnings.append('tests/%s is ignored (only .in and .out files are used).' % name)

        both = inputs & outputs
        # Samples first, then the rest in natural order (1, 2, ..., 10, 11).
        ordered = sorted(both, key=lambda n: (not n.lower().startswith('sample'), natural_key(n)))
        total = 0
        for name in ordered:
            if not re.match(r'^[A-Za-z0-9_.-]{1,90}$', name):
                self.fail('tests/%s.in: test names may only use letters, digits, ".", "-" and "_".' % name)
                continue
            for ext in ('.in', '.out'):
                total += os.path.getsize(os.path.join(folder, name + ext))
            self.tests.append((name, name + '.in', name + '.out'))
        if not both and not self.errors:
            self.fail('The tests folder has no test pairs (for example 1.in and 1.out).')
        if total > MAX_TEST_BYTES:
            self.fail('The test files add up to more than 256 MB.')

    def _read_subtasks(self):
        subtasks = self.config.get('subtasks')
        if subtasks is None:
            return
        if not isinstance(subtasks, list) or not subtasks:
            self.fail('problem.yml: "subtasks" must be a list (see the example in the guide).')
            return
        names = [t[0] for t in self.tests]
        used = set()
        for i, subtask in enumerate(subtasks, 1):
            if not isinstance(subtask, dict) or set(subtask) - {'points', 'tests'}:
                self.fail('problem.yml: subtask %d needs exactly "points" and "tests".' % i)
                continue
            points = subtask.get('points')
            if not isinstance(points, int) or isinstance(points, bool) or points < 0:
                self.fail('problem.yml: subtask %d: "points" must be a whole number, 0 or more.' % i)
            patterns = subtask.get('tests')
            if isinstance(patterns, str):
                patterns = [patterns]
            if not isinstance(patterns, list) or not all(isinstance(p, (str, int)) for p in patterns):
                self.fail('problem.yml: subtask %d: "tests" must list test names, for example ["1-*"].' % i)
                continue
            matched = []
            for pattern in map(str, patterns):
                found = [n for n in names if fnmatch.fnmatchcase(n, pattern)]
                if not found:
                    self.fail('problem.yml: subtask %d: no test matches "%s".' % (i, pattern))
                matched.extend(n for n in found if n not in matched)
            if matched:
                self.batches.append((points, matched))
                used.update(matched)
        for name in names:
            if name not in used:
                self.warnings.append('test %s (tests/%s.in and .out) is in no subtask, so it is not used.' %
                                     (name, name))
        if self.ok and sum(p for p, _ in self.batches) <= 0:
            self.fail('problem.yml: the subtasks are worth 0 points in total.')

    # ---------------------------------------------------------------- output
    def cases(self):
        """The test data as (type, input, output, points) rows, in the site's test-case format."""
        if not self.batches:
            return [('C', inp, out, 1) for _, inp, out in self.tests]
        files = {name: (inp, out) for name, inp, out in self.tests}
        rows = []
        for points, names in self.batches:
            rows.append(('S', '', '', points))
            rows.extend(('C', files[n][0], files[n][1], None) for n in names)
            rows.append(('E', '', '', None))
        return rows


def find_problem_folders(root):
    """Every folder under ``root`` that contains a problem.yml (folders starting with "_" or "." are skipped)."""
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith(('.', '_')) and d != 'tests')
        if 'problem.yml' in filenames:
            found.append(dirpath)
            dirnames[:] = []
    return found


def main(argv):
    root = argv[1] if len(argv) > 1 else '.'
    folders = find_problem_folders(root)
    if not folders:
        print('No problem folders (folders with a problem.yml) found under %s.' % root)
        return 1
    codes = {}
    bad = 0
    for path in folders:
        problem = ProblemFolder(path)
        if problem.code in codes:
            problem.add_error('Another folder has the same problem code: %s.' % codes[problem.code])
        codes.setdefault(problem.code, path)
        print('%s %s (%d tests)' % ('OK  ' if problem.ok else 'FAIL', problem.code, len(problem.tests)))
        for message in problem.errors:
            print('     error: ' + message)
        for message in problem.warnings:
            print('     note:  ' + message)
        bad += not problem.ok
    print('\n%d problem(s) checked, %d with errors.' % (len(folders), bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
