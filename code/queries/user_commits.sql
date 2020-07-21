# Commit per user, used for development speed analysis

# Lecagy SQL

# into commit_per_user_2016
Select 
Author.email as author_email
, count(distinct commit) as dis_commits
, count(commit) as commits
, count(distinct case when (
(((LENGTH(REGEXP_REPLACE(lower(message), '(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")((choose|take|set|use)\\s*(the|a)?\\s*correct|(not|isn\'t|doesn\'t)\\s+work(s|ing)?|bad initialization|buffer overflow|bug(s|z)?|bugfix(es)?|correct\\s*(a|the|some|few|this)|correct(ed|ion|ly|s)?|dangling pointer|deadlock|defect|double free|error|fail(ed|s)?|failure(s)?|fault(s)?|faulty initialization|fix(ed|es)?|fixin(s)?|fixing(s)?|fixup(s)?|flaw(s)?|hang|heap overflow|incorrect(ly)?|memory leak|missing\\s(default value|initialization|switch case)|mistake(s|n|nly)?|null pointer|overrun|problem(s)|race condition|resource leak|revert|segmentation fault|workaround|wrong(nly)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")', '#')) 	
-
 LENGTH(REGEXP_REPLACE(lower(message), '(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")((choose|take|set|use)\\s*(the|a)?\\s*correct|(not|isn\'t|doesn\'t)\\s+work(s|ing)?|bad initialization|buffer overflow|bug(s|z)?|bugfix(es)?|correct\\s*(a|the|some|few|this)|correct(ed|ion|ly|s)?|dangling pointer|deadlock|defect|double free|error|fail(ed|s)?|failure(s)?|fault(s)?|faulty initialization|fix(ed|es)?|fixin(s)?|fixing(s)?|fixup(s)?|flaw(s)?|hang|heap overflow|incorrect(ly)?|memory leak|missing\\s(default value|initialization|switch case)|mistake(s|n|nly)?|null pointer|overrun|problem(s)|race condition|resource leak|revert|segmentation fault|workaround|wrong(nly)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")', ''))))
-
((LENGTH(REGEXP_REPLACE(lower(message), '(((\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")fix(ed|s|es|ing)?.{1,40}(#|(camel|snake|kebab|flat|lower|upper)\\s*case|code review|coding style|comment(s)?|cosmetic|cr(s)?(-)?|documentation|format(s|ing)?|help|remark(s)|space(s)?|style|styling|typo(s)?|warning(s)?|whitespace(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|"))|((#|(camel|snake|kebab|flat|lower|upper)\\s*case|code review|coding style|comment(s)?|cosmetic|cr(s)?(-)?|documentation|format(s|ing)?|help|remark(s)|space(s)?|style|styling|typo(s)?|warning(s)?|whitespace(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|").{1,40}(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")fix(ed|s|es|ing)?(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|"))|((error check(ing)?|error handling|error message(s)?|error report(s|ing)?|exception handling|fixed point)))', '#')) 	
-
 LENGTH(REGEXP_REPLACE(lower(message), '(((\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")fix(ed|s|es|ing)?.{1,40}(#|(camel|snake|kebab|flat|lower|upper)\\s*case|code review|coding style|comment(s)?|cosmetic|cr(s)?(-)?|documentation|format(s|ing)?|help|remark(s)|space(s)?|style|styling|typo(s)?|warning(s)?|whitespace(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|"))|((#|(camel|snake|kebab|flat|lower|upper)\\s*case|code review|coding style|comment(s)?|cosmetic|cr(s)?(-)?|documentation|format(s|ing)?|help|remark(s)|space(s)?|style|styling|typo(s)?|warning(s)?|whitespace(s)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|").{1,40}(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")fix(ed|s|es|ing)?(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|"))|((error check(ing)?|error handling|error message(s)?|error report(s|ing)?|exception handling|fixed point)))', ''))))
- 
((LENGTH(REGEXP_REPLACE(lower(message), '(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")(lack|n\'t|never|nobody|none|not|nothing|without)(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|").{0,20}(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")((choose|take|set|use)\\s*(the|a)?\\s*correct|(not|isn\'t|doesn\'t)\\s+work(s|ing)?|bad initialization|buffer overflow|bug(s|z)?|bugfix(es)?|correct\\s*(a|the|some|few|this)|correct(ed|ion|ly|s)?|dangling pointer|deadlock|defect|double free|error|fail(ed|s)?|failure(s)?|fault(s)?|faulty initialization|fix(ed|es)?|fixin(s)?|fixing(s)?|fixup(s)?|flaw(s)?|hang|heap overflow|incorrect(ly)?|memory leak|missing\\s(default value|initialization|switch case)|mistake(s|n|nly)?|null pointer|overrun|problem(s)|race condition|resource leak|revert|segmentation fault|workaround|wrong(nly)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")', '#')) 	
-
 LENGTH(REGEXP_REPLACE(lower(message), '(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")(lack|n\'t|never|nobody|none|not|nothing|without)(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|").{0,20}(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")((choose|take|set|use)\\s*(the|a)?\\s*correct|(not|isn\'t|doesn\'t)\\s+work(s|ing)?|bad initialization|buffer overflow|bug(s|z)?|bugfix(es)?|correct\\s*(a|the|some|few|this)|correct(ed|ion|ly|s)?|dangling pointer|deadlock|defect|double free|error|fail(ed|s)?|failure(s)?|fault(s)?|faulty initialization|fix(ed|es)?|fixin(s)?|fixing(s)?|fixup(s)?|flaw(s)?|hang|heap overflow|incorrect(ly)?|memory leak|missing\\s(default value|initialization|switch case)|mistake(s|n|nly)?|null pointer|overrun|problem(s)|race condition|resource leak|revert|segmentation fault|workaround|wrong(nly)?)(\\s|\\.|\\?|\\!|\\[|\\]|\\)|\\:|^|$|\\,|\'|")', ''))))) > 0
)  then commit else null end) as hits
, max(repo_name) as repo_name
, count(distinct repo_name) as repos
From 
(select * from
[bigquery-public-data:github_repos.commits] ) as inSql
Where
year(author.date) = 2016
Group by 
author_email
;


