# Create distinct repositories table
# into tfdd_repos
Select
repository as repo_name
from 
tfdd.tfdd
group by
repository
order by 
repository

# Collect tfdd commits into a seperate small table
# into valid_commits
select 
c.commit as commit
, author.name
, author.email
, committer.name
, committer.email
, subject
, message
, c.repo_name as repo_name
,  author.date.seconds as date_seconds
from
flatten([bigquery-public-data:github_repos.commits], repo_name) as c
join
tfdd.tfdd_repos as d
on c.repo_name = d.repo_name