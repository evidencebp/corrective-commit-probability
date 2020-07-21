# Development speed twin experiments


# Standard Sql
WITH YourTable AS( SELECT 'ChristianSi/lytspel' AS repo_name
UNION ALL SELECT 'jaceklaskowski/kafka-notebook'
UNION ALL SELECT 'undisbeliever/untech-editor'
UNION ALL SELECT 'Codeception/Codeception'
UNION ALL SELECT 'no_slash')
SELECT repo_name, substr(repo_name, strpos(repo_name,'/') +1)
FROM YourTable

# TODO - match with repos for just valid repositories

# Standard Sql
drop table if exists ccp.user_commits_per_rep;

# User in repo contribution
# into user_commits_per_rep
# Legacy
# Allow large results
create table
ccp.user_commits_per_rep
partition by
fake_date
cluster by
Author_email, repo_name
as
Select
repo_name
, Author_email
, extract(year from commit_date) as year
, count(distinct commit) as commits
, count(distinct case when is_corrective > 0 then commit else null end) as corrective_commits_commits
, 1.0*count(distinct case when is_corrective > 0 then commit else null end)/count(distinct commit) as corrective_commits_ratio
, max(DATE('1980-01-01')) as  fake_date
from
ccp.classified_commits
Group by
repo_name
, Author_email
, year
;

drop table if exists ccp.user_commits_profile;

create table
ccp.user_commits_profile
partition by
fake_date
cluster by
Author_email
as
select
Author_email
, count(distinct repo_name) as repos_num
, count(distinct case when commits > 11 then repo_name else null end) as repos_num_above_11
, sum(commits) as commits # might contain duplicates
, sum(corrective_commits_commits) as corrective_commits_commits # might contain duplicates
, max(DATE('1980-01-01')) as  fake_date
from
ccp.user_commits_per_rep
group by
Author_email
;

drop table if exists ccp.project_user_contribution_stats;

# into project_user_contribution_stats
# Legacy, Large results
create table
ccp.project_user_contribution_stats
partition by
fake_date
cluster by
repo_name, year
as
Select
u.Repo_name as repo_name
, year
, max(DATE('1980-01-01')) as  fake_date
# Users
, count(distinct author_email) as users
, count(distinct case when u.commits > 11 then author_email else null end) as users_above_11
, count(distinct case when u.commits > 500 then author_email else null end) as users_above_500

# commits
, sum(u.commits ) as commits
, sum(u.corrective_commits_commits ) as corrective_commits_commits
, 1.0*sum(u.corrective_commits_commits )/sum(u.commits ) as corrective_commits_ratio

, sum( case when  u.commits > 500 then 500 else u.commits end ) as users_capped_commit
, sum( case when u.commits > 11 then u.commits else 0 end) as users_above_11_commits
, sum( case when u.commits > 11 then case when  u.commits > 500 then 500 else u.commits end else 0 end) as commits_above_11_500_cap

# ratios
, case when count(distinct case when  u.commits > 11 then author_email else null end) > 0
then
1.0*sum( u.commits) /
    count(distinct case when  u.commits > 11 then author_email else null end)
else null end as commits_per_above11_users
, case when count(distinct case when u.commits > 11 then author_email else null end) > 0 then
1.0*sum( case when u.commits > 11 then commits else 0 end)
    /count(distinct case when u.commits > 11 then author_email else null end)
else null end as users_above_11_commits_per_above11_users
, case when count(distinct case when  u.commits > 11 then author_email else null end) > 0 then
1.0*sum( case when u.commits > 11 then case when u.commits > 500 then 500 else u.commits end else 0 end)
    /count(distinct case when  u.commits > 11 then author_email else null end)
else null end as users_above_11_500_cap_per_above11_users
From
ccp.user_commits_per_rep as u
Group by
repo_name
, year
;


