drop table if exists ccp.invloved_dev_churn;

create table
ccp.invloved_dev_churn
partition by
fake_date
cluster by
base_year, repo_name
as
Select
prev.year as year
, prev.repo_name as repo_name
, count(distinct prev.author_email) as base_year_developers
, count(distinct cur.author_email) as continuing_developers
, 1.0*count(distinct cur.author_email)/count(distinct prev.author_email) as continuing_developers_ratio
, DATE('1980-01-01') as  fake_date
from
ccp.user_commits_per_rep as prev
left join
ccp.user_commits_per_rep as cur
on
prev.year + 1 = cur.year
and
prev.repo_name = cur.repo_name
and
prev.author_email = cur.author_email
where
prev.commits > 11
group by
base_year
, repo_name
;

drop table if exists ccp.developer_on_boarding;

create table
ccp.developer_on_boarding
partition by
fake_date
cluster by
entry_year, repo_name
as
Select
cur.year as year
, cur.repo_name as repo_name
, count(distinct cur.author_email) as comming_developers
, count(distinct case when cur.commits > 11 then cur.author_email else null end) as comming_involved_developers
, 1.0*count(distinct case when cur.commits > 11 then cur.author_email else null end)
/count(distinct cur.author_email) as comming_involved_developers_ratio
, DATE('1980-01-01') as  fake_date
from
ccp.user_commits_per_rep as cur
left join
ccp.user_commits_per_rep as prev
on
prev.year < cur.year
and
prev.repo_name = cur.repo_name
and
prev.author_email = cur.author_email
where
# We want developers that didn't work on the repository before
prev.author_email is null
group by
entry_year
, repo_name
;
