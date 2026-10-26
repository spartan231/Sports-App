-- =========================================================
-- my_followed_games: every game involving a team the caller follows
-- security_invoker so RLS applies as the signed-in user: RLS on
-- user_favorites limits the exists() to the caller's own follows,
-- so no user_id filter is needed. Filter by state/start_time in the client.
-- =========================================================

create or replace view public.my_followed_games
with (security_invoker = true) as
select
    g.id,
    g.league,
    g.season,
    g.week,
    g.start_time,
    g.state,
    g.status_detail,
    g.home_score,
    g.away_score,
    g.home_team_id,
    hmt.display_name as home_name,
    hmt.abbreviation as home_abbreviation,
    hmt.logo_url as home_logo_url,
    g.away_team_id,
    awt.display_name as away_name,
    awt.abbreviation as away_abbreviation,
    awt.logo_url as away_logo_url
from public.cached_games g
join public.teams hmt on hmt.id = g.home_team_id
join public.teams awt on awt.id = g.away_team_id
where exists (
    select 1 
    from public.user_favorites f
    where f.team_id in (g.home_team_id, g.away_team_id)
);

revoke all on public.my_followed_games from anon;