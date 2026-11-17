# PNOI shared notes for AI assistants

This file is the shared memory between the AI assistants working on PNOI (currently **Claude** and **Devin**) and the
project owner (**@lrnnz**). The assistants cannot see each other's chats, so anything the other one needs to know
goes here.

**Every assistant, every session:**

1. Read this whole file before doing anything.
2. Follow it. If the owner tells you something that contradicts it, do what the owner says and update this file in
   the same pull request.
3. When you finish a piece of work, update [Current status](#current-status) and add a line to the
   [Work log](#work-log). When the owner tells you a lasting preference or decision, add it to
   [Decisions the owner has made](#decisions-the-owner-has-made).
4. Keep this file factual and short. No secrets, passwords, email addresses or personal details, ever.

---

## What PNOI is

**PNOI (Penchick National Olympiad in Informatics)** is a competitive programming website for the Philippines: a
place where students solve programming problems, join timed rated contests and climb a leaderboard.

- **Inspiration:** Codeforces and AtCoder. Like them, PNOI runs regular rated rounds, has a problem archive, ratings
  and rating colours. AtCoder's cleanliness is the standard for clarity. Kattis and AtCoder are the reference for
  list pages with a filter panel at the side.
- **But it must not look like any of them, and above all not like DMOJ.** PNOI is built on DMOJ's code, and the owner
  has rejected every design that still resembled DMOJ. PNOI has its own identity.
- **Audience:** Filipino students, mostly in elementary and high school (Grade 4 to Grade 12), plus some college
  students, and the teachers and organisers who run contests for them. Many are beginners and many are minors.
  Many will use a phone. Design and write for them:
  - plain, friendly English; no jargon without explanation;
  - Philippine context by default: Philippine time (`Asia/Manila`), schools, grade levels and regions on profiles,
    school rankings;
  - ask for as little personal information as possible, keep it optional, and let students hide it.
- **Contest style:** rated Codeforces/AtCoder-style rounds first. IOI-style subtasks and partial scoring are
  supported (the judge has them) and matter for olympiad training.
- **Languages students can submit in:** C++17, C++20 and Python 3 only.
- **Stage:** not launched. It runs only on the owner's computer. There is no launch date. The eventual hosting budget
  is about $5 to $15 a month. The repository is public.

## The owner

- Knows competitive programming well. Is a **beginner** at GitHub, web development and running a website.
- Explain what you did and why in plain words. Give exact steps when the owner has to do something.
- Likes to **choose from options**: for any new look or layout, show two or three mock-ups or screenshots and let the
  owner pick. Do not pick a new design direction yourself.
- Reviews and merges every pull request personally.

## Roles

- **Claude** is the main assistant. It works on the owner's computer, where the full site runs with a real judge, so
  it can test things end to end. It reviews and tests what Devin has done, keeps the overall direction consistent,
  and handles anything touching the local setup, the judge, data or settings.
- **Devin** helps when the owner hands it a task, usually while Claude is unavailable. Typical tasks: rebuilding a
  page in the PNOI design, writing documentation. Devin works from the repository only and cannot see the owner's
  local site, so it must say clearly in each pull request what it could not test.
- **Taking turns:** only one assistant works at a time. Never work on a page or file that has an open pull request
  from the other assistant. Start every task from the latest `master`.
- **The owner** decides everything about direction and design.

## Rules

1. Work on a branch and open a pull request against **`Penchick-NOI/online-judge`, branch `master`**. Never open a
   pull request against `DMOJ/online-judge` (GitHub suggests it by default because this is a fork). Never push to
   `master`.
2. One pull request per task. The description says what changed, what was tested, and what was **not** tested.
   Include screenshots for anything visual, at desktop and phone width.
3. Never commit secrets, passwords, or `dmoj/local_settings.py`, `uwsgi.ini`, `websocket/config.js`. Never commit
   problem test data.
4. Keep the visible **Source code** link in the footer. The licence (AGPL-3.0) requires it.
5. Do not delete branches, files or data you did not create, unless the owner says so.
6. Do not upgrade Django or other dependencies, merge from `DMOJ/online-judge`, or change how contestant code is run,
   unless the owner asks. Contestant code is untrusted; it must only ever run inside DMOJ's own judge sandbox.
7. Hosting, domain, email and deployment are for later and only when the owner asks.
8. If something is unclear, ask the owner.

## The design: "Araw"

*Araw* is Tagalog for "sun" (and "day"). The look is warm, bright and proudly Filipino: the blue, red and sun-yellow
of the Philippine flag on a warm cream page.

### What the owner wants it to feel like

- **Unique to PNOI.** Not a recoloured DMOJ. When a page still has DMOJ's structure, rebuild its markup; do not just
  restyle it.
- **Rich and impressive, not plain.** The owner's words: the site should be "less underwhelming". Use the colours
  boldly; give pages real structure (cards, panels, stats, side panels). An empty-looking page is a failure.
- **Still clear.** AtCoder-level readability. Students must find the problem, the submit button and their result
  immediately.

### Colours, type and shapes

All of these are CSS variables at the top of `resources/pnoi.scss`. Use the variables, never raw colour codes.

| Role | Variable | Value |
| --- | --- | --- |
| Page background (warm cream) | `--pn-bg` | `#fffbf2` |
| Cards and panels | `--pn-surface` | `#ffffff` |
| Text | `--pn-text` | `#1b2440` |
| Muted text | `--pn-muted` | `#6b6f80` |
| Blue: links, headings, primary identity | `--pn-blue` | `#1d3a8a` |
| Red: the main action button, errors | `--pn-red` | `#d7263d` |
| Sun yellow: highlights, avatar ring | `--pn-yellow` | `#f9b916` |
| Green: accepted / success | `--pn-green` | `#1e8e5a` |
| Lines | `--pn-line`, `--pn-line-strong` | `#e6dabd`, `#cdbb8f` |

- **Type:** serif display font for page titles (`--pn-display`), system sans for everything else (`--pn-sans`),
  monospace for code and problem codes (`--pn-mono`). No web fonts are loaded.
- **Outlines:** every card (`.pn-card`) has a tan outline (`--pn-line-strong`) and a soft shadow (`--pn-shadow`),
  and box titles sit on a cream strip, so the parts of a page are easy to tell apart.
- **Shapes:** rounded cards (`--pn-radius`, 14px), pill-shaped tabs, buttons and verdict labels.
- **Light theme only** for now. There is no dark mode; do not add one unless asked.

### Layout

- **Slim dark icon rail** on the left (`.pn-rail`, dark navy): icon plus small label for each section, the user's
  picture and account menu at the bottom. On phones it becomes a bar along the bottom.
- **Home page is a dashboard:** next contest, the student's own rating and recent submissions, top users, past
  contests.
- **Problem page is a split workspace:** statement, submissions and details in tabs on the left; language choice,
  code editor, submit button and the live result on the right. Students submit without leaving the page.
- **List pages have a filter panel on the right** (problem list, submissions list), which folds behind a
  **Filters** button on phones. Use this pattern for any other long list.
- **Profile** has a card on the left (picture, name, school, grade, region, stats) and content on the right.
- Every page must work at phone width (about 375px) with no sideways scrolling.

## How the front end is built

- **`templates/base.html`** is the page skeleton, written for PNOI. Do not change it without the owner's say-so.
  The styling hook is `body[data-pn]` (the body's class attribute is overwritten by a script, so do not rely on it).
- **`resources/pnoi.scss`** holds the entire PNOI design. Classes start with `pn-`. Add new rules just above the
  line `// ---------------------------------------------------------------- legacy`. It is compiled by
  `make_style.sh`.
- **Rebuilt or not?** A rebuilt template contains `{% block legacy_css %}{% endblock %}`, which stops DMOJ's old
  stylesheet from loading on that page. A template without it still has the old layout. To rebuild a page: add that
  line, rewrite the markup with `pn-` classes, and check nothing on the page still depended on the old stylesheet.
- **Building blocks to reuse:** `.pn-card`, `.pn-panel`, `.pn-table`, `.pn-btn` (`pn-btn-red` for the one main
  action, `pn-btn-soft`, `pn-btn-sm`, `pn-btn-block`), `.pn-form`, `.pn-auth` (centred card for account pages),
  verdict pills `.pn-v pn-v-<result>`, pill tabs via `templates/tabs-base.html`, rating colours `.rate-*`.
  Dropdowns use select2 with `theme: 'default'`.
- **Avoid `<nav>` and `<footer>` elements** in templates; the old stylesheet styles them and breaks pages that are
  not rebuilt yet.
- **Good examples to copy from:** `templates/user/edit-profile.html`, `templates/contest/list.html`,
  `templates/problem/list.html`, `templates/registration/login.html`.
- **Back end:** Django 4.2 with Jinja2 templates. It must run on **Python 3.12**; the admin pages crash on
  Python 3.14. `django-admin-sortable2` is pinned below 2.3 for the same reason.
- **Site content that lives in the database** (languages, the About page, the welcome news post) is saved as fixtures in
  `judge/fixtures/` so a new server can load it.
- **PNOI's own profile fields:** `school`, `grade_class_year` (the year the student finishes Grade 12, so the grade
  moves up each June), `student_status`, `region`, `show_school`, in `judge/models/profile.py`.

## Decisions the owner has made

Newest last. Do not undo these without the owner's say-so.

- Build on a fork of DMOJ instead of writing a site from scratch.
- Rated rounds first; C++ and Python only.
- Finish the site's own design first, then guides, then content.
- Rejected, in order: a recoloured DMOJ ("Dagat" teal palette), a monospace grid restyle. Reason both times: still
  looked like DMOJ.
- Chose the **Araw** palette and look from three full concepts.
- Asked for the layout to be richer ("less underwhelming"), then chose: **dashboard layout with a slim dark icon
  rail**, and a split problem page.
- PNOI is for Filipino students, so profiles carry **school, grade level and region**. The organisations box and the
  default-language dropdown were removed from sign-up and edit profile.
- Sign-up asks for school details (optional); the leaderboard has a school column and per-school rankings.
- List pages (problems, submissions) use a **right-hand filter panel**; the statistics pie chart was removed from the
  submissions list.
- The site-theme choice and the time-zone map picker are hidden or removed; new accounts default to `Asia/Manila`.
- The users list is titled **Users** (not "Leaderboard"). It shows rank, rating, username, school and points: no
  profile pictures and no problems-solved count. Staff accounts (admins, organisers) are hidden from it; students
  with zero points still appear.
- Contests list: no big banner and no cards (the banner wasted space; cards would not fit many contests). Both
  **Upcoming** and **Past contests** are lists of rows. Running contests come first in Upcoming, labelled "Ongoing".
  Past contests have exactly three filters (Rated, Type, Joined). The page shows how many people joined each
  contest, keeps **Virtual join**, and uses friendly dates ("Sat, Nov 21 · 12:09 PM"). The **Calendar tab is
  hidden** until the calendar page is rebuilt.
- Contests are rated unless said otherwise: do not tag contests "rated"; tag the exceptions "unrated".
- Home page: no big banner, stat boxes or rating chart (the owner found the page full of wasted space). Main
  column: contests, Try next, your recent submissions. Right column: your own card (rating, rank, solved), or a
  Log in / Sign up card for visitors, then Top users and News.
- Staff accounts must never appear in rankings anywhere (users list, profile ranks, home page).
- On list pages the owner wants little-used filters tucked away, no sliders, and no verdict counts or statistics
  that could discourage students.
- News posts keep their comment section and show who wrote them. No Facebook/Twitter share buttons.
- The parts of a page must be obviously separate: cards have a darker tan outline, a soft shadow and a cream strip
  behind box titles (chosen from three options). The left rail and the footer were left as they are.
- Organizations: the Organizations page is just a simple list. Each organization's own page is its member
  leaderboard (chosen from ten options): name, a short description and the Join button on top, the ranked member
  table below, and a "Find members" panel on the right. The name "Organizations" is kept.
- **Students are ranked by contest rating**, like Codeforces and AtCoder, everywhere (users list, organization
  pages, home page, profile, school rank). A student who has not been rated yet has no rank and is listed after
  the rated ones. Practice points are still shown and can be sorted by, but do not rank anyone.
- **Verified badge:** a student is "Verified" (credible) automatically after `PNOI_VERIFIED_MIN_CONTESTS` (5) rated
  contests with a clean record. Any disqualification removes it. No manual approval.
- **Problem difficulty is calculated automatically**: the rating at which a contestant had a 50% chance of
  solving the problem in its contest (as Codeforces and AtCoder do). Until there is enough data, the setter's own
  estimate is shown, marked as an estimate (`~1200`). Built: `judge/utils/difficulty.py`, run when a contest
  is rated. Problem points are a separate, older number and are still entered by hand.
- **Organizations are groups of students** (clubs, training groups), not official schools. Any student can ask to
  start one; it appears only after the owner's team approves it. Built: `OrganizationProposal`, the page
  `/organizations/new`, and approve / reject actions in the admin pages.

## Current status

*Update this section when you finish work.*

**Rebuilt in the PNOI design:** home dashboard, problem list, problem page, submit page, submissions list, submission
result and source pages, contest list (upcoming list, past list with a filter panel), contest page, contest
scoreboard, users list (with a right-hand filter panel: search, region, sort), profile, edit profile, log in, sign up,
password and other account pages, About, single news post (with its comment section), organizations (the list, an
organization's page, asking to join).

**Still in DMOJ's old layout (to rebuild):** the organiser-only organisation pages (edit, manage members, review
join requests, class pages), tickets, contest statistics,
contest calendar (its tab is hidden; the page still exists at its address), status pages (judges, languages), two-
factor setup, "download your data", problem test data editor, problem editorial page. Comment sections are styled
for PNOI only inside `.pn-comments` (used on the news post); they are still left out of the rebuilt problem and
contest pages.

**Guides:** `docs/pnoi/` has tested organiser guides for adding a problem and running a contest.

**Known gaps:** the edit profile page scrolls sideways on phones; no dark mode; maths rendering (Mathoid) is
switched off; live updates show "disconnected" locally; no real problems or contests yet; staff accounts can still
appear on the organiser-only "Manage members" and class pages; the old `.pn-dash*` and
`.pn-stat*` rules in `pnoi.scss` are no longer used; `502.html` and `logo.png` at the repository root are still
DMOJ's; new interface text has no translations.

## Work log

*One line per finished piece of work: date, who, what, pull request.*

- 2026-11-14 to 15, Claude: Araw design, page skeleton and all student-facing pages (PRs 6 to 14).
- 2026-11-15, Devin: organiser guides (PR 15); problem list with right-hand filter panel (PR 16); submissions list
  with filter panel and day groups (PR 17).
- 2026-11-16, Claude: tested the guides end to end and corrected them; fixed the admin "Add contest" crash; default
  time zone set to Asia/Manila (PR 18). Added this file.
- 2026-11-16, Devin: users list retitled "Users", with a right-hand panel (search by username or school, region,
  sort), medals for the top three, staff accounts hidden, problems column removed (PR 20). Tested locally without
  a judge; organisation member lists were not checked.
- 2026-11-16, Devin: contests list rebuilt as an upcoming list (running contests first, labelled "Ongoing") + a
  past list with a Rated / Type / Joined panel; Calendar tab hidden; friendlier dates; "unrated" tag instead of "rated"
  (PR 21). Tested locally without a judge; pressing Join was not tried. The home page and the contest page still
  show a "rated" tag.
- 2026-11-16, Devin: home page rebuilt as lists on the left and your card, Top users and News on the right; staff
  hidden from Top users and from your rank (PR 22). Tested locally without a judge.
- 2026-11-16, Devin: About page fixed, same format: it no longer loads the old stylesheet and its text no longer
  runs off the screen on phones (PR 23). Applies to every flat page that uses `flatpages/markdown.html`.
- 2026-11-16, Claude: reviewed and tested PRs 20 to 23 on the full local site (filters, privacy of hidden schools,
  staff hidden, phone width). Follow-up fixes: phone bottom bar no longer cuts off labels; visitors see "Log in to
  join" instead of a greyed-out Join on the contests list; staff and unlisted accounts show no rank on their home
  card or profile. The contest page has no "rated" tag, only a sentence saying who the contest is rated for, which
  was kept. Not tried: pressing Join / Virtual join from the new list; widths below 375px.
- 2026-11-16, Devin: single news post rebuilt: article card with author and date, comments card (restyled, same
  markup and scripts as before), "More news" and upcoming contests on the right; Facebook/Twitter share buttons
  removed (PR 25). Tested locally: voting, replying, posting and editing a comment as a student, phone width. Not
  tried: staff moderation links (hide, votes, admin), locked comments, maths in posts.
- 2026-11-16, Devin: stronger outlines on every page: darker line colours, a soft shadow on cards, cream strips
  behind box titles (PR 26). Only `pnoi.scss` changed. Checked on the rebuilt pages at desktop and phone width.
  Noticed, not fixed: the edit profile page scrolls sideways on phones (the description editor's toolbar).
- 2026-11-16, Devin: organizations rebuilt: a simple list, an organization page that is its member leaderboard with
  a "Find members" panel (search, sort), and the "ask to join" form and its confirmation page (PR 27). Staff are
  left out of the member ranking and the member counts. Tested locally: join, leave, ask to join, search, phone
  width. Not tested: the organiser-only pages (left in the old layout), class requests, more than 100 members.
- 2026-11-17, Claude: reviewed and tested PRs 25 to 27 on the full local site (join, leave, ask to join, hidden
  schools, staff left out, phone width). Then: DMOJ's in-joke error messages for muted users and for users with no
  solved problem reworded in plain English; the local demo news post replaced by a "Welcome to PNOI" post (saved
  as `judge/fixtures/pnoi_news.json`), and the demo comment and the demo "DMOJ" organization deleted locally. Not
  tried: posting a comment as a student who has solved a problem. Still open: edit profile scrolls sideways on
  phones.
- 2026-11-17, Claude: users are now ranked by rating everywhere (users list, organization page, home "Top users"
  and own card, profile, school rank; unrated students show no rank); "Practice points" is the other sort.
  Verified badge added to profiles (`Profile.is_verified`), with "2 of 5 rated contests" progress on your own
  profile. Tested with temporary rated accounts. Not checked: phone width for the badge; the badge is on the
  profile page only, not next to names in lists.
- 2026-11-17, Claude: automatic problem difficulty. New `Problem` fields `difficulty_estimate` (setter's guess),
  `difficulty_calculated` and `difficulty` (what is shown; migration 0154). Rating a contest recalculates the
  difficulty of its problems when it had at least `PNOI_DIFFICULTY_MIN_CONTESTANTS` (10) rated contestants.
  Problem list: a sortable Difficulty column, and the Beginner / Intermediate / Advanced shortcuts now go by
  difficulty (below 1200, 1200 to 1799, 1800+) instead of points. Difficulty is hidden while inside a contest.
  Tested with two simulated rated contests. Not checked: phone width; a problem used in several contests simply
  keeps the result of the one rated last.
- 2026-11-17, Claude: students can ask to start an organization (`/organizations/new`, model
  `OrganizationProposal`, migration 0155). Staff approve or reject in the admin pages; approving creates the
  organization with the student as its administrator and first member. The Organizations page shows a student
  the state of their request and shows staff how many are waiting. New guide `docs/pnoi/organizations.md`.
  Tested end to end locally, including phone width. The page skeleton does not show Django flash messages, so
  feedback is shown on the Organizations page instead.
