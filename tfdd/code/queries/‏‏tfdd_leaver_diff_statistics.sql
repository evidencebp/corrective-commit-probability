
# Legacy Sql
# into tfdd.tfdd_leavers_diff_statistics

SELECT 
repo_name
, leaver
, tfdd_date
, status

, commits_after_1_months -  commits_before_1_months as commits_diff_1_months
, if(commits_before_1_months > 0, 1.0*(commits_after_1_months -  commits_before_1_months)/commits_before_1_months, null) 
as commits_rel_diff_1_months

, bug_hits_after_1_months -  bug_hits_before_1_months as bug_hits_1_months
, if(bug_hits_before_1_months > 0, 1.0*(bug_hits_after_1_months -  bug_hits_before_1_months)/bug_hits_before_1_months, null) 
as bug_hits_rel_diff_1_months

, bug_ratio_after_1_months -  bug_ratio_before_1_months as bug_ratio_1_months
, if(bug_ratio_before_1_months > 0, 1.0*(bug_ratio_after_1_months -  bug_ratio_before_1_months)/bug_ratio_before_1_months, null) 
as bug_ratio_rel_diff_1_months

, refactor_after_1_months -  refactor_before_1_months as refactor_diff_1_months
, if(refactor_before_1_months > 0, 1.0*(refactor_after_1_months -  refactor_before_1_months)/refactor_before_1_months, null) 
as refactor_rel_diff_1_months

# 3 months
, commits_after_3_months -  commits_before_3_months as commits_diff_3_months 
, if(commits_before_3_months > 0, 1.0*(commits_after_3_months -  commits_before_3_months )/commits_before_3_months , null) 
as commits_rel_diff_3_months 

, bug_hits_after_3_months -  bug_hits_before_3_months as bug_hits_3_months 
, if(bug_hits_before_3_months > 0, 1.0*(bug_hits_after_3_months -  bug_hits_before_3_months )/bug_hits_before_3_months , null) 
as bug_hits_rel_diff_3_months 

, bug_ratio_after_3_months -  bug_ratio_before_3_months as bug_ratio_3_months 
, if(bug_ratio_before_3_months > 0, 1.0*(bug_ratio_after_3_months -  bug_ratio_before_3_months )/bug_ratio_before_3_months , null) 
as bug_ratio_rel_diff_3_months 

, refactor_after_3_months -  refactor_before_3_months as refactor_diff_3_months 
, if(refactor_before_3_months > 0, 1.0*(refactor_after_3_months -  refactor_before_3_months )/refactor_before_3_months , null) 
as refactor_rel_diff_3_months 

# 6 months 
, commits_after_6_months  -  commits_before_6_months  as commits_diff_6_months  
, if(commits_before_6_months  > 0, 1.0*(commits_after_6_months  -  commits_before_6_months  )/commits_before_6_months  , null) 
as commits_rel_diff_6_months  

, bug_hits_after_6_months  -  bug_hits_before_6_months  as bug_hits_6_months  
, if(bug_hits_before_6_months  > 0, 1.0*(bug_hits_after_6_months  -  bug_hits_before_6_months  )/bug_hits_before_6_months  , null) 
as bug_hits_rel_diff_6_months  

, bug_ratio_after_6_months  -  bug_ratio_before_6_months  as bug_ratio_6_months  
, if(bug_ratio_before_6_months  > 0, 1.0*(bug_ratio_after_6_months  -  bug_ratio_before_6_months  )/bug_ratio_before_6_months  , null) 
as bug_ratio_rel_diff_6_months  

, refactor_after_6_months  -  refactor_before_6_months  as refactor_diff_6_months  
, if(refactor_before_6_months  > 0, 1.0*(refactor_after_6_months  -  refactor_before_6_months  )/refactor_before_6_months  , null) 
as refactor_rel_diff_6_months  

# 12 months 
, commits_after_12_months   -  commits_before_12_months   as commits_diff_12_months   
, if(commits_before_12_months   > 0, 1.0*(commits_after_12_months   -  commits_before_12_months   )/commits_before_12_months   , null) 
as commits_rel_diff_12_months   

, bug_hits_after_12_months   -  bug_hits_before_12_months   as bug_hits_12_months   
, if(bug_hits_before_12_months   > 0, 1.0*(bug_hits_after_12_months   -  bug_hits_before_12_months   )/bug_hits_before_12_months   , null) 
as bug_hits_rel_diff_12_months   

, bug_ratio_after_12_months   -  bug_ratio_before_12_months   as bug_ratio_12_months   
, if(bug_ratio_before_12_months   > 0, 1.0*(bug_ratio_after_12_months   -  bug_ratio_before_12_months   )/bug_ratio_before_12_months   , null) 
as bug_ratio_rel_diff_12_months   

, refactor_after_12_months   -  refactor_before_12_months   as refactor_diff_12_months   
, if(refactor_before_12_months   > 0, 1.0*(refactor_after_12_months   -  refactor_before_12_months   )/refactor_before_12_months   , null) 
as refactor_rel_diff_12_months   

FROM [hotspots-readability:tfdd.tfdd_leavers_raw_statistics] 



