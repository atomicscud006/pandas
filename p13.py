import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')
api_key = "Cxe41MDVyJhXQYGuVGx7"

def mortgage_30y():
    df = quandl.get("FMAC/MORTG", trim_start = '1975-01-01' ,authtoken=api_key)
    df['Value'] = (df['Value'] - df['Value'][0]) / df['Value'][0] * 100.0
    df = df.resample("M").mean()
    df.columns = ['M30']
    df.to_pickle('m30.pickle')

def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][0][1:]


def grab_initial_state_dat():
    states = state_list()
    main_df = pd.DataFrame()
    for abbv in states:
        query = ("FMAC/HPI_" + str(abbv))
        df = quandl.get(query, authtoken=api_key)
        df.columns = [str(abbv)]
        df[abbv] = (df[abbv] - df[abbv][0]) / df[abbv][0] * 100.0

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)


    pickle_out = open('fiddy_states.pickle', 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()


def HPI_benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df['Value'] = (df['Value'] - df['Value'][0]) / df['Value'][0] * 100.0
    return df

m30 = pd.read_pickle('m30.pickle')
HPI_data = pd.read_pickle('fiddy_states.pickle')
HPI_bench = HPI_benchmark()

state_HPI_M30 = HPI_data.join(m30)

print(state_HPI_M30.corr()['M30'].describe())


