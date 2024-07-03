import pandas as pd


def oe_to_data_transformed():
    dtype = {
        'gameid': 'object',
        'datacompleteness': 'object',
        'url': 'object',
        'league': 'object',
        'year': 'int64',
        'split': 'object',
        'playoffs': 'float64',
        'date': 'object',
        'game': 'int64',
        'patch': 'object',
        'participantid': 'int64',
        'side': 'object',
        'position': 'object',
        'playername': 'object',
        'playerid': 'object',
        'teamname': 'object',
        'teamid': 'object',
        'champion': 'object',
        'ban1': 'object',
        'ban2': 'object',
        'ban3': 'object',
        'ban4': 'object',
        'ban5': 'object',
        'pick1': 'object',
        'pick2': 'object',
        'pick3': 'object',
        'pick4': 'object',
        'pick5': 'object',
        'gamelength': 'object',
        'result': 'int64',
        'kills': 'float64',
        'deaths': 'float64',
        'assists': 'float64',
        'teamkills': 'float64',
        'teamdeaths': 'float64',
        'doublekills': 'float64',
        'triplekills': 'float64',
        'quadrakills': 'float64',
        'pentakills': 'float64',
        'firstblood': 'float64',
        'firstbloodkill': 'float64',
        'firstbloodassist': 'float64',
        'firstbloodvictim': 'float64',
        'team kpm': 'float64',
        'ckpm': 'float64',
        'firstdragon': 'float64',
        'dragons': 'float64',
        'opp_dragons': 'float64',
        'elementaldrakes': 'float64',
        'opp_elementaldrakes': 'float64',
        'infernals': 'float64',
        'mountains': 'float64',
        'clouds': 'float64',
        'oceans': 'float64',
        'chemtechs': 'float64',
        'hextechs': 'float64',
        'dragons (type unknown)': 'float64',
        'elders': 'float64',
        'opp_elders': 'float64',
        'firstherald': 'float64',
        'heralds': 'float64',
        'opp_heralds': 'float64',
        'void_grubs': 'float64',
        'opp_void_grubs': 'float64',
        'firstbaron': 'float64',
        'barons': 'float64',
        'opp_barons': 'float64',
        'firsttower': 'float64',
        'towers': 'float64',
        'opp_towers': 'float64',
        'firstmidtower': 'float64',
        'firsttothreetowers': 'float64',
        'turretplates': 'float64',
        'opp_turretplates': 'float64',
        'inhibitors': 'float64',
        'opp_inhibitors': 'float64',
        'damagetochampions': 'float64',
        'dpm': 'float64',
        'damageshare': 'float64',
        'damagetakenperminute': 'float64',
        'damagemitigatedperminute': 'float64',
        'wardsplaced': 'float64',
        'wpm': 'float64',
        'wardskilled': 'float64',
        'wcpm': 'float64',
        'controlwardsbought': 'float64',
        'visionscore': 'float64',
        'vspm': 'float64',
        'totalgold': 'float64',
        'earnedgold': 'float64',
        'earned gpm': 'float64',
        'earnedgoldshare': 'float64',
        'goldspent': 'float64',
        'gspd': 'float64',
        'gpr': 'float64',
        'total cs': 'float64',
        'minionkills': 'float64',
        'monsterkills': 'float64',
        'monsterkillsownjungle': 'float64',
        'monsterkillsenemyjungle': 'float64',
        'cspm': 'float64',
        'goldat10': 'float64',
        'xpat10': 'float64',
        'csat10': 'float64',
        'opp_goldat10': 'float64',
        'opp_xpat10': 'float64',
        'opp_csat10': 'float64',
        'golddiffat10': 'float64',
        'xpdiffat10': 'float64',
        'csdiffat10': 'float64',
        'killsat10': 'float64',
        'assistsat10': 'float64',
        'deathsat10': 'float64',
        'opp_killsat10': 'float64',
        'opp_assistsat10': 'float64',
        'opp_deathsat10': 'float64',
        'goldat15': 'float64',
        'xpat15': 'float64',
        'csat15': 'float64',
        'opp_goldat15': 'float64',
        'opp_xpat15': 'float64',
        'opp_csat15': 'float64',
        'golddiffat15': 'float64',
        'xpdiffat15': 'float64',
        'csdiffat15': 'float64',
        'killsat15': 'float64',
        'assistsat15': 'float64',
        'deathsat15': 'float64',
        'opp_killsat15': 'float64',
        'opp_assistsat15': 'float64',
        'opp_deathsat15': 'float64'

    }

    # Load data from CSV file
    file_path = 'DataSources/lol_lec.csv'
    data = pd.read_csv(file_path, dtype=dtype)

    # Remove unnecessary columns
    columns_to_remove = [
        'datacompleteness', 'url', 'league', 'split', 'year', 'side', 'champion', 'ban1', 'ban2', 'ban3', 'ban4',
        'ban5', 'pick1', 'pick2', 'pick3', 'pick4', 'pick5', 'quadrakills', 'pentakills',
        'infernals', 'mountains', 'clouds', 'oceans', 'chemtechs', 'hextechs', 'dragons (type unknown)', 'void_grubs',
        'opp_void_grubs', 'monsterkillsownjungle', 'monsterkillsenemyjungle'
    ]

    data = data.drop(columns=[col for col in columns_to_remove if col in data.columns])

    # Convert 'date' column to datetime type
    data['date'] = pd.to_datetime(data['date'], errors='coerce')

    # Create separate tables for player and team stats based on participantid
    player_stats = data[data['participantid'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])].copy()
    team_stats = data[data['participantid'].isin([100, 200])].copy()

    # Remove specified columns from player stats
    columns_to_remove_player = [
        'playerid', 'teamid', 'gamelength', 'teamkills', 'teamdeaths', 'firstblood', 'team kpm',
        'ckpm', 'firstdragon', 'dragons', 'opp_dragons', 'elementaldrakes', 'opp_elementaldrakes', 'elders',
        'opp_elders',
        'firstherald', 'heralds', 'opp_heralds', 'firstbaron', 'gspd', 'gpr', 'firsttower', 'towers', 'opp_towers',
        'firstmidtower', 'firsttothreetowers', 'turretplates', 'opp_turretplates', 'participantid'
    ]

    player_stats = player_stats.drop(columns=[col for col in columns_to_remove_player if col in player_stats.columns])

    # Remove specified columns from team stats
    columns_to_remove_team = [
        'position', 'playername', 'playerid', 'teamid', 'kills', 'deaths', 'dragons', 'opp_dragons', 'damageshare',
        'earnedgoldshare', 'total cs', 'firstbloodkill', 'firstbloodassist', 'firstbloodvictim'
    ]
    team_stats = team_stats.drop(columns=[col for col in columns_to_remove_team if col in team_stats.columns])

    # Save the resulting tables to CSV files
    player_stats.to_csv('Data/player_stats.csv', index=False)
    team_stats.to_csv('Data/team_stats.csv', index=False)

    print("oe_to_data_transformed.py COMPLETED - Data/player_stats.csv, Data/team_stats.csv")
