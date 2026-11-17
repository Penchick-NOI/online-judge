import io
import json
import os
import sys
import tarfile
import tempfile
import zipfile

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from judge.models import Language, Problem, ProblemData, ProblemGroup, ProblemTestCase, ProblemType, Profile
from judge.utils.pnoi_problem_files import ProblemFolder, find_problem_folders
from judge.utils.problem_data import ProblemDataCompiler


class ImportFailed(Exception):
    pass


class Command(BaseCommand):
    help = ('Load PNOI problem folders (problem.yml, statement.md, tests/) into the site. Give a folder, or "-" to '
            'read a tar archive from standard input. See docs/pnoi/problem-files.md.')

    def add_arguments(self, parser):
        parser.add_argument('path', help='a folder of problem folders, or - to read a tar archive from stdin')
        parser.add_argument('--only', nargs='+', metavar='CODE', help='only these problem codes')
        parser.add_argument('--check', action='store_true', help='only check the folders; change nothing')

    def handle(self, *args, **options):
        if options['path'] == '-':
            with tempfile.TemporaryDirectory() as tmp:
                with tarfile.open(fileobj=sys.stdin.buffer, mode='r|*') as tar:
                    tar.extractall(tmp, filter='data')
                return self.run(tmp, options)
        if not os.path.isdir(options['path']):
            raise CommandError('Not a folder: %s' % options['path'])
        return self.run(options['path'], options)

    def run(self, root, options):
        problems = [ProblemFolder(path) for path in find_problem_folders(root)]
        if options['only']:
            wanted = set(options['only'])
            problems = [p for p in problems if p.code in wanted]
            for code in sorted(wanted - {p.code for p in problems}):
                self.stderr.write('No folder for problem %s.' % code)
        if not problems:
            raise CommandError('No problem folders (folders with a problem.yml) found.')

        seen = {}
        for problem in problems:
            if problem.code in seen:
                problem.fail('Another folder has the same problem code: %s.' % seen[problem.code])
            seen.setdefault(problem.code, problem.path)

        done = failed = 0
        for problem in problems:
            if not problem.ok:
                failed += 1
                self.stdout.write(self.style.ERROR('FAIL %s' % problem.code))
                for message in problem.errors:
                    self.stdout.write('  error: ' + message)
                self.write_notes(problem.warnings)
                continue
            if options['check']:
                done += 1
                self.stdout.write(self.style.SUCCESS('OK   %s (%d tests)' % (problem.code, len(problem.tests))))
                self.write_notes(problem.warnings)
                continue
            try:
                created, notes = self.import_problem(problem)
            except ImportFailed as e:
                failed += 1
                self.stdout.write(self.style.ERROR('FAIL %s' % problem.code))
                self.stdout.write('  error: %s' % e)
                continue
            done += 1
            self.stdout.write(self.style.SUCCESS('%s %s (%d tests)' % (
                'NEW  ' if created else 'UPDATED', problem.code, len(problem.tests))))
            self.write_notes(problem.warnings + notes)

        verb = 'checked' if options['check'] else 'loaded'
        self.stdout.write('\n%d problem(s) %s, %d failed.' % (done, verb, failed))
        if failed:
            raise CommandError('Some problems were not %s; see the errors above.' % verb)

    def write_notes(self, notes):
        for message in notes:
            self.stdout.write('  note: ' + message)

    @transaction.atomic
    def import_problem(self, folder):
        config = folder.config
        notes = []

        group, made = ProblemGroup.objects.get_or_create(name=config.get('group', 'practice'),
                                                         defaults={'full_name': config.get('group', 'practice')})
        if made:
            notes.append('new problem group "%s" created; give it a proper name in the admin pages.' % group.name)
        types = []
        for name in config['types']:
            problem_type, made = ProblemType.objects.get_or_create(name=name, defaults={'full_name': name})
            if made:
                notes.append('new problem type "%s" created; give it a proper name in the admin pages.' % name)
            types.append(problem_type)

        problem = Problem.objects.filter(code=folder.code).first()
        created = problem is None
        if created:
            problem = Problem(code=folder.code)
        problem.name = config['name'].strip()
        problem.description = folder.statement
        problem.summary = config.get('summary', '')
        problem.time_limit = config['time_limit']
        problem.memory_limit = config['memory_limit'] * 1024
        problem.group = group
        problem.partial = True
        problem.is_manually_managed = False
        problem.difficulty_estimate = config.get('difficulty')
        if config.get('points') is not None:
            problem.points = config['points']
        if 'public' in config:
            problem.is_public = config['public']
        problem.save()   # Problem.save() sets the points from the difficulty.

        problem.types.set(types)

        languages = list(Language.objects.filter(key__in=config['languages']))
        missing = set(config['languages']) - {lang.key for lang in languages}
        if missing:
            notes.append('unknown language keys skipped: %s.' % ', '.join(sorted(missing)))
        if not languages:
            raise ImportFailed('none of the languages in "languages" exist on this site.')
        problem.allowed_languages.set(languages)

        if config['authors']:
            profiles = list(Profile.objects.filter(user__username__in=config['authors']))
            unknown = set(config['authors']) - {p.user.username for p in profiles}
            if unknown:
                notes.append('no account yet for author(s) %s; add them later by importing again.' %
                             ', '.join(sorted(unknown)))
            if profiles:
                problem.authors.set(profiles)

        self.import_tests(problem, folder)
        return created, notes

    def import_tests(self, problem, folder):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
            for _, inp, out in folder.tests:
                archive.write(folder.file('tests', inp), inp)
                archive.write(folder.file('tests', out), out)
        files = [name for _, inp, out in folder.tests for name in (inp, out)]

        data, _ = ProblemData.objects.get_or_create(problem=problem)
        data.zipfile.save('tests.zip', ContentFile(buffer.getvalue()), save=False)
        data.checker = folder.config.get('checker', 'standard')
        data.checker_args = json.dumps(folder.config['checker_args']) if folder.config.get('checker_args') else ''
        data.generator = None
        data.save()

        ProblemTestCase.objects.filter(dataset=problem).delete()
        ProblemTestCase.objects.bulk_create([
            ProblemTestCase(dataset=problem, order=order, type=kind, input_file=inp, output_file=out,
                            points=points, is_pretest=False)
            for order, (kind, inp, out, points) in enumerate(folder.cases(), 1)
        ])

        ProblemDataCompiler.generate(problem, data, problem.cases.order_by('order'), files)
        data.refresh_from_db()
        if data.feedback:
            raise ImportFailed('the test data could not be set up: %s' % data.feedback)
