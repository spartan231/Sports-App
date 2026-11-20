-- user_favorites: teams a user follows (max 5, see favorites-cap.sql)
-- Run this before favorites-cap.sql and followed-games.sql.
-- user_id defaults to the caller, so the client only sends team_id.
create table if not exists public.user_favorites (
  user_id    uuid not null default auth.uid() references auth.users (id) on delete cascade,
  team_id    bigint not null references public.teams (id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (user_id, team_id)
);

create index if not exists user_favorites_team_idx on public.user_favorites (team_id);

-- No update policy, so favorites can only be added or removed
alter table public.user_favorites enable row level security;

create policy "Users can view their own favorites"
  on public.user_favorites for select
  to authenticated
  using ((select auth.uid()) = user_id);

-- Only followable teams (NFL + FBS), and only for yourself
create policy "Users can add their own favorites"
  on public.user_favorites for insert
  to authenticated
  with check (
    (select auth.uid()) = user_id
    and exists (select 1 from public.teams t where t.id = team_id and t.followable)
  );

create policy "Users can remove their own favorites"
  on public.user_favorites for delete
  to authenticated
  using ((select auth.uid()) = user_id);
