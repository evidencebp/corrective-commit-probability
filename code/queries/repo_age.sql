drop table if exists ccp.project_start_year;

# into project_start_year
# Legacy, Large results
create table
ccp.project_start_year
as
Select
u.Repo_name as repo_name
, min(year) as start_year
From
ccp.project_user_contribution_stats as as p
join
ccp.repos_full as r
on
p.repo_name = r.repo_name
where
y2019_ccp > 0
and
y2019_ccp < 1
Group by
u.repo_name
;

Select
(p.year - s.start_year) as age
, count(distinct s.repo_name) as repos
, avg(1.253*corrective_commits_ratio -0.053) as ccp_avg
, stddev(1.253*corrective_commits_ratio -0.053) as ccp_std
from
ccp.project_start_year as s
join
ccp.project_user_contribution_stats as p
on
p.repo_name = s.repo_name
where
s.start_year > 2007
group by
age
order by
age
;