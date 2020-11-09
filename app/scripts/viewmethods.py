
from app.variables import *
from app.scripts.biotable import *

import pandas as pd
import numpy as np


def generate_anitbiogram(organisms, colltypes, sites, ams, hosp, startdate, enddate):
    df = getdatatable()
    df['date'] = pd.to_datetime(df['date'])
    fields = ['test_id', 'department', 'sample_type', 'organism'] + ams
    df = df[df.organism.isin(organisms) & df.sample_type.isin(colltypes) & df.department.isin(sites)
            & df.hospital.isin(hosp) & ((df['date'] > startdate) & (df['date'] <= enddate))][fields]
    tdf = df.groupby(['organism'])
    dfr = df.replace(-1, 0)
    dfr = dfr.replace(2, 0)
    dfr = dfr.groupby(['organism']).sum()
    dfr.insert(0, ' All Antimicrobials', dfr.sum(axis=1, skipna=True))
    dfr.loc[' All Organisms'] = dfr.sum(axis=0, skipna=True)
    dfr = dfr.sort_index()
    dfi = df.replace(-1, 0)
    dfi = dfi.replace(1, 0)
    dfi = dfi.replace(2, 1)
    dfi = dfi.groupby(['organism']).sum()
    dfi.insert(0, ' All Antimicrobials', dfi.sum(axis=1, skipna=True))
    dfi.loc[' All Organisms'] = dfi.sum(axis=0, skipna=True)
    dfi = dfi.sort_index()
    dfs = df.replace(0, 3)
    dfs = dfs.replace(-1, 0)
    dfs = dfs.replace(2, 0)
    dfs = dfs.replace(1, 0)
    dfs = dfs.replace(3, 1)
    dfs = dfs.groupby(['organism']).sum()
    dfs.insert(0, ' All Antimicrobials', dfs.sum(axis=1, skipna=True))
    dfs.loc[' All Organisms'] = dfs.sum(axis=0, skipna=True)
    dfs = dfs.sort_index()
    # print(dfs)
    dff = dfs / (dfi + dfr + dfs) * 100
    dff = dff.replace(np.nan, 'null')
    return (dff)


def generate_graph(organisms, ams, hosp):
    df = getdatatable()
    df['date'] = pd.to_datetime(df['date'])
    print(organisms)
    print(ams)
    fields = ['date'] + ams
    print(fields)
    df = df[df.organism.isin(organisms) & df.hospital.isin(hosp)][fields]
    df.index = df.date
    dfr = df.replace(-1, 0)
    dfr = dfr.replace(2, 0)
    dfr = dfr.resample('M').sum()
    dfi = df.replace(-1, 0)
    dfi = dfi.replace(1, 0)
    dfi = dfi.replace(2, 1)
    dfi = dfi.resample('M').sum()
    dfs = df.replace(0, 3)
    dfs = dfs.replace(-1, 0)
    dfs = dfs.replace(2, 0)
    dfs = dfs.replace(1, 0)
    dfs = dfs.replace(3, 1)
    dfs = dfs.resample('M').sum()
    dff = dfs / (dfi + dfr + dfs) * 100
    dff = dff.replace(np.nan, '')
    dff = dff
    # tdf = tdf.apply(lambda _tdf: _tdf.sort_values(by=['date']))
    # df['date'] = str(df['date'])
    print(dff)
    return dff


def get_rsi(organisms, colltypes, sites, ams, hosp, startdate, enddate):
    df = getdatatable()
    df['date'] = pd.to_datetime(df['date']).dt.date
    print(type(startdate))
    fields = ['test_id', 'department', 'sample_type', 'organism'] + ams
    df = df[df.organism.isin(organisms) & df.sample_type.isin(colltypes) & df.department.isin(sites) & df.hospital.isin(hosp) & (
            (df['date'] > startdate) & (df['date'] <= enddate))][fields]
    tdf = df.groupby(['organism'])
    dfr = df.replace(-1, 0)
    dfr = dfr.replace(2, 0)
    dfr = dfr.groupby(['organism']).sum()
    # dfr.insert(0, ' All Antimicrobials', dfr.sum(axis=1,skipna=True))
    dfr.loc[' All Organisms'] = dfr.sum(axis=0, skipna=True)
    dfr = dfr.sort_index()
    dfi = df.replace(-1, 0)
    dfi = dfi.replace(1, 0)
    dfi = dfi.replace(2, 1)
    dfi = dfi.groupby(['organism']).sum()
    # dfi.insert(0, ' All Antimicrobials', dfi.sum(axis=1,skipna=True))
    dfi.loc[' All Organisms'] = dfi.sum(axis=0, skipna=True)
    dfi = dfi.sort_index()
    dfs = df.replace(0, 3)
    dfs = dfs.replace(-1, 0)
    dfs = dfs.replace(2, 0)
    dfs = dfs.replace(1, 0)
    dfs = dfs.replace(3, 1)
    dfs = dfs.groupby(['organism']).sum()
    # dfs.insert(0, ' All Antimicrobials', dfs.sum(axis=1,skipna=True))
    dfs.loc[' All Organisms'] = dfs.sum(axis=0, skipna=True)
    dfs = dfs.sort_index()

    return dfr, dfs, dfi


def getcdfat(cdf, a, b):
    try:
        return cdf.at[a, b]
    except KeyError:
        return 0


def rcount(series):
    print(series)
    return (series.values == 1).sum()
