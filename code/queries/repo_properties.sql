# This file contains the query that defines the scope of the research.
# It contains the condition to be included in the research (active enough in two years).
# It also runs the linguistic model in order to analyze later the CCP.
# The model are implemented using regular expression.
# We can count matches by replacing the match twice, once with ‘#’ and then with ‘’ check the # length difference.

# Standard sql
# into ccp.repos_corrective_properties
Select 
repo_name 
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
, count(distinct case when EXTRACT(year from commit_date) = 2016  then commit else null end)  as y2016_commits
, count(distinct case when EXTRACT(year from commit_date) = 2016  and is_corrective > 0
  then commit else null end) as y2016_hits
, count(distinct case when EXTRACT(year from commit_date) = 2017  then commit else null end)  as y2017_commits
, count(distinct case when EXTRACT(year from commit_date) = 2017  and is_corrective > 0
  then commit else null end) as y2017_hits
, count(distinct case when EXTRACT(year from commit_date) = 2018  then commit else null end)  as y2018_commits
, count(distinct case when EXTRACT(year from commit_date) = 2018  and is_corrective > 0
  then commit else null end) as y2018_hits
, count(distinct case when EXTRACT(year from commit_date) = 2019  then commit else null end)  as y2019_commits
, count(distinct case when EXTRACT(year from commit_date) = 2019  and is_corrective > 0
  then commit else null end) as y2019_hits
,  count(distinct case when ccp.bq_English(message) > 0 then commit else null end) as English_hits
from
ccp.classified_commits
Group by
Repo_name






