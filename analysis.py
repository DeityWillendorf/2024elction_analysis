import pandas as pd
pd.options.mode.chained_assignment = None
import os

PAST_PRESIDENTIAL_CSV_FILEPATH = '1976-2020-president.csv' #https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/42MVDX
PAST_SENATE_CSV_FILEPATH = '1976-2020-senate.csv' #https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/PEJ5QU
PAST_HOUSE_CSV_FILEPATH = '1976-2022-house.csv' #https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IG0UN2
PRESIDENTIAL_CSV_FILEPATH = 'presidential_2024.csv' #https://www.bbc.co.uk/news/articles/cvglg3klrpzo
SENATE_CSV_FILEPATH = 'senate_2024.csv' #https://www.bbc.co.uk/news/articles/cvglg3klrpzo
GOVERNER_CSV_FILEPATH = 'governer_2024.csv' #https://www.bbc.co.uk/news/articles/cvglg3klrpzo
ELIGIBLE_VOTERS_2020_CSV_FILEPATH = 'voter_registeration_2020.csv' #https://www.census.gov/data/tables/time-series/demo/voting-and-registration/p20-585.html table 4a
TURNOUT_2024_CSV_FILEPATH = 'Turnout_2024G_v0.3.csv' #https://election.lab.ufl.edu/2024-general-election-turnout/
TURNOUT_2020_CSV_FILEPATH = 'Turnout_2020G_v1.2.csv' #https://election.lab.ufl.edu/voter-turnout/2020-general-election-turnout/
TURNOUT_2016_CSV_FILEPATH = 'Turnout_2016G_v1.0.csv' #https://election.lab.ufl.edu/voter-turnout/2016-general-election-turnout-rates/
TURNOUT_2012_CSV_FILEPATH = 'Turnout_2012G_v1.0.csv' #https://election.lab.ufl.edu/voter-turnout/2012-general-election-turnout-rates/


def read_mit_database(path, year, state, party):
    df = pd.read_csv(path)
    #print(df.to_string())
    res = df.loc[(df['year'].isin(year)) & (df['state'].isin(state)) &
                 (df['party_simplified'].isin(party)) &
                 (df['candidate'].notnull())]
    df.sort_values('state')
    #print(res.to_string())
    return res


def find_all_state_pres(year, states, parties):
    demrep1620 = read_mit_database(PAST_PRESIDENTIAL_CSV_FILEPATH, year,
                                   states, parties)
    #print(demrep1620.to_string())
    return demrep1620


def find_all_senate(year, states, parties):
    demrep1620 = read_mit_database(PAST_SENATE_CSV_FILEPATH, year, states,
                                   parties)
    #print(demrep1620.to_string())
    return demrep1620


def find_all_house(year, states, parties):
    df = pd.read_csv(PAST_HOUSE_CSV_FILEPATH)
    df.sort_values('state')
    demrep1620 = df.loc[(df['year'].isin(year)) & (df['state'].isin(states)) &
                        (df['party'].isin(parties)) &
                        (df['candidate'].notnull())]
    #print(demrep1620.to_string())
    return demrep1620


def find_all_eligible_voter_2020(states):
    df = pd.read_csv(ELIGIBLE_VOTERS_2020_CSV_FILEPATH, thousands=',')
    df.sort_values('STATE')
    res = df.loc[(df['STATE'].isin(states))]
    #print(res.to_string())
    return res


def find_turnout_per_year(yr, states):
    path = ''
    if yr == 2012:
        path = TURNOUT_2012_CSV_FILEPATH
    if yr == 2016:
        path = TURNOUT_2016_CSV_FILEPATH
    if yr == 2020:
        path = TURNOUT_2020_CSV_FILEPATH
    if yr == 2024:
        path = TURNOUT_2024_CSV_FILEPATH
    turn = pd.read_csv(path, skipinitialspace=True, thousands=',')
    turn.sort_values('STATE')
    turn['STATE']=turn['STATE'].str.replace("*","")
    turn['YEAR'] = yr
    res = turn.loc[(turn['STATE'].str.upper().isin(states))]
    #print(res.to_string())
    return res


def find_all_turnout(year, states):
    dfs = []
    for yr in year:
        if yr >= 2012:
            turn_yr = find_turnout_per_year(yr, states)
            dfs.append(turn_yr)
    res = pd.concat(dfs).reset_index(drop=True)
    #print(res.to_string())
    return res


def find_pres_2024(states):
    df = pd.read_csv(PRESIDENTIAL_CSV_FILEPATH,
                     skipinitialspace=True,
                     thousands=',')
    #print(df.to_string())
    party = [
        'Democrat', 'Republican (incumbent)', 'Democrat (incumbent)',
        'Republican'
    ]
    res = df.loc[(df['State'].str.upper().isin(states))
                 & (df['Party'].isin(party))]
    df.sort_values('State')
    #print(res.to_string())
    return res


