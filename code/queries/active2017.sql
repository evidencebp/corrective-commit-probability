# This file contains the query that defines the scope of the research.
# It contains the condition to be included in the research (active enough in two years).
# It also runs the linguistic model in order to analyze later the CCP.
# The model are implemented using regular expression.
# We can count matches by replacing the match twice, once with ‘#’ and then with ‘’ check the # length difference.

# Legacy sql
# into ccp.active_repos2017
Select
repo_name
, count(distinct commit) as commits
, count(distinct
case when year(USEC_TO_TIMESTAMP(committer.date.seconds*1000000))  = 2017  then commit else null end) as commits_2017
, count(distinct committer.email) as commiters
, min(USEC_TO_TIMESTAMP(committer.date.seconds*1000000)) as start_time
, max(USEC_TO_TIMESTAMP(committer.date.seconds*1000000)) as end_time
from
[bigquery-public-data:github_repos.commits]
Group by
Repo_name
Having
count(distinct
case when year(USEC_TO_TIMESTAMP(committer.date.seconds*1000000))  = 2017  then commit else null end) > 199

# Legacy Sql
# Large results
# Into active_2017_commits

SELECT
r.repo_name as repo_name
, commit
, message
, Author.email
, USEC_TO_TIMESTAMP(committer.date.seconds*1000000)  as commit_date
FROM
(select r.repo_name, commit, message, author.email, committer.date.seconds
from
#[bigquery-public-data:github_repos.commits]) as t
flatten([bigquery-public-data:github_repos.commits],  repo_name) as t
Join
[ccp.repos_2017_fork] as r
On t.repo_name = r.Repo_name
 )
where
# In order not to have more irrelevant commits and make the work reproducable, independed of the query run time
year(USEC_TO_TIMESTAMP(committer.date.seconds * 1000000)) < 2020


# Standard Sql
drop table if exists ccp.classified_commits_2017;

# into classified_commits
# Standard
# Allow large results
create table
ccp.classified_commits_2017
partition by
fake_date
cluster by
repo_name, commit_date, commit
as
Select
*
, ccp.bq_corrective(message) as is_corrective
, DATE('1980-01-01') as  fake_date
from
ccp.active_2017_commits
;

# Standard Sql
drop table if exists ccp.repos_properties_2017;

create table ccp.repos_properties_2017
as
Select
repo_name
, extract(year from commit_date) as year
, count(distinct commit) as commits
, count(distinct Author_email) as authors
, min(commit_date) as start_time
, max(commit_date) as end_time
, count(distinct case when (
is_corrective > 0
)  then commit else null end) as hits
, 1.0*count(distinct case when
is_corrective > 0
 then commit else null end) /count(distinct commit) as hit_ratio
, 1.253*(count(distinct case when
is_corrective > 0
 then commit else null end) /count(distinct commit)) -0.053 as ccp
from
ccp.classified_commits_2017
group by
repo_name
, year
order by
repo_name
, year

Select *
from
ccp.repos_properties_2017
where year = 2017


drop table if exists ccp.joint_commits_2017;

create table
ccp.joint_commits_2017
as
Select
f.repo_name as first_repo_name
, s.repo_name as second_repo_name
, count(distinct f.commit) as joint_commits
from
ccp.classified_commits_2017 as f
join
ccp.classified_commits_2017 as s
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


drop table if exists ccp.dominated_repos_2017;
# Standard sql
create table
ccp.dominated_repos_2017
as
Select
dominated.repo_name as repo_name
from
ccp.joint_commits_2017 as j
join
ccp.active_repos2017 as dominating
on
j.first_repo_name = dominating.repo_name
join
ccp.active_repos2017 as dominated
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


