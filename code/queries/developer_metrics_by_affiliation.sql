
select
author_email_domain
, count(*) as cases
, count(distinct d.author_email) as developers

, avg(files_owned_ccp ) as ccp
, avg(avg_coupling_code_size_cut ) as avg_coupling_code_size_cut
, avg(tests_presence ) as tests_presence
, avg(multiline_message_ratio ) as multiline_message_ratio
, avg(message_length_avg ) as message_length_avg_ratio
, avg(same_date_duration_avg ) as same_date_duration_avg
, avg(files_edited ) as files_edited
, avg(refactor_mle ) as refactor_mle
, avg(commit_days ) as commit_days
, avg(one_file_fix_rate ) as one_file_fix_rate
, avg(one_file_refactor_rate ) as one_file_refactor_rate
from
general.developer_profile as d
where commits >= 200
group by
author_email_domain
order by
count(distinct d.author_email) desc
;

select
case
when author_email_domain in
('google.com', 'redhat.com', 'microsoft.com', 'apache.org', 'intel.com',  'fb.com', '	googlemail.com', 'us.ibm.com', 'apple.com'
, 'amazon.com') then 'prestigious_conmpany'

when author_email_domain in
('mit.edu', 'stanford.edu', 'umich.edu', 'inria.fr', 'gatech.edu', 'cornell.edu') then 'prestigious_university'
else 'other'
end as prestigious
, count(*) as cases
, count(distinct d.author_email) as developers
, avg(files_owned_ccp ) as ccp
, avg(avg_coupling_code_size_cut ) as avg_coupling_code_size_cut
, avg(tests_presence ) as tests_presence
, avg(multiline_message_ratio ) as multiline_message_ratio
, avg(message_length_avg ) as message_length_avg_ratio
, avg(same_date_duration_avg ) as same_date_duration_avg
, avg(files_edited ) as files_edited
, avg(refactor_mle ) as refactor_mle
, avg(commit_days ) as commit_days
, avg(one_file_fix_rate ) as one_file_fix_rate
, avg(one_file_refactor_rate ) as one_file_refactor_rate
from
general.developer_profile as d
where commits >= 200
group by
prestigious
order by
count(distinct d.author_email) desc
;

select
case
when author_email_domain in
('google.com', 'redhat.com', 'microsoft.com', 'apache.org', 'intel.com',  'fb.com', '	googlemail.com', 'us.ibm.com', 'apple.com'
, 'amazon.com') then 'prestigious_conmpany'

when author_email_domain in
('mit.edu', 'stanford.edu', 'umich.edu', 'inria.fr', 'gatech.edu', 'cornell.edu') then 'prestigious_university'
else 'other'
end as prestigious
, count(*) as cases
, count(distinct d.author_email) as developers

, avg(files_owned_ccp ) as ccp
, avg(avg_coupling_code_size_cut ) as avg_coupling_code_size_cut
, avg(tests_presence ) as tests_presence
, avg(multiline_message_ratio ) as multiline_message_ratio
, avg(message_length_avg ) as message_length_avg_ratio
, avg(same_date_duration_avg ) as same_date_duration_avg
, avg(files_edited ) as files_edited
, avg(refactor_mle ) as refactor_mle
, avg(commit_days ) as commit_days
, avg(one_file_fix_rate ) as one_file_fix_rate
, avg(one_file_refactor_rate ) as one_file_refactor_rate


from
general.developer_profile as d
where commits >= 200
and
tests_presence < 0.01
group by
prestigious
order by
count(distinct d.author_email) desc
;

SELECT
case
when author_email_domain in
('google.com', 'redhat.com', 'microsoft.com', 'apache.org', 'intel.com',  'fb.com', '	googlemail.com', 'us.ibm.com', 'apple.com'
, 'amazon.com') then 'prestigious_conmpany'

when author_email_domain in
('mit.edu', 'stanford.edu', 'umich.edu', 'inria.fr', 'gatech.edu', 'cornell.edu') then 'prestigious_university'
else 'other'
end as prestigious
, count(*) as cases
, count(distinct d.author_email) as developers

, avg(files_owned_ccp ) as ccp
, avg(avg_coupling_code_size_cut ) as avg_coupling_code_size_cut
, avg(tests_presence ) as tests_presence
, avg(multiline_message_ratio ) as multiline_message_ratio
, avg(message_length_avg ) as message_length_avg_ratio
, avg(same_date_duration_avg ) as same_date_duration_avg
, avg(files_edited ) as files_edited
, avg(refactor_mle ) as refactor_mle
, avg(commit_days ) as commit_days
, avg(one_file_fix_rate ) as one_file_fix_rate
, avg(one_file_refactor_rate ) as one_file_refactor_rate

from general.companies as c
join
general.developer_per_repo_profile as d
on
regexp_contains(d.repo_name, concat('^', c.user))
where Company in ('ibm', 'Apple', 'Amazon', 'Google', 'Microsoft', 'Facebook')
and
commits >= 200
group by
prestigious
order by
count(distinct d.author_email) desc
;
