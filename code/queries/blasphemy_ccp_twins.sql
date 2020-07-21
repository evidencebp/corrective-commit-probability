drop table if exists ccp.blasphemy_ccp_env_porfile; 
    create table  ccp.blasphemy_ccp_env_porfile
    partition by fake_date
    cluster by repo_name
    as
    select
    repo_name
    
    ,  1.0*count(distinct case when     REGEXP_CONTAINS( lower(message), 'disappointing|disheartening|displeasing|mortifying|not up to (par|snuff)|poor|rotten|substandard|unsatisfactory|bad|horrible|terrible|shit|crap|lousy|awful|fuck|disgusting|hideous|nasty|scary|shameful|shame|shocking|repulsive|revolting|stink') then commit else null end)/count(distinct commit)  as blasphemy_hit_rate
    , max(DATE('1980-01-01')) as  fake_date
    from
    ccp.active_2019_commits_by_file
    group by
    repo_name
    
     having count(*) >= 12 
    ;    
    
drop table if exists ccp.blasphemy_ccp_twin_in_env_porfile; 
    create table ccp.blasphemy_ccp_twin_in_env_porfile





    partition by fake_date
    cluster by repo_name, Author_email
    as
    select
    repo_name
    , Author_email
    
    ,  1.0*count(distinct case when     REGEXP_CONTAINS( lower(message), 'disappointing|disheartening|displeasing|mortifying|not up to (par|snuff)|poor|rotten|substandard|unsatisfactory|bad|horrible|terrible|shit|crap|lousy|awful|fuck|disgusting|hideous|nasty|scary|shameful|shame|shocking|repulsive|revolting|stink') then commit else null end)/count(distinct commit)  as blasphemy_hit_rate
    , max(DATE('1980-01-01')) as  fake_date
    from
    ccp.active_2019_commits_by_file
    group by
    repo_name
    , Author_email
    
     having count(*) >= 12 
    ;    
    

    Select 
        twin_in_env1.blasphemy_hit_rate < twin_in_env2.blasphemy_hit_rate  - 0.01 as twin_improved
        , env1.blasphemy_hit_rate < env2.blasphemy_hit_rate  - 0.01 as env_improved
        
        , count(*) as cnt
        , count(distinct twin_in_env1.Author_email) as twins_cnt
        , count(distinct twin_in_env1.repo_name) as envs_cnt
    from
        ccp.blasphemy_ccp_twin_in_env_porfile as twin_in_env1
        join
        ccp.blasphemy_ccp_twin_in_env_porfile as twin_in_env2
        on
        twin_in_env1.Author_email = twin_in_env2.Author_email
        and
        twin_in_env1.repo_name <> twin_in_env2.repo_name
        
        join
        ccp.blasphemy_ccp_env_porfile as env1
        on
        twin_in_env1.repo_name = env1.repo_name
        join
        ccp.blasphemy_ccp_env_porfile as env2
        on
        twin_in_env2.repo_name = env2.repo_name
        group by
        twin_improved, env_improved
                
        order by
        twin_improved, env_improved
         
        ;
    