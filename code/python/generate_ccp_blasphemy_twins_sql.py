import os
from configuration import SCRIPTS_PATH
from twins_analysis import generate_twins_sql

def generate_ccp_blasphemy_twins_sql():

    name = 'blasphemy_ccp'
    generate_twins_sql(source_data_set='ccp.active_2019_commits_by_file'
                           , twin_column='Author_email'
                           , env_column='repo_name'
                           , metrics_dict={'blasphemy_hit_rate' : {'code' : "1.0*count(distinct case when     REGEXP_CONTAINS( lower(message),"
                                                " 'disappointing|disheartening|displeasing|mortifying|"
                                                "not up to (par|snuff)|poor|rotten|substandard|unsatisfactory|bad|"
                                                "horrible|terrible|shit|crap|lousy|awful|fuck|disgusting|hideous|nasty|"
                                                "scary|shameful|shame|shocking|repulsive|revolting|stink') "
                                                "then commit else null end)/count(distinct commit) "
                                                , 'the_higher_the_better' : False}}
                           , prefix=name + "_"
                           , output_file=os.path.join(SCRIPTS_PATH, "{}_twins.sql".format(name))
                           , control_variables=[]
                           , schema='ccp'
                           , twin_threshold=0.01
                           , env_threshold=0.01
                           , having_clause=' having count(*) >= 12 '
                       )


if __name__ == '__main__':
    generate_ccp_blasphemy_twins_sql()
