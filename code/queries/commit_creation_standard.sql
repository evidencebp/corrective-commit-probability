drop table if exists ccp.classified_commits;

create table
ccp.classified_commits
partition by
commit_month
cluster by
repo_name, author_email
as
select r.repo_name as repo_name
, commit
, message
, acumen.bq_corrective(message) > 0 as is_fix
, acumen.bq_adaptive(message) > 0 as is_adaptive
, acumen.bq_perfective(message) > 0 as is_perfective
, acumen.bq_refactor(message) > 0 as is_refactor
, acumen.bq_English(message) > 0 as is_English
, author.email as author_email
, TIMESTAMP_SECONDS(committer.date.seconds) as commit_timestamp
, DATE(TIMESTAMP_SECONDS(committer.date.seconds)) as commit_date
, cast(FORMAT_DATE('%Y-%m-01', DATE(TIMESTAMP_SECONDS(committer.date.seconds))) as date) as commit_month
from
`bigquery-public-data.github_repos.commits`
cross join UNNEST(repo_name) as commit_repo_name
Join
`ccp.repos` as r
On commit_repo_name = r.Repo_name
;



drop table if exists ccp.commits_with_file;

create table
ccp.commits_with_file
partition by
commit_month
cluster by
repo_name, commit, file
as
select r.repo_name as repo_name
, difference.old_path as file
, commit
, cast(FORMAT_DATE('%Y-%m-01', DATE(TIMESTAMP_SECONDS(committer.date.seconds))) as date) as commit_month
from
`bigquery-public-data.github_repos.commits`
cross join UNNEST(repo_name) as commit_repo_name
cross join UNNEST(difference) as difference
Join
`ccp.repos` as r
On commit_repo_name = r.Repo_name
;

drop table if exists ccp.classified_commits_with_file;

create table
ccp.classified_commits_with_file
partition by
commit_month
cluster by
repo_name, file, author_email
as
select
c.*
, file
from
ccp.classified_commits as c
Join
ccp.commits_with_file as f
on
c.commit = f.commit
and
c.repo_name = f.repo_name
;
