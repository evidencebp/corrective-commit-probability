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

, avg(cur.single_line_message_ratio ) as cur_single_line_message_ratio
, avg(first_year.single_line_message_ratio ) as first_year_single_line_message_ratio
, avg(cur.single_line_message_ratio - first_year.single_line_message_ratio ) as single_line_message_ratio_delta

, avg(cur.same_date_duration_avg ) as cur_same_date_duration_avg
, avg(first_year.same_date_duration_avg ) as first_year_same_date_duration_avg
, avg(cur.same_date_duration_avg - first_year.same_date_duration_avg ) as same_date_duration_avg_delta


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
cur.year = 2019
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
