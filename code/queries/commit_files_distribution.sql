# Corrective commits' file distribution
# into corrective_commits_files_dist.csv
select
files
, count(*) as cnt
from
general.enhanced_commits
where
extract(year from commit_timestamp) = 2019
and
is_corrective
and files > 0
group by
files
order by
files
;

# Not Corrective commits' file distribution
# into non_corrective_commits_files_dist.csv
select
files
, count(*) as cnt
from
general.enhanced_commits
where
extract(year from commit_timestamp) = 2019
and
not is_corrective
and files > 0
group by
files
order by
files
;