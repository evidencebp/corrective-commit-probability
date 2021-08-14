select
count(*)/count(distinct pull_request_id) as avg_commit_per_pull_request
from
general_ght.pull_request_commits
;
