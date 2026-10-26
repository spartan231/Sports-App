# /// script
# dependencies = [
#   "httpx",
#   "python-dotenv",
#   "supabase",
# ]
# ///
"""Daily refresh of NFL and FBS standings from ESPN into public.standings.

Fetches everything first and only writes if every followable team has a row,
so a bad ESPN response never leaves the table half-updated.
Run from the repo root: uv run supabase/scripts/fetch_standings.py
"""

import os
from datetime import datetime, timezone

from dotenv import load_dotenv, find_dotenv
from supabase import create_client

import espn

SOURCES = {
    # level=3 splits the NFL into its 8 divisions
    "nfl": ("/v2/sports/football/nfl/standings", {"level": 3}),
    "college-football": ("/v2/sports/football/college-football/standings", {"group": 80}),
}


def groups(node):
    """Yield (group name, standings) for every group that ranks teams directly."""
    standings = node.get("standings")
    if standings and standings.get("entries"):
        yield node["name"], standings
    for child in node.get("children", []):
        yield from groups(child)


def parse_record(summary):
    """'7-1' or '7-1-1' -> (wins, losses, ties)."""
    parts = [int(p) for p in summary.split("-")]
    return parts[0], parts[1], parts[2] if len(parts) > 2 else 0


def to_row(league, team_id, group_name, rank, entry, season, now):
    stats = {s["type"]: s for s in entry["stats"]}
    wins, losses, ties = parse_record(stats["total"]["summary"])
    return {
        "team_id": team_id,
        "season": season,
        "league": league,
        "group_name": group_name,
        "group_rank": rank,
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "conf_record": stats.get("vsconf", {}).get("summary"),
        "points_for": int(stats["pointsfor"]["value"]),
        "points_against": int(stats["pointsagainst"]["value"]),
        "updated_at": now,
    }


def main():
    load_dotenv(find_dotenv())
    supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
    now = datetime.now(timezone.utc).isoformat()

    teams = supabase.table("teams").select("id, league, espn_id").eq("followable", True).execute().data
    team_ids = {(t["league"], t["espn_id"]): t["id"] for t in teams}

    rows = []
    for league, (path, params) in SOURCES.items():
        for group_name, standings in groups(espn.get(path, params)):
            for rank, entry in enumerate(standings["entries"], start=1):
                team_id = team_ids.get((league, entry["team"]["id"]))
                if team_id is None:
                    print(f"Skipping {entry['team']['displayName']}: not in teams table")
                    continue
                rows.append(to_row(league, team_id, group_name, rank, entry, standings["season"], now))

    missing = set(team_ids.values()) - {row["team_id"] for row in rows}
    if missing:
        raise SystemExit(f"{len(missing)} followable teams missing from ESPN standings; nothing written")

    supabase.table("standings").upsert(rows, on_conflict="team_id,season").execute()
    print(f"Upserted {len(rows)} standings rows")


if __name__ == "__main__":
    main()