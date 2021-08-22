
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


# 每张地图的时间
create table match_map_time_2020
SELECT match_id,game_number,map_name,
       sum(time_to_sec(t)) as map_time from (
                       SELECT match_id,
                              game_number,
                              map_name,
                              round_start_time,
                              round_end_time,
                              timediff(STR_TO_DATE(round_end_time, '%Y-%m-%d %H:%i:%s'),
                                       STR_TO_DATE(round_start_time, '%Y-%m-%d %H:%i:%s')) as t
                       from match_map_stats
                       where round_start_time > "2020-01-01 00:00:01" and round_start_time < "2021-01-01 00:00:01"
                   ) as tmp
group by match_id,game_number,map_name;


SELECT match_id,
      map_name,
      round_start_time,
      round_end_time,
      timediff(STR_TO_DATE(round_end_time, '%Y-%m-%d %H:%i:%s'),
               STR_TO_DATE(round_start_time, '%Y-%m-%d %H:%i:%s')) as t
from match_map_stats
where match_id = 30991;



SELECT * ,m2.map_time
FROM match_map_stats as m1 INNER JOIN match_map_time_2020 as m2
    ON m1.match_id = m2.match_id and m1.map_name = m2.map_name;


create table match_map_result_2020
select
    distinct t2.match_id,match_winner,
    IF(match_winner = team_one_name,team_two_name, team_one_name) as match_loser,
    t2.game_number as map_number,t2.map_name,
    t2.map_winner, t2.map_loser, t2.map_time
from (
    SELECT m1.match_id,m1.match_winner ,
           m1.team_one_name,m1.team_two_name,
           m1.game_number,m1.map_name,m1.map_winner,m1.map_loser
           ,m2.map_time
    FROM match_map_stats as m1 INNER JOIN match_map_time_2020 as m2
        ON m1.match_id = m2.match_id and m1.map_name = m2.map_name ) as t2
;

create table player_role
select distinct team_name,player_name from phs_2020_1;

# 提取伤害量
create table all_heroes_damage_2020_1
SELECT t1.esports_match_id, t1.map_name, t1.player_name,
       t1.team_name, t1.stat_name, t1.stat_amount, t2.stat_amount as time_played from
              (
            select esports_match_id, map_name, player_name, team_name, stat_name, stat_amount
              from phs_2020_1
              where stat_name = 'Hero Damage Done'
                and hero_name = 'All Heroes') as t1 ## 需要的统计量
JOIN
               ( select esports_match_id, map_name,player_name,team_name,stat_name,stat_amount
                  from phs_2020_1 as t2
                  where stat_name = 'Time Played' and hero_name = 'All Heroes'
                ) as t2  # 时间
on t1.esports_match_id = t2.esports_match_id
       and t1.map_name = t2.map_name
       and t1.player_name = t2.player_name