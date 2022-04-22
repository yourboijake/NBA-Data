import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='filename for raw data')
parser.add_argument('--w', type=int, help='number of weeks to aggregate trailing data')
parser.add_argument('--d', type=bool, help='boolean to determine whether to include a longer time frame, in addition to ')
args = parser.parse_args()

if args.w:
    window_size = args.w
else:
    window_size = 5

def get_extra_feats(filename):
    tdf = pd.read_csv(filename)
    tdf['W/L_binary'] = tdf['W/L_home'].map({'W': 0, 'L': 1})
    tdf.rename(columns={'MATCHUP_away': 'MATCHUP'}, inplace=True)

    #compute number of possessions
    tdf['POSS_home'] = 0.96 * (tdf['FGA_home'] - tdf['OREB_home'] - \
                                tdf['TOV_home'] + 0.475 * tdf['FTA_home'])

    tdf['POSS_away'] = 0.96 * (tdf['FGA_away'] - tdf['OREB_away'] - \
                                tdf['TOV_away'] + 0.475 * tdf['FTA_away'])

    #compute offensive and defensive efficiency
    tdf['OE_home'] = tdf['PTS_home'] * 100 / tdf['POSS_home']
    tdf['DE_home'] = tdf['PTS_away'] * 100 / tdf['POSS_home']
    tdf['OE_away'] = tdf['PTS_away'] * 100 / tdf['POSS_away']
    tdf['DE_away'] = tdf['PTS_home'] * 100 / tdf['POSS_away']

    #compute competitor-adjusted offensive and defensive efficiency
    tdf['AdjOE_home'] = tdf['OE_home'] / tdf['OE_away']
    tdf['AdjDE_home'] = tdf['DE_home'] / tdf['DE_away']
    tdf['AdjOE_away'] = tdf['OE_away'] / tdf['OE_home']
    tdf['AdjDE_away'] = tdf['DE_away'] / tdf['DE_home']

    #compute effective field goal %
    tdf['EFG%_home'] = (tdf['FGM_home'] + 0.5 * tdf['3PM_home'])/tdf['FGA_home']
    tdf['EFG%_away'] = (tdf['FGM_away'] + 0.5 * tdf['3PM_away'])/tdf['FGA_away']

    #compute turnover %
    tdf['TOV%_home'] = tdf['TOV_home']/tdf['POSS_home']
    tdf['TOV%_away'] = tdf['TOV_away']/tdf['POSS_away']

    #compute offensive rebound percentage
    tdf['OREB%_home'] = tdf['OREB_home'] / (tdf['OREB_home'] + tdf['DREB_away'])
    tdf['OREB%_away'] = tdf['OREB_away'] / (tdf['OREB_away'] + tdf['DREB_home'])

    #compute free throw rate
    tdf['FTR_home'] = tdf['FTA_home'] / tdf['FGA_home']
    tdf['FTR_away'] = tdf['FTA_away'] / tdf['FGA_away']

    #compute pythagorean expectation
    #pythag expectation = (Points Scored)^16.5/[Points Scored)^16.5 + (Points Allowed)^16.5)]
    tdf['PYTHAG_home'] = np.power(tdf['PTS_home'], 16.5) / (np.power(tdf['PTS_home'], 16.5) + \
                                                           np.power(tdf['PTS_away'], 16.5))
    tdf['PYTHAG_away'] = np.power(tdf['PTS_away'], 16.5) / (np.power(tdf['PTS_away'], 16.5) + \
                                                           np.power(tdf['PTS_home'], 16.5))

    #compute free-throw differential
    tdf['FTDIFF_home'] = tdf['FTA_home'] / tdf['FTA_away']
    tdf['FTDIFF_away'] = tdf['FTA_away'] / tdf['FTA_home']

    #compute assist to turnover ratio
    tdf['AST/TO_home'] = tdf['AST_home'] / tdf['TOV_home']
    tdf['AST/TO_away'] = tdf['AST_away'] / tdf['TOV_away']

    #compute assisted field goal %
    tdf['AST/FGM_home'] = tdf['AST_home'] / tdf['FGM_home']
    tdf['AST/FGM_away'] = tdf['AST_away'] / tdf['FGM_away']

    return tdf

