-- =========================================================
-- profiles: one row per auth user, created by trigger below
-- =========================================================
create table public.profiles (
  id         uuid primary key references auth.users (id) on delete cascade,
  username   text not null unique check (char_length(username) between 3 and 24),
  role       text not null default 'member' check (role in ('member', 'admin')),
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

create policy "Users can view their own profile"
  on public.profiles for select
  to authenticated
  using ((select auth.uid()) = id);

create policy "Users can update their own profile"
  on public.profiles for update
  to authenticated
  using ((select auth.uid()) = id)
  with check ((select auth.uid()) = id);

-- Users may only change their username, never their role
revoke update on public.profiles from authenticated;
grant update (username) on public.profiles to authenticated;

-- =========================================================
-- teams: populated from ESPN by supabase/scripts/populate_teams.py
-- ESPN ids collide across leagues, so (league, espn_id) is the natural key
-- followable = true for NFL + FBS teams (set by populate script);
-- FCS opponents added by the score poller stay false so they show in
-- scores but not in search
-- =========================================================
create table public.teams (
  id           bigint generated always as identity primary key,
  league       text not null check (league in ('nfl', 'college-football')),
  espn_id      text not null,
  abbreviation text,
  display_name text not null,
  short_name   text,
  location     text,
  nickname     text,
  color        text,
  logo_url     text,
  conference   text,
  followable   boolean not null default false,
  updated_at   timestamptz not null default now(),
  unique (league, espn_id)
);

create index teams_followable_idx on public.teams (league, followable);

alter table public.teams enable row level security;

create policy "Logged-in users can read teams"
  on public.teams for select
  to authenticated
  using (true);

-- =========================================================
-- cached_games: ESPN scoreboard snapshots, refreshed by the poller
-- =========================================================
create table public.cached_games (
  id            bigint generated always as identity primary key,
  league        text not null check (league in ('nfl', 'college-football')),
  espn_event_id text not null,
  season        int not null,
  week          int,
  start_time    timestamptz not null,
  state         text not null check (state in ('pre', 'in', 'post')),
  status_detail text,
  home_team_id  bigint not null references public.teams (id),
  away_team_id  bigint not null references public.teams (id),
  home_score    int,
  away_score    int,
  updated_at    timestamptz not null default now(),
  unique (league, espn_event_id)
);

create index cached_games_start_time_idx on public.cached_games (start_time);
create index cached_games_home_team_idx  on public.cached_games (home_team_id);
create index cached_games_away_team_idx  on public.cached_games (away_team_id);

alter table public.cached_games enable row level security;

create policy "Logged-in users can read games"
  on public.cached_games for select
  to authenticated
  using (true);

-- =========================================================
-- Signup trigger: create a profile row for every new auth user
-- =========================================================
create function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = ''
as $$
begin
  insert into public.profiles (id, username)
  values (
    new.id,
    coalesce(new.raw_user_meta_data ->> 'username', 'user_' || left(new.id::text, 8))
  );
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();