drop table if exists ccp.file_quality_reference;

create table ccp.file_quality_reference
as
select
repo_name
, file
, 1.0* count(distinct commit) as commits
, 1.0*count(distinct case when     REGEXP_CONTAINS( lower(message)
,'low(?:-| )quality')     then commit else null end)/count(distinct commit) as low_quality_hit_rate

, 1.0*count(distinct case when     REGEXP_CONTAINS( lower(message)
,'technical.debt')     then commit else null end)/count(distinct commit) as technical_debt_hit_rate
, 1.0*count(distinct case when     REGEXP_CONTAINS( lower(message)
,'code.smell(s)?')     then commit else null end)/count(distinct commit) as code_smell_hit_rate
, 1.0*count(distinct case when     REGEXP_CONTAINS( lower(message)
, 'disappointing|disheartening|displeasing|mortifying|not up to (par|snuff)|poor|rotten|substandard|unsatisfactory|bad|horrible|terrible|shit|crap|lousy|awful|fuck|disgusting|hideous|nasty|scary|shameful|shame|shocking|repulsive|revolting|stink')
then commit else null end)/count(distinct commit) as swearing_hit_rate


, 1.0*count(distinct case when     REGEXP_CONTAINS( lower(message)
,'function')     then commit else null end)/count(distinct commit) as function_hit_rate
, 1.0*count(distinct case when     REGEXP_CONTAINS( lower(message)
,'algorithm')     then commit else null end)/count(distinct commit) as algorithm_hit_rate
, 1.0*count(distinct case when     REGEXP_CONTAINS( lower(message)
,'singelton')     then commit else null end)/count(distinct commit) as singelton_hit_rate

from
ccp.active_2019_commits_by_file as f
#where
#length(message) > 200
group by
repo_name
, file
having
count(distinct commit) > 9
;

