# Based on https://gist.github.com/arfon/49ca314a5b0a00b1ebf91167db3ff02c
# By Arfon Smith

# See also
# https://changelog.com/podcast/209
# https://blog.jessfraz.com/post/analyzing-github-pull-request-data-with-big-query/
# https://medium.com/@hoffa/github-top-countries-201608-13f642493773#.beemirtdc
# https://github.blog/2017-01-19-github-data-ready-for-you-to-explore-with-bigquery/
# https://geeksta.net/geeklog/exploring-expressions-emotions-github-commit-messages/

# Legacy sql
SELECT repo_name as repo_name
     , path as path
     , REGEXP_EXTRACT(line, r' ([a-z0-9\._]*)\.') as package
     , count(*) as imports
FROM (
 SELECT SPLIT(content, '\n') line, r.repo_name as repo_name, path
 FROM
 [bigquery-public-data:github_repos.contents] as cnt
 join
 [bigquery-public-data:github_repos.files] as f
 on
 cnt.id = f.id
 join
 [hotspots-readability:ccp.repos_full] as r on
 f.repo_name = r.repo_name
 WHERE content CONTAINS 'import'
 AND path LIKE '%.java'
 and r.y2019_ccp > 0
 and r.y2019_ccp < 0
 HAVING LEFT(line, 6)='import'
)
GROUP BY
repo_name
, path
, package
;

drop table if exists ccp.relevant_java_imports;


create table
ccp.relevant_java_imports
as
select
i.*
from
ccp.java_imports as i
join
ccp.repos_full as r
on i.repo_name = r.repo_name
;

drop table if exists ccp.imports_per_path;

create table ccp.imports_per_path
as
select
repo_name
, path
, count(distinct package) as package
, sum(imports) as imports
from
ccp.relevant_java_imports
group by
repo_name
, path
;


drop table if exists ccp.imports_per_repo;

create table ccp.imports_per_repo
as
select
repo_name
, count(distinct path) as paths
, avg(package) as package_avg
, avg(imports) as imports_avg
from
ccp.imports_per_path
group by
repo_name
;


drop table if exists ccp.file_reuse_reference;

create table ccp.file_reuse_reference
as
select
repo_name
, file
, 1.0* count(distinct commit) as commits
, 1.0*count(distinct case when     REGEXP_CONTAINS( lower(message)
,'re(?:-| )?us(e|es|ed|ing)|re(?:-| )?usability')     then commit else null end)/count(distinct commit) as reuse_hit_rate
from
ccp.active_2019_commits_by_file as f
group by
repo_name
, file
having
count(distinct commit) > 9
;


select
count(*) as count
, avg(case when reuse_hit_rate > 0.1
then package
else null end) as reuse_avg
, avg(case when reuse_hit_rate > 0.1
then null
else package end) as not_reuse_avg
, stddev(case when reuse_hit_rate > 0.1
then package
else null end) as reuse_std
, stddev(case when reuse_hit_rate > 0.1
then null
else package end) as not_reuse_std
, sum(case when reuse_hit_rate > 0.1
then 1
else 0 end) as reuse_cnt
, sum(case when reuse_hit_rate > 0.1
then 0
else 1 end) as not_reuse_cnt
from
ccp.file_reuse_reference as h
join
ccp.imports_per_path as p
on
h.repo_name = p.repo_name
and h.file = p.path
;


