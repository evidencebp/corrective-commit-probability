# The  following view is used to abstract the table datails (e.g., year)
# and internal logic (exculding forks)

# Standard sql

CREATE OR REPLACE VIEW
ccp.repos
as
select
*
from `hotspots-readability.ccp.repos_full`
where
not Fork
and y2019_ccp > 0
and y2019_ccp < 1
;
