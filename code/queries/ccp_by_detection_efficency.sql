select
detection_efficiency
, avg(ccp) as ccp
, count(*) as repos
, count(*)/7362 as repos_ratio
from
general.repo_properties
group by
detection_efficiency
;