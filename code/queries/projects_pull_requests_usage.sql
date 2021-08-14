select
pull_requests > 0 as f
, count(*)
from
general_ght.repo_profile
group by
f
order by
f
;
