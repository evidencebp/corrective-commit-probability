Select *
from ccp.classified_commits

where
(LENGTH(REGEXP_REPLACE(lower(message),'(vulnerabilit(?:y|ies)|cve(-d+)?(-d+)?|security|cyber|threat(s)?)', '@'))
-LENGTH(REGEXP_REPLACE(lower(message),'(vulnerabilit(?:y|ies)|cve(-d+)?(-d+)?|security|cyber|threat(s)?)', '')))
> 0

Select
count(distinct commit) as commits
, count(distinct case when is_corrective > 0  then commit else null end) as corrective_commits
, 1.0*count(distinct case when is_corrective > 0  then commit else null end)/count(distinct commit) as corrective_commits_ratio
, count(distinct repo_name) as repositories
, count(distinct case when is_corrective > 0  then repo_name else null end) as corrective_repo_name
, 1.0*count(distinct case when is_corrective > 0 then repo_name else null end)/count(distinct repo_name) as corrective_repo_ratio
from
ccp.cyber_classified_commits

Select
commits
, count(distinct repo_name) as repositories
from
(
Select
repo_name
, count(distinct commit) as commits
from
ccp.cyber_classified_commits
group by
repo_name
) as innerSql
group by
commits
order by commits


