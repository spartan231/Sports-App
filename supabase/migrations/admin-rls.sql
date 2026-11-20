-- Admin access: admins can list users, change roles, view and
-- remove any user's favorites, and delete users.
-- Run after init_schema.sql and user-favorites.sql.
-- Make the first admin from the SQL editor:
-- update public.profiles set role = 'admin' where username = '<name>';

-- security definer so the lookup skips profiles RLS (a policy on
-- profiles that selects from profiles would otherwise recurse)
create or replace function public.is_admin()
returns boolean
language sql
stable
security definer set search_path = ''
as $$
  select exists (
    select 1 from public.profiles
    where id = (select auth.uid()) and role = 'admin'
  );
$$;

create policy "Admins can view all profiles"
  on public.profiles for select
  to authenticated
  using ((select public.is_admin()));

create policy "Admins can view all favorites"
  on public.user_favorites for select
  to authenticated
  using ((select public.is_admin()));

create policy "Admins can remove any favorite"
  on public.user_favorites for delete
  to authenticated
  using ((select public.is_admin()));

-- Members can only update their username, so a policy can't open up
-- the role column for admins alone. Role changes go through here.
create or replace function public.admin_set_role(target_user uuid, new_role text)
returns void
language plpgsql
security definer set search_path = ''
as $$
begin
  if not public.is_admin() then
    raise exception 'Only admins can change roles';
  end if;
  if target_user = (select auth.uid()) then
    raise exception 'Admins cannot change their own role';
  end if;
  update public.profiles set role = new_role where id = target_user;
end;
$$;

-- Deletes the auth user; profiles and user_favorites cascade.
create or replace function public.admin_delete_user(target_user uuid)
returns void
language plpgsql
security definer set search_path = ''
as $$
begin
  if not public.is_admin() then
    raise exception 'Only admins can delete users';
  end if;
  if target_user = (select auth.uid()) then
    raise exception 'Admins cannot delete themselves';
  end if;
  delete from auth.users where id = target_user;
end;
$$;
