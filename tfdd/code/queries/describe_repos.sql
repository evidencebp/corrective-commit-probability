# Standard Sql
Select
repo_name
, count(distinct commit) as commits
# authors
, count(distinct author_email) as author_emails
# Start, end
, min(TIMESTAMP_SECONDS(date_seconds)) as start_time
, max(TIMESTAMP_SECONDS(date_seconds)) as end_time
# Bug fix rate
, 1.0*count(distinct if(bq_classification, commit, null))/count(distinct commit) as bug_fix_hit_rate
from
tfdd.valid_commits_classified
group by
repo_name
order by
repo_name