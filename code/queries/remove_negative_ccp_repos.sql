drop table if exists general.commits_new_year;

create table
general.commits_new_year
as
select
c.*
from
`bigquery-public-data.github_repos.commits` as c
cross join  UNNEST(repo_name) as commit_repo_name
Join
general.repos_2020 as r
On commit_repo_name = r.Repo_name
;

drop table if exists general.enhanced_commits_new_year;

create table
general.enhanced_commits_new_year
as
select
r.repo_name as repo_name
, commit
, max(general.bq_corrective(message) > 0) as is_corrective

from
general.commits_new_year
cross join  UNNEST(repo_name) as commit_repo_name
Join
general.repos_2020 as r
On commit_repo_name = r.Repo_name
cross join  UNNEST(parent) as parent
group by
r.repo_name
, commit
;

drop table if exists general.repos_ccp_new_year;

create table
general.repos_ccp_new_year
as
select
repo_name as repo_name
, count(distinct commit) as commits
, avg(if(is_corrective, 1,0)) as corrective_rate
, general.bq_ccp_mle(avg(if(is_corrective , 1,0))) as ccp
from
general.enhanced_commits_new_year
group by
repo_name
;

drop table if exists general.valid_repos_new_year;

create table
general.valid_repos_new_year
as
select
r.*
, False as Is_Company
from
general.repos_2020 as r
join
general.repos_ccp_new_year as v
on
r.repo_name = v.Repo_name
where
v.ccp > 0
and
v.ccp < 1
;

# TODO - update companies repos in real values
update general.valid_repos_new_year
set Is_Company = null
where true
;


drop table if exists general.commits_new_year;
drop table if exists general.enhanced_commits_new_year;
drop table if exists general.repos_ccp_new_year;
