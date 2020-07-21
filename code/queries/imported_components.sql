# packages to lifter out
drop table if exists ccp.java_common_packages;
create table ccp.java_common_packages
as
select
package
, count(distinct path) as importing_files
, count(distinct repo_name) as repositories
from
ccp.relevant_java_imports
group by
package
having
count(distinct repo_name) > 1
order by
count(distinct path) desc
;

# TODO - import * is not handeled well, probably leading to many FN
# TODO - add package and path "first name", the file name to speed up matching
drop table if exists ccp.java_imports_per_match;
create table ccp.java_imports_per_match
as
select
i.*
, lower(i.path) as lower_path
, mod(abs(FARM_FINGERPRINT(i.repo_name)) , 9973) as repo_hash
, lower(concat(replace(i.package, '.', '/'), '.java')) as package_as_path
,
 lower(reverse(replace(i.package, '.', '/'))) as package_to_match
, lower(reverse(SUBSTR(i.path, 0, length(i.path) -5))) as path_to_match
, length(i.path) as path_length
, length(i.package) as package_length
, length(concat(replace(i.package, '.', '/'), '.java'))  as package_as_path_length
from
ccp.relevant_java_imports as i
left join
ccp.java_common_packages as p
on
i.package = p.package
where
not REGEXP_CONTAINS(lower(i.path), 'test')
and
not REGEXP_CONTAINS(i.package, r"^java\.|junit|^javax\.|^org.jetbrains|^android|^com.intellij|^org.eclipse|^org.eclipse|^org.w3c")
and p.package is null
# TODO - remove
#and repo_name = 'Azure/azure-sdk-for-java'
;

# Performance improvement - remove java and other irrelevant packages
drop table if exists ccp.java_imported;

create table
ccp.java_imported
as
select
imported.repo_name as imported_repo_name
, imported.path as imported_path
, importing.path as importing_path
from
ccp.java_imports_per_match as importing
join
ccp.java_imports_per_match as imported
on
importing.repo_hash = imported.repo_hash
and
importing.repo_name = imported.repo_name
and
imported.path_length >= importing.package_as_path_length
where
substr(imported.path_to_match, 1,importing.package_length) = importing.package_to_match
;

drop table if exists ccp.java_repo_reuse;

create table
ccp.java_repo_reuse
as
SELECT
imported_repo_name as repo_name
, count(*) as links
, count(distinct imported_path) as imported_paths
, count(distinct importing_path) as importing_paths
from
ccp.java_imported
group by
imported_repo_name
order by
count(*) desc
;


drop table if exists ccp.file_reuse_reference_by_repo;

create table ccp.file_reuse_reference_by_repo
as
select
repo_name
, 1.0* count(distinct commit) as commits
, 1.0*count(distinct case when     REGEXP_CONTAINS( lower(message)
,'re(?:-| )?us(e|es|ed|ing)|re(?:-| )?usability')     then commit else null end) as reuse_commits
from
ccp.active_2019_commits_by_file as f
group by
repo_name
having
count(distinct commit) > 9
;


select
count(*) as count
# Links
, avg(case when reuse_commits > 9
then links
else null end) as links_avg
, avg(case when reuse_commits > 9
then null
else links end) as not_links_avg
, stddev(case when reuse_commits > 9
then links
else null end) as links_std
, stddev(case when reuse_commits > 9
then null
else links end) as not_links_std

# imported_paths
, avg(case when reuse_commits > 9
then imported_paths
else null end) as imported_paths_avg
, avg(case when reuse_commits > 9
then null
else imported_paths end) as not_imported_paths_avg
, stddev(case when reuse_commits > 9
then imported_paths
else null end) as imported_paths_std
, stddev(case when reuse_commits > 9
then null
else imported_paths end) as not_imported_paths_std

# importing_paths
, avg(case when reuse_commits > 9
then importing_paths
else null end) as importing_paths_avg
, avg(case when reuse_commits > 9
then null
else importing_paths end) as not_importing_paths_avg
, stddev(case when reuse_commits > 9
then importing_paths
else null end) as importing_paths_std
, stddev(case when reuse_commits > 9
then null
else importing_paths end) as not_importing_paths_std



, sum(case when reuse_commits > 9
then 1
else 0 end) as reuse_cnt
, sum(case when reuse_commits > 9
then 0
else 1 end) as not_reuse_cnt
from
ccp.file_reuse_reference_by_repo as h
 join
ccp.java_repo_reuse as p
on
h.repo_name = p.repo_name

;


