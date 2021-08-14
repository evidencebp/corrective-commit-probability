
select
author_email_domain
, count(*) as cases
, count(distinct d.author_email) as developers

, avg(files_owned_ccp ) as ccp
, avg(avg_coupling_code_size_cut ) as avg_coupling_code_size_cut
, avg(tests_presence ) as tests_presence
, avg(single_line_message_ratio ) as single_line_message_ratio
, avg(same_date_duration_avg ) as same_date_duration_avg


from
general.developer_profile as d
where commits >= 50
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
, avg(single_line_message_ratio ) as single_line_message_ratio
, avg(same_date_duration_avg ) as same_date_duration_avg
from
general.developer_profile as d
where commits >= 50
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
, avg(single_line_message_ratio ) as single_line_message_ratio
, avg(same_date_duration_avg ) as same_date_duration_avg


from
general.developer_profile as d
where commits >= 50
and
tests_presence < 0.01
group by
prestigious
order by
count(distinct d.author_email) desc
;

