drop table if exists team_match_stat_all_2020_withRank_v3;
create table team_match_stat_all_2020_withRank_v3
select match_id,t1_name,t2_name,t1_win,
       (avg10_t1_All_Damage_Done - avg10_t2_All_Damage_Done) as t1_t2_All_Damage_Done,
        (avg10_t1_Assists - avg10_t2_Assists) as t1_t2_Assists,
        (avg10_t1_Average_Time_Alive - avg10_t2_Average_Time_Alive) as t1_t2_Average_Time_Alive,
        (avg10_t1_Barrier_Damage_Done - avg10_t2_Barrier_Damage_Done) as t1_t2_Barrier_Damage_Done,
        (avg10_t1_Damage_Blocked - avg10_t2_Damage_Blocked) as t1_t2_Damage_Blocked,
        (avg10_t1_Damage_Done - avg10_t2_Damage_Done) as t1_t2_Damage_Done,
        (avg10_t1_Damage_Taken - avg10_t2_Damage_Taken) as t1_t2_Damage_Taken,
        (avg10_t1_Deaths - avg10_t2_Deaths) as t1_t2_Deaths,
        (avg10_t1_Eliminations - avg10_t2_Eliminations) as t1_t2_Eliminations,
        (avg10_t1_Final_Blows - avg10_t2_Final_Blows) as t1_t2_Final_Blows,
        (avg10_t1_Hero_Damage_Done - avg10_t2_Hero_Damage_Done) as t1_t2_Hero_Damage_Done,
        (avg10_t1_Multikills - avg10_t2_Multikills) as t1_t2_Multikills,
        (avg10_t1_Objective_Kills - avg10_t2_Objective_Kills) as t1_t2_Objective_Kills,
        (avg10_t1_Objective_Time - avg10_t2_Objective_Time) as t1_t2_Objective_Time,
        (avg10_t1_Offensive_Assists - avg10_t2_Offensive_Assists) as t1_t2_Offensive_Assists,
        (avg10_t1_Time_Alive - avg10_t2_Time_Alive) as t1_t2_Time_Alive,
        (avg10_t1_Time_Building_Ultimate - avg10_t2_Time_Building_Ultimate) as t1_t2_Time_Building_Ultimate,
        (avg10_t1_Time_Elapsed_per_Ultimate_Earned - avg10_t2_Time_Elapsed_per_Ultimate_Earned) as t1_t2_Time_Elapsed_per_Ultimate_Earned,
        (avg10_t1_Time_Holding_Ultimate - avg10_t2_Time_Holding_Ultimate) as t1_t2_Time_Holding_Ultimate,
        (avg10_t1_Time_Played - avg10_t2_Time_Played) as t1_t2_Time_Played,
        (`avg10_t1_Ultimates_Earned_-_Fractional` - `avg10_t2_Ultimates_Earned_-_Fractional`) as `t1_t2_Ultimates_Earned_-_Fractional`,
        (avg10_t1_Ultimates_Used - avg10_t2_Ultimates_Used) as t1_t2_Ultimates_Used,
        (`avg10_t1_Damage_-_Quick_Melee` - `avg10_t2_Damage_-_Quick_Melee`) as `t1_t2_Damage_-_Quick_Melee`,
        (avg10_t1_Defensive_Assists - avg10_t2_Defensive_Assists) as t1_t2_Defensive_Assists,
        (avg10_t1_Environmental_Kills - avg10_t2_Environmental_Kills) as t1_t2_Environmental_Kills,
        (avg10_t1_Healing_Done - avg10_t2_Healing_Done) as t1_t2_Healing_Done,
        (avg10_t1_Knockback_Kills - avg10_t2_Knockback_Kills) as t1_t2_Knockback_Kills,
        (avg10_t1_Melee_Final_Blows - avg10_t2_Melee_Final_Blows) as t1_t2_Melee_Final_Blows,
        (avg10_t1_Melee_Percentage_of_Final_Blows - avg10_t2_Melee_Percentage_of_Final_Blows) as t1_t2_Melee_Percentage_of_Final_Blows,
        (avg10_t1_Shots_Fired - avg10_t2_Shots_Fired) as t1_t2_Shots_Fired,
        (avg10_t1_Weapon_Accuracy - avg10_t2_Weapon_Accuracy) as t1_t2_Weapon_Accuracy,
        (avg10_t1_Environmental_Deaths - avg10_t2_Environmental_Deaths) as t1_t2_Environmental_Deaths,
        (avg10_t1_Solo_Kills - avg10_t2_Solo_Kills) as t1_t2_Solo_Kills,
        (avg10_t1_Turrets_Destroyed - avg10_t2_Turrets_Destroyed) as t1_t2_Turrets_Destroyed,
        (avg10_t1_Teleporter_Pads_Destroyed - avg10_t2_Teleporter_Pads_Destroyed) as t1_t2_Teleporter_Pads_Destroyed,
        (avg10_t1_Recon_Assists - avg10_t2_Recon_Assists) as t1_t2_Recon_Assists,
        (t1_officialwin_before - t2_officialwin_before) as t1_t2_officialwin_before,
         (t1_pagerank_before - t2_pagerank_before) as t1_t2_pagerank_before,
         (t1_playerrank_before - t2_playerrank_before) as t1_t2_playerrank_before
