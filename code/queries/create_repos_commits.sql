# Legacy Sql
# Large results
# Into active_2019_commits

SELECT
r.repo_name as repo_name
, commit
, message
, Author.email as author_email
, author.name as author_name
, USEC_TO_TIMESTAMP(committer.date.seconds*1000000)  as commit_date
FROM
(select r.repo_name, commit, message, author.email, committer.date.seconds
from
#[bigquery-public-data:github_repos.commits]) as t
flatten([bigquery-public-data:github_repos.commits],  repo_name) as t
Join
[ccp.repos_2019] as r
On t.repo_name = r.Repo_name
 )
where
# In order not to have more irrelevant commits and make the work reproducable, independed of the query run time
year(USEC_TO_TIMESTAMP(committer.date.seconds * 1000000)) < 2020


# Legacy Sql
# Large results
# Into active_2019_commits_by_file
drop table if exists ccp.active_2019_commits_by_file;

SELECT
r.repo_name as repo_name
, commit
, message
, Author.email
, file
, USEC_TO_TIMESTAMP(committer.date.seconds*1000000)  as commit_date
, year(USEC_TO_TIMESTAMP(committer.date.seconds*1000000))  as year
FROM
(select r.repo_name, commit, message, author.email, difference.old_path as file, committer.date.seconds
from
#[bigquery-public-data:github_repos.commits]) as t
flatten([bigquery-public-data:github_repos.commits],  repo_name) as t
Join
[ccp.repos_2019] as r
On t.repo_name = r.Repo_name
 )
where
# In order not to have more irrelevant commits and make the work reproducable, independed of the query run time
year(USEC_TO_TIMESTAMP(committer.date.seconds * 1000000)) < 2020
;
