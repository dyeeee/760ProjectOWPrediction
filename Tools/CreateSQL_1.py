all_features = [
    "All Damage Done",
    "Assists",
    "Average Time Alive",
    "Barrier Damage Done",
    "Damage Blocked",
    "Damage Done",
    "Damage Taken",
    "Deaths",
    "Eliminations",
    "Final Blows",
    "Hero Damage Done",
    "Multikills",
    "Objective Kills",
    "Objective Time",
    "Offensive Assists",
    "Time Alive",
    "Time Building Ultimate",
    "Time Elapsed per Ultimate Earned",
    "Time Holding Ultimate",
    "Time Played",
    "Ultimates Earned - Fractional",
    "Ultimates Used",
    "Damage - Quick Melee",
    "Defensive Assists",
    "Environmental Kills",
    "Healing Done",
    "Knockback Kills",
    "Melee Final Blows",
    "Melee Percentage of Final Blows",
    "Shots Fired",
    "Weapon Accuracy",
    "Environmental Deaths",
    "Solo Kills",
    "Turrets Destroyed",
    "Teleporter Pads Destroyed",
    "Recon Assists"]

# for str in all_features:
#     result = '''SUM(IF(stat_name = '{0}', stat_amount,0)) as "{0}",'''.format(str)
#     print(result)

# for str in all_features:
#     result = '''SUM(`{0}`) as '{0}','''.format(str)
#     print(result)


# for str in all_features:
#     result = '`{0}` as t2_{1},'.format(str, str.replace(" ", "_"))
#     result2 = 't1_{0},'.format(str.replace(" ", "_"))
#     print(result2)

# for str in all_features:
#     result = 't1_{0}/Time_Played*600 as avg10_t1_{0},'.format(str.replace(" ", "_"))
#     result2 = 't2_{0}/Time_Played*600 as avg10_t2_{0},'.format(str.replace(" ", "_"))
#     print(result,result2)


# for str in all_features:
#     result = "(avg10_t1_{0} - avg10_t2_{0}) as t1_t2_{0},".format(str.replace(" ", "_"))
#     print(result)

for str in all_features:
    result = "avg10_t1_{0},avg10_t2_{0},".format(str.replace(" ", "_"))
    print(result,end="")