from team_match_stat_all_2020_withRank_v2;


drop table if exists TESTSET_V3;
create table TESTSET_V3
select match_id,t1_name,t2_name,t1_win,
       (avg10_t1_All_Damage_Done - avg10_t2_All_Damage_Done) as t1_t2_All_Damage_Done,
        (avg10_t1_Assists - avg10_t2_Assists) as t1_t2_Assists,
        (avg10_t1_Average_Time_Alive - avg10_t2_Average_Time_Alive) as t1_t2_Average_Time_Alive,
        (avg10_t1_Barrier_Damage_Done - avg10_t2_Barrier_Damage_Done) as t1_t2_Barrier_Damage_Done,
        (avg10_t1_Damage_Blocked - avg10_t2_Damage_Blocked) as t1_t2_Damage_Blocked,
        (avg10_t1_Damage_Done - avg10_t2_Damage_Done) as t1_t2_Damage_Done,
        (avg10_t1_Damage_Taken - avg10_t2_Damage_Taken) as t1_t2_Damage_Taken,
        (avg10_t1_Deaths - avg10_t2_Deaths) as t1_t2_Deaths,
        (avg10_t1_Eliminations - avg10_t2_Eliminations) as t1_t2_Eliminations,
        (avg10_t1_Final_Blows - avg10_t2_Final_Blows) as t1_t2_Final_Blows,
        (avg10_t1_Hero_Damage_Done - avg10_t2_Hero_Damage_Done) as t1_t2_Hero_Damage_Done,
        (avg10_t1_Multikills - avg10_t2_Multikills) as t1_t2_Multikills,
        (avg10_t1_Objective_Kills - avg10_t2_Objective_Kills) as t1_t2_Objective_Kills,
        (avg10_t1_Objective_Time - avg10_t2_Objective_Time) as t1_t2_Objective_Time,
        (avg10_t1_Offensive_Assists - avg10_t2_Offensive_Assists) as t1_t2_Offensive_Assists,
        (avg10_t1_Time_Alive - avg10_t2_Time_Alive) as t1_t2_Time_Alive,
        (avg10_t1_Time_Building_Ultimate - avg10_t2_Time_Building_Ultimate) as t1_t2_Time_Building_Ultimate,
        (avg10_t1_Time_Elapsed_per_Ultimate_Earned - avg10_t2_Time_Elapsed_per_Ultimate_Earned) as t1_t2_Time_Elapsed_per_Ultimate_Earned,
        (avg10_t1_Time_Holding_Ultimate - avg10_t2_Time_Holding_Ultimate) as t1_t2_Time_Holding_Ultimate,
        (avg10_t1_Time_Played - avg10_t2_Time_Played) as t1_t2_Time_Played,
        (`avg10_t1_Ultimates_Earned_-_Fractional` - `avg10_t2_Ultimates_Earned_-_Fractional`) as `t1_t2_Ultimates_Earned_-_Fractional`,
        (avg10_t1_Ultimates_Used - avg10_t2_Ultimates_Used) as t1_t2_Ultimates_Used,
        (`avg10_t1_Damage_-_Quick_Melee` - `avg10_t2_Damage_-_Quick_Melee`) as `t1_t2_Damage_-_Quick_Melee`,
        (avg10_t1_Defensive_Assists - avg10_t2_Defensive_Assists) as t1_t2_Defensive_Assists,
        (avg10_t1_Environmental_Kills - avg10_t2_Environmental_Kills) as t1_t2_Environmental_Kills,
        (avg10_t1_Healing_Done - avg10_t2_Healing_Done) as t1_t2_Healing_Done,
        (avg10_t1_Knockback_Kills - avg10_t2_Knockback_Kills) as t1_t2_Knockback_Kills,
        (avg10_t1_Melee_Final_Blows - avg10_t2_Melee_Final_Blows) as t1_t2_Melee_Final_Blows,
        (avg10_t1_Melee_Percentage_of_Final_Blows - avg10_t2_Melee_Percentage_of_Final_Blows) as t1_t2_Melee_Percentage_of_Final_Blows,
        (avg10_t1_Shots_Fired - avg10_t2_Shots_Fired) as t1_t2_Shots_Fired,
        (avg10_t1_Weapon_Accuracy - avg10_t2_Weapon_Accuracy) as t1_t2_Weapon_Accuracy,
        (avg10_t1_Environmental_Deaths - avg10_t2_Environmental_Deaths) as t1_t2_Environmental_Deaths,
        (avg10_t1_Solo_Kills - avg10_t2_Solo_Kills) as t1_t2_Solo_Kills,
        (avg10_t1_Turrets_Destroyed - avg10_t2_Turrets_Destroyed) as t1_t2_Turrets_Destroyed,
        (avg10_t1_Teleporter_Pads_Destroyed - avg10_t2_Teleporter_Pads_Destroyed) as t1_t2_Teleporter_Pads_Destroyed,
        (avg10_t1_Recon_Assists - avg10_t2_Recon_Assists) as t1_t2_Recon_Assists,
        (t1_officialwin_before - t2_officialwin_before) as t1_t2_officialwin_before,
         (t1_pagerank_before - t2_pagerank_before) as t1_t2_pagerank_before,
         (t1_playerrank_before - t2_playerrank_before) as t1_t2_playerrank_before
from TESTSET_V2;