# Contribution twins comparison
# Twins comparison
# into contribution_twins_stat
Select
First_t.year
, count(*) as pairs
, count( distinct First_t.repo_name) as repos_num
, count(distinct First_t.Author_email) as authors
, sum(case when
 ( (first_t_project.users_above_11_commits_per_above11_users < second_t_project.users_above_11_commits_per_above11_users
and
    First_t.commits < second_t.commits)
          Or
 (first_t_project.users_above_11_commits_per_above11_users > second_t_project.users_above_11_commits_per_above11_users
and
    First_t.commits > second_t.commits)

) then 1 else 0 end) as match_users_above_11_commits_per_above11_users
, sum(case when
 ( (first_t_project.users_above_11_commits_per_above11_users < second_t_project.users_above_11_commits_per_above11_users
and
    First_t.commits > second_t.commits)
          Or
 (first_t_project.users_above_11_commits_per_above11_users > second_t_project.users_above_11_commits_per_above11_users
and
    First_t.commits < second_t.commits)

) then 1 else 0 end) as mismatch_users_above_11_commits_per_above11_users
#### Cap mismatch
####### Too low cases, seems to have a bug

, sum(case when ( (first_t_project.users_above_11_500_cap_per_above11_users < second_t_project.users_above_11_500_cap_per_above11_users
and
    First_t.commits < second_t.commits)
          Or
 (first_t_project.users_above_11_500_cap_per_above11_users > second_t_project.users_above_11_500_cap_per_above11_users
and
    First_t.commits > second_t.commits)

) then 1 else 0 end) as cap_match
, sum(case when ( (first_t_project.users_above_11_500_cap_per_above11_users < second_t_project.users_above_11_500_cap_per_above11_users
and
    First_t.commits > second_t.commits)
          Or
 (first_t_project.users_above_11_500_cap_per_above11_users > second_t_project.users_above_11_500_cap_per_above11_users
and
    First_t.commits < second_t.commits)

) then 1 else 0 end) as cap_mismatch

From
ccp.user_commits_per_rep as first_t
Join
ccp.user_commits_per_rep as second_t
On
First_t.Author_email = second_t.Author_email
And
First_t.year = second_t.year

# same user, different projects
Join
ccp.project_user_contribution_stats as first_t_project
On
First_t.repo_name = first_t_project.Repo_name
Join
ccp.project_user_contribution_stats  as second_t_project
On
second_t.repo_name = second_t_project.Repo_name
# TODO - add different sub repo name
join
ccp.user_commits_profile as profile
on
First_t.Author_email = profile.Author_email
where
# <> is enough to compare project
# < is for breaking symmetry and not getting both (a,b) and (b,a)
# Using symetric in order not to effect statistics like #authors
First_t.repo_name <> second_t.repo_name
and
# Avoid forks
substr(First_t.repo_name, strpos(First_t.repo_name,'/') +1) <> substr(second_t.repo_name, strpos(second_t.repo_name,'/') +1)
and
First_t.commits > 11
 and
Second_t.commits > 11
and
profile.repos_num < 11
and profile.repos_num > 1
Group by
First_t.year
;



Select
First_t.commits -10 > second_t.commits as first_user_better
, first_t_project.users_above_11_500_cap_per_above11_users -10  > second_t_project.users_above_11_500_cap_per_above11_users as first_project_better
, count(*) as pairs
, count( distinct First_t.repo_name) as repos_num
, count(distinct First_t.Author_email) as authors
From
ccp.user_commits_per_rep as first_t
Join
ccp.user_commits_per_rep as second_t
On
First_t.Author_email = second_t.Author_email
And
First_t.year = second_t.year
# same user, different projects
Join
ccp.project_user_contribution_stats as first_t_project
On
First_t.repo_name = first_t_project.Repo_name
Join
ccp.project_user_contribution_stats  as second_t_project
On
second_t.repo_name = second_t_project.Repo_name
#join
#ccp.user_commits_profile as profile
#on
#First_t.Author_email = profile.Author_email
where
# <> is enough to compare project
# < is for breaking symmetry and not getting both (a,b) and (b,a)
# Using symetric in order not to effect statistics like #authors
First_t.repo_name <> second_t.repo_name
and
# Avoid forks
substr(First_t.repo_name, strpos(First_t.repo_name,'/') +1) <> substr(second_t.repo_name, strpos(second_t.repo_name,'/') +1)
and
First_t.commits > 11
 and
Second_t.commits > 11
# and profile.repos_num < 11
# and profile.repos_num > 1
and First_t.year >= 2014
Group by
first_user_better
, first_project_better
order by
first_user_better
, first_project_better
;










