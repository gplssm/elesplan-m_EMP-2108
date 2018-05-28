from elesplan_m_EMP_E_2018.model import ElesplanMOneYearModel
from oemof import solph


def elesplan_m(data_path, year, scenario):
    model_2020 = ElesplanMOneYearModel(year=year,
                            debug=True,
                            data_path=data_path)

    # Load data
    model_2020.load_csv(data_path, year, scenario)

    # Create energy system graph
    es = solph.EnergySystem(
        timeindex=model_2020.table_collection['demand'].index)
    model_2020.add_nodes2solph(es=es)

    # Create model & solve
    model_2020.create_model()
    model_2020.solve()


if __name__ == '__main__':

    data_path = '/home/guido/rli_local/elesplan_m_EMP_E_2018_data/data/csv/' \
                'EMP-E_2018-3Regions-2H'

    year = 2020
    scenario = 'EMP-E_2018-3Regions-2H'

    elesplan_m(data_path, year, scenario)
