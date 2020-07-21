
# Standard Sql
drop table if exists ccp.commit_size;

# into commit_size
# Standard
# Allow large results
create table
ccp.commit_size
partition by
fake_date
cluster by
repo_name, commit
as
Select
repo_name
, commit
, max(Author_email) as Author_email
, max(commit_date) as commit_date
, max(is_corrective) as is_corrective
, count(distinct file) as files
, count(distinct file) - count(distinct case when is_test then file else null end) as non_test_files
, count(distinct case when is_test then file else null end) as test_files
, DATE('1980-01-01') as  fake_date
from
ccp.classified_2019_commits_by_file
group by
repo_name
, commit
;

# Commit size distribution
Select
files
, count(distinct commit) as commits
from
ccp.commit_size
group by
files
order by
files
;

# Commit size per corrective/ not corrective type
# 103 is the 99 percentile in the files commit size distribution
# commit_size_by_corrective.csv
select
is_corrective > 0 as corrective_commit
, count(distinct commit) as commits
, avg(files) as avg_files
, avg(case when files > 103 then 103 else files end) as avg_capped_files
, avg(non_test_files) as avg_non_test_files
, avg(case when non_test_files > 103 then 103 else non_test_files end) as avg_capped_non_test_files
, avg(test_files) as avg_test_files
, avg(case when test_files > 103 then 103 else test_files end) as avg_capped_test_files
from
ccp.commit_size
group by
corrective_commit
;

drop table if exists ccp.coupling_by_repo;

# coupling_by_repo.csv creation
# Commit size per corrective/ not corrective type
# 103 is the 99 percentile in the files commit size distribution
# Standard Sql
# into coupling_by_repo
# Standard
# Allow large results
create table
ccp.coupling_by_repo
partition by
fake_date
cluster by
repo_name, year
as
select
repo_name
, extract(year from commit_date) as year
, avg(files) as avg_files
, stddev(files) as std_files
, avg(case when files > 103 then 103 else files end) as avg_capped_files
, stddev(case when files > 103 then 103 else files end) as std_capped_files
, avg(non_test_files) as avg_non_test_files
, avg(case when non_test_files > 103 then 103 else non_test_files end) as avg_capped_non_test_files
, avg(test_files) as avg_test_files
, avg(case when test_files > 103 then 103 else test_files end) as avg_capped_test_files
, DATE('1980-01-01') as  fake_date
from
ccp.commit_size
where
is_corrective = 0
group by
repo_name
, year
;

drop table if exists ccp.coupling_by_repo_by_user;

# into coupling_by_repo_by_user
# Standard
# Allow large results
create table
ccp.coupling_by_repo_by_user
partition by
fake_date
cluster by
repo_name, year, Author_email
as
select
repo_name
, extract(year from commit_date) as year
, Author_email
, count(distinct commit) as commits
, avg(files) as avg_files
, avg(case when files > 103 then 103 else files end) as avg_capped_files
, avg(non_test_files) as avg_non_test_files
, avg(case when non_test_files > 103 then 103 else non_test_files end) as avg_capped_non_test_files
, avg(test_files) as avg_test_files
, avg(case when test_files > 103 then 103 else test_files end) as avg_capped_test_files
, DATE('1980-01-01') as  fake_date
from
ccp.commit_size
where
is_corrective = 0
group by
repo_name
, year
, Author_email
;