# into commit_per_user_dist
Select
Dis_commits
, count(distinct author_email) as users
From
[ccp.commit_per_user_2016]
Group by 
Dis_commits
Order by
Dis_commits
;

# into user_commits_per_rep
# Legacy,  Allow Large Results
Select
c.Author.email as author_email
, c.repo_name as repo_name
, year(USEC_TO_TIMESTAMP(c.committer.date.seconds*1000000)) as year
, count(distinct c.commit) as dis_commits
, count(c.commit) as commits
From
(select * from
[bigquery-public-data:github_repos.commits] as commits
) as c
Where
year(USEC_TO_TIMESTAMP(c.committer.date.seconds*1000000)) in (2016, 2017, 2018, 2019)
Group by
author_email
, c.repo_name
, year
;


# into users_per_project_plus_cap
Select 
u.Repo_name as repo_name
, count(distinct case when year = 2016 then author_email else null end) as users_2016
, count(distinct case when year = 2017 then author_email else null end) as users_2017
, count(distinct case when year = 2018 then author_email else null end) as users_2018
, count(distinct case when year = 2019 then author_email else null end) as users_2019
, count(distinct case when year = 2016 and u.commits > 11 then author_email else null end) as users_2016_above_11
, count(distinct case when year = 2017 and u.commits > 11 then author_email else null end) as users_2017_above_11
, count(distinct case when year = 2018 and u.commits > 11 then author_email else null end) as users_2018_above_11
, count(distinct case when year = 2019 and u.commits > 11 then author_email else null end) as users_2019_above_11
, sum( case when year = 2016 then u.commits else 0 end) as commits_2016
, sum( case when year = 2017 then u.commits else 0 end) as commits_2017
, sum( case when year = 2018 then u.commits else 0 end) as commits_2018
, sum( case when year = 2019 then u.commits else 0 end) as commits_2019
, sum( case when year = 2016  and u.commits > 11 then u.commits else 0 end) as users_commit_2016_above_11
, sum( case when year = 2017  and u.commits > 11 then u.commits else 0 end) as users_commit_2017_above_11
, sum( case when year = 2018  and u.commits > 11 then u.commits else 0 end) as users_commit_2018_above_11
, sum( case when year = 2019  and u.commits > 11 then u.commits else 0 end) as users_commit_2019_above_11
, sum( case when year = 2016 then case when u.commits < 484 then u.commits else 484 end  else 0 end) as users_capped_commit_2016
, sum( case when year = 2017 then case when u.commits < 484 then u.commits else 484 end else 0 end) as users_capped_commit_2017
, sum( case when year = 2018 then case when u.commits < 484 then u.commits else 484 end else 0 end) as users_capped_commit_2018
, sum( case when year = 2019 then case when u.commits < 484 then u.commits else 484 end else 0 end) as users_capped_commit_2019
, sum( case when year = 2016  and u.commits > 11 then case when u.commits < 484 then u.commits else 484 end else 0 end) as users_capped_commit_2016_above_11
, sum( case when year = 2017  and u.commits > 11 then case when u.commits < 484 then u.commits else 484 end else 0 end) as users_capped_commit_2017_above_11
, sum( case when year = 2018  and u.commits > 11 then case when u.commits < 484 then u.commits else 484 end else 0 end) as users_capped_commit_2018_above_11
, sum( case when year = 2019  and u.commits > 11 then case when u.commits < 484 then u.commits else 484 end else 0 end) as users_capped_commit_2019_above_11
From
[ccp.user_commits_per_rep] as u
Join
[ccp.repos] as r
On u.repo_name = r.repo_name
Group by
repo_name
;




