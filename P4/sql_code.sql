## 找出所有all heroes，全部数据
drop  table  if exists all_heroes_stat_all_2020to2021_tmp1;
Create table all_heroes_stat_all_2020to2021_tmp1
SELECT *
from (
    (select *
    from phs_2020_1
    where hero_name = "All Heroes"
      and (stat_name in  (select distinct stat_name
                            from phs_2020_1
                            where hero_name = "All Heroes"))
      order by esports_match_id)
      #and esports_match_id = 30991
    union
    (select *
    from phs_2020_2
    where hero_name = "All Heroes"
      and (stat_name in  (select distinct stat_name
                            from phs_2020_1
                            where hero_name = "All Heroes"))
        order by esports_match_id)
        union
    (select *
    from phs_2021_1
    where hero_name = "All Heroes"
      and (stat_name in  (select distinct stat_name
                            from phs_2021_1
                            where hero_name = "All Heroes"))
        order by esports_match_id)

    ) as t1;

# 每一列横向展开
drop table if exists all_heroes_stat_all_2020to2021_Player;
Create table all_heroes_stat_all_2020to2021_Player
SELECT esports_match_id, map_name, team_name, player_name,
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
GROUP BY esports_match_id, map_name, team_name, player_name;


drop table if exists all_heroes_stat_all_2020_tmp3;
Create table all_heroes_stat_all_2020_tmp3
Select esports_match_id,team_name,
    SUM(`All Damage Done`) as 'All Damage Done',
    SUM(`Assists`) as 'Assists',
    SUM(`Average Time Alive`) as 'Average Time Alive',
    SUM(`Barrier Damage Done`) as 'Barrier Damage Done',
    SUM(`Damage Blocked`) as 'Damage Blocked',
    SUM(`Damage Done`) as 'Damage Done',
    SUM(`Damage Taken`) as 'Damage Taken',
    SUM(`Deaths`) as 'Deaths',
    SUM(`Eliminations`) as 'Eliminations',
    SUM(`Final Blows`) as 'Final Blows',
    SUM(`Hero Damage Done`) as 'Hero Damage Done',
    SUM(`Multikills`) as 'Multikills',
    SUM(`Objective Kills`) as 'Objective Kills',
    SUM(`Objective Time`) as 'Objective Time',
    SUM(`Offensive Assists`) as 'Offensive Assists',
    SUM(`Time Alive`) as 'Time Alive',
    SUM(`Time Building Ultimate`) as 'Time Building Ultimate',
    SUM(`Time Elapsed per Ultimate Earned`) as 'Time Elapsed per Ultimate Earned',
    SUM(`Time Holding Ultimate`) as 'Time Holding Ultimate',
    SUM(`Time Played`)/6 as 'Time Played',
    SUM(`Ultimates Earned - Fractional`) as 'Ultimates Earned - Fractional',
    SUM(`Ultimates Used`) as 'Ultimates Used',
    SUM(`Damage - Quick Melee`) as 'Damage - Quick Melee',
    SUM(`Defensive Assists`) as 'Defensive Assists',
    SUM(`Environmental Kills`) as 'Environmental Kills',
    SUM(`Healing Done`) as 'Healing Done',
    SUM(`Knockback Kills`) as 'Knockback Kills',
    SUM(`Melee Final Blows`) as 'Melee Final Blows',
    SUM(`Melee Percentage of Final Blows`) as 'Melee Percentage of Final Blows',
    SUM(`Shots Fired`) as 'Shots Fired',
    SUM(`Weapon Accuracy`) as 'Weapon Accuracy',
    SUM(`Environmental Deaths`) as 'Environmental Deaths',
    SUM(`Solo Kills`) as 'Solo Kills',
    SUM(`Turrets Destroyed`) as 'Turrets Destroyed',
    SUM(`Teleporter Pads Destroyed`) as 'Teleporter Pads Destroyed',
    SUM(`Recon Assists`) as 'Recon Assists'
from all_heroes_stat_all_2020to2021_tmp2
where team_name in (select distinct match_winner from match_result_2020)
group by esports_match_id,team_name;


