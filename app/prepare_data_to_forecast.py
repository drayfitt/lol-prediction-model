import pandas as pd


def prepare_data_to_forecast(predictions_path):
    last_results = pd.read_csv('Data/merged_team_player_stats.csv')
    predict = pd.read_csv(predictions_path)
    teams_df = pd.read_csv('Data/teams.csv')

    # Merge team1_id based on team_1 name
    predict = predict.merge(teams_df, how='left', left_on='team_1', right_on='teamname').drop(
        columns=['teamname']).rename(columns={'team_id': 'team1_id'})
    # Merge team2_id based on team_2 name
    predict = predict.merge(teams_df, how='left', left_on='team_2', right_on='teamname').drop(
        columns=['teamname']).rename(columns={'team_id': 'team2_id'})

    last_results = last_results.sort_values(by=['date'], ascending=False)
    last_results = last_results.drop_duplicates('teamname', keep='first')

    last_results.drop(
        columns=['gameid', 'date', 'patch', 'participantid', 'bot_playername', 'jng_playername', 'mid_playername',
                 'sup_playername', 'top_playername'], inplace=True)

    stats_df_team1 = last_results.add_suffix('_team1')
    data = predict.merge(stats_df_team1, how='left', left_on='team_1', right_on='teamname_team1')

    stats_df_team2 = last_results.add_suffix('_team2')
    data = data.merge(stats_df_team2, how='left', left_on='team_2', right_on='teamname_team2')

    data.drop(columns=['date', 'team_1', 'team1_id', 'team_2', 'team2_id', 'teamname_team1', 'teamname_team2',
                       'team_id_team1', 'team_id_team2'], inplace=True)

    data.to_csv('Predictions/ready.csv', index=False)
    print("prepare_data_to_forecast.py COMPLETED - Predictions/ready.csv")