SELECT 
d.status
, count(*) as tfdd_events
, count(distinct d.repo_name) as repositories
, count(distinct d.leaver) as leavers
, avg(commits_diff_1_months) as commits_diff_1_months_avg
# , stddev(commits_diff_1_months) as commits_diff_1_months_sd
, avg(commits_rel_diff_1_months)as commits_rel_diff_1_months_avg
# , stddev(commits_rel_diff_1_months) as commits_rel_diff_1_months_sd
, avg(bug_hits_1_months) as bug_hits_diff_1_months_avg
# , stddev(bug_hits_1_months) as bug_hits_1_months_sd
, avg(bug_hits_rel_diff_1_months) as bug_hits_rel_diff_1_months_avg
# , stddev(bug_hits_rel_diff_1_months) as bug_hits_rel_diff_1_months_sd
, avg(bug_ratio_1_months) as bug_ratio_1_months_avg
# , stddev(bug_ratio_1_months) as bug_ratio_1_months_sd
, avg(bug_ratio_rel_diff_1_months) as bug_ratio_rel_diff_1_months_avg
# , stddev(bug_ratio_rel_diff_1_months) as bug_ratio_rel_diff_1_months_sd
, avg(refactor_diff_1_months) as refactor_diff_1_months_avg
# , stddev(refactor_diff_1_months) as refactor_diff_1_months_sd
, avg(refactor_rel_diff_1_months) as refactor_rel_diff_1_months_avg
# , stddev(refactor_rel_diff_1_months) as refactor_rel_diff_1_months_sd

, avg(commits_diff_3_months) as commits_diff_3_months_avg
# , stddev(commits_diff_3_months) as commits_diff_3_months_sd
, avg(commits_rel_diff_3_months) as commits_rel_diff_3_months_avg
# , stddev(commits_rel_diff_3_months) as commits_rel_diff_3_months_sd
, avg(bug_hits_3_months) as bug_hits_diff_3_months_avg
# , stddev(bug_hits_3_months) as bug_hits_diff_3_months_sd
, avg(bug_hits_rel_diff_3_months) as bug_hits_rel_diff_3_months_avg
# , stddev(bug_hits_rel_diff_3_months) as bug_hits_rel_diff_3_months_sd
, avg(bug_ratio_3_months) as bug_ratio_3_months_avg
# , stddev(bug_ratio_3_months) as bug_ratio_3_months_sd
, avg(bug_ratio_rel_diff_3_months) as bug_ratio_rel_diff_3_months_avg
# , stddev(bug_ratio_rel_diff_3_months) as bug_ratio_rel_diff_3_months_sd
, avg(refactor_diff_3_months) as refactor_diff_3_months_avg
# , stddev(refactor_diff_3_months) as refactor_diff_3_months_sd
, avg(refactor_rel_diff_3_months) as refactor_rel_diff_3_months_avg
# , stddev(refactor_rel_diff_3_months) as refactor_rel_diff_3_months_sd 

, avg(commits_diff_6_months) as commits_diff_6_months_avg
# , stddev(commits_diff_6_months) as commits_diff_6_months_sd
, avg(commits_rel_diff_6_months) as commits_rel_diff_6_months_avg
# , stddev(commits_rel_diff_6_months) as commits_rel_diff_6_months_sd
, avg(bug_hits_6_months) as bug_hits_6_diff_months_avg
# , stddev(bug_hits_6_months) as bug_hits_diff_6_months_sd
, avg(bug_hits_rel_diff_6_months) as bug_hits_rel_diff_6_months_avg
# , stddev(bug_hits_rel_diff_6_months) as bug_hits_rel_diff_6_months_sd
, avg(bug_ratio_6_months) as bug_ratio_6_months_avg
# , stddev(bug_ratio_6_months) as bug_ratio_6_months_sd
, avg(bug_ratio_rel_diff_6_months) as bug_ratio_rel_diff_6_months_avg
# , stddev(bug_ratio_rel_diff_6_months) as bug_ratio_rel_diff_6_months_sd
, avg(refactor_diff_6_months) as refactor_diff_6_months_avg
# , stddev(refactor_diff_6_months) as refactor_diff_6_months_sd
, avg(refactor_rel_diff_6_months) as refactor_rel_diff_6_months_avg
# , stddev(refactor_rel_diff_6_months) as refactor_rel_diff_6_months_sd 

, avg(commits_diff_12_months) as commits_diff_12_months_avg
# , stddev(commits_diff_12_months) as commits_diff_12_months_sd
, avg(commits_rel_diff_12_months) as commits_rel_diff_12_months_avg
# , stddev(commits_rel_diff_12_months) as commits_rel_diff_12_months_sd
, avg(bug_hits_12_months) as bug_hits_diff_12_months_avg
# , stddev(bug_hits_12_months) as bug_hits_diff_12_months_sd
, avg(bug_hits_rel_diff_12_months) as bug_hits_rel_diff_12_months_avg
# , stddev(bug_hits_rel_diff_12_months) as bug_hits_rel_diff_12_months_sd
, avg(bug_ratio_12_months) as bug_ratio_12_months_avg
# , stddev(bug_ratio_12_months) as bug_ratio_12_months_sd
, avg(bug_ratio_rel_diff_12_months) as bug_ratio_rel_diff_12_months_avg
# , stddev(bug_ratio_rel_diff_12_months) as bug_ratio_rel_diff_12_months_sd
, avg(refactor_diff_12_months) as refactor_diff_12_months_avg
# , stddev(refactor_diff_12_months) as refactor_diff_12_months_sd
, avg(refactor_rel_diff_12_months) as refactor_rel_diff_12_months_avg
# , stddev(refactor_rel_diff_12_months) as refactor_rel_diff_12_months_sd 

FROM [hotspots-readability:tfdd.tfdd_leavers_diff_statistics] as d
join 
[hotspots-readability:tfdd.tfdd_leavers_raw_statistics] as r
on
d.repo_name = r.repo_name
and
d.tfdd_date = r.tfdd_date
and
d.leaver = r.leaver

where
commits_before_1_months > 9
and
commits_after_1_months > 9

group by
d.status
order by
d.status