## 合并为每个matchid一行
drop table if exists all_heroes_stat_all_2020_tmp3;
CREATE TABLE all_heroes_stat_all_2020_tmp3
SELECT match_id,t1_Time_Played as Time_Played,
       t1_name,
       t1_All_Damage_Done,
        t1_Assists,
        t1_Average_Time_Alive,
        t1_Barrier_Damage_Done,
        t1_Damage_Blocked,
        t1_Damage_Done,
        t1_Damage_Taken,
        t1_Deaths,
        t1_Eliminations,
        t1_Final_Blows,
        t1_Hero_Damage_Done,
        t1_Multikills,
        t1_Objective_Kills,
        t1_Objective_Time,
        t1_Offensive_Assists,
        t1_Time_Alive,
        t1_Time_Building_Ultimate,
        t1_Time_Elapsed_per_Ultimate_Earned,
        t1_Time_Holding_Ultimate,
        t1_Time_Played,
        `t1_Ultimates_Earned_-_Fractional`,
        t1_Ultimates_Used,
        `t1_Damage_-_Quick_Melee`,
        t1_Defensive_Assists,
        t1_Environmental_Kills,
        t1_Healing_Done,
        t1_Knockback_Kills,
        t1_Melee_Final_Blows,
        t1_Melee_Percentage_of_Final_Blows,
        t1_Shots_Fired,
        t1_Weapon_Accuracy,
        t1_Environmental_Deaths,
        t1_Solo_Kills,
        t1_Turrets_Destroyed,
        t1_Teleporter_Pads_Destroyed,
        t1_Recon_Assists,
        t2_name,
       t2_All_Damage_Done,
        t2_Assists,
        t2_Average_Time_Alive,
        t2_Barrier_Damage_Done,
        t2_Damage_Blocked,
        t2_Damage_Done,
        t2_Damage_Taken,
        t2_Deaths,
        t2_Eliminations,
        t2_Final_Blows,
        t2_Hero_Damage_Done,
        t2_Multikills,
        t2_Objective_Kills,
        t2_Objective_Time,
        t2_Offensive_Assists,
        t2_Time_Alive,
        t2_Time_Building_Ultimate,
        t2_Time_Elapsed_per_Ultimate_Earned,
        t2_Time_Holding_Ultimate,
        t2_Time_Played,
        `t2_Ultimates_Earned_-_Fractional`,
        t2_Ultimates_Used,
        `t2_Damage_-_Quick_Melee`,
        t2_Defensive_Assists,
        t2_Environmental_Kills,
        t2_Healing_Done,
        t2_Knockback_Kills,
        t2_Melee_Final_Blows,
        t2_Melee_Percentage_of_Final_Blows,
        t2_Shots_Fired,
        t2_Weapon_Accuracy,
        t2_Environmental_Deaths,
        t2_Solo_Kills,
        t2_Turrets_Destroyed,
        t2_Teleporter_Pads_Destroyed,
        t2_Recon_Assists
