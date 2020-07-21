
# Standard Sql
drop table if exists ccp.classified_commits;

# into classified_commits
# Standard
# Allow large results
create table
ccp.classified_commits
partition by
fake_date
cluster by
repo_name, commit
as
Select
*
, ccp.bq_corrective(message) as is_corrective
, DATE('1980-01-01') as  fake_date
from
ccp.active_2019_commits
;




# Standard Sql
drop table if exists ccp.classified_2019_commits_by_file;

# into classified_2019_commits_by_file
# Standard
# Allow large results
create table
ccp.classified_2019_commits_by_file
partition by
fake_date
cluster by
repo_name, commit
as
Select
*
, ccp.bq_corrective(message) as is_corrective
, ((LENGTH(REGEXP_REPLACE(lower(file), 'test', '#'))
            - LENGTH(REGEXP_REPLACE(lower(file), 'test', '')))) > 0 as is_test
, lower(reverse(substr(reverse(file), 0, strpos(reverse(file),'.')))) as extension
, lower(reverse(substr(reverse(file), 0, strpos(reverse(file),'/')))) as file_name
, file as full_file_name
, DATE('1980-01-01') as  fake_date
from
ccp.active_2019_commits_by_file
;
