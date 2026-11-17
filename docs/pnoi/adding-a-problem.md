# Adding a problem

This guide walks you through creating a new problem on PNOI and uploading its test data. There are two parts:

1. **Create the problem** in the admin pages (name, statement, limits, points, languages).
2. **Upload the test data** in the test data editor (the input and output files the judge uses to check answers).

A problem stays hidden from students until you tick **Publicly visible**, so you can work on it safely.

## Before you start

- Log in to the site. Click your picture at the bottom of the menu on the left and choose **Admin**. This opens the admin pages
  (the address ends in `/admin/`).
- Every problem must belong to a **problem group** and have at least one **problem type**. If the
  **Problem group** or **Problem types** list is empty (or has nothing suitable) when you create the problem, add
  them first:
  - On the admin home page, find **Problem groups** and click **Add**. Fill in **Problem group ID** (a short code,
    for example `pnoi2026`) and **Problem group name** (for example `PNOI 2026`), then click **Save**. The group is
    shown under *Category* in the problem list.
  - Find **Problem types** and click **Add**. Fill in **Problem category ID** (for example `greedy`) and
    **Problem category name** (for example `Greedy`), then click **Save**.
- Prepare your test files on your computer (see [Part 2](#part-2-upload-the-test-data)).

## Part 1: Create the problem

1. On the admin home page, find **Problems** and click **Add** next to it. A form called *Add problem* opens.
2. Fill in the fields at the top of the form:
   - **Problem code** — a short, unique code. It appears in the web address after `/problem/`, so `sumtwo`
     becomes `/problem/sumtwo`. Use only lowercase letters `a`–`z` and digits `0`–`9`, no spaces, at most 20
     characters. You cannot reuse a code that another problem already has.
   - **Problem name** — the title students see, for example `Sum of Two`. Up to 100 characters.
   - **Publicly visible** — leave this **unticked** for now. You will tick it at the end (step 9).
   - **Manually managed** — leave this unticked. If it is ticked, the **Edit test data** link is hidden and you
     cannot use the test data editor.
   - **Date of publishing** — optional. It is shown as the problem's date; it does **not** publish the problem
     automatically.
   - **Creators** — add yourself (and any co-authors). These users can edit the problem and are listed as its
     authors. **Curators** can edit it without being listed. **Testers** can see it before it is public.
   - **Organizations** — leave empty for a normal problem. If you pick organisations, only their members can see
     the problem.
3. Write the statement in **Problem body**. This is the text students read. It uses Markdown, a simple way to
   format text:
   - `## Input` makes a heading, `**bold**` makes **bold**, `*italic*` makes *italic*.
   - Put sample input and output in code blocks: a line with three backticks (```` ``` ````), the text, then
     another line with three backticks.
   - Maths goes between `~` signs, for example `~1 \le N \le 10^5~` (or `$$ ... $$` for a formula on its own
     line). Whether it is drawn as a nice formula depends on the site's maths setting (`MATHOID_URL`); ask the site
     administrator if formulas show up as plain text.
   - The editor has a preview so you can check the result before saving.

   A typical layout:

   ````markdown
   Given two integers, print their sum.

   ## Input Specification

   One line with two integers ~a~ and ~b~ (~-10^9 \le a, b \le 10^9~).

   ## Output Specification

   Print ~a + b~.

   ## Sample Input

   ```
   1 2
   ```

   ## Sample Output

   ```
   3
   ```
   ````

4. Under **Taxonomy**, choose at least one entry in **Problem types** and pick a **Problem group**. Both are
   required.
5. Under **Points**:
   - **Points** — leave it empty. PNOI works out the points from the difficulty below: the difficulty divided by
     100, so a `1200` problem is worth 12 points. Once the problem has a difficulty this box cannot be edited.
     You only type points for a problem with no difficulty estimate at all.
   - **Allows partial points** — ticked by default: students get part of the points when they pass only some
     test cases (or batches), and those count towards their practice points. Untick it if only a full solve
     should count.
   - **Short circuit** — if ticked, the judge stops at the first failed test case instead of running the rest.
     Leave it unticked if you want partial points.
   Under **Difficulty**, just below:
   - **Difficulty estimate** — your own guess of how hard the problem is, on the same scale as ratings: `800` is
     the easiest, `1200` is a typical beginner problem, `2000` and above is hard. The problem list shows it with
     a `~` in front (for example `~1200`) so students know it is a guess. Fill it in: the points come from it.
   - **Calculated difficulty** — you cannot type here. After the problem has been used in a rated contest and
     you click **Rate**, the site works out the difficulty by itself and shows it here and on the problem list,
     replacing your estimate. It needs at least 10 rated contestants in that contest. The problem's points
     change with it, and every student's practice points are updated.
6. Under **Limits**:
   - **Time limit** — in **seconds**. Fractional values work, for example `1` or `1.5`.
   - **Memory limit** — in **kilobytes**, not megabytes. Multiply megabytes by 1024. For example 256 MB is
     `262144` and 512 MB is `524288`.
   - Further down the page, the **Language-specific resource limits** table lets you give one language a
     different **Language** / **Time limit** / **Memory limit** (for example, more time for Python 3). Use
     **Add another Language-specific resource limit** for more rows. Leave it empty if every language uses the
     same limits.
7. Under **Language**, tick the languages students may submit in, in **Allowed languages**. PNOI offers
   **C++17**, **C++20** and **Python 3**. The **Check all** box ticks all of them at once.
8. Click **Save and continue editing** at the bottom. The page reloads with a message like
   *The problem "Sum of Two" was added successfully*. If something is wrong, the field with the problem is
   outlined in red with an explanation; fix it and save again.
9. When the problem and its test data are ready, tick **Publicly visible** and click **Save**. Students can now
   see the problem in the problem list. You can also hide or show several problems at once: on the problem list in
   the admin pages, tick the problems, choose **Mark problems as public** or **Mark problems as private** in the
   *Action* menu, and click **Go**.

> **Tip:** If the problem is only for a contest, you can leave **Publicly visible** unticked. Students in the
> contest still see it while the contest runs. See [Running a contest](running-a-contest.md).

To come back to a problem later, open it on the site (`/problem/<code>`) and click **Edit problem**, or find it in
**Problems** in the admin pages.

## Part 2: Upload the test data

The judge runs a student's program on each **input file** and compares what the program prints with the matching
**output file** (the correct answer).

### Prepare a ZIP file

1. On your computer, create one input file and one output file for each test case. Plain text files work best. A
   naming pattern where the output file name is the input file name with `in` replaced by `out` saves you typing,
   because the editor fills in the output file for you. For example:

   ```
   sum.1.in   sum.1.out
   sum.2.in   sum.2.out
   sum.3.in   sum.3.out
   ```

2. Put all of these files into one ZIP archive (on most computers: select the files, right-click, and choose
   *Compress* or *Send to → Compressed (zipped) folder*). The file name must end in `.zip`.

### Open the test data editor

1. Go to the problem's page on the site, for example `/problem/sumtwo`.
2. Click **Edit test data**. A page titled *Editing data for Sum of Two* opens.

### Upload the ZIP file

1. Next to **Data zip file**, click **Choose File** and select your ZIP file.
2. Click **Submit!** at the bottom of the page. The page reloads. Now the **Input file** and **Output file** columns
   are drop-down lists containing the files from your ZIP.

If you get an error instead, check that the file name ends in `.zip` and that it is a real ZIP archive.

### Choose a checker

The **Checker** decides how a student's output is compared with the correct output. Pick one from the **Checker**
list near the top of the page. If you leave it empty (`---------`), no checker is written into the configuration
and the judge uses its default, which is the standard comparison.

| Checker | Use it when |
| --- | --- |
| **Standard** | Most problems: the answer is a fixed set of words or numbers. |
| **Floats** | The answer contains decimal numbers that may differ slightly because of rounding. |
| **Floats (absolute)** | Decimal answers, where you want to allow a fixed (absolute) error. |
| **Floats (relative)** | Decimal answers, where you want to allow an error relative to the size of the answer. |
| **Non-trailing spaces** | Spaces inside a line matter, but spaces at the end of a line do not. |
| **Sorted** | The lines of the answer may be printed in any order. |
| **Byte identical** | The output must match the correct output exactly, character for character. |
| **Line-by-line** | Each line of the output is compared separately. |

The comparison itself is done by the judge, which is a separate program from this website, so test your problem
with a real submission (see [Test the problem](#test-the-problem)) to be sure the checker behaves as you expect.

When you choose one of the **Floats** checkers, a small number box appears next to the list. It is the precision,
in decimal digits (default `6`). Changing it fills in the checker arguments for you, for example
`{"precision": 6}`.

The checker arguments (the box right after the **Checker** list, which has no label of its own) are for advanced
settings, written as a JSON object (text in curly brackets). Leave it empty
if you are unsure. If the text is not a valid JSON object, the page shows an error.

The other settings at the top (**Generator file**, **Enable unicode**, **Disable bigInteger / bigDecimal**,
**Output limit length**, **Output prefix length**) can usually be left as they are.

### Add test cases

Each row in the table at the bottom is one test case. Click **Add new case** to add more rows.

For a simple problem where every test case is worth some points:

1. In each row, leave **Type** as **Normal case**.
2. Choose the **Input file**. If a matching output file exists (same name with `in` replaced by `out`), the
   **Output file** is filled in automatically; otherwise choose it yourself.
3. Type the **Points** for that case, for example `10`. Every normal case outside a batch needs points.
4. Tick **Pretest?** only if the case is a pretest (used in contests that run pretests).
5. Click **Submit!**.

The order of the rows is the order in which the cases are judged. You can drag rows to reorder them. To remove a
row, tick **Delete?** and click **Submit!**.

### Group cases into batches (subtasks)

A **batch** is a group of test cases that is scored together: the student gets the batch's points only if they
pass **every** case in it. Batches are how you make subtasks.

To make a batch:

1. Add a row with **Type** set to **Batch start**. Put the batch's **Points** on this row (for example `90`).
   Leave **Input file** and **Output file** empty on this row.
2. Below it, add one row of **Type** **Normal case** for each test case in the batch. Choose the input and
   output files. Leave **Points** empty on these rows; the batch start row holds the points.
3. Add a row with **Type** set to **Batch end**.
4. Click **Submit!**.

Example: one sample case worth 10 points, then a batch of three cases worth 90 points.

| Type | Input file | Output file | Points |
| --- | --- | --- | --- |
| Normal case | `sum.1.in` | `sum.1.out` | 10 |
| Batch start | | | 90 |
| Normal case | `sum.2.in` | `sum.2.out` | |
| Normal case | `sum.3.in` | `sum.3.out` | |
| Normal case | `sum.4.in` | `sum.4.out` | |
| Batch end | | | |

**Batch dependencies** (optional): a batch can depend on earlier batches, so it is only judged if those were passed.
Tick **Batch dependencies** next to **Show columns** to see the column, click **Edit** on the batch start row,
type the numbers of earlier batches separated by commas (the first batch is `1`, the second `2`, and so on), and
click **Save**. You can only depend on batches that come **before** this one.

The **Show columns** checkboxes (**Output prefix**, **Output limit**, **Checker**, **Generator args**,
**Batch dependencies**) only show or hide extra columns. They are for per-case overrides you rarely need.

### Check the result

After a successful **Submit!**, a **View YAML** link appears at the top of the page. It shows the configuration the
judge will use (a file called `init.yml`). Each case and batch should be listed there with the points you gave.

If something is wrong, the page still reloads, but a message appears at the top of it and no usable configuration
is written, so read the top of the page after every **Submit!**. Common messages:

- *Points must be defined for non-batch case #N.* — a normal case outside a batch has no points.
- *Input file for case N does not exist* / *Output file for case N does not exist* — the file name is not in the
  ZIP. Check the spelling, or upload a new ZIP.
- *Batch start case #N requires points.* — put the points on the **Batch start** row.
- *Empty batches not allowed.* — there is no normal case between a **Batch start** and a **Batch end**.
- *Attempt to end batch outside of one in case #N.* — a **Batch end** has no matching **Batch start** above it.
- *Dependencies must depend on previous batches for batch start case #N.* — a batch dependency points to the
  same batch or a later one.

### Test the problem

Before making the problem public, submit a correct solution (and ideally a wrong one) yourself from the problem page
and check that you get the result you expect.

With the example above (one case worth 10 points and a batch worth 90), a correct solution scores 100 / 100. A
solution that passes only the first case scores 10 / 100 when **Allows partial points** is ticked: the judge stops
the batch at its first wrong answer and the remaining cases of that batch are shown as skipped.

If you submit several times in a row very quickly, the site may refuse for a moment (it limits how fast one person
can submit). Wait a few seconds and try again.
