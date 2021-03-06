from elesplan_m_EMP_E_2018.model import ElesplanMOneYearModel
from oemof import solph
import argparse, sys
import json
import os


def elesplan_m(scenario_path, year, scenario, solver='gurobi',
               solver_options=None,debug=False):

    data_path = os.path.join(scenario_path, 'data')

    # Instantiate model
    model_2020 = ElesplanMOneYearModel(
        year=year,
        debug=debug,
        data_path=data_path)

    # Load data
    model_2020.load_csv(data_path, year, scenario)

    # Create energy system
    es = solph.EnergySystem(
        timeindex=model_2020.table_collection['demand'].index)

    # Create model & solve
    model_2020.create_model(es)
    model_2020.solve(solver=solver, solver_options=solver_options)

    # Save results
    results_path = os.path.join(scenario_path, 'results', 'raw')
    if not os.path.isdir(results_path):
        os.makedirs(results_path)
    model_2020.dump_es(
        os.path.join(results_path, 'results_{}.es'.format(scenario)))


def elesplan_m_cmd():

    parser = argparse.ArgumentParser(
        description="Run elesplan-m for EMP 2018." + \
                    "Available scenarios are listed in "
                    "\n <link-to-table-in-repo-wiki>",
        # epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('data_path',
                        type=str,
                        help='Path to folder containing scenario files.')

    args = parser.parse_args(sys.argv[1:])

    # read config
    config = json.load(open(os.path.join(args.data_path, 'config.cfg')))

    elesplan_m(args.data_path, config['years'][0], config['scenario'],
               solver=config['solver'],
               solver_options=config['solver_options'])


if __name__ == '__main__':
    pass