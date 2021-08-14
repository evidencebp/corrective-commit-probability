select
package
, count(distinct repo_name) as repos
from
effort_estimation.java_imports
group by
package
order by
count(distinct repo_name) desc
;
# Selected output
# java.security
# java.sql, javax.sql
# javax.servlet
# java.util.concurrent.locks
# android.os, android.content
# javax.crypto


select
domain
, count(distinct r.repo_name) as repos
, round(avg(ccp),2) as CCP
from
general.repo_properties as r
join
(
select
repo_name
, case
when package in ('java.security', 'javax.crypto') then 'Security'
when package in ('java.sql', 'javax.sql') then 'Database'
when regexp_contains(package,'javax.servlet') then 'Servlet'
when regexp_contains(package, 'java.util.concurrent') then 'Concurrent'
when regexp_contains(package, 'android') then 'Android'
when regexp_contains(package,'org.w3c.dom') then 'W3c_dom'
when regexp_contains(package,'javax.swing') then 'Swing'
end as domain
from
effort_estimation.java_imports
group by
repo_name
, domain
) as repo_domain
on r.repo_name = repo_domain.repo_name
group by
domain
order by
domain
;
