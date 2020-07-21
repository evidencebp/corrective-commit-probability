Select
c.*
, ccp.bq_corrective(message) as is_corrective
, ccp.bq_English(message) as is_English
, length(message) as message_length
from
ccp.active_2019_commits as c
join
ccp.repos_full as r
on
c.repo_name = r.repo_name
where
y2019_hit_rate < 0.042
and substr(c.commit, 6,1) in ('1', '7', '8','c')
limit 5000
