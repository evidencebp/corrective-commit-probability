
# coupling twins comparison
# Twins comparison
# into coupling_twins_stat

drop table if exists ccp.coupling_twins_stat;


create table ccp.coupling_twins_stat
as
Select
first_project.year
, count(*) as pairs
, count( distinct first_project.repo_name) as repos_num
, count(distinct first_user_profile.Author_email) as authors

, 1.0*sum(case when
 ( (first_user_profile.avg_capped_files < second_user_profile.avg_capped_files
and
    first_project.avg_capped_files < second_project.avg_capped_files)
          Or
 (first_user_profile.avg_capped_files > second_user_profile.avg_capped_files
and
    first_project.avg_capped_files > second_project.avg_capped_files)

) then 1 else 0 end)/count(*) as match_avg_capped_files_ratio

, 1.0*sum(case when
 ( (first_user_profile.avg_capped_files  < second_user_profile.avg_capped_files
and
    first_project.avg_capped_files + 1 < second_project.avg_capped_files)
          Or
 (first_user_profile.avg_capped_files > second_user_profile.avg_capped_files
and
    first_project.avg_capped_files > second_project.avg_capped_files +1)

) then 1 else 0 end)/sum(case when
 ( (
    first_project.avg_capped_files + 1 < second_project.avg_capped_files)
          Or
 (
    first_project.avg_capped_files > second_project.avg_capped_files +1)

) then 1 else 0 end) as match_avg_capped_files_ratio_s1

From
ccp.coupling_by_repo_by_user as first_user_profile
Join
ccp.coupling_by_repo_by_user as second_user_profile
On
first_user_profile.Author_email = second_user_profile.Author_email
And
first_user_profile.year = second_user_profile.year

# same user, different projects
Join
ccp.coupling_by_repo as first_project
On
first_user_profile.repo_name = first_project.Repo_name
Join
ccp.coupling_by_repo  as second_project
On
second_user_profile.repo_name = second_project.Repo_name
# TODO - add different sub repo name
join
ccp.user_commits_profile as profile
on
first_user_profile.Author_email = profile.Author_email
where
# <> is enough to compare project
# < is for breaking symmetry and not getting both (a,b) and (b,a)
# Using symetric in order not to effect statistics like #authors
first_user_profile.repo_name <> second_user_profile.repo_name
and
# Avoid forks
substr(first_user_profile.repo_name, strpos(first_user_profile.repo_name,'/') +1)
    <> substr(second_user_profile.repo_name, strpos(second_user_profile.repo_name,'/') +1)
and
first_user_profile.commits > 11
 and
second_user_profile.commits > 11
and
profile.repos_num < 11
and profile.repos_num > 1
and
first_project.year > 2007
Group by
first_project.year
order by
first_project.year
;

# Coupling CM
Select
first_user_profile.avg_capped_files < second_user_profile.avg_capped_files as twin_improved
, first_project.avg_capped_files < second_project.avg_capped_files as env_improved
, count(*) as pairs
, count( distinct first_project.repo_name) as repos_num
, count(distinct first_user_profile.Author_email) as authors
From
ccp.coupling_by_repo_by_user as first_user_profile
Join
ccp.coupling_by_repo_by_user as second_user_profile
On
first_user_profile.Author_email = second_user_profile.Author_email
And
first_user_profile.year = second_user_profile.year

# same user, different projects
Join
ccp.coupling_by_repo as first_project
On
first_user_profile.repo_name = first_project.Repo_name
Join
ccp.coupling_by_repo  as second_project
On
second_user_profile.repo_name = second_project.Repo_name
# TODO - add different sub repo name
join
ccp.user_commits_profile as profile
on
first_user_profile.Author_email = profile.Author_email
where
# <> is enough to compare project
# < is for breaking symmetry and not getting both (a,b) and (b,a)
# Using symetric in order not to effect statistics like #authors
first_user_profile.repo_name <> second_user_profile.repo_name
and
# Avoid forks
substr(first_user_profile.repo_name, strpos(first_user_profile.repo_name,'/') +1)
    <> substr(second_user_profile.repo_name, strpos(second_user_profile.repo_name,'/') +1)
and
first_user_profile.commits > 11
 and
second_user_profile.commits > 11
and
profile.repos_num < 11
and profile.repos_num > 1
and
first_project.year > 2007
group by
twin_improved, env_improved
order by
twin_improved, env_improved
;
