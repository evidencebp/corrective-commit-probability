

drop table if exists ccp.non_fork_commits_tmp;

# Legacy, large results
# Into ccp.non_fork_commits_tmp
SELECT
r.repo_name as repo_name
, commit
FROM
(select r.repo_name, commit
from
flatten([bigquery-public-data:github_repos.commits],  repo_name) as t
Join
[ccp.active_2019_atleast_200_gitprop] as r
On t.repo_name = r.Repo_name
  where
 year(USEC_TO_TIMESTAMP(committer.date.seconds*1000000))  = 2019
 )

drop table if exists ccp.non_fork_commits;

# Standard
create table
ccp.non_fork_commits
partition by
fake_date
cluster by
repo_name, commit
as
Select
*
, DATE('1980-01-01') as  fake_date
from
ccp.non_fork_commits_tmp
;

drop table if exists ccp.joint_commits;

create table
ccp.joint_commits
as
Select
f.repo_name as first_repo_name
, s.repo_name as second_repo_name
, count(distinct f.commit) as joint_commits
from
ccp.non_fork_commits as f
join
ccp.non_fork_commits as s
on
f.commit = s.commit
# not breaking simmetry with first_repo_name > second_repo_name and doubling the storage to ease work later
where
f.repo_name != s.repo_name
group by
first_repo_name
, second_repo_name
having
count(distinct f.commit) > 50
;


drop table if exists ccp.dominated_repos;
# Standard sql
create table
ccp.dominated_repos
as
Select
dominated.repo_name as repo_name
from
ccp.joint_commits as j
join
ccp.active_repos2019_atleast_100 as dominating
on
j.first_repo_name = dominating.repo_name
join
ccp.active_repos2019_atleast_100 as dominated
on
j.second_repo_name = dominated.repo_name
where
(
(dominating.repo_name != dominated.repo_name)
and
(
(dominating.commits > dominated.commits)
or
(dominating.commits = dominated.commits and dominating.repo_name > dominated.repo_name)

)
)
group by
dominated.repo_name
;

# Clean up
drop table if exists ccp.non_fork_commits_tmp;

drop table if exists ccp.non_fork_commits;
drop table if exists ccp.joint_commits;
drop table if exists ccp.dominated_repos;

