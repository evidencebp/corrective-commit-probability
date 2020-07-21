# Standard Sql
WITH YourTable AS( SELECT 'main.c' AS path
UNION ALL SELECT 'script.py'
UNION ALL SELECT 'a.b.go'
UNION ALL SELECT 'readme')
SELECT path, lower(reverse(substr(reverse(path), 0, strpos(reverse(path),'.'))))
FROM YourTable



# into file_extension_properties
# Standard SQL
select
lower(reverse(substr(reverse(path), 0, strpos(reverse(path),'.')))) as extension
, count(distinct concat(repo_name, path)) as files
, count(distinct repo_name) as repositories
, avg(size) as avg_size
, stddev(size) as std_size
from
`bigquery-public-data.github_repos.files` as f
join
`bigquery-public-data.github_repos.contents` as c
on f.id = c.id
group by extension
having
count(*) > 500
and
count(distinct repo_name) > 10
order by extension desc
;


Select *
From
`hotspots-readability.ccp.file_extension_properties`
Where strpos(extension, "~") = 0
Order by files desc;

#The top 28 programming languages out of the 100 extensions with most files, 94% of the files.
('.bat', '.c', '.cc', '.coffee', '.cpp', '.cs', '.cxx', '.go',
       '.groovy', '.h', '.hpp', '.hs', '.java', '.js', '.lua', '.m',
       '.module', '.php', '.pl', '.pm', '.py', '.rb', '.s', '.scala',
       '.sh', '.swift', '.tpl', '.twig')
# Same list with .h and .hpp excluded since they are for headers
('.bat', '.c', '.cc', '.coffee', '.cpp', '.cs', '.cxx', '.go',
       '.groovy', '.hs', '.java', '.js', '.lua', '.m',
       '.module', '.php', '.pl', '.pm', '.py', '.rb', '.s', '.scala',
       '.sh', '.swift', '.tpl', '.twig')

# into programming_file_size_dist
select
round(size/1024) as size # in KB
, count(distinct concat(repo_name, path)) as files
from
`bigquery-public-data.github_repos.files` as f
join
`bigquery-public-data.github_repos.contents` as c
on f.id = c.id
Where
lower(reverse(substr(reverse(path), 0, strpos(reverse(path),'.'))))
In
('.bat', '.c', '.cc', '.coffee', '.cpp', '.cs', '.cxx', '.go',
       '.groovy', '.hs', '.java', '.js', '.lua', '.m',
       '.module', '.php', '.pl', '.pm', '.py', '.rb', '.s', '.scala',
       '.sh', '.swift', '.tpl', '.twig')

group by size
order by size
;

# 26/12/2019 max = 127505, avg = 15.6
# Legacy Sql
Select
max(size) as max_size
, sum(size*files)/sum(files) as avg_file_size_kb
from
[ccp.programming_file_size_dist]

