
# 创建2020赛果表
drop table match_result_2020;

create table match_result_2020
select
    distinct match_id,match_winner,
    IF(match_winner = team_one_name,team_two_name, team_one_name) as match_loser
from match_map_stats
where round_start_time > "2020-01-01 00:00:01" and round_start_time < "2021-01-01 00:00:01"
# where match_id = 10224
;