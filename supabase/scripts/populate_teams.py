# /// script
# dependencies = [
#   "httpx",
#   "python-dotenv",
#   "supabase",
# ]
# ///
"""
One-time load of NFL and FBS teams from ESPN into public.teams.

Run from the repo root: uv run supabase/scripts/populate_teams.py
"""

import os
from datetime import datetime, timezone

import httpx
from dotenv import load_dotenv, find_dotenv
from supabase import create_client

ESPN = "https://site.api.espn.com/apis"


def get(url):
    resp = httpx.get(url, timeout=15)
    resp.raise_for_status()
    return resp.json()


def team_details(league):
    """All teams in a league from ESPN, keyed by ESPN id."""
    data = get(f"{ESPN}/site/v2/sports/football/{league}/teams?limit=1000")
    return {t["team"]["id"]: t["team"] for t in data["sports"][0]["leagues"][0]["teams"]}


def nfl_conferences():
    """ESPN id -> division name, e.g. "AFC East"."""
    data = get(f"{ESPN}/site/v2/sports/football/nfl/groups")
    return {
        team["id"]: division["name"]
        for conference in data["groups"]
        for division in conference["children"]
        for team in division["teams"]
    }


def fbs_conferences():
    """ESPN id -> conference name, for FBS teams only (group 80)."""
    data = get(f"{ESPN}/v2/sports/football/college-football/standings?group=80")
    result = {}
    for conference in data["children"]:
        # Some conferences (Sun Belt) split their standings into divisions
        for group in [conference, *conference.get("children", [])]:
            for entry in group.get("standings", {}).get("entries", []):
                result[entry["team"]["id"]] = conference["name"]
    return result


def to_row(league, team, conference, now):
    logos = team.get("logos") or [{}]
    return {
        "league": league,
        "espn_id": team["id"],
        "abbreviation": team.get("abbreviation"),
        "display_name": team["displayName"],
        "short_name": team.get("shortDisplayName"),
        "location": team.get("location"),
        "nickname": team.get("name"),
        "color": team.get("color"),
        "logo_url": logos[0].get("href"),
        "conference": conference,
        "followable": True,
        "updated_at": now,
    }


def main():
    load_dotenv(find_dotenv())
    supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
    now = datetime.now(timezone.utc).isoformat()

    rows = []
    for league, conferences in [("nfl", nfl_conferences()), ("college-football", fbs_conferences())]:
        details = team_details(league)
        for espn_id, conference in conferences.items():
            rows.append(to_row(league, details[espn_id], conference, now))
        print(f"{league}: {len(conferences)} teams")

    supabase.table("teams").upsert(rows, on_conflict="league,espn_id").execute()
    print(f"Upserted {len(rows)} teams")


if __name__ == "__main__":
    main()
