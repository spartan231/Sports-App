from supabase_client import supabase


def is_admin():
    return bool(supabase.rpc("is_admin").execute().data)


def list_users():
    # Admins see every profile via RLS; members only see their own
    return (
        supabase.table("profiles")
        .select("id, username, role, created_at")
        .order("created_at")
        .execute()
        .data
    )


def set_role(user_id, role):
    supabase.rpc("admin_set_role", {"target_user": user_id, "new_role": role}).execute()


def delete_user(user_id):
    supabase.rpc("admin_delete_user", {"target_user": user_id}).execute()
