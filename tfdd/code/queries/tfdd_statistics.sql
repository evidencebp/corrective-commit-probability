drop table if exists tfdd.tfdd_raw_statistics;

# Standard Sql
# tfdd.tfdd_raw_statistics
create table
tfdd.tfdd_raw_statistics
as
Select
repo_name
, tfdd_date
, status

# 1 month before
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > - 1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null)) as commits_before_1_months
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.bq_classification
, context.commit, null)) as bug_hits_before_1_months

, if( count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null) )> 0
,1.0*count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.bq_classification
, context.commit, null)) / count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null))
, 0) as bug_ratio_before_1_months

, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.refactor_matches > 0
, context.commit, null)) as refactor_before_1_months
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.refactor_matches > 0
, context.commit, null)) / count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null))
, 0) as refactor_ratio_before_1_months


# 1 month after
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1
, context.commit, null)) as commits_after_1_months
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.bq_classification
, context.commit, null)) as bug_hits_after_1_months

, if( count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) <1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1
, context.commit, null)) > 0
, 1.0*count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.bq_classification
, context.commit, null)) / count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1
, context.commit, null))
, 0 ) as bug_ratio_after_1_months

, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 1*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.refactor_matches > 0
, context.commit, null)) as refactor_after_1_months

# 3 month before
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > - 3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null)) as commits_before_3_months
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.bq_classification
, context.commit, null)) as bug_hits_before_3_months

, if( count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null) )> 0

,1.0*count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.bq_classification
, context.commit, null)) / count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null))
, 0) as bug_ratio_before_3_months

, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.refactor_matches > 0
, context.commit, null)) as refactor_before_3_months

, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.refactor_matches > 0
, context.commit, null))/ count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null))
, 0) as refactor_ratio_before_3_months



# 3 month after
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1
, context.commit, null)) as commits_after_3_months
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.bq_classification
, context.commit, null)) as bug_hits_after_3_months

, if( count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1
, context.commit, null)) > 0
, 1.0*count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.bq_classification
, context.commit, null)) , count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.refactor_matches > 0
, context.commit, null)) as refactor_after_3_months
 as bug_ratio_after_3_months

, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.refactor_matches > 0
, context.commit, null)) as refactor_after_3_months

, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.refactor_matches > 0
, context.commit, null)), count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 3*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.refactor_matches > 0
, context.commit, null)) as refactor_ratio_after_3_months
 as refactor_after_3_months


# 6 month before
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > - 6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null)) as commits_before_6_months
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.bq_classification
, context.commit, null)) as bug_hits_before_6_months

, if( count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null) )> 0

,1.0*count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.bq_classification
, context.commit, null)) / count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null))
, 0) as bug_ratio_before_6_months

, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.refactor_matches > 0
, context.commit, null)) as refactor_before_6_months
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.refactor_matches > 0
, context.commit, null))/ count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null))
, 0) as refactor_ratio_before_6_months


# 6 month after
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1
, context.commit, null)) as commits_after_6_months
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.bq_classification
, context.commit, null)) as bug_hits_after_6_months

, if( count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) <6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1
, context.commit, null)) > 0

, 1.0*count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.bq_classification
, context.commit, null)) / count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1
, context.commit, null))
, 0 ) as bug_ratio_after_6_months

, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.refactor_matches > 0
, context.commit, null)) as refactor_after_6_months

, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.refactor_matches > 0
, context.commit, null)) / count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 6*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1
, context.commit, null))
, 0 )as refactor_ratio_after_6_months


# 12 month before
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > - 12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null)) as commits_before_12_months
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.bq_classification
, context.commit, null)) as bug_hits_before_12_months

, if( count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null) )> 0

,1.0*count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.bq_classification
, context.commit, null)) / count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null))
, 0) as bug_ratio_before_12_months

, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.refactor_matches > 0
, context.commit, null)) as refactor_before_12_months
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1 and context.refactor_matches > 0
, context.commit, null))/ count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > -12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < -1
, context.commit, null))
, 0) as refactor_ratio_before_12_months


# 12 month after
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1
, context.commit, null)) as commits_after_12_months
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.bq_classification
, context.commit, null)) as bug_hits_after_12_months

, if( count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) <12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1
, context.commit, null)) > 0

, 1.0*count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.bq_classification
, context.commit, null)) / count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1
, context.commit, null))
, 0 ) as bug_ratio_after_12_months

, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.refactor_matches > 0
, context.commit, null)) as refactor_after_12_months
, count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1 and context.refactor_matches > 0
, context.commit, null))/ count(distinct IF(TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) < 12*30 and TIMESTAMP_DIFF(TIMESTAMP_SECONDS(context.date_seconds), tfdd_event.tfdd_date, DAY) > 1
, context.commit, null))
, 0 ) as refactor_ratio_after_12_months


, count(distinct commit) as commits
, 1.0*count(distinct if(bq_classification, commit, null))/count(distinct commit) as bug_fix_hit_rate
, 1.0*count(distinct if(refactor_matches > 0, commit, null))/count(distinct commit) as refactor_hit_rate
from
tfdd.tfdd as tfdd_event
join
tfdd.valid_commits_classified as context
on
tfdd_event.repository = context.repo_name
group by
repo_name
, tfdd_date
, status
order by
repo_name
, tfdd_date
, status
;