def find_senate_2024(states):
    df = pd.read_csv(SENATE_CSV_FILEPATH, skipinitialspace=True, thousands=',')
    #print(df.to_string())
    party = ['Democratic', 'Republican']
    res = df.loc[(df['State'].str.upper().isin(states))
                 & (df['Party'].isin(party))]
    df.sort_values('State')
    #print(res.to_string())
    return res


def find_governer_2024(states):
    df = pd.read_csv(GOVERNER_CSV_FILEPATH,
                     skipinitialspace=True,
                     thousands=',')
    #print(df.to_string())
    party = [
        'Democratic', 'Republican (incumbent)', 'Democratic (incumbent)',
        'Republican'
    ]
    res = df.loc[(df['State'].str.upper().isin(states))
                 & (df['Party'].isin(party))]
    df.sort_values('State')
    #print(res.to_string())
    return res


def form_table(presidential24, senate24, past_pres, past_senate, year,
               bbc_party_list, party_name_mit, party_name_sen):
    dem_24 = presidential24.loc[presidential24['Party'].isin(bbc_party_list)][[
        'State', 'Votes', 'Expected votes counted (%)'
    ]]
    dem_24['State'] = dem_24['State'].str.upper()
    dem_tb = pd.DataFrame()
    dem_tb = pd.concat([dem_tb, dem_24]).reset_index(drop=True)
    dem_tb.rename(columns={
        'Votes':
        '2024 President',
        'Expected votes counted (%)':
        '2024 Pres Expected votes counted (%)'
    },
                  inplace=True)
    #print(dem_24.to_string())
    for y in year:
        pres_y = past_pres.loc[(past_pres['party_simplified'] == party_name_mit)
                               & (past_pres['year'] == y)][[
                                   'state', 'candidatevotes', 'totalvotes'
                               ]].reset_index(drop=True)
        pres_y.rename(columns={
            'candidatevotes': str(y) + ' president',
            'state': 'State',
            'totalvotes': str(y) + ' pres totalvotes'
        },
                      inplace=True)
        #print(pres_y.to_string())
        dem_tb = pd.merge(dem_tb, pres_y, on='State')
    #print(dem_tb.to_string())
    sen_24 = senate24.loc[senate24['Party'] == party_name_sen][[
        'State', 'Votes', 'Expected votes counted (%)'
    ]].reset_index(drop=True)
    sen_24['State'] = sen_24['State'].str.upper()
    sen_24.rename(columns={
        'Votes':
        '2024 Senate',
        'Expected votes counted (%)':
        '2024 Senate Expected votes counted (%)'
    },
                  inplace=True)
    dem_tb = pd.merge(dem_tb, sen_24, on='State', how='outer')
    for y in year:
        sen_y = past_senate.loc[
            (past_senate['party_simplified'] == party_name_mit)
            & (past_senate['year'] == y)][[
                'state', 'candidatevotes', 'totalvotes'
            ]].reset_index(drop=True)
        sen_y = sen_y.groupby(sen_y['state']).aggregate({
            'candidatevotes': 'sum',
            'totalvotes': 'first'
        }).reset_index()
        sen_y.rename(columns={
            'candidatevotes': str(y) + ' senate',
            'state': 'State',
            'totalvotes': str(y) + ' sen totalvotes'
        },
                     inplace=True)
        #print(sen_y.to_string())
        dem_tb = pd.merge(dem_tb, sen_y, on='State', how='outer')
    return dem_tb


def form_turnout(year, turnout):
    df = turnout.loc[turnout['YEAR'] == 2024][['STATE']]
    df.rename(columns={'STATE': 'State'}, inplace=True)
    #print(df.to_string())
    for y in year:
        tr_y = turnout.loc[turnout['YEAR'] == y][[
            'STATE', 'TOTAL_BALLOTS_COUNTED', 'VEP', 'VEP_TURNOUT_RATE'
        ]].reset_index(drop=True)
        tr_y.rename(columns={
            'STATE': 'State',
            'TOTAL_BALLOTS_COUNTED': str(y) + ' TOTAL_BALLOTS_COUNTED',
            'VEP': str(y) + ' VEP',
            'VEP_TURNOUT_RATE': str(y) + ' VEP_TURNOUT_RATE'
        },
                    inplace=True)
        df = pd.merge(df, tr_y, on='State', how='outer')
    #print(df.to_string())
    return df


