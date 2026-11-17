# Problem files

The problem-setting team writes problems as **folders of files** in the private GitHub repository
`Penchick-NOI/pnoi-problems`. The site owner then loads them into PNOI with one command. Teammates need no
account on the site and no access to the owner's computer, and the same folders will load into the real server
once PNOI is hosted.

This page is the full reference for the folder format. The problems repository's README has a short how-to for
teammates.

## The folder

Each problem is one folder inside `problems/`. **The folder's name is the problem code**: lowercase letters `a`–`z`
and digits `0`–`9`, at most 20 characters. It becomes the web address, so `problems/sumtwo` becomes
`/problem/sumtwo`.

```
problems/
  sumtwo/
    problem.yml     settings: name, limits, difficulty, subtasks
    statement.md    the statement students read
    tests/
      sample.in     test files, in pairs: every .in has a .out with the same name
      sample.out
      1-1.in
      1-1.out
      ...
```

Folders whose names start with `_` (such as `_template`) are skipped, so they can hold templates and examples.

## problem.yml

```yaml
name: Sum of Two           # the title students see (required)
authors: [juan, maria]     # PNOI usernames of the setters
group: pnoi2026            # problem group ID (default: practice)
types: [math, greedy]      # topic IDs, at least one (required)
time_limit: 1              # seconds (required)
memory_limit: 256          # megabytes (required)
difficulty: 1200           # your estimate, 800 to 3500 (required)
public: false              # true makes it visible to students as soon as it is loaded
```

| Setting | Meaning |
| --- | --- |
| `name` | The title, up to 100 characters. |
| `authors` | Usernames on PNOI. They are listed as the problem's authors and, with the Problem setters role, can edit it on the site. Names without an account yet are skipped with a note; load the problem again once the account exists. |
| `group` | A short ID such as `pnoi2026`. A group that does not exist yet is created; give it a proper name in the admin pages afterwards. |
| `types` | Topic IDs such as `math`, `greedy`, `dp`. New ones are created like groups. |
| `time_limit` | In seconds, for example `1` or `2.5`. For rated rounds use **2 to 3 times** your own solution's time. |
| `memory_limit` | In megabytes, for example `256`. |
| `difficulty` | Your estimate on the rating scale (800 easiest, 3500 hardest). Points come from it (difficulty ÷ 100). After a rated contest the site replaces it with the measured difficulty. |
| `public` | `true` or `false`. Leave it out to keep whatever the site already has. |
| `subtasks` | Optional; see below. |

Rarely needed:

| Setting | Meaning |
| --- | --- |
| `checker` | How answers are compared. `standard` (the default) ignores extra spaces and blank lines at the end. Others: `floats`, `floatsabs`, `floatsrel` (decimal answers), `identical` (byte for byte), `sorted`, `linecount`, `rstripped`. |
| `checker_args` | Settings for the checker, for example `{precision: 6}` for `floats`. |
| `languages` | Which languages may be used. Default: `[CPP17, CPP20, PY3]`. |
| `summary` | A one-line summary shown in some lists. |
| `points` | Only for a problem without `difficulty`. |

## statement.md

The statement in Markdown, the same as in the admin pages (see [Adding a problem](adding-a-problem.md#part-1-create-the-problem)):
`## Input` for headings, `**bold**`, maths between `~` signs such as `~1 \le N \le 10^5~`, and samples in code
blocks between lines of three backticks. Write the samples into the statement yourself; the test files are never
shown to students.

## tests/

- Every test is a pair: `NAME.in` (what the program reads) and `NAME.out` (the correct answer).
- Names may use letters, digits, `.`, `-` and `_`.
- Tests whose names start with `sample` are judged first; the rest follow in natural order (`2` before `10`).
- Other files in the folder are ignored.
- All test files together must be under 256 MB.

**Without subtasks**, every test is worth the same and students get partial points for the tests they pass.

**With subtasks** (IOI style), a subtask's points are given only if **every** test in it passes:

```yaml
subtasks:
  - points: 30
    tests: ["sample", "1-*"]   # the sample and every test whose name starts with 1-
  - points: 70
    tests: ["2-*"]
```

`*` matches anything, so `1-*` matches `1-1`, `1-2`, `1-10`. A test can be in more than one subtask. A test in no
subtask is not used (the check says so). The subtask points are shares of the problem: a student who passes only
the first subtask above gets 30% of the problem's points.

## Checking the folders

Every change pushed to the problems repository is checked automatically on GitHub (the **Actions** tab shows a
green tick or a red cross with the reasons). To check on your own computer, with Python and PyYAML installed:

```bash
python3 pnoi_problem_files.py problems
```

The checker is [`judge/utils/pnoi_problem_files.py`](../../judge/utils/pnoi_problem_files.py) in this repository.

## Loading the problems into the site (owner)

On the owner's computer, in WSL:

1. Get the latest problems. The first time:

   ```bash
   git clone https://github.com/Penchick-NOI/pnoi-problems.git /srv/pnoi-docker/pnoi-problems
   ```

   After that:

   ```bash
   git -C /srv/pnoi-docker/pnoi-problems pull
   ```

2. Load them:

   ```bash
   cd /srv/pnoi-docker/dmoj
   tar -C ../pnoi-problems -cf - problems | docker compose exec -T site python3 manage.py pnoi_import_problems -
   ```

   Add `--only sumtwo othercode` to load only some problems, or `--check` to check without changing anything.

The command prints `NEW`, `UPDATED` or `FAIL` for each problem, with the reasons for any failure. A problem that
fails is left as it was; the others still load.

Loading again **updates** a problem: its name, statement, limits, difficulty estimate, test data and subtasks are
replaced by what is in the folder. So make changes in the repository, not on the site, or they will be overwritten
the next time. Submissions made before a test data change keep their old scores until they are rejudged (as staff,
on the problem's page click **Manage submissions**, then rejudge them).
