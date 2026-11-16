"""PNOI: automatic problem difficulty.

A problem's difficulty is the rating at which a contestant had a 50% chance of solving it in the contest it was
used in, which is how Codeforces and AtCoder describe difficulty. It is worked out from the rated contestants of
that contest: who solved the problem and who did not, and how strong each of them was.
"""
from django.conf import settings
from django.db.models import Max


def solve_probability(rating, difficulty):
    # The usual Elo curve: equal rating and difficulty means a 50% chance.
    return 1.0 / (1.0 + 10.0 ** ((difficulty - rating) / 400.0))


def estimate_difficulty(results):
    """Return the difficulty for one problem, or None when there are too few contestants.

    `results` is a list of (rating, solved) pairs, one per rated contestant.
    """
    count = len(results)
    if count < settings.PNOI_DIFFICULTY_MIN_CONTESTANTS:
        return None

    low, high = settings.PNOI_DIFFICULTY_RANGE
    # If everyone or no one solved it there is no exact answer, so count half a contestant the other way.
    solved = min(max(sum(1 for _, ok in results if ok), 0.5), count - 0.5)

    # The expected number of solvers falls as the difficulty rises, so search for the matching difficulty.
    lo, hi = low - 2000.0, high + 2000.0
    for _ in range(60):
        mid = (lo + hi) / 2
        expected = sum(solve_probability(rating, mid) for rating, _ in results)
        if expected > solved:
            lo = mid
        else:
            hi = mid
    difficulty = int(round((lo + hi) / 2 / 100.0)) * 100
    return min(max(difficulty, low), high)


def update_contest_difficulties(contest):
    """Recalculate the difficulty of every problem of a contest that has just been rated."""
    from judge.models import ContestSubmission, Rating

    ratings = list(Rating.objects.filter(contest=contest).select_related('participation'))
    if not ratings:
        return

    # A contestant's strength is their rating going into the contest; for a first contest, the rating it gave.
    strength = {}
    for rating in ratings:
        previous = (Rating.objects.filter(user_id=rating.user_id, contest__end_time__lt=contest.end_time)
                    .order_by('-contest__end_time').values_list('rating', flat=True).first())
        strength[rating.participation_id] = previous if previous is not None else rating.rating

    best = {}
    for row in (ContestSubmission.objects.filter(participation_id__in=list(strength))
                .values('participation_id', 'problem_id').annotate(best=Max('points'))):
        best[row['participation_id'], row['problem_id']] = row['best'] or 0

    for contest_problem in contest.contest_problems.select_related('problem'):
        results = [(value, best.get((participation_id, contest_problem.id), 0) >= contest_problem.points)
                   for participation_id, value in strength.items()]
        difficulty = estimate_difficulty(results)
        if difficulty is not None:
            problem = contest_problem.problem
            problem.difficulty_calculated = difficulty
            problem.save(update_fields=['difficulty_calculated', 'difficulty'])
