import reegis_tools.scenario_tools
import oemof.solph as solph
from oemof.tools import economics
import elesplan_m_EMP_E_2018.tools as tools
import logging
from oemof import outputlib
import os


CONV_PP = ['Coal', 'CCGT', 'OCGT', 'Nuclear']


class ElesplanMOneYearModel(reegis_tools.scenario_tools.Scenario):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_path = kwargs.get('data_path', '')

    def create_nodes(self, nodes=None):
        # Create  a special dictionary that will raise an error if a key is
        # updated. This avoids the
        nodes = reegis_tools.scenario_tools.NodeDict()

        # Create global fuel sources
        ng_bus_label = "bus_natural_gas"
        nodes[ng_bus_label] = solph.Bus(label=ng_bus_label)
        ng_cs_label = 'source_natural_gas_'
        nodes[ng_cs_label] = solph.Source(
            label=ng_cs_label, outputs={nodes[ng_bus_label]: solph.Flow(
                variable_costs=self.table_collection['fuel'].loc['Natural gas', 'cost'],
                emission=self.table_collection['fuel'].loc['Natural gas', 'cost'])})
        
        uranium_bus_label = "bus_uranium"
        nodes[uranium_bus_label] = solph.Bus(label=uranium_bus_label)
        uranium_cs_label = 'source_uranium_'
        nodes[uranium_cs_label] = solph.Source(
            label=uranium_cs_label, outputs={nodes[uranium_bus_label]: solph.Flow(
                variable_costs=self.table_collection['fuel'].loc[
                    'Uranium', 'cost'],
                emission=self.table_collection['fuel'].loc[
                    'Uranium', 'cost'])})

        coal_bus_label = "bus_coal_{}"
        nodes[coal_bus_label] = solph.Bus(label=coal_bus_label)
        coal_cs_label = 'source_coal_'
        nodes[coal_cs_label] = solph.Source(
            label=coal_cs_label,
            outputs={nodes[coal_bus_label]: solph.Flow(
                variable_costs=self.table_collection['fuel'].loc[
                    'Coal', 'cost'],
                emission=self.table_collection['fuel'].loc[
                    'Coal', 'co2_emissions'])})

        capacity = self.table_collection['transformer_capacity'].groupby(
                    ['region', 'technology']).sum()
        
        # Create energy system for each region
        for region in self.table_collection['demand'].columns:
            region_label = region.replace(" ", '_')

            # Create electricity bus
            el_bus_label = "bus_el_{}".format(
                region_label)
            nodes[el_bus_label] = solph.Bus(label=el_bus_label)

            # Create conventional power plants
            parameter_capacity = self.table_collection['power_plants'].loc[CONV_PP].join(
                capacity.loc[region, 'capacity'])
            for idx, row in parameter_capacity.iterrows():
                conv_label = '{0}_{1}'.format(
                    idx.replace(' ', '_'), region_label)
                nodes[conv_label] = solph.Transformer(
                    label=conv_label,
                    inputs={nodes[coal_cs_label]: solph.Flow()},
                    outputs={nodes[el_bus_label]: solph.Flow(
                        variable_cost=row['opex_var'],
                        # TODO: wie können opex_fix berücksichtigt werden?
                        investment=solph.Investment(
                            ep_costs=economics.annuity(
                                capex=row['capex'],
                                n=row['lifetime'],
                                wacc=row['wacc']),
                            existing=row['capacity']
                        ))},
                    conversion_factors={nodes[el_bus_label]: row['efficiency']})

            # Create RES power plants

            # Connect demand
            demand_label = "demand_{}".format(region_label)
            nodes[demand_label] = solph.Sink(
                label=demand_label,
                inputs={nodes[el_bus_label]: solph.Flow(
                    actual_value=self.table_collection['demand'][region],
                    fixed=True,
                    nominal_value=1)})


            # Connect storages

            # Add excess term to balance curtailment

        # Add transmission system
        trm_params = self.table_collection['transmission_params']
        length_capacity = self.table_collection[
            'transmission_capacity'].set_index(['from', 'to']).join(
            self.table_collection['transmission_length'].set_index(
                ['from', 'to'])).reset_index()
        for row, pair in length_capacity.iterrows():
            lines = [(pair['from'], pair['to']), (pair['to'], pair['from'])]
            for line in lines:
                region_1 = line[0].replace(" ", '_')
                region_2 = line[1].replace(" ", '_')
                line_label = 'transmission_{0}_{1}'.format(region_1, region_2)
                bus_label_in = 'bus_el_{0}'.format(region_1)
                bus_label_out = 'bus_el_{0}'.format(region_2)

                nodes[line_label] = solph.Transformer(
                    label=line_label,
                    inputs={nodes[bus_label_in]: solph.Flow()},
                    outputs={nodes[bus_label_out]: solph.Flow(
                        variable_cost=float(trm_params['opex_var']),
                        # TODO: wie können opex_fix berücksichtigt werden?
                        investment=solph.Investment(
                            ep_costs=economics.annuity(
                                capex=float(trm_params['capex'] * pair['length']),
                                n=float(trm_params['lifetime']),
                                wacc=float(trm_params['wacc'])),
                            existing=pair['capacity']
                        )
                    )},
                    conversion_factors={
                        nodes[bus_label_out]:
                            float(trm_params['relative_losses_per_1000_km'] *
                            pair['length'] / 1e3)
                    })

        # Add emission constraint

        # Add regional supply constraint

        return nodes



    def load_csv(self, data_path, year, suffix=''):
        """Load scenario from an excel-file."""
        self.table_collection = tools.load_csv(
            data_path,
            suffix=suffix,
            year=year)

    def solve(self, solver='gurobi', with_duals=None):

        logging.info("Optimising using {0}.".format(solver))

        if with_duals:
            self.model.receive_duals()

        if self.debug:
            filename = os.path.join(
                self.data_path, 'elesplan-m.lp')
            logging.info('Store lp-file in {0}.'.format(filename))
            self.model.write(filename,
                             io_options={'symbolic_solver_labels': True})

        self.model.solve(solver=solver, solve_kwargs={'tee': True})
        self.es.results['main'] = outputlib.processing.results(self.model)
        self.es.results['meta'] = outputlib.processing.meta_results(self.model)
        self.es.results['param'] = outputlib.processing.param_results(self.es)
        self.es.results['scenario'] = self.scenario_info()
        self.results = self.es.results['main']