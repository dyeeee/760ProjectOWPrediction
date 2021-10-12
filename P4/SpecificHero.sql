
drop  table  if exists ana_stat_all_2020to2021_tmp1;
Create table ana_stat_all_2020to2021_tmp1
SELECT *
from (
    (select *
    from phs_2020_1
    where hero_name = "Ana"
      and (stat_name in  (select distinct stat_name
                            from phs_2020_1
                            where hero_name = "Ana"))
      order by esports_match_id)
      #and esports_match_id = 30991
    union
    (select *
    from phs_2020_2
    where hero_name = "Ana"
      and (stat_name in  (select distinct stat_name
                            from phs_2020_1
                            where hero_name = "Ana"))
        order by esports_match_id)
        union
    (select *
    from phs_2021_1
    where hero_name = "Ana"
      and (stat_name in  (select distinct stat_name
                            from phs_2021_1
                            where hero_name = "Ana"))
        order by esports_match_id)
    ) as t1;



# 每一列横向展开
drop table if exists ana_stat_all_2020to2021_Player;
Create table ana_stat_all_2020to2021_Player
SELECT esports_match_id, team_name, player_name,
        SUM(IF(stat_name = 'All Damage Done', stat_amount,0)) as "All Damage Done",
        SUM(IF(stat_name = 'Assists', stat_amount,0)) as "Assists",
        SUM(IF(stat_name = 'Average Time Alive', stat_amount,0)) as "Average Time Alive",
        SUM(IF(stat_name = 'Barrier Damage Done', stat_amount,0)) as "Barrier Damage Done",
        SUM(IF(stat_name = 'Damage Blocked', stat_amount,0)) as "Damage Blocked",
        SUM(IF(stat_name = 'Damage Done', stat_amount,0)) as "Damage Done",
        SUM(IF(stat_name = 'Damage Taken', stat_amount,0)) as "Damage Taken",
        SUM(IF(stat_name = 'Deaths', stat_amount,0)) as "Deaths",
        SUM(IF(stat_name = 'Eliminations', stat_amount,0)) as "Eliminations",
        SUM(IF(stat_name = 'Final Blows', stat_amount,0)) as "Final Blows",
        SUM(IF(stat_name = 'Hero Damage Done', stat_amount,0)) as "Hero Damage Done",
        SUM(IF(stat_name = 'Multikills', stat_amount,0)) as "Multikills",
        SUM(IF(stat_name = 'Objective Kills', stat_amount,0)) as "Objective Kills",
        SUM(IF(stat_name = 'Objective Time', stat_amount,0)) as "Objective Time",
        SUM(IF(stat_name = 'Offensive Assists', stat_amount,0)) as "Offensive Assists",
        SUM(IF(stat_name = 'Time Alive', stat_amount,0)) as "Time Alive",
        SUM(IF(stat_name = 'Time Building Ultimate', stat_amount,0)) as "Time Building Ultimate",
        SUM(IF(stat_name = 'Time Elapsed per Ultimate Earned', stat_amount,0)) as "Time Elapsed per Ultimate Earned",
        SUM(IF(stat_name = 'Time Holding Ultimate', stat_amount,0)) as "Time Holding Ultimate",
        SUM(IF(stat_name = 'Time Played', stat_amount,0)) as "Time Played",
        SUM(IF(stat_name = 'Ultimates Earned - Fractional', stat_amount,0)) as "Ultimates Earned - Fractional",
        SUM(IF(stat_name = 'Ultimates Used', stat_amount,0)) as "Ultimates Used",
        SUM(IF(stat_name = 'Damage - Quick Melee', stat_amount,0)) as "Damage - Quick Melee",
        SUM(IF(stat_name = 'Defensive Assists', stat_amount,0)) as "Defensive Assists",
        SUM(IF(stat_name = 'Environmental Kills', stat_amount,0)) as "Environmental Kills",
        SUM(IF(stat_name = 'Healing Done', stat_amount,0)) as "Healing Done",
        SUM(IF(stat_name = 'Knockback Kills', stat_amount,0)) as "Knockback Kills",
        SUM(IF(stat_name = 'Melee Final Blows', stat_amount,0)) as "Melee Final Blows",
        SUM(IF(stat_name = 'Melee Percentage of Final Blows', stat_amount,0)) as "Melee Percentage of Final Blows",
        SUM(IF(stat_name = 'Shots Fired', stat_amount,0)) as "Shots Fired",
        SUM(IF(stat_name = 'Weapon Accuracy', stat_amount,0)) as "Weapon Accuracy",
        SUM(IF(stat_name = 'Environmental Deaths', stat_amount,0)) as "Environmental Deaths",
        SUM(IF(stat_name = 'Solo Kills', stat_amount,0)) as "Solo Kills",
        SUM(IF(stat_name = 'Turrets Destroyed', stat_amount,0)) as "Turrets Destroyed",
        SUM(IF(stat_name = 'Teleporter Pads Destroyed', stat_amount,0)) as "Teleporter Pads Destroyed",
        SUM(IF(stat_name = 'Recon Assists', stat_amount,0)) as "Recon Assists"
FROM all_heroes_stat_all_2020_tmp1
where team_name in (select distinct match_winner from match_result_2020)
GROUP BY esports_match_id, team_name, player_name;