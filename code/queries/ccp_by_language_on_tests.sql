Select
extension
, count(distinct s.repo_name) as repositories
, count(distinct s.commit) as commits
, count(distinct case when s.is_corrective > 0 then s.commit else null end) as corrective_commits
, count(distinct case when s.is_corrective > 0 then s.commit else null end)/count(distinct s.commit) as corrective_hit_rate
from
ccp.commit_size as s
join
ccp.classified_2019_commits_by_file as f
on
s.repo_name = f.repo_name
and
s.commit = f.commit
where
s.files = 1
and
f.is_test
group by
extension
having
count(distinct s.repo_name) > 20

Select
substr(file_name, 0, strpos(file_name, '.')) as base_name
, extension
, count(distinct repo_name) as repositories
, count(distinct commit) as commits
, count(distinct case when is_corrective > 0 then commit else null end) as corrective_commits
, count(distinct case when is_corrective > 0 then commit else null end)/count(distinct commit) as corrective_hit_rate
from
ccp.classified_2019_commits_by_file as f
group by
base_name
, extension
having
count(distinct repo_name) > 20
order by
base_name
, extension

;

