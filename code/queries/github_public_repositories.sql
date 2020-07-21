# Legacy sql
select count( distinct repo_name)
from
[bigquery-public-data:github_repos.commits]
where
year(USEC_TO_TIMESTAMP(committer.date.seconds*1000000)) < 2020