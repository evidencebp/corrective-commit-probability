select
first_year.year
, count(*) as cases
, count(distinct d.author_email) as developers

, avg(cur.files_owned_ccp ) as cur_ccp
, avg(first_year.files_owned_ccp ) as first_year_ccp
, avg(cur.files_owned_ccp - first_year.files_owned_ccp ) as ccp_delta

, avg(cur.avg_coupling_code_size_cut ) as cur_avg_coupling_code_size_cut
, avg(first_year.avg_coupling_code_size_cut ) as first_year_avg_coupling_code_size_cut
, avg(cur.avg_coupling_code_size_cut - first_year.avg_coupling_code_size_cut ) as avg_coupling_code_size_cut_delta

, avg(cur.tests_presence ) as cur_tests_presence
, avg(first_year.tests_presence ) as first_year_tests_presence
, avg(cur.tests_presence - first_year.tests_presence ) as tests_presence_delta


, avg(cur.same_date_duration_avg ) as cur_same_date_duration_avg
, avg(first_year.same_date_duration_avg ) as first_year_same_date_duration_avg
, avg(cur.same_date_duration_avg - first_year.same_date_duration_avg ) as same_date_duration_avg_delta

, avg(cur.message_length_avg ) as cur_message_length_avg
, avg(first_year.message_length_avg ) as first_message_length_avg
, avg(cur.message_length_avg - first_year.message_length_avg ) as message_length_avg_delta

, avg(cur.multiline_message_ratio ) as cur_multiline_message_ratio
, avg(first_year.multiline_message_ratio ) as first_multiline_message_ratio
, avg(cur.multiline_message_ratio - first_year.multiline_message_ratio ) as multiline_message_ratio_delta

, avg(cur.files_edited ) as cur_files_edited
, avg(first_year.files_edited ) as first_files_edited
, avg(cur.files_edited - first_year.files_edited ) as files_edited_delta


, avg(cur.refactor_mle ) as cur_refactor_mle
, avg(first_year.refactor_mle ) as first_refactor_mle
, avg(cur.refactor_mle - first_year.refactor_mle ) as refactor_mle_delta

, avg(cur.commit_days ) as cur_commit_days
, avg(first_year.commit_days ) as first_commit_days
, avg(cur.commit_days - first_year.commit_days ) as commit_days_delta

, avg(cur.one_file_fix_rate ) as cur_one_file_fix_rate
, avg(first_year.one_file_fix_rate ) as first_one_file_fix_rate
, avg(cur.one_file_fix_rate - first_year.one_file_fix_rate ) as one_file_fix_rate_delta

, avg(cur.one_file_refactor_rate ) as cur_one_file_refactor_rate
, avg(first_year.one_file_refactor_rate ) as first_one_file_refactor_rate
, avg(cur.one_file_refactor_rate - first_year.one_file_refactor_rate ) as one_file_refactor_rate_delta

from
general.developer_per_repo_profile as d
join
general.developer_per_repo_profile_per_year as cur
on
d.repo_name= cur.repo_name
and
d.author_email = cur.author_email
join
general.developer_per_repo_profile_per_year as first_year
on
d.repo_name= first_year.repo_name
and
d.author_email= first_year.author_email

where
cur.year = 2020
and
first_year.year = extract(year from d.min_commit_timestamp)
# different years
and
cur.year <> first_year.year
# enough commits per year
and
cur.commits >= 50
and
first_year.commits >= 50
group by
first_year.year
order by
first_year.year desc
;
