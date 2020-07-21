# This file contains the query that defines the scope of the research.
# It contains the condition to be included in the research (active enough in two years).
# It also runs the linguistic model in order to analyze later the CCP.
# The model are implemented using regular expression.
# We can count matches by replacing the match twice, once with ‘#’ and then with ‘’ check the # length difference.

# Legacy sql
# into ccp.active_repos2019
Select 
repo_name 
, count(distinct commit) as commits
, count(distinct
case when year(USEC_TO_TIMESTAMP(committer.date.seconds*1000000))  = 2019  then commit else null end) as commits_2019
, count(distinct committer.email) as commiters
, min(USEC_TO_TIMESTAMP(committer.date.seconds*1000000)) as start_time
, max(USEC_TO_TIMESTAMP(committer.date.seconds*1000000)) as end_time
from
[bigquery-public-data:github_repos.commits]
Group by
Repo_name
Having
count(distinct
case when year(USEC_TO_TIMESTAMP(committer.date.seconds*1000000))  = 2019  then commit else null end) > 99