def sum_table(dem_tb, rep_tb, years, turnout, reg2020):
    header1 = ['State', '2024 President', '2024 Senate']
    #print(header)
    dem = dem_tb[header1].set_index('State')
    rep = rep_tb[header1].set_index('State')
    #print(dem.to_string())
    #print(rep.to_string())
    sum_24 = dem + rep
    sum_24 = sum_24.drop_duplicates()
    sum_24 = pd.merge(sum_24,
                      dem_tb[['State',
                              '2024 Pres Expected votes counted (%)']],
                      on='State')
    sum_24['2024 pres expected'] = sum_24['2024 President'] / (
        sum_24['2024 Pres Expected votes counted (%)'].str.rstrip('%').astype(
            'float') / 100.0)
    print(sum_24.to_string())
    header2 = ['State', '2024 Senate Expected votes counted (%)']
    for y in years:
        header2.append(str(y) + ' pres totalvotes')
    for y in years:
        header2.append(str(y) + ' sen totalvotes')
    all_sum = pd.merge(sum_24, dem_tb[header2], on='State')

    yr = [2024, 2020, 2016, 2012]
    tur = form_turnout(yr, turnout)
    all_sum = pd.merge(all_sum, tur, on='State', how='outer')

    reg20 = reg2020[[
        'STATE', 'total_citizen_population', 'Total registered', 'Total voted'
    ]]
    reg20['total_citizen_population'] = reg20[
        'total_citizen_population'].apply(lambda x: x * 1000)
    reg20.rename(columns={
        'STATE': 'State',
        'total_citizen_population': '2020 total_citizen_population',
        'Total registered': '2020 Total registered',
        'Total voted': '2020 Total voted'
    },
                 inplace=True)
    all_sum = pd.merge(all_sum, reg20, on='State', how='outer')
    all_sum=all_sum.drop_duplicates()
    #print(all_sum.to_string())
    return all_sum

def extract_states():
    df = pd.read_csv(TURNOUT_2024_CSV_FILEPATH)
    lstate = df['STATE'].tolist()
    #print(lstate)
    return lstate

def extract_blue_24_states():
    df = pd.read_csv(PRESIDENTIAL_CSV_FILEPATH)
    lstate = df.loc[df['Party']=='Democrat (incumbent)']['State'].str.upper().tolist()
    #print(lstate)
    return lstate

def extract_red_24_states():
    df = pd.read_csv(PRESIDENTIAL_CSV_FILEPATH)
    lstate = df.loc[df['Party']=='Republican (incumbent)']['State'].str.upper().tolist()
    #print(lstate)
    return lstate

def find_presidential24_per_state_sum(states):
    df = pd.read_csv(PRESIDENTIAL_CSV_FILEPATH,
                     skipinitialspace=True,
                     thousands=',')
    #print(df.to_string())
    df.sort_values('State')
    res = df.loc[(df['State'].str.upper().isin(states))]
    res = res[['State','Votes']]
    sum = res.groupby('State').sum()
    print(sum.to_string())

if __name__ == "__main__":

    year = [2020, 2016, 2012, 2008, 2004]
    states = [
        'ARIZONA', 'FLORIDA', 'GEORGIA', 'IOWA', 'MICHIGAN', 'NEVADA', 'NORTH CAROLINA',
        'PENNSYLVANIA', 'TEXAS', 'WISCONSIN'
    ] # battle ground states + FL + TX
    #states = extract_states() #all states
    #states = extract_blue_24_states()
    #states = extract_red_24_states()
    parties = ['DEMOCRAT', 'REPUBLICAN']
    past_pres = find_all_state_pres(year, states, parties)
    past_senate = find_all_senate(year, states, parties)
    past_house = find_all_house(year, states, parties)

    registered2020 = find_all_eligible_voter_2020(states)
    turnout = find_all_turnout([2024, 2020, 2016, 2012, 2008, 2004], states)

    presidential24 = find_pres_2024(states)
    senate24 = find_senate_2024(states)
    governor24 = find_governer_2024(states)

    find_presidential24_per_state_sum(states)

    bbc_party_dem = [
        'Democrat', 'Democrat (incumbent)', 'Democratic',
        'Democratic (incumbent)'
    ]
    #print(past_senate.to_string())
    dem_tb = form_table(presidential24, senate24, past_pres, past_senate, year,
                        bbc_party_dem, 'DEMOCRAT', 'Democratic')
    #print(dem_tb.to_string())
    bbc_party_rep = ['Republican (incumbent)', 'Republican']
    rep_tb = form_table(presidential24, senate24, past_pres, past_senate, year,
                        bbc_party_rep, 'REPUBLICAN', 'Republican')

    sum_tb = sum_table(dem_tb=dem_tb,
                       rep_tb=rep_tb,
                       years=year,
                       turnout=turnout,
                       reg2020=registered2020)
    pd.concat([
        pd.DataFrame({'State': ['dems']}), dem_tb,
        pd.DataFrame({'State': ['rep']}), rep_tb,
        pd.DataFrame({'State': ['sum']}), sum_tb
    ]).to_csv('all.csv', encoding='utf-8', index=False)
