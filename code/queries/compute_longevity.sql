

# Legacy sql

Select
c.repo_name as repo_name
, max(USEC_TO_TIMESTAMP(committer.date.seconds*1000000)) as end_time
, max(committer.date.seconds*1000000) as end_time_unixtime
, max(DATEDIFF(USEC_TO_TIMESTAMP(committer.date.seconds*1000000), DATE('2018-6-30'))) as days_from_2018_june
, max(DATEDIFF(USEC_TO_TIMESTAMP(committer.date.seconds*1000000), DATE('2018-12-31'))) as days_from_2018_end
, max(DATEDIFF(USEC_TO_TIMESTAMP(committer.date.seconds*1000000), DATE('2019-6-30'))) as days_from_2019_june
, max(DATEDIFF(USEC_TO_TIMESTAMP(committer.date.seconds*1000000), DATE('2019-12-31'))) as days_from_2019_end
from
flatten([bigquery-public-data:github_repos.commits],  repo_name) as c
join
[ccp.repos_full_2018] as r
on
c.repo_name = r.repo_name
Group by
Repo_name

# 2017


Select
c.repo_name as repo_name
, max(USEC_TO_TIMESTAMP(committer.date.seconds*1000000)) as end_time
, max(committer.date.seconds*1000000) as end_time_unixtime
, max(DATEDIFF(USEC_TO_TIMESTAMP(committer.date.seconds*1000000), DATE('2018-6-30'))) as days_from_2018_june
, max(DATEDIFF(USEC_TO_TIMESTAMP(committer.date.seconds*1000000), DATE('2018-12-31'))) as days_from_2018_end
, max(DATEDIFF(USEC_TO_TIMESTAMP(committer.date.seconds*1000000), DATE('2019-6-30'))) as days_from_2019_june
, max(DATEDIFF(USEC_TO_TIMESTAMP(committer.date.seconds*1000000), DATE('2019-12-31'))) as days_from_2019_end
from
flatten([bigquery-public-data:github_repos.commits],  repo_name) as c
join
[ccp.repos_2017_fork] as r
on
c.repo_name = r.repo_name
where
not Fork
Group by
Repo_name

# Legacy sql
# into ccp.active_repos2017
Select
repo_name
, count(distinct commit) as commits
, count(distinct
case when year(USEC_TO_TIMESTAMP(committer.date.seconds*1000000))  = 2017  then commit else null end) as commits_2017
ccp.bq_corrective(message)
, count(distinct
case when year(USEC_TO_TIMESTAMP(committer.date.seconds*1000000))  = 2017 and ccp.bq_corrective(message) then commit else null end) as commits_2017
, 1.0*count(distinct
case when year(USEC_TO_TIMESTAMP(committer.date.seconds*1000000))  = 2017 and ccp.bq_corrective(message) then commit else null end)
/count(distinct
case when year(USEC_TO_TIMESTAMP(committer.date.seconds*1000000))  = 2017  then commit else null end) as commits_corrective_rate


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






