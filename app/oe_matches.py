import pandas as pd


def oe_matches():
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

    # Load file
    file_path = 'DataSources/lol_lec.csv'
    df = pd.read_csv(file_path, dtype=dtype)

    # Filter rows where participantid is 100 or 200 (teams stats)
    filtered_df = df[df['participantid'].isin([100, 200])]

    # Aggregate the matches to create the desired dataframe
    aggregated_df = filtered_df.pivot_table(index='gameid', columns='participantid', values=['teamname', 'result'],
                                            aggfunc='first').reset_index()

    # Renaming columns to match the desired output
    aggregated_df.columns = ['gameid', 'result', 'result2', 'team1', 'team2']

    aggregated_df.drop(columns='result2', inplace=True)

    # Extracting the date from the original dataframe
    date_df = filtered_df[['gameid', 'date']].drop_duplicates()

    # Merging the date information with the aggregated dataframe
    result_df = pd.merge(aggregated_df, date_df, on='gameid')

    # Reordering columns
    result_df = result_df[['gameid', 'date', 'team1', 'team2', 'result']]

    # Converting the date column to datetime format
    result_df['date'] = pd.to_datetime(result_df['date'])

    # Sorting the dataframe by date in ascending order
    result_df = result_df.sort_values(by='date')

    # Save the resulting dataframe to a new CSV file
    result_df.to_csv('Data/matches.csv', index=False)

    print("oe_matches.py COMPLETED - Data/matches.csv")
