# Running a contest

This guide explains how to create a contest on PNOI, what participants see while it runs, and how to rate it
(update everyone's rating) when it is over.

You need the problems first. Create them as described in [Adding a problem](adding-a-problem.md), including their
test data. Contest problems do **not** have to be public: participants can open them during the contest.

## Before you start: check your time zone

All dates and times in the admin pages are read in **your own profile's time zone**, not Philippine time
automatically. New accounts start in Philippine time (`Asia/Manila`), but an older account, such as the first
administrator account, may still be set to another zone (for example `America/Toronto`), so check this first:

1. Click your picture at the bottom of the menu on the left and choose **Edit profile**.
2. Under **Preferences**, set **Time zone** to `Asia/Manila` (or the zone you want to type times in) and click
   **Update profile**.

Participants also see contest times in their own profile's time zone.

## Part 1: Create the contest

1. Click your picture at the bottom of the menu on the left and choose **Admin**.
2. On the admin home page, find **Contests** and click **Add** next to it. A form called *Add contest* opens.

### The basic details

- **Contest id** — the short key for the contest. It is used in the web address, so `pnoi2026r1` becomes
  `/contest/pnoi2026r1`. Use only lowercase letters `a`–`z` and digits `0`–`9`, no spaces, at most 20
  characters. It must be unique.
- **Contest name** — the title participants see, for example `PNOI 2026 Round 1`. Up to 100 characters.
- **Authors** — add yourself. Authors can edit the contest and are listed as its authors. **Curators** can edit
  it without being listed. **Testers** can try the contest before it is public. **Spectators** can watch the
  contest without taking part. **Testers see submissions** and **Testers see scoreboard** decide what testers may
  see.

### Settings

- **Publicly visible** — tick this when the contest should appear on the contest list. While it is unticked, only
  the authors, curators, testers and site staff can see it. Even for a contest limited to an organisation (see
  [Access](#access-who-can-see-and-join)), this box must be ticked for the organisation's members to see it.
- **Scoreboard visibility** — when participants can see the rankings:
  **Visible**, **Hidden for duration of contest**, **Hidden for duration of participation** or
  **Hidden permanently**.
- **Run pretests only** — tick only if your test data marks some cases as pretests (**Pretest?** in the test
  data editor) and you want only those to be judged during the contest.
- The other settings (**No comments**, **Hide problem tags**, **Hide problem authors**,
  **Show short form settings display**, **Contest lock**, **Precision points**) can be left as they are.

### Scheduling

- **Start time** and **End time** — when the contest opens and closes. Each has a date box and a time box; the
  admin page has **Today** / **Now** shortcuts and a calendar and clock. Times are in your profile's time zone
  (see above).
- **Time limit** — optional. Leave it empty if everyone simply competes from **Start time** to **End time**. If you
  fill it in (for example `03:00:00` for three hours), each participant gets that much time from the moment they
  click **Join contest**, as long as it is before **End time**. This is useful for a contest window, for example
  "any three hours during the weekend".

### Details

- **Description** — optional text shown on the contest page, written in Markdown (see
  [Adding a problem](adding-a-problem.md) for a short Markdown introduction). Rules, allowed materials and contact
  information are good things to put here.

### Format

- **Contest format** — how scores and the ranking are calculated. The choices are **Default**, **IOI**,
  **IOI (pre-2016)**, **ICPC**, **AtCoder** and **ECOO**. For an olympiad-style contest with partial scores,
  **IOI** is the usual choice.
- **Contest format configuration** and **Contest problem label script** are advanced; leave them empty unless you
  know you need them.

### Rating

Ratings are numbers on participants' profiles that go up or down depending on how they do in rated contests.

- **Contest rated** — tick this if the contest should count towards ratings. If it is unticked, the contest cannot
  be rated later.
- **Rate all** — if ticked, participants who joined but made no submissions are rated too. If unticked, they are
  skipped.
- **Rating floor** / **Rating ceiling** — optional. Participants with a rating below the floor or above the ceiling
  are not rated.
- **Exclude from ratings** — choose participants who should not be rated (for example, organisers who joined to
  test).
- **Performance ceiling override** is advanced; leave it empty.

### Access: who can see and join

If you leave every field in this section empty, any logged-in user can see the contest (once **Publicly visible**
is ticked) and join it.

- **Access code** — optional. If you type a code here, participants must enter it before they can join. Leave it
  empty to disable.
- **Private contestants** — if you choose users here, **only these users** can see the contest.
- **Organizations** — if you choose organisations here, only their members can see the contest.
- **Classes** — for an organisation-private contest, limits it further to these classes.
- **Join organizations** — if you choose organisations here, everyone may still see the contest, but only members
  of these organisations can join it.
- **View contest scoreboard** — extra users who may always see the rankings, even when **Scoreboard visibility**
  hides them.
- **Can see contest submissions** — extra users who may see participants' submissions.

### Justice

- **Personae non gratae** — users chosen here are banned from joining this contest.

### Add the problems

At the bottom of the form is a table of contest problems.

1. Click **Add another Problem** to add a row.
2. In **Problem**, start typing the problem's code or name and choose it from the list.
3. In **Points**, type how many points the problem is worth **in this contest** (whole numbers only). This can be
   different from the problem's normal points.
4. **Partial** — ticked by default. Leave it ticked if participants should get points for passing some test cases
   or batches; untick it if only a full solve should count.
5. **Is pretested** — tick if this problem should use its pretests during the contest.
6. **Max submissions** — optional. The most submissions a participant may make on this problem. Leave it empty for
   no limit.
7. **Output prefix length override** — leave as it is.
8. Repeat for each problem. Drag the rows to put the problems in the order participants should see them. To remove
   a problem, tick **Delete?** on its row.

### Save

Click **Save and continue editing**. The page reloads with a message like
*The contest "PNOI 2026 Round 1" was added successfully*. If something is wrong, the field with the problem is shown
in red with an explanation. Fix it and save again.

To edit the contest later, open it on the site and click the **Edit** tab, or find it in **Contests** in the admin
pages.

## Part 2: What participants see

1. Participants open **Contests** from the menu (address `/contests/`). Your contest is listed once it is
   **Publicly visible** and they are allowed to see it.
2. On the contest's page (`/contest/<contest id>`) there are tabs: **Info**, **Rankings** (or **Hidden Rankings**
   while the scoreboard is hidden) and, after joining, **Participation**.
3. **Before the start**, the page shows *Starting in …* with a countdown, the contest length and the start time.
   There is no join button yet.
4. **During the contest**, logged-in participants see a **Join contest** button. When they click it, the browser
   asks *Are you sure you want to join? Joining a contest starts your timer, after which it becomes unstoppable.*
   If an **Access code** is set, they are asked to enter it first.
   Users who are not allowed to join see the button greyed out with *You cannot join this contest.*, or a
   **Spectate contest** button if they may watch. Visitors who are not logged in see **Log in to participate**.
5. After joining, participants are taken to the **Problems** list, which now shows only the contest's problems and
   their contest points. A small box at the bottom of the screen shows the contest name and the time left.
   Each problem page has the statement, the limits and a submit button.
6. On the **Info** tab, participants see *You have … remaining.* and a **Leave contest** button. Leaving does not
   stop their timer. The list of contest problems on the **Info** tab itself is only shown to everyone **after the
   contest has ended** (authors, curators, testers and spectators see it earlier).
7. The **Info** tab also summarises the rules: whether the contest is rated, how many problems there are, whether
   partial scoring and pretests are used, whether there is a submission limit, whether the scoreboard is visible,
   and whether an access code is needed.
8. **After the contest ends**, anyone who can see the contest can click **Virtual join** to try it later under
   the same time conditions. Virtual participations appear separately and are never rated.

## Part 3: Rate the contest afterwards

Do this only after the contest has ended and you are happy with the results (for example, after any rejudging).
Your account needs the permission to rate contests (**Rate contests**).

1. Open the contest in the admin pages (**Contests** → click the contest name).
2. Scroll to the bar at the bottom of the form, where the **Save** buttons are. A **Rate** button sits there too.
   (The **Rejudge** buttons are somewhere else: one on each row of the **Problems** table.) **Rate** only appears when
   **Contest rated** is ticked, the **End time** has passed, and your account has the rating permission.
3. Click **Rate**. The page reloads when the ratings have been calculated. The same click also works out the
   difficulty of each problem in the contest (see "Difficulty" in the problem guide).
4. Check the **Rankings** tab or participants' profiles to see the new ratings.

What the rating includes:

- Only real participations, not virtual ones.
- Participants with no submissions are skipped, unless **Rate all** is ticked.
- Participants listed in **Exclude from ratings**, and those outside **Rating floor** / **Rating ceiling**, are
  skipped.

If you change something and click **Rate** again, the ratings of this contest **and of every rated contest that
ended after it** are deleted and recalculated in order. This is safe to do, but it can change ratings from later
contests too.

The contest list in the admin pages also has a **Rate all ratable contests** link, which recalculates every rated
contest that has ended. You normally do not need it.