from (select
            esports_match_id as match_id,
            team_name        as t1_name,
            `All Damage Done` as t1_All_Damage_Done,
            `Assists` as t1_Assists,
            `Average Time Alive` as t1_Average_Time_Alive,
            `Barrier Damage Done` as t1_Barrier_Damage_Done,
            `Damage Blocked` as t1_Damage_Blocked,
            `Damage Done` as t1_Damage_Done,
            `Damage Taken` as t1_Damage_Taken,
            `Deaths` as t1_Deaths,
            `Eliminations` as t1_Eliminations,
            `Final Blows` as t1_Final_Blows,
            `Hero Damage Done` as t1_Hero_Damage_Done,
            `Multikills` as t1_Multikills,
            `Objective Kills` as t1_Objective_Kills,
            `Objective Time` as t1_Objective_Time,
            `Offensive Assists` as t1_Offensive_Assists,
            `Time Alive` as t1_Time_Alive,
            `Time Building Ultimate` as t1_Time_Building_Ultimate,
            `Time Elapsed per Ultimate Earned` as t1_Time_Elapsed_per_Ultimate_Earned,
            `Time Holding Ultimate` as t1_Time_Holding_Ultimate,
            `Time Played` as t1_Time_Played,
            `Ultimates Earned - Fractional` as `t1_Ultimates_Earned_-_Fractional`,
            `Ultimates Used` as t1_Ultimates_Used,
            `Damage - Quick Melee` as `t1_Damage_-_Quick_Melee`,
            `Defensive Assists` as t1_Defensive_Assists,
            `Environmental Kills` as t1_Environmental_Kills,
            `Healing Done` as t1_Healing_Done,
            `Knockback Kills` as t1_Knockback_Kills,
            `Melee Final Blows` as t1_Melee_Final_Blows,
            `Melee Percentage of Final Blows` as t1_Melee_Percentage_of_Final_Blows,
            `Shots Fired` as t1_Shots_Fired,
            `Weapon Accuracy` as t1_Weapon_Accuracy,
            `Environmental Deaths` as t1_Environmental_Deaths,
            `Solo Kills` as t1_Solo_Kills,
            `Turrets Destroyed` as t1_Turrets_Destroyed,
            `Teleporter Pads Destroyed` as t1_Teleporter_Pads_Destroyed,
            `Recon Assists` as t1_Recon_Assists
     from all_heroes_stat_all_2020_tmp2) as tt1
        inner join
    (select
            esports_match_id as match_id_2,
            team_name        as t2_name,
            `All Damage Done` as t2_All_Damage_Done,
            `Assists` as t2_Assists,
            `Average Time Alive` as t2_Average_Time_Alive,
            `Barrier Damage Done` as t2_Barrier_Damage_Done,
            `Damage Blocked` as t2_Damage_Blocked,
            `Damage Done` as t2_Damage_Done,
            `Damage Taken` as t2_Damage_Taken,
            `Deaths` as t2_Deaths,
            `Eliminations` as t2_Eliminations,
            `Final Blows` as t2_Final_Blows,
            `Hero Damage Done` as t2_Hero_Damage_Done,
            `Multikills` as t2_Multikills,
            `Objective Kills` as t2_Objective_Kills,
            `Objective Time` as t2_Objective_Time,
            `Offensive Assists` as t2_Offensive_Assists,
            `Time Alive` as t2_Time_Alive,
            `Time Building Ultimate` as t2_Time_Building_Ultimate,
            `Time Elapsed per Ultimate Earned` as t2_Time_Elapsed_per_Ultimate_Earned,
            `Time Holding Ultimate` as t2_Time_Holding_Ultimate,
            `Time Played` as t2_Time_Played,
            `Ultimates Earned - Fractional` as `t2_Ultimates_Earned_-_Fractional`,
            `Ultimates Used` as t2_Ultimates_Used,
            `Damage - Quick Melee` as `t2_Damage_-_Quick_Melee`,
            `Defensive Assists` as t2_Defensive_Assists,
            `Environmental Kills` as t2_Environmental_Kills,
            `Healing Done` as t2_Healing_Done,
            `Knockback Kills` as t2_Knockback_Kills,
            `Melee Final Blows` as t2_Melee_Final_Blows,
            `Melee Percentage of Final Blows` as t2_Melee_Percentage_of_Final_Blows,
            `Shots Fired` as t2_Shots_Fired,
            `Weapon Accuracy` as t2_Weapon_Accuracy,
            `Environmental Deaths` as t2_Environmental_Deaths,
            `Solo Kills` as t2_Solo_Kills,
            `Turrets Destroyed` as t2_Turrets_Destroyed,
            `Teleporter Pads Destroyed` as t2_Teleporter_Pads_Destroyed,
            `Recon Assists` as t2_Recon_Assists
     from all_heroes_stat_all_2020_tmp2) as tt2
    on tt1.match_id = tt2.match_id_2 and
       tt1.t1_name != tt2.t2_name
where tt1.t1_name > tt2.t2_name;