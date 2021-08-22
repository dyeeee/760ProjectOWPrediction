
## 找出所有all heroes，英雄伤害、治疗、最后一击、死亡、时间数据
drop  table  all_heroes_stat_1_2020_tmp1;
Create table all_heroes_stat_1_2020_tmp1
SELECT *
from (
    (select *
    from phs_2020_1
    where hero_name = "All Heroes"
      and (stat_name = "Hero Damage Done"
        or stat_name = "Healing Done"
        or stat_name = "Final Blows"
        or stat_name = "Deaths"
          or stat_name = "Time Played"
          )
      order by esports_match_id)
      #and esports_match_id = 30991
    union
    (select *
    from phs_2020_2
    where hero_name = "All Heroes"
      and (stat_name = "Hero Damage Done"
        or stat_name = "Healing Done"
        or stat_name = "Final Blows"
        or stat_name = "Deaths"
          or stat_name = "Time Played"
          )
        order by esports_match_id)
      #and esports_match_id = 34844
    ) as t1;


# 每一列横向展开
Create table all_heroes_stat_1_2020_tmp2
SELECT esports_match_id, map_name, team_name, player_name,
       SUM(IF(stat_name = 'Hero Damage Done', stat_amount,0)) as "Hero Damage Done",
       SUM(IF(stat_name = 'Healing Done', stat_amount,0)) as "Healing Done",
       SUM(IF(stat_name = 'Final Blows', stat_amount,0)) as "Final Blows",
       SUM(IF(stat_name = 'Deaths', stat_amount,0)) as "Deaths",
       SUM(IF(stat_name = 'Time Played', stat_amount,0)) as "Time Played"
FROM all_heroes_stat_1_2020_tmp1
GROUP BY esports_match_id, map_name, team_name, player_name;

# 按比赛ID和队伍求和
Create table team_match_stat_2020_tmp1
Select esports_match_id,team_name,
       sum(`Hero Damage Done`) as 'Hero_Damage_Done',
       sum(`Healing Done`) as 'Healing_Done',
       sum(`Final Blows`) as 'Final_Blows',
       sum(`Deaths`) as 'Deaths',
       sum(`Time Played`)/6 as `Time_Played`
from all_heroes_stat_1_2020_tmp2
group by esports_match_id,team_name;


## 合并为每个matchid一行
drop table team_match_stat_2020_tmp2;
CREATE TABLE team_match_stat_2020_tmp2
SELECT match_id,Time_Played,
       t1_name,t1_Hero_Damage_done,
       t1_Healing_Done,t1_Final_Blows,t1_Deaths,
       t2_name,t2_Hero_Damage_done,
       t2_Healing_Done,t2_Final_Blows,t2_Deaths
from (select esports_match_id as match_id,
            team_name        as t1_name,
            Hero_Damage_Done as t1_Hero_Damage_done,
            Healing_Done     as t1_Healing_Done,
            Final_Blows      as t1_Final_Blows,
            Deaths           as t1_Deaths,
            Time_Played      as Time_Played
     from team_match_stat_2020_tmp1) as tt1
        inner join
    (select esports_match_id as match_id_2,
            team_name        as t2_name,
            Hero_Damage_Done as t2_Hero_Damage_done,
            Healing_Done     as t2_Healing_Done,
            Final_Blows      as t2_Final_Blows,
            Deaths           as t2_Deaths
     from team_match_stat_2020_tmp1) as tt2
    on tt1.match_id = tt2.match_id_2 and
       tt1.t1_name != tt2.t2_name
where tt1.t1_name > tt2.t2_name;

## 关联胜负
CREATE TABLE team_match_stat_2020_tmp3
select *
from team_match_stat_2020_tmp2 as t1
      inner join
  (
      select t2.match_id as mid,
             t2.match_winner,
             t2.match_loser
      from match_result_2020 as t2
  ) as tt
  on t1.match_id = tt.mid;


## 最终结果
CREATE table team_match_stat_2020
SELECT match_id,
       IF(match_winner=t1_name,1,0) as t1_win,
       #match_winner,t1_name,t2_name,
       t1_Hero_Damage_done/Time_played*60 as avg_10_t1_Hero_Damage_Done,
       t1_Final_Blows/Time_played*60 as avg_10_t1_Final_Blows,
       t1_Healing_done/Time_played*60 as avg_10_t1_Healing_done,
       t1_Deaths/Time_played*60 as avg_10_t1_Deaths,
       t2_Hero_Damage_done/Time_played*60 as avg_10_t2_Hero_Damage_done,
       t2_Final_Blows/Time_played*60 as avg_10_t2_Final_Blows,
       t2_Healing_done/Time_played*60 as avg_10_t2_Healing_done,
       t2_Deaths/Time_played*60 as avg_10_t2_Deaths
FROM team_match_stat_2020_tmp3;