# into ccp_by_quality_terms.csv
select
count(*) as count
, avg(1.253*corrective_rate -0.053) as ccp_avg
, stddev(1.253*corrective_rate -0.053) as ccp_std
# low_quality_hit_rate
, avg(case when low_quality_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as low_quality_avg
, avg(case when low_quality_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_low_quality_avg
, stddev(case when low_quality_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as low_quality_std
, stddev(case when low_quality_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_low_quality_std
, sum(case when low_quality_hit_rate > 0.1
then 1
else 0 end) as low_quality_cnt
, sum(case when low_quality_hit_rate > 0.1
then 0
else 1 end) as not_low_quality_cnt


# technical_debt_hit_rate
, avg(case when technical_debt_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as technical_debt_avg
, avg(case when technical_debt_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_technical_debt_avg
, stddev(case when technical_debt_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as technical_debt_std
, stddev(case when technical_debt_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_technical_debt_std
, sum(case when technical_debt_hit_rate > 0.1
then 1
else 0 end) as technical_debt_cnt
, sum(case when technical_debt_hit_rate > 0.1
then 0
else 1 end) as not_technical_debt_cnt

# code_smell_hit_rate
, avg(case when code_smell_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as code_smell_avg
, avg(case when code_smell_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_code_smell_avg
, stddev(case when code_smell_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as code_smell_std
, stddev(case when code_smell_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_code_smell_std
, sum(case when code_smell_hit_rate > 0.1
then 1
else 0 end) as code_smell_cnt
, sum(case when code_smell_hit_rate > 0.1
then 0
else 1 end) as not_code_smell_cnt

# swearing_hit_rate
, avg(case when swearing_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as swearing_avg
, avg(case when swearing_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_swearing_avg
, stddev(case when swearing_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as swearing_std
, stddev(case when swearing_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_swearing_std
, sum(case when swearing_hit_rate > 0.1
then 1
else 0 end) as swearing_cnt
, sum(case when swearing_hit_rate > 0.1
then 0
else 1 end) as not_swearing_cnt


#  function_hit_rate
, avg(case when  function_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as  function_avg
, avg(case when  function_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_function_avg
, stddev(case when  function_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as  function_std
, stddev(case when  function_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_function_std
, sum(case when  function_hit_rate > 0.1
then 1
else 0 end) as  function_cnt
, sum(case when  function_hit_rate > 0.1
then 0
else 1 end) as not_function_cnt


# algorithm_hit_rate
, avg(case when algorithm_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as algorithm_avg
, avg(case when algorithm_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_algorithm_avg
, stddev(case when algorithm_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as algorithm_std
, stddev(case when algorithm_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_algorithm_std
, sum(case when algorithm_hit_rate > 0.1
then 1
else 0 end) as algorithm_cnt
, sum(case when algorithm_hit_rate > 0.1
then 0
else 1 end) as not_algorithm_cnt

# singelton_hit_rate
, avg(case when singelton_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as singelton_avg
, avg(case when singelton_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_singelton_avg
, stddev(case when singelton_hit_rate > 0.1
then 1.253*corrective_rate -0.053
else null end) as singelton_std
, stddev(case when singelton_hit_rate > 0.1
then null
else 1.253*corrective_rate -0.053 end) as not_singelton_std
, sum(case when singelton_hit_rate > 0.1
then 1
else 0 end) as singelton_cnt
, sum(case when singelton_hit_rate > 0.1
then 0
else 1 end) as not_singelton_cnt

from
ccp.file_quality_reference as h
join
ccp.file_properties as p
on
h.repo_name = p.repo_name
and h.file = p.full_file_name
;

drop table if exists ccp.repo_quality_reference;

create table ccp.repo_quality_reference
as
select
repo_name
, count(distinct commit) as commits
, count(distinct case when     REGEXP_CONTAINS( lower(message)
,'low(?:-| )quality')     then commit else null end) as low_quality_commits
, count(distinct case when     REGEXP_CONTAINS( lower(message)
,'technical.debt')     then commit else null end) as technical_debt_commits
, count(distinct case when     REGEXP_CONTAINS( lower(message)
,'hot(?:-| )spot')     then commit else null end) as hot_spot_commits
, count(distinct case when     REGEXP_CONTAINS( lower(message)
,'code.smell(s)?')     then commit else null end) as code_smell_commits
, count(distinct case when     REGEXP_CONTAINS( lower(message)
, 'disappointing|disheartening|displeasing|mortifying|not up to (par|snuff)|poor|rotten|substandard|unsatisfactory|bad|horrible|terrible|shit|crap|lousy|awful|fuck|disgusting|hideous|nasty|scary|shameful|shame|shocking|repulsive|revolting|stink')
then commit else null end) as swearing_commits
, 1.0*count(distinct case when     REGEXP_CONTAINS( lower(message)
,'function')     then commit else null end) as function_commits
, 1.0*count(distinct case when     REGEXP_CONTAINS( lower(message)
,'algorithm')     then commit else null end) as algorithm_commits
, 1.0*count(distinct case when     REGEXP_CONTAINS( lower(message)
,'singelton')     then commit else null end) as singelton_commits

from
ccp.active_2019_commits
group by
repo_name
;


# into ccp_by_quality_terms_by_repo.csv
select
count(*) as repos

# low_quality_hit_rate
, avg(case when low_quality_commits > 9
then 1.253*hit_ratio -0.053
else null end) as low_quality_avg
, avg(case when low_quality_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_low_quality_avg
, stddev(case when  low_quality_commits > 9
then 1.253*hit_ratio -0.053
else null end) as low_quality_std
, stddev(case when  low_quality_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_low_quality_std
, sum(case when  low_quality_commits > 9
then 1
else 0 end) as low_quality_cnt
, sum(case when  low_quality_commits > 9
then 0
else 1 end) as not_low_quality_cnt


# hot_spot
, avg(case when hot_spot_commits > 9
then 1.253*hit_ratio -0.053
else null end) as hot_spot_avg
, avg(case when hot_spot_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_hot_spot_avg
, stddev(case when  hot_spot_commits > 9
then 1.253*hit_ratio -0.053
else null end) as hot_spot_std
, stddev(case when  hot_spot_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_hot_spot_std
, sum(case when  hot_spot_commits > 9
then 1
else 0 end) as hot_spot_cnt
, sum(case when  hot_spot_commits > 9
then 0
else 1 end) as not_hot_spot_cnt

# technical_debt
, avg(case when technical_debt_commits > 9
then 1.253*hit_ratio -0.053
else null end) as technical_debt_avg
, avg(case when technical_debt_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_technical_debt_avg
, stddev(case when  technical_debt_commits > 9
then 1.253*hit_ratio -0.053
else null end) as technical_debt_std
, stddev(case when  technical_debt_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_technical_debt_std
, sum(case when  technical_debt_commits > 9
then 1
else 0 end) as technical_debt_cnt
, sum(case when  technical_debt_commits > 9
then 0
else 1 end) as not_technical_debt_cnt

# code_smell_hit_rate
, avg(case when code_smell_commits > 9
then 1.253*hit_ratio -0.053
else null end) as code_smell_avg
, avg(case when code_smell_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_code_smell_avg
, stddev(case when  code_smell_commits > 9
then 1.253*hit_ratio -0.053
else null end) as code_smell_std
, stddev(case when  code_smell_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_code_smell_std
, sum(case when  code_smell_commits > 9
then 1
else 0 end) as code_smell_cnt
, sum(case when  code_smell_commits > 9
then 0
else 1 end) as not_code_smell_cnt

# swearing_hit_rate
, avg(case when swearing_commits > 9
then 1.253*hit_ratio -0.053
else null end) as swearing_avg
, avg(case when swearing_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_swearing_avg
, stddev(case when  swearing_commits > 9
then 1.253*hit_ratio -0.053
else null end) as swearing_std
, stddev(case when  swearing_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_swearing_std
, sum(case when  swearing_commits > 9
then 1
else 0 end) as swearing_cnt
, sum(case when  swearing_commits > 9
then 0
else 1 end) as not_swearing_cnt

# function_hit_rate
, avg(case when function_commits > 9
then 1.253*hit_ratio -0.053
else null end) as function_avg
, avg(case when function_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_function_avg
, stddev(case when  function_commits > 9
then 1.253*hit_ratio -0.053
else null end) as function_std
, stddev(case when  function_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_function_std
, sum(case when  function_commits > 9
then 1
else 0 end) as function_cnt
, sum(case when  function_commits > 9
then 0
else 1 end) as not_function_cnt

# algorithm_hit_rate
, avg(case when algorithm_commits > 9
then 1.253*hit_ratio -0.053
else null end) as algorithm_avg
, avg(case when algorithm_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_algorithm_avg
, stddev(case when  algorithm_commits > 9
then 1.253*hit_ratio -0.053
else null end) as algorithm_std
, stddev(case when  algorithm_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_algorithm_std
, sum(case when  algorithm_commits > 9
then 1
else 0 end) as algorithm_cnt
, sum(case when  algorithm_commits > 9
then 0
else 1 end) as not_algorithm_cnt

# singelton_hit_rate
, avg(case when singelton_commits > 9
then 1.253*hit_ratio -0.053
else null end) as singelton_avg
, avg(case when singelton_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_singelton_avg
, stddev(case when  singelton_commits > 9
then 1.253*hit_ratio -0.053
else null end) as singelton_std
, stddev(case when  singelton_commits > 9
then null
else 1.253*hit_ratio -0.053 end) as not_singelton_std
, sum(case when  singelton_commits > 9
then 1
else 0 end) as singelton_cnt
, sum(case when  singelton_commits > 9
then 0
else 1 end) as not_singelton_cnt

from
ccp.repo_quality_reference as l
join
ccp.repos as r
on
l.repo_name = r.repo_name
;


# low quality hits distribution
select
round(low_quality_hit_rate, 2) as low_quality_hit_rate
, count(*) as files
from
ccp.file_quality_reference
where commits > 9
group by
low_quality_hit_rate
order by
low_quality_hit_rate
;
