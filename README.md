# PNOI — Penchick National Olympiad in Informatics

PNOI is a competitive programming platform for the Philippines: a problem
archive, an automatic judge, and online contests, in the spirit of Codeforces
and AtCoder.

**Status:** early development. The site currently runs only on a development
machine; there is no public instance yet.

## Plans

- Regular rated rounds with full-solve scoring
- IOI-style tasks with subtasks and partial scoring, later
- C++ and Python at launch
- A clean, modern PNOI look in light and dark mode
- Features for Philippine schools and regions

## Built on DMOJ

PNOI is a fork of [DMOJ: Modern Online Judge](https://github.com/DMOJ/online-judge),
the open-source judge and contest system that has hosted several national
olympiads. Judging uses the [DMOJ judge server](https://github.com/DMOJ/judge-server).
Thank you to the DMOJ team and contributors.

## Running it locally

PNOI runs on Linux. The development setup uses
[dmoj-docker](https://github.com/Ninjaclasher/dmoj-docker) with this repository
in place of `dmoj/repo`; see that project and the
[DMOJ documentation](https://docs.dmoj.ca/) for installation.

## License

Like DMOJ, PNOI is licensed under the
[GNU Affero General Public License v3.0](LICENSE). If you run a modified
version as a website, you must make your modified source code available to
its users.
