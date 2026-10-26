-- =========================================================
-- standings: one row per team per season, refreshed daily by
-- supabase/scripts/fetch_standings.py
-- group_name is the smallest group ESPN ranks teams in:
-- NFL division ("AFC East") or FBS conference/division ("Sun Belt - East")
-- =========================================================
create table public.standings (
  team_id        bigint not null references public.teams (id) on delete cascade,
  season         int not null,
  league         text not null check (league in ('nfl', 'college-football')),
  group_name     text not null,
  group_rank     int not null,
  wins           int not null,
  losses         int not null,
  ties           int not null default 0,
  conf_record    text,
  points_for     int,
  points_against int,
  updated_at     timestamptz not null default now(),
  primary key (team_id, season)
);

alter table public.standings enable row level security;

create policy "Logged-in users can read standings"
  on public.standings for select
  to authenticated
  using (true);