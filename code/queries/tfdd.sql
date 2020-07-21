drop table if exists tfdd.tfdd_statistics_6_months;

# Standard Sql
# tfdd.tfdd_statistics_6_months
create table
tfdd.tfdd_statistics_6_months
as
Select
repo_name
, tfdd_date
, status

#  before
## Commits
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 0
 , context.commit, null)) as commits_before
, count(distinct  IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 0  and context.bq_classification
, context.commit, null)) as bug_hits_before

## Bug ratio
, if(count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 0
 , context.commit, null)) > 0
 , count(distinct  IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 0  and context.bq_classification
, context.commit, null))/count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 0
 , context.commit, null))
 , null) as bug_ratio_before

## refactor ratio
, if(count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 0
 , context.commit, null)) > 0
 , count(distinct  IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 0  and context.refactor_matches > 0
, context.commit, null))/count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 0
 , context.commit, null))
 , null) as refactor_ratio_before


#  after
## bugs
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 0
 , context.commit, null)) as commits_after
, count(distinct  IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 0  and context.bq_classification
, context.commit, null)) as bug_hits_after

## Bugs ratio
, if(count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 0
 , context.commit, null)) > 0
 , count(distinct  IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 0  and context.bq_classification
, context.commit, null))/count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 0
 , context.commit, null))
 , null) as bug_ratio_after

## Bugs ratio
, if(count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 0
 , context.commit, null)) > 0
 , count(distinct  IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 0  and context.refactor_matches > 0
, context.commit, null))/count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 0
 , context.commit, null))
 , null) as refactor_ratio_after


, count(distinct commit) as commits
, 1.0*count(distinct if(bq_classification, commit, null))/count(distinct commit) as bug_fix_hit_rate
, 1.0*count(distinct if(refactor_matches > 0, commit, null))/count(distinct commit) as refactor_hit_rate
, '6_months' as context
from
tfdd.tfdd as tfdd_event
join
tfdd.valid_commits_classified as context
on
tfdd_event.repository = context.repo_name
where
abs(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY)) < 6*30
and abs(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY)) <> 0
group by
repo_name
, tfdd_date
, status
order by
repo_name
, tfdd_date
, status
;



Select
avg((commits_after - commits_before)/commits_before) as commits_relative_change
, avg(1.253*(bug_ratio_after - bug_ratio_before)) as bug_ratio_change # 1.253*x -0.053
# We can ommit the addaptive constant of the mle since it is added in both cases
, avg(1.695*(refactor_ratio_after - refactor_ratio_before)) as refactor_change # 1.695*x -0.034
from
tfdd.tfdd_statistics_6_months
where
commits_before > 0
and
bug_ratio_before > 0
;
