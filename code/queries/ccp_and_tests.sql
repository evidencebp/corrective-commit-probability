
select
 tests_presence < 0.01 as not_tested
, count(distinct r.repo_name) as repos
, round(avg(ccp),2) as avg_ccp
from
general.repo_properties as r
group by
 not_tested
order by
 not_tested
;

