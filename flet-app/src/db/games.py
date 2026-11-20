from datetime import datetime, timezone

from supabase_client import supabase

TEAM_FIELDS = "id, display_name, abbreviation, logo_url, color"


def followed_games(state=None, limit=50):
    query = supabase.table("my_followed_games").select("*")
    if state:
        query = query.eq("state", state)
    return query.order("start_time").limit(limit).execute().data


def followed_teams():
    rows = (
        supabase.table("user_favorites")
        .select("teams(id, display_name, abbreviation, logo_url, color, league)")
        .execute()
        .data
    )
    return [row["teams"] for row in rows] # type: ignore


def upcoming_games(league=None, limit=50):
    # cached_games has two FKs to teams, so name the constraint to pick each side
    query = (
        supabase.table("cached_games")
        .select(
            "id, league, season, week, start_time, state, status_detail, "
            f"home:teams!cached_games_home_team_id_fkey({TEAM_FIELDS}), "
            f"away:teams!cached_games_away_team_id_fkey({TEAM_FIELDS})"
        )
        .eq("state", "pre")
        .gte("start_time", datetime.now(timezone.utc).isoformat())
    )
    if league:
        query = query.eq("league", league)
    return query.order("start_time").limit(limit).execute().data
