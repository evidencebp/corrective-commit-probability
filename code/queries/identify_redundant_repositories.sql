
drop table if exists general.non_fork_commits_tmp;

create table
general.non_fork_commits_tmp
as
select
commit_repo_name
, c.*
from
`bigquery-public-data.github_repos.commits` as c
cross join  UNNEST(repo_name) as commit_repo_name
Join
general.2020_above_50_10_jan as r
On commit_repo_name = r.Repo_name
;


drop table if exists general.non_fork_commits;

# Standard
create table
general.non_fork_commits
partition by
fake_date
cluster by
commit_repo_name, commit
as
Select
*
, DATE('1980-01-01') as  fake_date
from
general.non_fork_commits_tmp
;

drop table if exists general.joint_commits;

create table
general.joint_commits
as
Select
f.commit_repo_name as first_repo_name
, s.commit_repo_name as second_repo_name
, count(distinct f.commit) as joint_commits
from
general.non_fork_commits as f
join
general.non_fork_commits as s
on
f.commit = s.commit
# not breaking symmetry with first_repo_name > second_repo_name and doubling the storage to ease work later
where
f.commit_repo_name != s.commit_repo_name
group by
first_repo_name
, second_repo_name
having
count(distinct f.commit) > 50
;

drop table if exists general.repo_commits;

create table
general.repo_commits
as
Select
f.commit_repo_name as repo_name
, count(distinct f.commit) as commits
from
general.non_fork_commits as f
group by
f.commit_repo_name
;

drop table if exists general.dominated_repos;

create table
general.dominated_repos
as
Select
dominated.repo_name as repo_name
from
general.joint_commits as j
join
general.repo_commits as dominating
on
j.first_repo_name = dominating.repo_name
join
general.repo_commits as dominated
on
j.second_repo_name = dominated.repo_name
where

(dominating.repo_name != dominated.repo_name)
and
(
(dominating.commits > dominated.commits)
and
(dominated.commits = j.joint_commits)
#or
#(dominating.commits = dominated.commits and dominating.repo_name > dominated.repo_name)

)
group by
dominated.repo_name
;


drop table if exists general.2020_above_50_10_jan_no_dominated;

create table
general.2020_above_50_10_jan_no_dominated
as
select
r.*
from
general.2020_above_50_10_jan as r
left join
general.dominated_repos as d
on
r.repo_name = d.repo_name
where
d.repo_name is null
;

# Clean up
drop table if exists general.non_fork_commits_tmp;

drop table if exists general.non_fork_commits;
drop table if exists general.joint_commits;
drop table if exists general.dominated_repos;

