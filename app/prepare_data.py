import pandas as pd


def prepare_data(date_to, lec_only):
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

    # Loading three OraclesElixir files from https://oracleselixir.com/tools/downloads
    df1 = pd.read_csv('DataSources/OraclesElixir/2024_LoL_esports_match_data_from_OraclesElixir.csv', dtype=dtype)
    df2 = pd.read_csv('DataSources/OraclesElixir/2023_LoL_esports_match_data_from_OraclesElixir.csv', dtype=dtype)
    df3 = pd.read_csv('DataSources/OraclesElixir/2022_LoL_esports_match_data_from_OraclesElixir.csv', dtype=dtype)

    # Combining DataFrames into one DataFrame
    combined_df = pd.concat([df1, df2, df3], ignore_index=True)

    combined_df = combined_df[~combined_df['datacompleteness'].isin(['ignore', 'partial'])]

    if lec_only:
        combined_df = combined_df[combined_df['league'] == 'LEC']

    # Convert 'date' column to datetime type
    combined_df['date'] = pd.to_datetime(combined_df['date'])

    # Cutoff date
    cutoff_date = pd.to_datetime(date_to)

    # Removing entries where 'date' is before cutoff_date
    combined_df = combined_df[combined_df['date'] <= cutoff_date]

    # Filling empty teamnames
    combined_df['teamname'] = combined_df['teamname'].fillna('unknown team')
    # Replace teamnames after merging Mad Lions and KOI
    combined_df['teamname'] = combined_df['teamname'].replace('MAD Lions KOI', 'MAD Lions')
    combined_df['teamname'] = combined_df['teamname'].replace('KOI', 'MAD Lions')

    teams = combined_df['teamname'].unique()
    team_df = pd.DataFrame(teams, columns=['teamname'])
    team_df['team_id'] = range(1, len(team_df) + 1)
    team_df.to_csv('Data/teams.csv', index=False)

    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv('DataSources/lol_lec.csv', index=False)

    print("prepare_data.py COMPLETED - DataSources/lol_lec.csv, Data/teams.csv")
