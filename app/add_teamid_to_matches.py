import sys
import pandas as pd


def add_teamid_to_matches():
    teams_df_dtype = {
        'team_id': 'int64',
        'teamname': 'object'
    }

    # Load the CSV files
    matches_df = pd.read_csv('Data/matches.csv')
    teams_df = pd.read_csv('Data/teams.csv', dtype=teams_df_dtype)

    # Merge team data into matches data

    merged_df = matches_df.merge(teams_df, how='left', left_on='team1', right_on='teamname', suffixes=('', '_team1'))
    merged_df = merged_df.merge(teams_df, how='left', left_on='team2', right_on='teamname',
                                suffixes=('_team1', '_team2'))

    # Rename the columns to make it clear which team each ID belongs to
    merged_df.rename(columns={'team_id_team1': 'team1_id', 'teamname_team1': 'team1_teamname',
                              'team_id_team2': 'team2_id', 'teamname_team2': 'team2_teamname'
                              }, inplace=True)

    merged_df = merged_df.dropna(subset=['team1_id'])
    merged_df = merged_df.dropna(subset=['team2_id'])

    merged_df['team1_id'] = merged_df['team1_id'].astype('int64')
    merged_df['team2_id'] = merged_df['team2_id'].astype('int64')

    # Drop redundant team_name columns from the merged dataframe
    merged_df.drop(columns=['team1', 'team2'], inplace=True)

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv('Data/merged_matches_with_team_ids.csv', index=False)

    print("add_teamid_to_matches.py COMPLETED - Data/merged_matches_with_team_ids.csv")
