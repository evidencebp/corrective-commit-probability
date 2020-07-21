
# Compute repository extensions

# Selects one arbitrary extension (the max by lexical order) per repository.
# Should help in course diffrention where a repository has a single extension
# into repo_programming_file_size_99
select
f.repo_name
,  max(lower(reverse(substr(reverse(path), 0, strpos(reverse(path),'.'))))) as repo_max_extension
,  count(distinct lower(reverse(substr(reverse(path), 0, strpos(reverse(path),'.'))))) as repo_extensions_num
, count(distinct path) as files
, avg(size) as avg_size
, avg(case when size > 181*1024 then 181*1024 else size end) as capped_avg_file # 99 percentile in source code length dist
, stddev(size) as std_size
, stddev(case when size > 181*1024 then 181*1024 else size end) as capped_std_file

from
`bigquery-public-data.github_repos.files` as f
join
`bigquery-public-data.github_repos.contents` as c
on f.id = c.id
Join
`hotspots-readability.ccp.repos` As repos
On
f.repo_name = repos.repo_name
Where
lower(reverse(substr(reverse(path), 0, strpos(reverse(path),'.'))))
In
('.bat', '.c', '.cc', '.coffee', '.cpp', '.cs', '.cxx', '.go',
       '.groovy', '.hs', '.java', '.js', '.lua', '.m',
       '.module', '.php', '.pl', '.pm', '.py', '.rb', '.s', '.scala',
       '.sh', '.swift', '.tpl', '.twig')
group by f.repo_name
order by f.repo_name
;

select *
from
[hotspots-readability:ccp.repo_programming_file_size_99]
order by
repo_name
limit 10000;


select *
from
[hotspots-readability:ccp.repo_programming_file_size_99]
order by
repo_name
limit 10000
offset 10000
;


# into repo_programming_file_size_by_extension_99
select
f.repo_name
, lower(reverse(substr(reverse(path), 0, strpos(reverse(path),'.')))) as extension
,  count(distinct lower(reverse(substr(reverse(path), 0, strpos(reverse(path),'.'))))) as extensions_num
, count(distinct path) as files
, count(distinct f. repo_name) as repositories
, avg(size) as avg_size
, avg(case when size > 181*1024 then 181*1024 else size end) as capped_avg_file
, stddev(size) as std_size
, stddev(case when size > 181*1024 then 181*1024 else size end) as capped_std_file

from
`bigquery-public-data.github_repos.files` as f
join
`bigquery-public-data.github_repos.contents` as c
on f.id = c.id
Join
`hotspots-readability.ccp.repos` As repos
On
f.repo_name = repos.repo_name
Where
lower(reverse(substr(reverse(path), 0, strpos(reverse(path),'.'))))
In
('.bat', '.c', '.cc', '.coffee', '.cpp', '.cs', '.cxx', '.go',
       '.groovy', '.hs', '.java', '.js', '.lua', '.m',
       '.module', '.php', '.pl', '.pm', '.py', '.rb', '.s', '.scala',
       '.sh', '.swift', '.tpl', '.twig')
group by f.repo_name, extension
order by f.repo_name, extension
;

# repo_programming_file_size_with_major_extension99
Select
p.*
, m.extension as major_extension
, m.files as major_files
, m.avg_size as major_avg_size
, m.capped_avg_file as major_capped_avg_file
, m.std_size as major_std_size
, m.capped_std_file as major_capped_std_file
, 1.0*m.files/p.files as major_extension_ratio
From
`hotspots-readability.ccp.repo_programming_file_size_99` as p
Join
`hotspots-readability.ccp.repo_programming_file_size_by_extension_99` as m
On
P.repo_name = m.repo_name
Where
M.files > p.files/2
;








