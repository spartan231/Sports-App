from supabase_client import supabase


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