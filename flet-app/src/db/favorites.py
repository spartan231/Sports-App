from supabase_client import supabase


def add_favorite(team_id):
    # user_id defaults to auth.uid(); the cap trigger rejects a 6th team
    return supabase.table("user_favorites").insert({"team_id": team_id}).execute().data


def remove_favorite(team_id):
    # RLS limits the delete to the caller's own rows
    return supabase.table("user_favorites").delete().eq("team_id", team_id).execute().data
