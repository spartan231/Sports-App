-- =========================================================
-- Cap each user at 5 favorite teams
-- =========================================================
create function public.enforce_favorites_cap()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if (select count(*) from public.user_favorites where user_id = new.user_id) >= 5 then
    raise exception 'You can follow at most 5 teams';
  end if;
  return new;
end;
$$;

create trigger user_favorites_cap
  before insert on public.user_favorites
  for each row execute function public.enforce_favorites_cap();