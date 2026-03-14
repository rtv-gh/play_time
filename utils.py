import math
import random


def allocate_halves(num_players: int, total_slots: int) -> dict[str, int]:
    """
    Return a dict mapping index → number of halves that player should play.
    Distributes total_slots as evenly as possible across num_players.
    Players with index < remainder get (base+1), the rest get base.
    """
    base = total_slots // num_players
    remainder = total_slots % num_players
    return {i: base + (1 if i < remainder else 0) for i in range(num_players)}


def build_schedule(
    players: list[str],
    halves_each: dict[int, int],
    num_games: int,
    players_per_half: int = 8,
    seed: int | None = None,
) -> list[dict]:
    """
    Build a fair schedule.
    Returns a list of dicts, one per game:
        {"1st": [name, ...], "2nd": [name, ...]}

    Strategy:
    - Track remaining halves for each player.
    - For each half (1st and 2nd of each game), pick the 8 players who have
      the most remaining halves still to play, breaking ties randomly.
    - This greedy approach guarantees fairness without backtracking.
    """
    if seed is not None:
        random.seed(seed)

    remaining = {p: halves_each[i] for i, p in enumerate(players)}
    schedule = []

    total_halves = num_games * 2

    for game_idx in range(num_games):
        game = {}
        for half_label in ("1st", "2nd"):
            # Sort by remaining halves desc, shuffle within ties
            sorted_players = sorted(
                players,
                key=lambda p: (-remaining[p], random.random()),
            )
            chosen = sorted_players[:players_per_half]
            for p in chosen:
                remaining[p] -= 1
            game[half_label] = sorted(chosen)  # alphabetical for display
        schedule.append(game)

    return schedule
