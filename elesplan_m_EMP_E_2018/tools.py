import os
import pandas as pd


def load_csv(filepath, suffix=None, sheet_cfg=None, year=None):

    if suffix:
        FILENAME = 'elesplan-m_data_{}'.format(suffix)
    else:
        FILENAME = 'elesplan-m_data'

    # load power plant parameters
    transformer_params = pd.read_csv(
        os.path.join(filepath, FILENAME + '_transformer_parameters.csv'),
        index_col=['year', 'technology'])
    transformer_capacity = pd.read_csv(
        os.path.join(filepath,
                     FILENAME + '_initial_capacity_2020.csv'))
    max_capacity = pd.read_csv(
        os.path.join(filepath,
                     FILENAME + '_max_capacity.csv'),
        index_col=['region', 'technology'])
    feedin = pd.read_csv(
        os.path.join(filepath, FILENAME + '_feedin.csv'),
        index_col=['region', 'date'],
        parse_dates=['date'])
    
    # load fuel parameters
    fuel_params = pd.read_csv(
        os.path.join(filepath, FILENAME + '_fuel_parameters.csv'),
        index_col=['year', 'fuel'])

    # read demand
    demand = pd.read_csv(
        os.path.join(filepath, FILENAME + '_demand.csv'),
        index_col=['date'],
        parse_dates=['date'])

    # read transmission data
    transmission_params = pd.read_csv(
        os.path.join(filepath, FILENAME + '_transmission_parameters.csv'))
    transmission_length = pd.read_csv(
        os.path.join(filepath, FILENAME + '_transmission_length.csv'))
    transmission_capacity = pd.read_csv(
        os.path.join(filepath, FILENAME + '_initial_transmission_capacity_2020.csv'))



    if year:
        transformer_params = transformer_params.loc[year]
        fuel_params = fuel_params.loc[year]
        demand = demand.loc[demand.index.year == year]

    return {
        'power_plants': transformer_params,
        'transformer_capacity': transformer_capacity,
        'max_capacity': max_capacity,
        'feedin': feedin,
        'demand': demand,
        'fuel': fuel_params,
        'transmission_params': transmission_params,
        'transmission_length': transmission_length,
        'transmission_capacity': transmission_capacity
    }