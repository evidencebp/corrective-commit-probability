# project with swaer
select
blasphemy_hit_rate = 0 as f
, count(*)
from
ccp.blasphemy_ccp_env_porfile
group by
f
order by
f
;

# Authors that swear
select
blasphemy_hit_rate = 0 as f
, count(*)
from
(
    select
  Author_email

    ,  1.0*count(distinct case when     REGEXP_CONTAINS( lower(message), 'disappointing|disheartening|displeasing|mortifying|not up to (par|snuff)|poor|rotten|substandard|unsatisfactory|bad|horrible|terrible|shit|crap|lousy|awful|fuck|disgusting|hideous|nasty|scary|shameful|shame|shocking|repulsive|revolting|stink') then commit else null end)/count(distinct commit)  as blasphemy_hit_rate
    , max(DATE('1980-01-01')) as  fake_date
    from
    ccp.active_2019_commits_by_file
    group by
  Author_email
     having count(*) >= 12


) as inSql
group by
f
order by
f
;
