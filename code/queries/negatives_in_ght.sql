select 
if( y2019_ccp <= 0, 1,0) as negative_ccp
, count(distinct r.repo_name) as repos
, avg(if(r.authors =1,1,0)) as single_author
, 1.0*count(distinct rp.repo_name)/count(distinct r.repo_name) as in_ght
#, 1.0*count(distinct if(issues > 0, rp.repo_name, null))/count(distinct rp.repo_name) as has_issues
#, avg(issues) as issues_avg
#, 1.0*count(distinct if(pull_requests > 0, rp.repo_name, null))/count(distinct rp.repo_name) as has_pull_requests
#, avg(pull_requests) as pull_requests_avg
from
general_ght.repos_full as r
left join
general_ght.repo_profile as rp
on
r.repo_name = rp.repo_name
where
r.y2019_ccp <= 1
group by
negative_ccp
order by
negative_ccp
;