def get_trailing_data(df, team_name, window_size):
    home_cols = ['TEAM_home', 'TEAM_away', 'GAME_DATE_home', 'W/L_binary', 'MIN_home',
                'PTS_home', 'FGM_home', 'FGA_home', 'FG%_home', '3PM_home', '3PA_home',
                '3P%_home', 'FTM_home', 'FTA_home', 'FT%_home', 'OREB_home', 'DREB_home',
                'REB_home', 'AST_home', 'STL_home', 'BLK_home', 'TOV_home', 'PF_home',
                '+/-_home', 'POSS_home', 'OE_home', 'DE_home', 'EFG%_home', 'AdjOE_home',
                'AdjDE_home', 'OREB%_home', 'FTR_home', 'PYTHAG_home', 'FTDIFF_home',
                'AST/TO_home', 'AST/FGM_home', 'TOV%_home', 'MATCHUP']

    away_cols = ['TEAM_away', 'TEAM_home', 'GAME_DATE_home', 'W/L_binary', 'MIN_away',
                'PTS_away', 'FGM_away', 'FGA_away', 'FG%_away', '3PM_away', '3PA_away',
                '3P%_away', 'FTM_away', 'FTA_away', 'FT%_away', 'OREB_away', 'DREB_away',
                'REB_away', 'AST_away', 'STL_away', 'BLK_away', 'TOV_away', 'PF_away',
                '+/-_away', 'POSS_away', 'OE_away', 'DE_away', 'EFG%_away', 'AdjOE_away',
                'AdjDE_away', 'OREB%_away', 'FTR_away', 'PYTHAG_away', 'FTDIFF_away',
                'AST/TO_away', 'AST/FGM_away', 'TOV%_away', 'MATCHUP']

    home_games = df.loc[df['TEAM_home'] == team_name, home_cols]
    away_games = df.loc[df['TEAM_away'] == team_name, away_cols]

    #fix away_games columns to match up with home_games
    away_games['W/L_binary'] = away_games['W/L_binary'].map({0:1, 1:0})
    away_rename_dict = dict(zip(away_cols, [i.replace('away', 'home') for i in away_cols]))
    away_rename_dict['TEAM_home'] = 'TEAM_away'
    away_games.rename(columns=away_rename_dict, inplace=True)

    #append dataframe to end of home_games
    home_games['TEAM_is_away'] = 0
    away_games['TEAM_is_away'] = 1
    home_games = home_games.append(away_games)

    #sort ascending to make oldest games nan when getting rolling data
    home_games['GAME_DATE_home'] = pd.to_datetime(home_games['GAME_DATE_home'])
    home_games.sort_values(by='GAME_DATE_home', inplace=True)

    #include column on match outcome that isn't rolling
    home_games['MATCHUP_outcome'] = home_games['W/L_binary']

    rolling_cols = ['GAME_DATE_home']
    for col in home_cols:
        if 'MATCHUP' in col or col == 'GAME_DATE_home' or 'TEAM' in col: continue
        rolling_cols.append(col.replace('home', 'rolling')+ '_' + str(window_size))
        home_games[col.replace('home', 'rolling') + '_' + str(window_size)] \
        = home_games[col].shift().rolling(window=window_size).mean()

    rolling_cols = ['TEAM_home', 'TEAM_away', 'TEAM_is_away',
                    'MATCHUP', 'MATCHUP_outcome'] + rolling_cols

    #print(away_games['W/L_binary'].value_counts())
    #print(home_games.loc[~(home_games['MATCHUP_outcome'].isin([0, 1]))].head())

    return home_games[rolling_cols].sort_values(by='GAME_DATE_home', ascending=False).dropna()

#generate data for all the teams
def generate_all_data(tdf, window_size):
    #get the rolling data for all the teams
    team_dfs = []
    for team in tdf['TEAM_home'].unique():
        team_dfs.append(get_trailing_data(tdf, team, window_size))

    rolling_df = pd.concat(team_dfs)
    rolling_df.dropna(inplace=True)
    rolling_df2 = rolling_df.copy()

    #add columns corresponding to matching team_home/team_away
    final_df = rolling_df.merge(rolling_df2, how='inner', left_on=['TEAM_away', 'GAME_DATE_home'],
                                right_on=['TEAM_home', 'GAME_DATE_home'])
    #drop duplicate rows
    final_df['MATCHUP_sorted'] = final_df['MATCHUP_x'].apply(lambda x : ''.join(sorted(x)))
    final_df.sort_values(by='TEAM_is_away_x', inplace=True)
    final_df.drop_duplicates(subset=['MATCHUP_sorted', 'GAME_DATE_home'], inplace=True)

    #export de-dupped data to csv
    rename_dict = dict(zip(final_df.columns, [i.replace('_x', '_home').replace('_y', '_away') for i in final_df.columns]))
    final_df.rename(columns=rename_dict, inplace=True)
    final_df.rename(columns={'TEAM_home_home': 'TEAM_home',
                             'TEAM_away_home': 'TEAM_away',
                            'MATCHUP_outcome_home': 'MATCHUP_outcome'}, inplace=True)

    #identify columns to drop
    drop_cols = ['TEAM_home_away', 'TEAM_away_away',
                 'MATCHUP_away', 'MATCHUP_sorted',
                 'MATCHUP_outcome_away', 'TEAM_is_away_home', 'TEAM_is_away_away']
    return final_df.drop(columns=drop_cols).sort_values(by='GAME_DATE_home', ascending=False)

def main():
    raw_df = get_extra_feats(args.f)
    feat_df = generate_all_data(raw_df, window_size)

    type_dict = dict(zip(feat_df.columns, feat_df.dtypes.values.astype(str)))

    #add in transformed variables: square, square root, and logarithm
    for col in feat_df.columns:
        if type_dict[col] != 'int64' and type_dict[col] != 'float64': continue
        #add square column
        feat_df[col+'_sq'] = feat_df[col] * feat_df[col]

        #add square root
        feat_df[col+'_sqrt'] = np.sqrt(np.clip(feat_df[col], 0.000001, None))

        #add logarithm
        feat_df[col+'_sqrt'] = np.log(np.clip(feat_df[col], 0.000001, None))

    #export to csv
    feat_df.to_csv(f'team_data_rolling_{window_size}yr.csv', index=False)

main()
