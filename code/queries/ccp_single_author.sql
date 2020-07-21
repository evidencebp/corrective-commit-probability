drop table if exists ccp.active_2019_commits_by_file_single_author;

create table
ccp.active_2019_commits_by_file_single_author
partition by
fake_date
cluster by
repo_name, Author_email
as
Select c.*
from
ccp.classified_2019_commits_by_file as c
join
 ccp.file_properties as p
on
c.repo_name = p.repo_name
and
c.file = p.full_file_name
where
authors =1
;
