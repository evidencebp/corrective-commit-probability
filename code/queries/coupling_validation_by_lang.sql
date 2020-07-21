drop table if exists ccp.active_2019_files_coupling;

create table ccp.active_2019_files_coupling
as
select f.repo_name as repo_name
, file
, count(distinct f.commit) as commits
, count(distinct case when     REGEXP_CONTAINS( message, 'coupling|coupled')     then f.commit else null end) as commits_with_coupling
, 1.0*count(distinct case when     REGEXP_CONTAINS( message, 'coupling|coupled')     then f.commit else null end)/count(distinct f.commit) as coupling_hit_rate
, avg(case when is_corrective > 0 then files else null end ) as avg_non_corrective_files
, avg(case when is_corrective > 0 then non_test_files else null end ) as avg_non_corrective_non_test_files
, avg(case when is_corrective > 0 then case when files > 103 then 103 else non_test_files end else null end ) as avg_capped_non_corrective_files
, avg(case when is_corrective > 0 then case when non_test_files > 103 then 103 else non_test_files end else null end ) as avg_capped_non_corrective_non_test_files
from
ccp.active_2019_commits_by_file as f
join
ccp.commit_size as cs
on f.commit = cs.commit
where
cs.files < 103 # removing too big commits
group by
repo_name
, file
Having count(distinct f.commit) > 9
;

Select round(coupling_hit_rate, 2) as coupling_hit_rate,
count(*) as files
, avg(avg_non_corrective_files) as avg_non_corrective_files
, avg(avg_non_corrective_non_test_files) as avg_non_corrective_non_test_files
, avg(avg_capped_non_corrective_files) as avg_capped_non_corrective_files
, avg(avg_capped_non_corrective_non_test_files) as avg_capped_non_corrective_non_test_files
from
ccp.active_2019_files_coupling
group by
coupling_hit_rate
order by
coupling_hit_rate;

# Into distributions\coupled_by_name.csv
# The 0.1 is chosen to be more than a single commit with a file
# with the minimal threshold of 10 commits
Select round(coupling_hit_rate, 2) > 0.1 as coupled_by_name,
count(*) as files
, avg(avg_non_corrective_files) as avg_non_corrective_files
, avg(avg_non_corrective_non_test_files) as avg_non_corrective_non_test_files
, avg(avg_capped_non_corrective_files) as avg_capped_non_corrective_files
, avg(avg_capped_non_corrective_non_test_files) as avg_capped_non_corrective_non_test_files
from
ccp.active_2019_files_coupling
group by
coupled_by_name
order by
coupled_by_name;

