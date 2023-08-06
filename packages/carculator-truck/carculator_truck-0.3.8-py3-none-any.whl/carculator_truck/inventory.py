import csv
import glob
import itertools
import re
from inspect import currentframe, getframeinfo
from pathlib import Path

import numpy as np
import xarray as xr
import yaml
from scipy import sparse
from scipy.sparse.linalg import spsolve

from . import DATA_DIR
from .background_systems import BackgroundSystemModel
from .export import ExportInventory
from .geomap import Geomap

np.warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

REMIND_FILES_DIR = DATA_DIR / "IAM"


def get_dict_input():
    """
    Load a dictionary with tuple ("name of activity", "location", "unit", "reference product") as key, row/column
    indices as values.

    :return: dictionary with `label:index` pairs.
    :rtype: dict

    """
    filename = "dict_inputs_A_matrix_trucks.csv"
    filepath = DATA_DIR / filename
    if not filepath.is_file():
        raise FileNotFoundError("The dictionary of activity labels could not be found.")
    csv_dict = {}
    count = 0
    with open(filepath) as f:
        input_dict = csv.reader(f, delimiter=";")
        for row in input_dict:
            if "(" in row[1]:
                row[1] = eval(row[1])
                csv_dict[(row[0], row[1], row[2])] = count
            else:
                csv_dict[(row[0], row[1], row[2], row[3])] = count
            count += 1

    return csv_dict


class InventoryCalculation:
    """
    Build and solve the inventory for results characterization and inventory export

    Vehicles to be analyzed can be filtered by passing a `scope` dictionary.
    Some assumptions in the background system can also be adjusted by passing a `background_configuration` dictionary.

    .. code-block:: python

        scope = {
                        'powertrain':['BEV', 'FCEV', 'ICEV-p'],
                    }
        bc = {'country':'CH', # considers electricity network losses for Switzerland
              'custom electricity mix' : [[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                                         ], # in this case, 100% nuclear for the second year
              'fuel blend':{
                  'cng':{ #specify fuel bland for compressed gas
                        'primary fuel':{
                            'type':'biogas - sewage sludge',
                            'share':[0.9, 0.8, 0.7, 0.6] # shares per year. Must total 1 for each year.
                            },
                        'secondary fuel':{
                            'type':'syngas',
                            'share': [0.1, 0.2, 0.3, 0.4]
                            }
                        },
                 'diesel':{
                        'primary fuel':{
                            'type':'synthetic diesel - energy allocation',
                            'share':[0.9, 0.8, 0.7, 0.6]
                            },
                        'secondary fuel':{
                            'type':'biodiesel - cooking oil',
                            'share': [0.1, 0.2, 0.3, 0.4]
                            }
                        },
                'hydrogen':{
                        'primary fuel':{'type':'electrolysis', 'share':[1, 0, 0, 0]},
                        'secondary fuel':{'type':'smr - natural gas', 'share':[0, 1, 1, 1]}
                        }
                    },
              'energy storage': {
                  'electric': {
                      'type':'NMC-622',
                      'origin': 'NO'
                  },
                  'hydrogen': {
                      'type':'carbon fiber'
                  }
              }
             }

        InventoryCalculation(CarModel.array,
                            background_configuration=background_configuration,
                            scope=scope,
                            scenario="RCP26")

    The `custom electricity mix` key in the background_configuration dictionary defines an electricity mix to apply,
    under the form of one or several array(s), depending on the number of years to analyze,
    that should total 1, of which the indices correspond to:

        - [0]: hydro-power
        - [1]: nuclear
        - [2]: natural gas
        - [3]: solar power
        - [4]: wind power
        - [5]: biomass
        - [6]: coal
        - [7]: oil
        - [8]: geothermal
        - [9]: waste incineration
        - [10]: biogas with CCS
        - [11]: biomass with CCS
        - [12]: coal with CCS
        - [13]: natural gas with CCS
        - [14]: wood with CCS

    If none is given, the electricity mix corresponding to the country specified in `country`
    will be selected. If no country is specified, Europe applies.

    The `primary` and `secondary` fuel keys contain an array with shares of alternative fuel
    for each year, to create a custom blend.
    If none is provided, a blend provided by the Integrated Assessment model REMIND is used,
    which will depend on the REMIND energy scenario selected.

    Here is a list of available fuel pathways:


    Hydrogen technologies
    --------------------
    "electrolysis"
    "smr - natural gas"
    "smr - natural gas with CCS"
    "smr - biogas"
    "smr - biogas with CCS"
    "coal gasification"
    "wood gasification"
    "wood gasification with CCS"
    "wood gasification with EF"
    "wood gasification with EF with CCS"
    "atr - natural gas"
    "atr - natural gas with CCS"
    "atr - biogas"
    "atr - biogas with CCS"

    Natural gas technologies
    ------------------------
    cng
    biogas - sewage sludge
    biogas - biowaste
    syngas

    Diesel technologies
    -------------------
    diesel
    biodiesel - algae
    biodiesel - cooking oil
    synthetic diesel - economic allocation
    synthetic diesel - energy allocation


    :ivar array: array from the CarModel class
    :vartype array: CarModel.array
    :ivar fuel_blend: a dictionary that contains fuel blend shares per type of fuel.
    :ivar scope: dictionary that contains filters for narrowing the analysis
    :ivar background_configuration: dictionary that contains choices for background system
    :ivar scenario: REMIND energy scenario to use ("SSP2-NPi": Nationally Implemented Policies, limits to 3.3°C by 2100,
          "SSP2-PkBudg1150": limits cumulative GHG emissions to 1,100 gigatons by 2100 (+2C),
          "SSP2-PkBudg500": limits cumulative GHG emissions to 500 gigatons by 2100 (+1.5C),
          "static": no forward-looking modification of the background inventories).
          "SSP2-NPi" selected by default.


    .. code-block:: python

    """

    def __init__(
        self,
        tm,
        scope=None,
        background_configuration=None,
        scenario="SSP2-NPi",
        method="recipe",
        method_type="midpoint",
    ):

        if scope is None:
            scope = {
                "size": tm.array.coords["size"].values.tolist(),
                "powertrain": tm.array.coords["powertrain"].values.tolist(),
                "year": tm.array.coords["year"].values.tolist(),
                "fu": {"unit": "tkm", "quantity": 1},
            }
        else:
            scope["size"] = scope.get("size", tm.array.coords["size"].values.tolist())
            scope["powertrain"] = scope.get(
                "powertrain", tm.array.coords["powertrain"].values.tolist()
            )
            scope["year"] = scope.get("year", tm.array.coords["year"].values.tolist())
            scope["fu"] = scope.get("fu", {"unit": "tkm", "quantity": 1})

        if "unit" not in scope["fu"]:
            scope["fu"]["unit"] = "tkm"
        else:
            if scope["fu"]["unit"] not in ["tkm", "vkm"]:
                raise NameError(
                    "Incorrect specification of functional unit. Must be 'tkm' or 'vkm'."
                )

        if "quantity" not in scope["fu"]:
            scope["fu"]["quantity"] = 1
        else:
            try:
                float(scope["fu"]["quantity"])
            except ValueError:
                raise ValueError("Incorrect quantity for the functional unit defined.")

        self.scope = scope
        self.scenario = scenario
        self.cycle = tm.cycle
        self.geo = Geomap()

        with open(DATA_DIR / "fuel_specs.yaml", "r", encoding="utf-8") as stream:
            self.fuel_specs = yaml.safe_load(stream)

        array = tm.array.sel(
            powertrain=self.scope["powertrain"],
            year=self.scope["year"],
            size=self.scope["size"],
        )

        # store some important specs for inventory documentation
        self.specs = tm.array.sel(
            parameter=[
                "combustion power",
                "electric power",
                "combustion power share",
                "lifetime kilometers",
                "kilometers per year",
                "target range",
                "TtW efficiency",
                "TtW energy",
                "fuel cell system efficiency",
                "electric energy stored",
                "oxidation energy stored",
                "energy battery mass",
                "available payload",
                "total cargo mass",
                "capacity utilization",
                "curb mass",
                "driving mass",
            ]
        )

        self.target_range = int(
            tm.array.sel(
                parameter="target range",
                value="reference" if "reference" in tm.array.coords["value"] else 0,
            )
            .mean()
            .values
        )

        if self.scope["fu"]["unit"] == "vkm":
            self.compliant_vehicles = array.sel(parameter="is_available") * 1

        else:
            # to qualify, at least 10% of the initial payload must remain
            self.compliant_vehicles = (
                (
                    (
                        array.sel(parameter="total cargo mass")
                        / array.sel(parameter="available payload")
                    )
                    >= 0.1
                )
                * 1
            ) * (array.sel(parameter="is_available") * 1)

        self.array = array.stack(desired=["size", "powertrain", "year"])

        self.iterations = len(tm.array.value.values)

        self.number_of_cars = (
            len(self.scope["size"])
            * len(self.scope["powertrain"])
            * len(self.scope["year"])
        )

        self.car_indices = []

        self.array_inputs = {
            x: i for i, x in enumerate(list(self.array.parameter.values), 0)
        }
        self.array_powertrains = {
            x: i for i, x in enumerate(list(self.array.powertrain.values), 0)
        }

        self.background_configuration = {}
        self.background_configuration["energy storage"] = tm.energy_storage
        if background_configuration:
            if "energy storage" in background_configuration:
                self.background_configuration["energy storage"].update(
                    background_configuration["energy storage"]
                )

            if "country" in background_configuration:
                self.background_configuration["country"] = background_configuration[
                    "country"
                ]
            else:
                self.background_configuration["country"] = tm.country

            if "custom electricity mix" in background_configuration:
                self.background_configuration[
                    "custom electricity mix"
                ] = background_configuration["custom electricity mix"]
            if "direct air capture" in background_configuration:
                self.background_configuration[
                    "direct air capture"
                ] = background_configuration["direct air capture"]

        self.inputs = get_dict_input()
        self.bs = BackgroundSystemModel()
        self.country = self.background_configuration.get("country", tm.country)
        self.add_additional_activities()
        self.rev_inputs = self.get_rev_dict_input()
        self.A = self.get_A_matrix()
        self.mix = self.define_electricity_mix_for_fuel_prep()

        self.fuel_blends = tm.fuel_blend
        self.fuel_dictionary = self.create_fuel_dictionary()

        if any(p in ["BEV", "PHEV-e"] for p in self.scope["powertrain"]):
            self.create_fuel_markets(
                fuel_type="electricity",
            )
        for fuel, val in self.fuel_blends.items():
            self.create_fuel_markets(
                fuel_type=fuel,
                primary=val["primary"]["type"],
                secondary=val.get("secondary", {"type": None})["type"],
                primary_share=val["primary"]["share"],
                secondary_share=val.get("secondary", {"share": None})["share"],
            )

        if "direct air capture" in self.background_configuration:
            if "heat source" in self.background_configuration["direct air capture"]:
                heat_source = self.background_configuration["direct air capture"][
                    "heat source"
                ]

                if heat_source != "waste heat":
                    self.select_heat_supplier(heat_source)

        self.index_cng = [self.inputs[i] for i in self.inputs if "ICEV-g" in i[0]]
        self.index_combustion_wo_cng = [
            self.inputs[i]
            for i in self.inputs
            if any(ele in i[0] for ele in ["ICEV-d", "PHEV-d", "HEV-d"])
        ]
        self.index_diesel = [self.inputs[i] for i in self.inputs if "ICEV-d" in i[0]]
        self.index_all_diesel = [
            self.inputs[i]
            for i in self.inputs
            if any(ele in i[0] for ele in ["ICEV-d", "HEV-d", "PHEV-d"])
        ]

        self.index_hybrid = [
            self.inputs[i] for i in self.inputs if any(ele in i[0] for ele in ["HEV-d"])
        ]
        self.index_plugin_hybrid = [
            self.inputs[i] for i in self.inputs if "PHEV" in i[0]
        ]
        self.index_fuel_cell = [self.inputs[i] for i in self.inputs if "FCEV" in i[0]]

        with open(
            DATA_DIR / "exhaust_and_noise_flows.yaml", "r", encoding="utf-8"
        ) as stream:
            flows = yaml.safe_load(stream)["exhaust"]

            d_comp = {
                "urban": "urban air close to ground",
                "suburban": "non-urban air or from high stacks",
                "rural": "low population density, long-term",
            }

            self.map_fuel_emissions = {
                (v, ("air", d_comp[comp]), "kilogram"): f"{k} direct emissions, {comp}"
                for k, v in flows.items()
                for comp in ["urban", "suburban", "rural"]
            }

        self.index_emissions = [self.inputs[i] for i in self.map_fuel_emissions.keys()]

        self.map_noise_emissions = {
            (
                f"noise, octave {i}, day time, {comp}",
                (f"octave {i}", "day time", comp),
                "joule",
            ): f"noise, octave {i}, day time, {comp}"
            for i in range(1, 9)
            for comp in ["urban", "suburban", "rural"]
        }

        with open(DATA_DIR / "elec_tech_map.yaml", "r", encoding="utf-8") as stream:
            self.elec_map = yaml.safe_load(stream)
            self.elec_map = {k: tuple(v) for k, v in self.elec_map.items()}

        self.index_noise = [self.inputs[i] for i in self.map_noise_emissions.keys()]

        self.list_cat, self.split_indices = self.get_split_indices()

        self.method = method

        if self.method == "recipe":
            self.method_type = method_type
        else:
            self.method_type = "midpoint"

        self.impact_categories = self.get_dict_impact_categories()

        # Load the B matrix
        self.B = None

    def get_results_table(self, split, sensitivity=False):
        """
        Format an xarray.DataArray array to receive the results.

        :param sensitivity:
        :param split: "components" or "impact categories". Split by impact categories only applicable when "endpoint" level is applied.
        :return: xarrray.DataArray
        """

        if split == "components":
            cat = [
                "direct - exhaust",
                "direct - non-exhaust",
                "energy chain",
                "maintenance",
                "glider",
                "powertrain",
                "energy storage",
                "road",
                "EoL",
            ]

        dict_impact_cat = list(self.impact_categories.keys())

        if not sensitivity:

            response = xr.DataArray(
                np.zeros(
                    (
                        self.B.shape[1],
                        len(self.scope["size"]),
                        len(self.scope["powertrain"]),
                        len(self.scope["year"]),
                        len(cat),
                        self.iterations,
                    )
                ),
                coords=[
                    dict_impact_cat,
                    self.scope["size"],
                    self.scope["powertrain"],
                    self.scope["year"],
                    cat,
                    np.arange(0, self.iterations),
                ],
                dims=[
                    "impact_category",
                    "size",
                    "powertrain",
                    "year",
                    "impact",
                    "value",
                ],
            )

        else:
            params = [a for a in self.array.value.values]
            response = xr.DataArray(
                np.zeros(
                    (
                        self.B.shape[1],
                        len(self.scope["size"]),
                        len(self.scope["powertrain"]),
                        len(self.scope["year"]),
                        self.iterations,
                    )
                ),
                coords=[
                    dict_impact_cat,
                    self.scope["size"],
                    self.scope["powertrain"],
                    self.scope["year"],
                    params,
                ],
                dims=["impact_category", "size", "powertrain", "year", "parameter"],
            )

        return response

    def get_sulfur_content(self, location, fuel, year):
        """
        Return the sulfur content in the fuel.
        If a region is passed, the average sulfur content over
        the countries the region contains is returned.
        :param location: str. A country or region ISO code
        :param fuel: str. "diesel" or "gasoline"
        :return: float. Sulfur content in ppm.
        """

        try:
            int(year)
        except ValueError:
            raise ValueError(
                "The year for which to fetch sulfur concentration values is not valid."
            )

        if location in self.bs.sulfur.country.values:
            sulfur_concentration = (
                self.bs.sulfur.sel(country=location, year=year, fuel=fuel).sum().values
            )
        else:
            # If the geography is in fact a region,
            # we need to calculate hte average sulfur content
            # across the region

            list_countries = self.geo.iam_to_ecoinvent_location(location)
            list_countries = [
                c for c in list_countries if c in self.bs.sulfur.country.values
            ]

            if len(list_countries) > 0:

                sulfur_concentration = (
                    self.bs.sulfur.sel(
                        country=list_countries,
                        year=year,
                        fuel=fuel,
                    )
                    .mean()
                    .values
                )
            else:

                # if we do not have the sulfur concentration for the required country, we pick Europe
                print(
                    "The sulfur content for {} fuel in {} could not be found. European average sulfur content is used instead.".format(
                        fuel, location
                    )
                )
                sulfur_concentration = (
                    self.bs.sulfur.sel(country="RER", year=year, fuel=fuel).sum().values
                )
        return sulfur_concentration

    def get_split_indices(self):
        """
        Return list of indices to split the results into categories.

        :return: list of indices
        :rtype: list
        """
        filename = "dict_split.csv"
        filepath = DATA_DIR / filename
        if not filepath.is_file():
            raise FileNotFoundError("The dictionary of splits could not be found.")

        with open(filepath) as f:
            csv_list = [[val.strip() for val in r.split(";")] for r in f.readlines()]
        (_, _, *header), *data = csv_list

        csv_dict = {}
        for row in data:
            key, sub_key, *values = row

            if key in csv_dict:
                if sub_key in csv_dict[key]:
                    csv_dict[key][sub_key].append(
                        {"search by": values[0], "search for": values[1]}
                    )
                else:
                    csv_dict[key][sub_key] = [
                        {"search by": values[0], "search for": values[1]}
                    ]
            else:
                csv_dict[key] = {
                    sub_key: [{"search by": values[0], "search for": values[1]}]
                }

        flatten = itertools.chain.from_iterable

        d = {}
        substance_list = []

        d["direct - exhaust"] = []
        d["direct - exhaust"].append(
            self.inputs[("Carbon dioxide, fossil", ("air",), "kilogram")]
        )
        d["direct - exhaust"].append(
            self.inputs[("Carbon dioxide, non-fossil", ("air",), "kilogram")]
        )
        d["direct - exhaust"].append(
            self.inputs[("Methane, fossil", ("air",), "kilogram")]
        )

        d["direct - exhaust"].extend(self.index_emissions)
        d["direct - exhaust"].extend(self.index_noise)

        substance_list.append(d["direct - exhaust"])

        for cat in csv_dict["components"]:
            d[cat] = list(
                flatten(
                    [
                        self.get_index_of_flows([l["search for"]], l["search by"])
                        for l in csv_dict["components"][cat]
                    ]
                )
            )
            substance_list.append(d[cat])

        list_ind = [d[x] for x in d]
        maxLen = max(map(len, list_ind))
        for row in list_ind:
            while len(row) < maxLen:
                row.extend([len(self.inputs) - 1])
        return list(d.keys()), list_ind

    def calculate_impacts(self, split="components", sensitivity=False):

        self.B = self.get_B_matrix()
        # Prepare an array to store the results
        results = self.get_results_table(split, sensitivity=sensitivity)

        # Create electricity and fuel market datasets
        self.create_electricity_market_for_fuel_prep()

        # Create electricity market dataset for battery production
        self.create_electricity_market_for_battery_production()

        # Fill in the A matrix with car parameters
        self.set_inputs_in_A_matrix(self.array.values)
        self.A = np.nan_to_num(self.A)

        new_arr = np.float32(
            np.zeros((self.A.shape[1], self.B.shape[1], len(self.scope["year"])))
        )

        f = np.zeros((np.shape(self.A)[1]))

        # Collect indices of activities contributing to the first level for year `y`
        arr = self.A[0, : -self.number_of_cars, self.car_indices].sum(axis=0)
        ind = np.nonzero(arr)[0]

        if self.scenario != "static":
            B = self.B.interp(
                year=self.scope["year"], kwargs={"fill_value": "extrapolate"}
            ).values
        else:
            B = self.B[0].values

        for a in ind:
            f[:] = 0
            f[a] = 1
            X = np.float32(spsolve(sparse.csr_matrix(self.A[0]), f.T))

            if self.scenario == "static":
                new_arr[a] = np.float32(X * B).sum(axis=-1).T[..., None]
            else:
                new_arr[a] = np.float32(X * B).sum(axis=-1).T

        shape = (
            self.iterations,
            len(self.scope["size"]),
            len(self.scope["powertrain"]),
            len(self.scope["year"]),
            self.A.shape[1],
        )

        arr = (
            self.A[:, :, -self.number_of_cars :].transpose(0, 2, 1).reshape(shape)
            * new_arr.transpose(1, 2, 0)[:, None, None, None, ...]
            * -1
        )
        arr = arr[..., self.split_indices].sum(axis=-1)

        if sensitivity:

            results[...] = arr.transpose(0, 2, 3, 4, 5, 1).sum(axis=-2)
            results /= results.sel(parameter="reference")

        else:
            results[...] = arr.transpose(0, 2, 3, 4, 5, 1)

        if self.scope["fu"]["unit"] == "tkm":
            load_factor = 1

        if self.scope["fu"]["unit"] == "vkm":
            load_factor = np.resize(
                self.array[self.array_inputs["total cargo mass"]].values / 1000,
                (
                    1,
                    len(self.scope["size"]),
                    len(self.scope["powertrain"]),
                    len(self.scope["year"]),
                    1,
                    1,
                ),
            )

        if sensitivity:
            return (
                results.astype("float32")
                * load_factor
                * self.compliant_vehicles.values[None, ...]
            )
        else:
            return results.astype("float32") * load_factor * self.compliant_vehicles

    def add_additional_activities(self):
        # Add as many rows and columns as cars to consider
        # Also add additional columns and rows for electricity markets
        # for fuel preparation and energy battery production

        maximum = max(self.inputs.values())

        for y in self.scope["year"]:

            if {"ICEV-d", "HEV-d", "PHEV-d"}.intersection(
                set(self.scope["powertrain"])
            ):
                maximum += 1
                self.inputs[
                    (
                        "fuel supply for diesel vehicles, " + str(y),
                        self.country,
                        "kilogram",
                        "fuel",
                    )
                ] = maximum

            if {"ICEV-g"}.intersection(set(self.scope["powertrain"])):
                maximum += 1
                self.inputs[
                    (
                        "fuel supply for gas vehicles, " + str(y),
                        self.country,
                        "kilogram",
                        "fuel",
                    )
                ] = maximum

            if {"FCEV"}.intersection(set(self.scope["powertrain"])):
                maximum += 1
                self.inputs[
                    (
                        "fuel supply for hydrogen vehicles, " + str(y),
                        self.country,
                        "kilogram",
                        "fuel",
                    )
                ] = maximum

            if {"BEV", "PHEV-d"}.intersection(set(self.scope["powertrain"])):
                maximum += 1
                self.inputs[
                    (
                        "electricity supply for electric vehicles, " + str(y),
                        self.country,
                        "kilowatt hour",
                        "electricity, low voltage, for battery electric vehicles",
                    )
                ] = maximum

            maximum += 1
            self.inputs[
                (
                    "electricity market for fuel preparation, " + str(y),
                    self.country,
                    "kilowatt hour",
                    "electricity, low voltage",
                )
            ] = maximum

            maximum += 1
            self.inputs[
                (
                    "electricity market for energy storage production, " + str(y),
                    self.background_configuration["energy storage"]["origin"],
                    "kilowatt hour",
                    "electricity, low voltage, for energy storage production",
                )
            ] = maximum

        for s in self.scope["size"]:
            for pt in self.scope["powertrain"]:
                for y in self.scope["year"]:
                    maximum += 1

                    if y < 1992:
                        euro_class = "EURO-0"
                    if 1992 <= y < 1995:
                        euro_class = "EURO-I"
                    if 1995 <= y < 1999:
                        euro_class = "EURO-II"
                    if 1999 <= y < 2005:
                        euro_class = "EURO-III"
                    if 2005 <= y < 2008:
                        euro_class = "EURO-IV"
                    if 2008 <= y < 2012:
                        euro_class = "EURO-V"
                    if y >= 2012:
                        euro_class = "EURO-VI"

                    if pt == "BEV":

                        chemistry = self.background_configuration["energy storage"][
                            "electric"
                        ][(pt, s, y)]

                        name = f"transport, freight, lorry, {pt}, {chemistry} battery, {s} gross weight, {y}, {self.cycle.lower()}"

                        if self.scope["fu"]["unit"] == "tkm":
                            unit = "ton-kilometer"
                        if self.scope["fu"]["unit"] == "vkm":
                            unit = "kilometer"

                        self.inputs[
                            (
                                name,
                                self.country,
                                unit,
                                "transport, freight, lorry",
                            )
                        ] = maximum

                    elif pt == "FCEV":

                        name = f"transport, freight, lorry, {pt}, {s} gross weight, {y}, {self.cycle.lower()}"

                        name = (
                            "transport, freight, lorry, "
                            + pt
                            + ", "
                            + s
                            + " gross weight, "
                            + str(y)
                            + ", "
                            + self.cycle.lower()
                        )

                        if self.scope["fu"]["unit"] == "tkm":
                            unit = "ton-kilometer"
                        if self.scope["fu"]["unit"] == "vkm":
                            unit = "kilometer"

                        self.inputs[
                            (
                                name,
                                self.country,
                                unit,
                                "transport, freight, lorry",
                            )
                        ] = maximum

                    else:

                        name = f"transport, freight, lorry, {pt}, {s} gross weight, {y}, {euro_class}, {self.cycle.lower()}"

                        if self.scope["fu"]["unit"] == "tkm":
                            unit = "ton-kilometer"
                        if self.scope["fu"]["unit"] == "vkm":
                            unit = "kilometer"

                        self.inputs[
                            (
                                name,
                                self.country,
                                unit,
                                f"transport, freight, lorry, {euro_class}",
                            )
                        ] = maximum

                    self.car_indices.append(maximum)

    def add_additional_activities_for_export(self):
        # Add as many rows and columns as trucks to consider
        # Also add additional columns and rows for electricity markets
        # for fuel preparation and energy battery production

        maximum = max(self.inputs.values())

        for s in self.scope["size"]:
            for pt in self.scope["powertrain"]:
                for y in self.scope["year"]:
                    maximum += 1

                    if y < 1992:
                        euro_class = "EURO-0"
                    if 1992 <= y < 1995:
                        euro_class = "EURO-I"
                    if 1995 <= y < 1999:
                        euro_class = "EURO-II"
                    if 1999 <= y < 2005:
                        euro_class = "EURO-III"
                    if 2005 <= y < 2008:
                        euro_class = "EURO-IV"
                    if 2008 <= y < 2012:
                        euro_class = "EURO-V"
                    if y >= 2012:
                        euro_class = "EURO-VI"

                    if pt == "BEV":
                        if s in ("3.5t", "7.5t"):
                            battery = self.background_configuration["energy storage"][
                                "electric"
                            ][(pt, s, y)]
                            name = f"Light duty truck, {pt}, {battery} battery, {s} gross weight, {y}, {self.cycle.lower()}"
                            ref = "Light duty truck"

                        if s in ("18t", "26t"):
                            battery = self.background_configuration["energy storage"][
                                "electric"
                            ][(pt, s, y)]
                            name = f"Medium duty truck, {pt}, {battery} battery, {s} gross weight, {y}, {self.cycle.lower()}"
                            ref = "Medium duty truck"

                        if s in ("32t", "40t", "60t"):
                            battery = self.background_configuration["energy storage"][
                                "electric"
                            ][(pt, s, y)]
                            name = f"Heavy duty truck, {pt}, {battery} battery, {s} gross weight, {y}, {self.cycle.lower()}"
                            ref = "Heavy duty truck"

                        self.inputs[
                            (
                                name,
                                self.country,
                                "unit",
                                ref,
                            )
                        ] = maximum

                    elif pt == "FCEV":
                        if s in ("3.5t", "7.5t"):
                            name = f"Light duty truck, {pt}, {s} gross weight, {y}, {self.cycle.lower()}"
                            ref = "Light duty truck"

                        if s in ("18t", "26t"):
                            name = f"Medium duty truck, {pt}, {s} gross weight, {y}, {self.cycle.lower()}"
                            ref = "Medium duty truck"

                        if s in ("32t", "40t", "60t"):
                            name = f"Heavy duty truck, {pt}, {s} gross weight, {y}, {self.cycle.lower()}"
                            ref = "Heavy duty truck"

                        self.inputs[
                            (
                                name,
                                self.country,
                                "unit",
                                ref,
                            )
                        ] = maximum

                    else:
                        if s in ("3.5t", "7.5t"):
                            name = f"Light duty truck, {pt}, {s} gross weight, {y}, {euro_class}, {self.cycle.lower()}"
                            ref = "Light duty truck, "

                        if s in ("18t", "26t"):
                            name = f"Medium duty truck, {pt}, {s} gross weight, {y}, {euro_class}, {self.cycle.lower()}"
                            ref = "Medium duty truck, "

                        if s in ("32t", "40t", "60t"):
                            name = f"Heavy duty truck, {pt}, {s} gross weight, {y}, {euro_class}, {self.cycle.lower()}"
                            ref = "Heavy duty truck, "

                        self.inputs[
                            (
                                name,
                                self.country,
                                "unit",
                                ref + euro_class,
                            )
                        ] = maximum

    def get_A_matrix(self):
        """
        Load the A matrix. The A matrix contains exchanges of products (rows) between activities (columns).

        :return: A matrix with three dimensions of shape (number of values, number of products, number of activities).
        :rtype: numpy.ndarray

        """
        filename = "A_matrix_trucks.csv"
        filepath = (
            Path(getframeinfo(currentframe()).filename)
            .resolve()
            .parent.joinpath("data/" + filename)
        )
        if not filepath.is_file():
            raise FileNotFoundError("The technology matrix could not be found.")

        # build matrix A from coordinates
        A_coords = np.genfromtxt(filepath, delimiter=";")
        indices_i = A_coords[:, 0].astype(int)
        indices_j = A_coords[:, 1].astype(int)
        initial_A = sparse.csr_matrix(
            (A_coords[:, 2], (indices_i, indices_j))
        ).toarray()

        new_A = np.identity(len(self.inputs))

        new_A[0 : np.shape(initial_A)[0], 0 : np.shape(initial_A)[0]] = initial_A

        # Resize the matrix to fit the number of iterations in `array`
        new_A = np.resize(new_A, (self.array.shape[1], new_A.shape[0], new_A.shape[1]))
        return new_A

    def get_B_matrix(self):
        """
        Load the B matrix. The B matrix contains impact assessment figures for a give impact assessment method,
        per unit of activity. Its length column-wise equals the length of the A matrix row-wise.
        Its length row-wise equals the number of impact assessment methods.

        :return: an array with impact values per unit of activity for each method.
        :rtype: numpy.ndarray

        """

        if self.method == "recipe":
            if self.method_type == "midpoint":
                list_file_names = glob.glob(
                    str(REMIND_FILES_DIR)
                    + "/*recipe_midpoint*{}*.csv".format(self.scenario)
                )
                list_file_names = sorted(
                    list_file_names, key=lambda x: int(re.findall("\d+", rf"{x}")[1])
                )
                B = np.zeros((len(list_file_names), 23, len(self.inputs)))
            elif self.method_type == "endpoint":
                list_file_names = glob.glob(
                    str(REMIND_FILES_DIR)
                    + "/*recipe_endpoint*{}*.csv".format(self.scenario)
                )
                list_file_names = sorted(
                    list_file_names, key=lambda x: int(re.findall("\d+", rf"{x}")[1])
                )
                B = np.zeros((len(list_file_names), 4, len(self.inputs)))
            else:
                raise TypeError(
                    "The LCIA method type should be either 'midpoint' or 'endpoint'."
                )

        else:
            list_file_names = glob.glob(
                str(REMIND_FILES_DIR) + "/*ilcd*{}*.csv".format(self.scenario)
            )
            list_file_names = sorted(
                list_file_names, key=lambda x: int(re.findall("\d+", rf"{x}")[1])
            )
            B = np.zeros((len(list_file_names), 19, len(self.inputs)))

        for f, fp in enumerate(list_file_names):
            initial_B = np.genfromtxt(fp, delimiter=";")

            new_B = np.zeros(
                (
                    np.shape(initial_B)[0],
                    len(self.inputs),
                )
            )

            new_B[0 : initial_B.shape[0], 0 : np.shape(initial_B)[1]] = initial_B

            B[f] = new_B

        list_impact_categories = list(self.impact_categories.keys())

        if self.scenario != "static":
            response = xr.DataArray(
                B,
                coords=[
                    [2005, 2010, 2020, 2030, 2040, 2050],
                    list_impact_categories,
                    list(self.inputs.keys()),
                ],
                dims=["year", "category", "activity"],
            )
        else:
            response = xr.DataArray(
                B,
                coords=[[2020], list_impact_categories, list(self.inputs.keys())],
                dims=["year", "category", "activity"],
            )

        return response

    def get_dict_impact_categories(self):
        """
        Load a dictionary with available impact assessment methods as keys, and assessment level and categories as values.

        ..code-block:: python

            {'recipe': {'midpoint': ['freshwater ecotoxicity',
                                   'human toxicity',
                                   'marine ecotoxicity',
                                   'terrestrial ecotoxicity',
                                   'metal depletion',
                                   'agricultural land occupation',
                                   'climate change',
                                   'fossil depletion',
                                   'freshwater eutrophication',
                                   'ionising radiation',
                                   'marine eutrophication',
                                   'natural land transformation',
                                   'ozone depletion',
                                   'particulate matter formation',
                                   'photochemical oxidant formation',
                                   'terrestrial acidification',
                                   'urban land occupation',
                                   'water depletion',
                                   'human noise',
                                   'primary energy, non-renewable',
                                   'primary energy, renewable']
                       }
           }

        :return: dictionary
        :rtype: dict
        """
        filename = "dict_impact_categories.csv"
        filepath = DATA_DIR / filename
        if not filepath.is_file():
            raise FileNotFoundError(
                "The dictionary of impact categories could not be found."
            )

        csv_dict = {}

        with open(filepath) as f:
            input_dict = csv.reader(f, delimiter=";")
            for row in input_dict:
                if row[0] == self.method and row[3] == self.method_type:
                    csv_dict[row[2]] = {
                        "method": row[1],
                        "category": row[2],
                        "type": row[3],
                        "abbreviation": row[4],
                        "unit": row[5],
                        "source": row[6],
                    }

        return csv_dict

    def get_rev_dict_input(self):
        """
        Reverse the self.inputs dictionary.

        :return: reversed dictionary
        :rtype: dict
        """
        return {v: k for k, v in self.inputs.items()}

    def get_index_vehicle_from_array(
        self, powertrain=[], size=[], year=[], method="or"
    ):
        """
        Return list of row/column indices of tm.array of labels
        that contain the string defined in `items_to_look_for`.

        :param items_to_look_for_also:
        :param method:
        :param items_to_look_for: string to search for
        :return: list
        """
        if not isinstance(powertrain, list):
            powertrain = [powertrain]

        if not isinstance(size, list):
            size = [size]

        if not isinstance(year, list):
            year = [year]

        list_vehicles = self.array.desired.values

        if method == "or":

            return [
                c
                for c, v in enumerate(list_vehicles)
                if set(powertrain + size + year).intersection(v)
            ]

        if method == "and":
            if powertrain == []:
                powertrain = self.scope["powertrain"]
            if size == []:
                size = self.scope["size"]
            if year == []:
                year = self.scope["year"]

            return [
                c
                for c, v in enumerate(list_vehicles)
                if set(powertrain).intersection(v)
                and set(size).intersection(v)
                and set(year).intersection(v)
            ]

    def get_index_of_flows(self, items_to_look_for, search_by="name"):
        """
        Return list of row/column indices of self.A of labels that contain the string defined in `items_to_look_for`.

        :param items_to_look_for: string
        :param search_by: "name" or "compartment" (for elementary flows)
        :return: list of row/column indices
        :rtype: list
        """
        if search_by == "name":
            return [
                int(self.inputs[c])
                for c in self.inputs
                if all(ele in c[0].lower() for ele in items_to_look_for)
            ]
        if search_by == "compartment":
            return [
                int(self.inputs[c])
                for c in self.inputs
                if all(ele in c[1] for ele in items_to_look_for)
            ]

    def resize_A_matrix_for_export(self):

        indices_to_remove = []

        for i in self.inputs:
            if (
                "duty truck, " in i[0]
                or "freight, lorry, " in i[0]
                and "market" not in i[0]
            ):

                if "transport" in i[0]:

                    if "BEV" in i[0]:
                        _, _, _, pt, _, size, year, _ = [
                            x.strip() for x in i[0].split(", ")
                        ]

                    elif "FCEV" in i[0]:
                        _, _, _, pt, size, year, _ = [
                            x.strip() for x in i[0].split(", ")
                        ]

                    else:
                        _, _, _, pt, size, year, _, _ = [
                            x.strip() for x in i[0].split(", ")
                        ]
                    size = size.replace(" gross weight", "")
                else:

                    if "EURO" in i[0]:
                        _, pt, size, year, _, _ = i[0].split(", ")
                    else:
                        if "BEV" in i[0]:
                            _, pt, _, size, year, _ = i[0].split(", ")
                        else:
                            _, pt, size, year, _ = i[0].split(", ")

                    size = size.replace(" gross weight", "")

                if (
                    self.compliant_vehicles.sel(
                        powertrain=pt, size=size, year=int(year)
                    )
                    == 0
                ):
                    indices_to_remove.append(self.inputs[i])
                    self.rev_inputs.pop(self.inputs[i])

        indices_to_preserve = [
            i for i in range(self.A.shape[1]) if i not in indices_to_remove
        ]

        self.A = self.A[
            np.ix_(range(self.A.shape[0]), indices_to_preserve, indices_to_preserve)
        ]

        self.rev_inputs = {v: k for v, k in enumerate(self.rev_inputs.values())}

    def export_lci(
        self,
        presamples=False,
        ecoinvent_version="3.8",
        db_name="carculator_truck db",
        create_vehicle_datasets=True,
    ):
        """
        Export the inventory as a dictionary. Also return a list of arrays that contain pre-sampled random values if
        :param db_name:
        :meth:`stochastic` of :class:`CarModel` class has been called.

        :param presamples: boolean.
        :param ecoinvent_version: str. "3.5", "3.6" or "uvek"
        :return: inventory, and optionally, list of arrays containing pre-sampled values.
        :rtype: list
        """
        self.car_indices = []
        self.inputs = get_dict_input()
        self.bs = BackgroundSystemModel()
        self.add_additional_activities()
        self.rev_inputs = self.get_rev_dict_input()
        self.A = self.get_A_matrix()

        if create_vehicle_datasets:

            # add vehicles datasets
            self.add_additional_activities_for_export()

            # Update dictionary
            self.rev_inputs = self.get_rev_dict_input()

            # resize A matrix
            self.A = self.get_A_matrix()

            # Create electricity and fuel market datasets
            self.create_electricity_market_for_fuel_prep()

            # Create electricity market dataset for battery production
            self.create_electricity_market_for_battery_production()

            # Create fuel markets
            if any(p in ["BEV", "PHEV-e"] for p in self.scope["powertrain"]):
                self.create_fuel_markets(
                    fuel_type="electricity",
                )
            for fuel, val in self.fuel_blends.items():
                self.create_fuel_markets(
                    fuel_type=fuel,
                    primary=val["primary"]["type"],
                    secondary=val.get("secondary", {"type": None})["type"],
                    primary_share=val["primary"]["share"],
                    secondary_share=val.get("secondary", {"share": None})["share"],
                )
            self.fuel_dictionary = self.create_fuel_dictionary()

            self.set_inputs_in_A_matrix_for_export(self.array.values)

        else:

            # Create electricity and fuel market datasets
            self.create_electricity_market_for_fuel_prep()

            # Create electricity market dataset for battery production
            self.create_electricity_market_for_battery_production()

            # Create fuel markets
            self.fuel_dictionary = self.create_fuel_dictionary()

            self.set_inputs_in_A_matrix(self.array.values)

        # Remove vehicles not compliant or available
        self.resize_A_matrix_for_export()

        if presamples:
            lci, array = ExportInventory(
                self.A, self.rev_inputs, db_name=db_name
            ).write_lci(
                presamples=presamples,
                ecoinvent_version=ecoinvent_version,
                vehicle_specs=self.specs,
            )
            return lci, array
        else:
            lci = ExportInventory(self.A, self.rev_inputs, db_name=db_name).write_lci(
                presamples=presamples,
                ecoinvent_version=ecoinvent_version,
                vehicle_specs=self.specs,
            )
            return lci

    def export_lci_to_bw(
        self,
        presamples=False,
        ecoinvent_version="3.8",
        db_name="carculator_truck db",
        create_vehicle_datasets=True,
    ):
        """
        Export the inventory as a `brightway2` bw2io.importers.base_lci.LCIImporter object
        with the inventory in the `data` attribute.

        .. code-block:: python

            # get the inventory
            i, _ = ic.export_lci_to_bw()

            # import it in a Brightway2 project
            i.match_database('ecoinvent 3.6 cutoff', fields=('name', 'unit', 'location', 'reference product'))
            i.match_database("biosphere3", fields=('name', 'unit', 'categories'))
            i.match_database(fields=('name', 'unit', 'location', 'reference product'))
            i.match_database(fields=('name', 'unit', 'categories'))

            # Create an additional biosphere database for the few flows that do not
            # exist in "biosphere3"
            i.create_new_biosphere("additional_biosphere", relink=True)

            # Check if all exchanges link
            i.statistics()

            # Register the database
            i.write_database()

        :return: LCIImport object that can be directly registered in a `brightway2` project.
        :rtype: bw2io.importers.base_lci.LCIImporter
        """
        self.car_indices = []
        self.inputs = get_dict_input()
        self.bs = BackgroundSystemModel()
        self.add_additional_activities()
        self.rev_inputs = self.get_rev_dict_input()
        self.A = self.get_A_matrix()

        if create_vehicle_datasets:

            # add vehicles datasets
            self.add_additional_activities_for_export()

            # Update dictionary
            self.rev_inputs = self.get_rev_dict_input()

            # resize A matrix
            self.A = self.get_A_matrix()

            # Create electricity and fuel market datasets
            self.create_electricity_market_for_fuel_prep()

            # Create electricity market dataset for battery production
            self.create_electricity_market_for_battery_production()

            # Create fuel markets
            if any(p in ["BEV", "PHEV-e"] for p in self.scope["powertrain"]):
                self.create_fuel_markets(
                    fuel_type="electricity",
                )
            for fuel, val in self.fuel_blends.items():
                self.create_fuel_markets(
                    fuel_type=fuel,
                    primary=val["primary"]["type"],
                    secondary=val.get("secondary", {"type": None})["type"],
                    primary_share=val["primary"]["share"],
                    secondary_share=val.get("secondary", {"share": None})["share"],
                )
            self.fuel_dictionary = self.create_fuel_dictionary()

            self.set_inputs_in_A_matrix_for_export(self.array.values)

        else:

            # Create electricity and fuel market datasets
            self.create_electricity_market_for_fuel_prep()

            # Create electricity market dataset for battery production
            self.create_electricity_market_for_battery_production()

            # Create fuel markets
            if any(p in ["BEV", "PHEV-e"] for p in self.scope["powertrain"]):
                self.create_fuel_markets(
                    fuel_type="electricity",
                )
            for fuel, val in self.fuel_blends.items():
                self.create_fuel_markets(
                    fuel_type=fuel,
                    primary=val["primary"]["type"],
                    secondary=val.get("secondary", {"type": None})["type"],
                    primary_share=val["primary"]["share"],
                    secondary_share=val.get("secondary", {"share": None})["share"],
                )
            self.fuel_dictionary = self.create_fuel_dictionary()

            self.set_inputs_in_A_matrix(self.array.values)

        # Remove vehicles not compliant or available
        self.resize_A_matrix_for_export()

        if presamples:
            lci, array = ExportInventory(
                self.A, self.rev_inputs, db_name=db_name
            ).write_lci_to_bw(
                presamples=presamples,
                ecoinvent_version=ecoinvent_version,
                vehicle_specs=self.specs,
            )
            return lci, array
        else:
            lci = ExportInventory(
                self.A, self.rev_inputs, db_name=db_name
            ).write_lci_to_bw(
                presamples=presamples,
                ecoinvent_version=ecoinvent_version,
                vehicle_specs=self.specs,
            )
            return lci

    def export_lci_to_excel(
        self,
        directory=None,
        ecoinvent_version="3.8",
        software_compatibility="brightway2",
        filename=None,
        create_vehicle_datasets=True,
        export_format="file",
    ):
        """
        Export the inventory as an Excel file (if the destination software is Brightway2) or a CSV file (if the destination software is Simapro) file.
        Also return the file path where the file is stored.

        :param filename:
        :param directory: directory where to save the file.
        :type directory: str
        :param ecoinvent_version: "3.6", "3.5" or "uvek"
        :param software_compatibility: "brightway2" or "simapro"
        :return: file path where the file is stored.
        :rtype: str
        """

        if software_compatibility not in ("brightway2", "simapro"):
            raise NameError(
                "The destination software argument is not valid. Choose between 'brightway2' or 'simapro'."
            )

        # Simapro inventory only for ecoinvent 3.6 or UVEK
        if software_compatibility == "simapro":
            if ecoinvent_version not in ("3.6", "uvek"):
                print(
                    "Simapro-compatible inventory export is only available for ecoinvent 3.6 or UVEK."
                )
                return

        self.car_indices = []
        self.inputs = get_dict_input()
        self.bs = BackgroundSystemModel()
        self.add_additional_activities()
        self.rev_inputs = self.get_rev_dict_input()
        self.A = self.get_A_matrix()
        self.create_fuel_dictionary()

        if create_vehicle_datasets:

            # add vehicles datasets
            self.add_additional_activities_for_export()

            # Update dictionary
            self.rev_inputs = self.get_rev_dict_input()

            # resize A matrix
            self.A = self.get_A_matrix()

            # Create electricity and fuel market datasets
            self.create_electricity_market_for_fuel_prep()

            # Create fuel markets
            if any(p in ["BEV", "PHEV-e"] for p in self.scope["powertrain"]):
                self.create_fuel_markets(
                    fuel_type="electricity",
                )
            for fuel, val in self.fuel_blends.items():
                self.create_fuel_markets(
                    fuel_type=fuel,
                    primary=val["primary"]["type"],
                    secondary=val.get("secondary", {"type": None})["type"],
                    primary_share=val["primary"]["share"],
                    secondary_share=val.get("secondary", {"share": None})["share"],
                )
            self.fuel_dictionary = self.create_fuel_dictionary()

            # Create electricity market dataset for battery production
            self.create_electricity_market_for_battery_production()

            self.set_inputs_in_A_matrix_for_export(self.array.values)

        else:

            # Create electricity and fuel market datasets
            self.create_electricity_market_for_fuel_prep()

            # Create electricity market dataset for battery production
            self.create_electricity_market_for_battery_production()

            # Create fuel markets
            self.fuel_dictionary = self.create_fuel_dictionary()

            self.set_inputs_in_A_matrix(self.array.values)

        # Remove vehicles not compliant or available
        self.resize_A_matrix_for_export()

        fp = ExportInventory(
            self.A, self.rev_inputs, db_name=filename or "carculator db"
        ).write_lci_to_excel(
            directory=directory,
            ecoinvent_version=ecoinvent_version,
            software_compatibility=software_compatibility,
            filename=filename,
            export_format=export_format,
            vehicle_specs=self.specs,
        )
        return fp

    def define_electricity_mix_for_fuel_prep(self):
        """
        This function defines a fuel mix based either on user-defined mix, or on default mixes for a given country.
        The mix is calculated as the average mix, weighted by the distribution of annually driven kilometers.
        :return:
        """

        if "custom electricity mix" in self.background_configuration:
            # If a special electricity mix is specified, we use it
            if not np.allclose(
                np.sum(self.background_configuration["custom electricity mix"], axis=1),
                [1] * len(self.scope["year"]),
            ):
                raise ValueError("The custom electricity mixes are not valid")

            mix = self.background_configuration["custom electricity mix"]

            if np.shape(mix)[0] != len(self.scope["year"]):
                raise ValueError(
                    "The number of electricity mixes ({}) must match with the "
                    "number of years ({}).".format(
                        np.shape(mix)[0], len(self.scope["year"])
                    )
                )

        else:
            use_year = [
                int(i)
                for i in (
                    self.array.values[
                        self.array_inputs["lifetime kilometers"],
                        :,
                        self.get_index_vehicle_from_array(
                            powertrain=[
                                "BEV",
                                "FCEV",
                                "PHEV-p",
                                "PHEV-d",
                                "ICEV-p",
                                "ICEV-d",
                                "HEV-p",
                                "HEV-d",
                                "ICEV-g",
                            ]
                        ),
                    ]
                    / self.array.values[
                        self.array_inputs["kilometers per year"],
                        :,
                        self.get_index_vehicle_from_array(
                            powertrain=[
                                "BEV",
                                "FCEV",
                                "PHEV-p",
                                "PHEV-d",
                                "ICEV-p",
                                "ICEV-d",
                                "HEV-p",
                                "HEV-d",
                                "ICEV-g",
                            ]
                        ),
                    ]
                )
                .mean(axis=1)
                .reshape((-1, len(self.scope["year"])))
                .mean(axis=0)
            ]

            if self.country not in self.bs.electricity_mix.country.values:
                print(
                    "The electricity mix for {} could not be found. Average European electricity mix is used instead.".format(
                        self.country
                    )
                )
                country = "RER"
            else:
                country = self.country

            mix = [
                self.bs.electricity_mix.sel(
                    country=country,
                    variable=[
                        "Hydro",
                        "Nuclear",
                        "Gas",
                        "Solar",
                        "Wind",
                        "Biomass",
                        "Coal",
                        "Oil",
                        "Geothermal",
                        "Waste",
                        "Biogas CCS",
                        "Biomass CCS",
                        "Coal CCS",
                        "Gas CCS",
                        "Wood CCS",
                        "Hydro, reservoir",
                        "Gas CCGT",
                        "Gas CHP",
                        "Solar, thermal",
                        "Wind, offshore",
                        "Lignite",
                    ],
                )
                .interp(
                    year=np.arange(year, year + use_year[y]),
                    kwargs={"fill_value": "extrapolate"},
                )
                .mean(axis=0)
                .values
                if year + use_year[y] <= 2050
                else self.bs.electricity_mix.sel(
                    country=country,
                    variable=[
                        "Hydro",
                        "Nuclear",
                        "Gas",
                        "Solar",
                        "Wind",
                        "Biomass",
                        "Coal",
                        "Oil",
                        "Geothermal",
                        "Waste",
                        "Biogas CCS",
                        "Biomass CCS",
                        "Coal CCS",
                        "Gas CCS",
                        "Wood CCS",
                        "Hydro, reservoir",
                        "Gas CCGT",
                        "Gas CHP",
                        "Solar, thermal",
                        "Wind, offshore",
                        "Lignite",
                    ],
                )
                .interp(
                    year=np.arange(year, 2051), kwargs={"fill_value": "extrapolate"}
                )
                .mean(axis=0)
                .values
                for y, year in enumerate(self.scope["year"])
            ]

        return mix

    def define_renewable_rate_in_mix(self):

        try:
            losses_to_low = float(self.bs.losses[self.country]["LV"])
        except KeyError:
            # If losses for the country are not found, assume EU average
            losses_to_low = float(self.bs.losses["RER"]["LV"])

        category_name = (
            "climate change"
            if self.method == "recipe"
            else "climate change - climate change total"
        )

        if self.method_type != "endpoint":
            if self.scenario != "static":
                year = self.scope["year"]
                co2_intensity_tech = (
                    self.B.sel(
                        category=category_name,
                        activity=list(self.elec_map.values()),
                    )
                    .interp(year=year, kwargs={"fill_value": "extrapolate"})
                    .values
                    * losses_to_low
                ) * 1000
            else:
                year = 2020
                co2_intensity_tech = np.resize(
                    (
                        self.B.sel(
                            category=category_name,
                            activity=list(self.elec_map.values()),
                            year=year,
                        ).values
                        * losses_to_low
                        * 1000
                    ),
                    (len(self.scope["year"]), 21),
                )
        else:
            co2_intensity_tech = np.zeros((len(self.scope["year"]), 21))

        sum_renew = [
            np.sum([self.mix[x][i] for i in [0, 3, 4, 5, 8]])
            for x in range(0, len(self.mix))
        ]

        return sum_renew, co2_intensity_tech

    def create_electricity_market_for_fuel_prep(self):
        """This function fills the electricity market that supplies battery charging operations
        and hydrogen production through electrolysis.
        """

        try:
            losses_to_low = float(self.bs.losses[self.country]["LV"])
        except KeyError:
            # If losses for the country are not found, assume EU average
            losses_to_low = float(self.bs.losses["RER"]["LV"])

        # Fill the electricity markets for battery charging and hydrogen production
        for y, year in enumerate(self.scope["year"]):
            m = np.array(self.mix[y]).reshape((-1, 21, 1))
            col_num = [
                self.inputs[i]
                for i in self.inputs
                if str(year) in i[0]
                and "electricity market for fuel preparation" in i[0]
            ]
            # Add electricity technology shares
            self.A[
                np.ix_(
                    np.arange(self.iterations),
                    [self.inputs[self.elec_map[t]] for t in self.elec_map],
                    col_num,
                )
            ] = (
                m * -1 * losses_to_low
            )

            # Add transmission network for high and medium voltage
            self.A[
                :,
                self.inputs[
                    (
                        "transmission network construction, electricity, high voltage",
                        "CH",
                        "kilometer",
                        "transmission network, electricity, high voltage",
                    )
                ],
                col_num,
            ] = (
                6.58e-9 * -1 * losses_to_low
            )

            self.A[
                :,
                self.inputs[
                    (
                        "transmission network construction, electricity, medium voltage",
                        "CH",
                        "kilometer",
                        "transmission network, electricity, medium voltage",
                    )
                ],
                col_num,
            ] = (
                1.86e-8 * -1 * losses_to_low
            )

            self.A[
                :,
                self.inputs[
                    (
                        "transmission network construction, long-distance",
                        "UCTE",
                        "kilometer",
                        "transmission network, long-distance",
                    )
                ],
                col_num,
            ] = (
                3.17e-10 * -1 * losses_to_low
            )

            # Add distribution network, low voltage
            self.A[
                :,
                self.inputs[
                    (
                        "distribution network construction, electricity, low voltage",
                        "CH",
                        "kilometer",
                        "distribution network, electricity, low voltage",
                    )
                ],
                col_num,
            ] = (
                8.74e-8 * -1 * losses_to_low
            )

            # Add supply of sulfur hexafluoride for transformers
            self.A[
                :,
                self.inputs[
                    (
                        "market for sulfur hexafluoride, liquid",
                        "RER",
                        "kilogram",
                        "sulfur hexafluoride, liquid",
                    )
                ],
                col_num,
            ] = (
                (5.4e-8 + 2.99e-9) * -1 * losses_to_low
            )

            # Add SF_6 leakage

            self.A[
                :, self.inputs[("Sulfur hexafluoride", ("air",), "kilogram")], col_num
            ] = ((5.4e-8 + 2.99e-9) * -1 * losses_to_low)

    def create_electricity_market_for_battery_production(self):
        """
        This funciton fills in the dataset that contains the electricity mix used for manufacturing battery cells
        :return:
        """

        battery_origin = self.background_configuration["energy storage"]["origin"]

        if battery_origin != "custom electricity mix":

            try:
                losses_to_low = float(self.bs.losses[battery_origin]["LV"])
            except KeyError:
                losses_to_low = float(self.bs.losses["CN"]["LV"])

            if battery_origin not in self.bs.electricity_mix.country.values:
                print(
                    "The electricity mix for {} could not be found. Average Chinese electricity mix is used for "
                    "battery manufacture instead.".format(self.country)
                )
                battery_origin = "CN"

            mix_battery_manufacturing = (
                self.bs.electricity_mix.sel(
                    country=battery_origin,
                    variable=[
                        "Hydro",
                        "Nuclear",
                        "Gas",
                        "Solar",
                        "Wind",
                        "Biomass",
                        "Coal",
                        "Oil",
                        "Geothermal",
                        "Waste",
                        "Biogas CCS",
                        "Biomass CCS",
                        "Coal CCS",
                        "Gas CCS",
                        "Wood CCS",
                        "Hydro, reservoir",
                        "Gas CCGT",
                        "Gas CHP",
                        "Solar, thermal",
                        "Wind, offshore",
                        "Lignite",
                    ],
                )
                .interp(year=self.scope["year"], kwargs={"fill_value": "extrapolate"})
                .values
            )

        else:
            # electricity mix for battery manufacturing same as `custom electricity mix`
            mix_battery_manufacturing = self.mix
            losses_to_low = 1.1

        # Fill the electricity markets for battery production
        for y, year in enumerate(self.scope["year"]):
            m = np.array(mix_battery_manufacturing[y]).reshape((-1, 21, 1))

            col_num = [
                self.inputs[i]
                for i in self.inputs
                if str(year) in i[0]
                and "electricity market for energy storage production" in i[0]
            ]

            self.A[
                np.ix_(
                    np.arange(self.iterations),
                    [self.inputs[self.elec_map[t]] for t in self.elec_map],
                    col_num,
                )
            ] = (
                m * losses_to_low * -1
            )

            # Add transmission network for high and medium voltage
            self.A[
                :,
                self.inputs[
                    (
                        "transmission network construction, electricity, high voltage",
                        "CH",
                        "kilometer",
                        "transmission network, electricity, high voltage",
                    )
                ],
                col_num,
            ] = (
                6.58e-9 * -1 * losses_to_low
            )

            self.A[
                :,
                self.inputs[
                    (
                        "transmission network construction, electricity, medium voltage",
                        "CH",
                        "kilometer",
                        "transmission network, electricity, medium voltage",
                    )
                ],
                col_num,
            ] = (
                1.86e-8 * -1 * losses_to_low
            )

            self.A[
                :,
                self.inputs[
                    (
                        "transmission network construction, long-distance",
                        "UCTE",
                        "kilometer",
                        "transmission network, long-distance",
                    )
                ],
                col_num,
            ] = (
                3.17e-10 * -1 * losses_to_low
            )

            # Add distribution network, low voltage
            self.A[
                :,
                self.inputs[
                    (
                        "distribution network construction, electricity, low voltage",
                        "CH",
                        "kilometer",
                        "distribution network, electricity, low voltage",
                    )
                ],
                col_num,
            ] = (
                8.74e-8 * -1 * losses_to_low
            )

            # Add supply of sulfur hexafluoride for transformers
            self.A[
                :,
                self.inputs[
                    (
                        "market for sulfur hexafluoride, liquid",
                        "RER",
                        "kilogram",
                        "sulfur hexafluoride, liquid",
                    )
                ],
                col_num,
            ] = (
                (5.4e-8 + 2.99e-9) * -1 * losses_to_low
            )

            # Add SF_6 leakage

            self.A[
                :, self.inputs[("Sulfur hexafluoride", ("air",), "kilogram")], col_num
            ] = ((5.4e-8 + 2.99e-9) * -1 * losses_to_low)

    def learning_rate_fuel(self, fuel, year, share, val):
        if fuel == "electrolysis":
            # apply some learning rate for electrolysis
            electrolysis = -0.3538 * (float(year) - 2010) + 58.589
            electricity = (val - 58 + electrolysis) * share
        elif fuel == "synthetic gasoline - energy allocation":
            # apply some learning rate for electrolysis
            h2 = 0.338
            electrolysis = -0.3538 * (float(year) - 2010) + 58.589
            electricity = val - (h2 * 58)
            electricity += electrolysis * h2
            electricity *= share

        elif fuel == "synthetic gasoline - economic allocation":
            # apply some learning rate for electrolysis
            h2 = 0.6385
            electrolysis = -0.3538 * (float(year) - 2010) + 58.589
            electricity = val - (h2 * 58)
            electricity += electrolysis * h2
            electricity *= share

        elif fuel == "synthetic diesel - energy allocation":
            # apply some learning rate for electrolysis
            h2 = 0.42
            electrolysis = -0.3538 * (float(year) - 2010) + 58.589
            electricity = val - (h2 * 58)
            electricity += electrolysis * h2
            electricity *= share

        elif fuel == "synthetic diesel - economic allocation":
            # apply some learning rate for electrolysis
            h2 = 0.183
            electrolysis = -0.3538 * (float(year) - 2010) + 58.589
            electricity = val - (h2 * 58)
            electricity += electrolysis * h2
            electricity *= share

        else:
            electricity = val * share
        return electricity

    def create_fuel_markets(
        self,
        fuel_type,
        primary=None,
        secondary=None,
        tertiary=None,
        primary_share=None,
        secondary_share=None,
        tertiary_share=None,
    ):
        """
        This function creates markets for fuel, considering a given blend, a given fuel type and a given year.
        It also adds separate electricity input in case hydrogen from electrolysis is needed somewhere in the fuel supply chain.
        :return:
        """

        d_dataset_name = {
            "petrol": "fuel supply for gasoline vehicles",
            "diesel": "fuel supply for diesel vehicles",
            "cng": "fuel supply for gas vehicles",
            "hydrogen": "fuel supply for hydrogen vehicles",
            "electricity": "electricity supply for electric vehicles",
        }

        if secondary_share is None:
            secondary_share = np.zeros_like(self.scope["year"])

        if fuel_type != "electricity":
            for y, year in enumerate(self.scope["year"]):

                if ~np.isclose(primary_share[y] + secondary_share[y], 1, rtol=1e-3):
                    sum_blend = primary_share[y] + secondary_share[y]
                    print(
                        f"The fuel blend for {fuel_type} in {year} is not equal to 1, but {sum_blend}."
                        f"The primary fuel share is adjusted so that the fuel blend equals 1."
                    )
                    primary_share[y] = 1 - secondary_share[y]

                for fuel, share in [
                    (primary, primary_share),
                    (secondary, secondary_share),
                ]:
                    if fuel:
                        dataset_name = f"{d_dataset_name[fuel_type]}, {year}"
                        if (
                            len(
                                [
                                    self.inputs[i]
                                    for i in self.inputs
                                    if i[0] == dataset_name
                                ]
                            )
                            > 0
                        ):
                            fuel_market_index = [
                                self.inputs[i]
                                for i in self.inputs
                                if i[0] == dataset_name
                            ][0]

                            try:
                                fuel_activity_index = self.inputs[
                                    tuple(self.fuel_specs[fuel]["name"])
                                ]
                            except KeyError:
                                raise KeyError(
                                    "One of the primary or secondary fuels specified in "
                                    "the fuel blend for {} is not valid.".format(
                                        fuel_type
                                    )
                                )

                            self.A[:, fuel_activity_index, fuel_market_index] = (
                                -1 * share[y]
                            )

                            additional_electricity = self.learning_rate_fuel(
                                fuel,
                                year,
                                share[y],
                                self.fuel_specs[fuel]["additional electricity"],
                            )

                            if additional_electricity > 0:
                                electricity_mix_index = [
                                    self.inputs[i]
                                    for i in self.inputs
                                    if i[0]
                                    == "electricity market for fuel preparation, "
                                    + str(year)
                                ][0]
                                self.A[:, electricity_mix_index, fuel_market_index] += (
                                    -1 * additional_electricity
                                )
        else:
            for year in self.scope["year"]:
                dataset_name = f"{d_dataset_name[fuel_type]}, {year}"

                electricity_market_index = [
                    self.inputs[i] for i in self.inputs if i[0] == dataset_name
                ][0]
                electricity_mix_index = [
                    self.inputs[i]
                    for i in self.inputs
                    if i[0] == "electricity market for fuel preparation, " + str(year)
                ][0]
                self.A[:, electricity_mix_index, electricity_market_index] = -1

    def find_inputs(
        self,
        value_in,
        value_out,
        find_input_by="name",
        zero_out_input=False,
        filter_activities=None,
    ):
        """
        Finds the exchange inputs to a specified functional unit
        :param zero_out_input:
        :param find_input_by: can be 'name' or 'unit'
        :param value_in: value to look for
        :param value_out: functional unit output
        :return: indices of all inputs to FU, indices of inputs of interest
        :rtype: tuple
        """

        if isinstance(value_out, str):
            value_out = [value_out]

        index_output = [
            self.inputs[i]
            for val in value_out
            for i in self.inputs
            if val.lower() in i[0].lower()
        ]

        f_vector = np.zeros((np.shape(self.A)[1]))
        f_vector[index_output] = 1

        X = np.float32(sparse.linalg.spsolve(sparse.csr_matrix(self.A[0]), f_vector.T))

        ind_inputs = np.nonzero(X)[0]

        if find_input_by == "name":
            ins = [
                i
                for i in ind_inputs
                if value_in.lower() in self.rev_inputs[i][0].lower()
            ]

        elif find_input_by == "unit":
            ins = [
                i
                for i in ind_inputs
                if value_in.lower() in self.rev_inputs[i][2].lower()
            ]
        else:
            raise ValueError("find_input_by must be 'name' or 'unit'")

        outs = [i for i in ind_inputs if i not in ins]

        if filter_activities:
            outs = [
                i
                for e in filter_activities
                for i in outs
                if e.lower() in self.rev_inputs[i][0].lower()
            ]

        ins = [
            i
            for i in ins
            if self.A[np.ix_(np.arange(0, self.A.shape[0]), [i], outs)].sum() != 0
        ]

        sum_supplied = X[ins].sum()

        if zero_out_input:
            # zero out initial inputs
            self.A[np.ix_(np.arange(0, self.A.shape[0]), ins, outs)] = 0
        else:
            return sum_supplied

    def create_fuel_dictionary(self):

        for val in self.fuel_specs.values():
            if any(
                i in val["name"][0].lower()
                for i in ("synthetic", "hydrogen", "ethanol", "biodiesel")
            ):
                val["additional electricity"] = self.find_inputs(
                    "kilowatt hour", val["name"][0], "unit"
                )
            else:
                val["additional electricity"] = 0

        for val in self.fuel_specs.values():
            if any(
                i in val["name"][0].lower() for i in ("synthetic", "hydrogen", "bio")
            ):
                self.find_inputs(
                    "kilowatt hour", val["name"][0], "unit", zero_out_input=True
                )

    def set_inputs_in_A_matrix(self, array):
        """
        Fill-in the A matrix. Does not return anything. Modifies in place.
        Shape of the A matrix (values, products, activities).

        :param array: :attr:`array` from :class:`TruckModel` class
        """

        # assembly operations
        self.A[
            :,
            self.inputs[
                (
                    "assembly operation, for lorry",
                    "RER",
                    "kilogram",
                    "assembly operation, for lorry",
                )
            ],
            -self.number_of_cars :,
        ] = (
            array[self.array_inputs["curb mass"]]
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        # Glider/Frame
        self.A[
            :,
            self.inputs[
                (
                    "frame, blanks and saddle, for lorry",
                    "RER",
                    "kilogram",
                    "frame, blanks and saddle, for lorry",
                )
            ],
            -self.number_of_cars :,
        ] = (
            (array[self.array_inputs["glider base mass"], :])
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        # Suspension + Brakes
        self.A[
            :,
            self.inputs[
                ("suspension, for lorry", "RER", "kilogram", "suspension, for lorry")
            ],
            -self.number_of_cars :,
        ] = (
            (
                array[
                    [
                        self.array_inputs["suspension mass"],
                        self.array_inputs["braking system mass"],
                    ],
                    :,
                ].sum(axis=0)
            )
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        # Wheels and tires
        self.A[
            :,
            self.inputs[
                (
                    "tires and wheels, for lorry",
                    "RER",
                    "kilogram",
                    "tires and wheels, for lorry",
                )
            ],
            -self.number_of_cars :,
        ] = (
            (array[self.array_inputs["wheels and tires mass"], :])
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        # Cabin
        self.A[
            :,
            self.inputs[("cabin, for lorry", "RER", "kilogram", "cabin, for lorry")],
            -self.number_of_cars :,
        ] = (
            (array[self.array_inputs["cabin mass"], :])
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        # Exhaust
        self.A[
            :,
            self.inputs[
                (
                    "exhaust system, for lorry",
                    "RER",
                    "kilogram",
                    "exhaust system, for lorry",
                )
            ],
            -self.number_of_cars :,
        ] = (
            (array[self.array_inputs["exhaust system mass"], :])
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        # Electrical system
        self.A[
            :,
            self.inputs[
                (
                    "power electronics, for lorry",
                    "RER",
                    "kilogram",
                    "power electronics, for lorry",
                )
            ],
            -self.number_of_cars :,
        ] = (
            (array[self.array_inputs["electrical system mass"], :])
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        # Transmission (52% transmission shaft, 36% gearbox + 12% retarder)
        self.A[
            :,
            self.inputs[
                (
                    "transmission, for lorry",
                    "RER",
                    "kilogram",
                    "transmission, for lorry",
                )
            ],
            -self.number_of_cars :,
        ] = (
            (array[self.array_inputs["transmission mass"], :] * 0.52)
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )
        self.A[
            :,
            self.inputs[
                ("gearbox, for lorry", "RER", "kilogram", "gearbox, for lorry")
            ],
            -self.number_of_cars :,
        ] = (
            (array[self.array_inputs["transmission mass"], :] * 0.36)
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )
        self.A[
            :,
            self.inputs[
                ("retarder, for lorry", "RER", "kilogram", "retarder, for lorry")
            ],
            -self.number_of_cars :,
        ] = (
            (array[self.array_inputs["transmission mass"], :] * 0.12)
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        # Other components, for non-electric and hybrid trucks
        index = self.get_index_vehicle_from_array(
            powertrain=["ICEV-d", "PHEV-d", "HEV-d", "ICEV-g"]
        )

        ind_A = [
            v
            for i, v in self.inputs.items()
            if any(x in i[0] for x in ["ICEV-d", "PHEV-d", "HEV-d", "ICEV-g"])
        ]

        self.A[
            :,
            self.inputs[
                (
                    "other components, for hybrid electric lorry",
                    "RER",
                    "kilogram",
                    "other components, for hybrid electric lorry",
                )
            ],
            ind_A,
        ] = (
            array[self.array_inputs["other components mass"], :, index]
            / array[self.array_inputs["lifetime kilometers"], :, index]
            / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
            * -1
        ).T

        # Other components, for electric trucks
        index = self.get_index_vehicle_from_array(powertrain=["BEV", "FCEV"])
        ind_A = [
            i
            for i in self.car_indices
            if any(x in self.rev_inputs[i][0] for x in ["BEV", "FCEV"])
        ]

        self.A[
            :,
            self.inputs[
                (
                    "other components, for electric lorry",
                    "RER",
                    "kilogram",
                    "other components, for electric lorry",
                )
            ],
            ind_A,
        ] = (
            array[self.array_inputs["other components mass"], :, index]
            / array[self.array_inputs["lifetime kilometers"], :, index]
            / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
            * -1
        ).T

        list_base_components_mass = [
            "glider base mass",
            "suspension mass",
            "braking system mass",
            "wheels and tires mass",
            "cabin mass",
            "electrical system mass",
            "other components mass",
            "transmission mass",
        ]

        self.A[
            :,
            self.inputs[
                ("Glider lightweighting", "GLO", "kilogram", "glider lightweighting")
            ],
            -self.number_of_cars :,
        ] = (
            (
                array[self.array_inputs["lightweighting"], :]
                * np.sum(
                    array[[self.array_inputs[x] for x in list_base_components_mass], :],
                    0,
                )
            )
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        index_16t = [
            i
            for i in self.car_indices
            if any(x in self.rev_inputs[i][0] for x in ("3.5t", "7.5t", "18t"))
        ]
        index_arr_16t = self.get_index_vehicle_from_array(size=["3.5t", "7.5t", "18t"])
        index_28t = [
            i
            for i in self.car_indices
            if any(x in self.rev_inputs[i][0] for x in ("26t", "32t"))
        ]
        index_arr_28t = self.get_index_vehicle_from_array(size=["26t", "32t"])

        index_40t = [
            i
            for i in self.car_indices
            if any(x in self.rev_inputs[i][0] for x in ("40t", "60t"))
        ]
        index_arr_40t = self.get_index_vehicle_from_array(size=["40t", "60t"])

        if len(index_16t) > 0:
            self.A[
                :,
                self.inputs[
                    (
                        "maintenance, lorry 16 metric ton",
                        "CH",
                        "unit",
                        "maintenance, lorry 16 metric ton",
                    )
                ],
                index_16t,
            ] = (
                1
                / array[self.array_inputs["lifetime kilometers"], :, index_arr_16t]
                / (
                    array[self.array_inputs["total cargo mass"], :, index_arr_16t]
                    / 1000
                )
                * (array[self.array_inputs["gross mass"], :, index_arr_16t] / 1000 / 16)
            ).T * -1

        if len(index_28t) > 0:
            self.A[
                :,
                self.inputs[
                    (
                        "maintenance, lorry 28 metric ton",
                        "CH",
                        "unit",
                        "maintenance, lorry 28 metric ton",
                    )
                ],
                index_28t,
            ] = (
                1
                / array[self.array_inputs["lifetime kilometers"], :, index_arr_28t]
                / (
                    array[self.array_inputs["total cargo mass"], :, index_arr_28t]
                    / 1000
                )
                * (array[self.array_inputs["gross mass"], :, index_arr_28t] / 1000 / 28)
            ).T * -1

        if len(index_40t) > 0:
            self.A[
                :,
                self.inputs[
                    (
                        "maintenance, lorry 40 metric ton",
                        "CH",
                        "unit",
                        "maintenance, lorry 40 metric ton",
                    )
                ],
                index_40t,
            ] = (
                1
                / array[self.array_inputs["lifetime kilometers"], :, index_arr_40t]
                / (
                    array[self.array_inputs["total cargo mass"], :, index_arr_40t]
                    / 1000
                )
                * (array[self.array_inputs["gross mass"], :, index_arr_40t] / 1000 / 40)
            ).T * -1

        # Powertrain components

        self.A[
            :,
            self.inputs[
                (
                    "market for converter, for electric passenger car",
                    "GLO",
                    "kilogram",
                    "converter, for electric passenger car",
                )
            ],
            -self.number_of_cars :,
        ] = (
            array[self.array_inputs["converter mass"], :]
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        self.A[
            :,
            self.inputs[
                (
                    "market for electric motor, electric passenger car",
                    "GLO",
                    "kilogram",
                    "electric motor, electric passenger car",
                )
            ],
            -self.number_of_cars :,
        ] = (
            array[self.array_inputs["electric engine mass"], :]
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        self.A[
            :,
            self.inputs[
                (
                    "market for inverter, for electric passenger car",
                    "GLO",
                    "kilogram",
                    "inverter, for electric passenger car",
                )
            ],
            -self.number_of_cars :,
        ] = (
            array[self.array_inputs["inverter mass"], :]
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        self.A[
            :,
            self.inputs[
                (
                    "market for power distribution unit, for electric passenger car",
                    "GLO",
                    "kilogram",
                    "power distribution unit, for electric passenger car",
                )
            ],
            -self.number_of_cars :,
        ] = (
            array[self.array_inputs["power distribution unit mass"], :]
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        self.A[
            :,
            self.inputs[
                (
                    "internal combustion engine, for lorry",
                    "RER",
                    "kilogram",
                    "internal combustion engine, for lorry",
                )
            ],
            -self.number_of_cars :,
        ] = (
            (
                array[
                    [self.array_inputs[l] for l in ["combustion engine mass"]],
                    :,
                ].sum(axis=0)
            )
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        self.A[
            :,
            self.inputs[("Ancillary BoP", "GLO", "kilogram", "Ancillary BoP")],
            -self.number_of_cars :,
        ] = (
            array[self.array_inputs["fuel cell ancillary BoP mass"], :]
            * (1 + array[self.array_inputs["fuel cell lifetime replacements"]])
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        self.A[
            :,
            self.inputs[("Essential BoP", "GLO", "kilogram", "Essential BoP")],
            -self.number_of_cars :,
        ] = (
            array[self.array_inputs["fuel cell essential BoP mass"], :]
            * (1 + array[self.array_inputs["fuel cell lifetime replacements"]])
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        self.A[
            :,
            self.inputs[("Stack", "GLO", "kilowatt", "Stack")],
            -self.number_of_cars :,
        ] = (
            array[self.array_inputs["fuel cell power"], :]
            * (1 + array[self.array_inputs["fuel cell lifetime replacements"]])
            / array[self.array_inputs["lifetime kilometers"], :]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        )

        # Start of printout

        print(
            "****************** IMPORTANT BACKGROUND PARAMETERS ******************",
            end="\n * ",
        )

        # Energy storage for electric trucks

        print(
            "The country of use is " + self.country,
            end="\n * ",
        )

        battery_tech = list(
            set(
                list(
                    self.background_configuration["energy storage"]["electric"].values()
                )
            )
        )
        battery_origin = self.background_configuration["energy storage"]["origin"]
        print(
            f"Energy batteries produced in {battery_origin} using {battery_tech}.",
            end="\n * ",
        )

        # Use the NMC inventory of Schmidt et al. 2019 for electric and hybrid trucks
        index = self.get_index_vehicle_from_array(
            powertrain=["BEV", "FCEV", "PHEV-d", "HEV-d"]
        )
        ind_A = [
            i
            for i in self.car_indices
            if any(
                x in self.rev_inputs[i][0] for x in ["BEV", "FCEV", "PHEV-d", "HEV-d"]
            )
        ]

        self.A[
            :, self.inputs[("Battery BoP", "GLO", "kilogram", "Battery BoP")], ind_A
        ] = (
            (
                array[self.array_inputs["battery BoP mass"], :, index]
                * (
                    1
                    + array[
                        self.array_inputs["battery lifetime replacements"], :, index
                    ]
                )
            )
            / array[self.array_inputs["lifetime kilometers"], :, index]
            / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
            * -1
        ).T

        # We look into `background_configuration` to see what battery chemistry to
        # use for each bus
        for veh, battery_tech in self.background_configuration["energy storage"][
            "electric"
        ].items():
            pwt, s, y = veh
            if (
                pwt in self.scope["powertrain"]
                and s in self.scope["size"]
                and y in self.scope["year"]
            ):

                battery_cell_label = (
                    "Battery cell, " + battery_tech,
                    "GLO",
                    "kilogram",
                    "Battery cell",
                )

                idx = self.get_index_vehicle_from_array(
                    powertrain=pwt, size=s, year=y, method="and"
                )

                ind_A = [
                    self.inputs[i]
                    for i in self.inputs
                    if all(str(x) in i[0] for x in list(veh))
                ]

                self.A[:, self.inputs[battery_cell_label], ind_A] = (
                    (
                        array[self.array_inputs["battery cell mass"], :, idx]
                        * (
                            1
                            + array[
                                self.array_inputs["battery lifetime replacements"],
                                :,
                                idx,
                            ]
                        )
                    )
                    / array[self.array_inputs["lifetime kilometers"], :, idx]
                    / (array[self.array_inputs["total cargo mass"], :, idx] / 1000)
                    * -1
                ).T

                # Fetch the overall input of electricity per kg of battery cell
                electricity_batt = self.find_inputs(
                    "kilowatt hour",
                    f"Battery cell, {battery_tech}",
                    "unit",
                    filter_activities=["NMC", "LFP", "LTO", "NCA"],
                )

                self.A[
                    np.ix_(
                        np.arange(self.iterations),
                        [
                            self.inputs[i]
                            for i in self.inputs
                            if str(y) in i[0]
                            and "electricity market for energy storage production"
                            in i[0]
                        ],
                        ind_A,
                    )
                ] = (
                    (
                        electricity_batt
                        * array[self.array_inputs["battery cell mass"], :, idx]
                        * (
                            1
                            + array[
                                self.array_inputs["battery lifetime replacements"],
                                :,
                                idx,
                            ]
                        )
                    )
                    / array[self.array_inputs["lifetime kilometers"], :, idx]
                    / (array[self.array_inputs["total cargo mass"], :, idx] / 1000)
                    * -1
                ).T[
                    :, None, :
                ]

        # zero out initial electricity input
        zeroed_out = []
        for veh, battery_tech in self.background_configuration["energy storage"][
            "electric"
        ].items():

            if battery_tech not in zeroed_out:

                self.find_inputs(
                    "kilowatt hour",
                    f"Battery cell, {battery_tech}",
                    "unit",
                    zero_out_input=True,
                )
                zeroed_out.append(battery_tech)

        # Use the inventory of Wolff et al. 2020 for lead acid battery for non-electric and non-hybrid trucks

        ind_A = [
            i
            for i in self.car_indices
            if any(x in self.rev_inputs[i][0] for x in ["ICEV-d", "ICEV-g"])
        ]
        index = self.get_index_vehicle_from_array(powertrain=["ICEV-d", "ICEV-g"])

        self.A[
            :,
            self.inputs[
                (
                    "lead acid battery, for lorry",
                    "RER",
                    "kilogram",
                    "lead acid battery, for lorry",
                )
            ],
            ind_A,
        ] = (
            (
                array[self.array_inputs["battery BoP mass"], :, index]
                * (
                    1
                    + array[
                        self.array_inputs["battery lifetime replacements"], :, index
                    ]
                )
            )
            / array[self.array_inputs["lifetime kilometers"], :, index]
            / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
            * -1
        ).T

        self.A[
            :,
            self.inputs[
                (
                    "lead acid battery, for lorry",
                    "RER",
                    "kilogram",
                    "lead acid battery, for lorry",
                )
            ],
            ind_A,
        ] += (
            (
                array[self.array_inputs["battery cell mass"], :, index]
                * (
                    1
                    + array[
                        self.array_inputs["battery lifetime replacements"], :, index
                    ]
                )
            )
            / array[self.array_inputs["lifetime kilometers"], :, index]
            / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
            * -1
        ).T

        # Fuel tank for diesel trucks
        index_A = [
            self.inputs[c]
            for c in self.inputs
            if any(ele in c[0] for ele in ["ICEV-d", "PHEV-d", "HEV-d"])
        ]
        index = self.get_index_vehicle_from_array(
            powertrain=["ICEV-d", "PHEV-d", "HEV-d"]
        )

        self.A[
            :,
            self.inputs[
                ("fuel tank, for diesel vehicle", "RER", "kilogram", "fuel tank")
            ],
            index_A,
        ] = (
            array[self.array_inputs["fuel tank mass"], :, index]
            / array[self.array_inputs["lifetime kilometers"], :, index]
            / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
            * -1
        ).T

        index = self.get_index_vehicle_from_array(powertrain="ICEV-g")
        self.A[
            :,
            self.inputs[
                (
                    "Fuel tank, compressed natural gas, 200 bar",
                    "RER",
                    "kilogram",
                    "Fuel tank, compressed natural gas, 200 bar",
                )
            ],
            self.index_cng,
        ] = (
            array[self.array_inputs["fuel tank mass"], :, index]
            / array[self.array_inputs["lifetime kilometers"], :, index]
            / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
            * -1
        ).T

        if "hydrogen" in self.background_configuration["energy storage"]:
            # If a customization dict is passed
            hydro_tank_technology = self.background_configuration["energy storage"][
                "hydrogen"
            ]["type"]
        else:
            hydro_tank_technology = "aluminium"

        dict_tank_map = {
            "carbon fiber": (
                "Fuel tank, compressed hydrogen gas, 700bar",
                "GLO",
                "kilogram",
                "Fuel tank, compressed hydrogen gas, 700bar",
            ),
            "hdpe": (
                "Fuel tank, compressed hydrogen gas, 700bar, with HDPE liner",
                "RER",
                "kilogram",
                "Hydrogen tank",
            ),
            "aluminium": (
                "Fuel tank, compressed hydrogen gas, 700bar, with aluminium liner",
                "RER",
                "kilogram",
                "Hydrogen tank",
            ),
        }

        index = self.get_index_vehicle_from_array(powertrain="FCEV")
        self.A[
            :,
            self.inputs[dict_tank_map[hydro_tank_technology]],
            self.index_fuel_cell,
        ] = (
            array[self.array_inputs["fuel tank mass"], :, index]
            / array[self.array_inputs["lifetime kilometers"], :, index]
            / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
            * -1
        ).T

        try:
            sum_renew, co2_intensity_tech = self.define_renewable_rate_in_mix()

        except AttributeError:
            sum_renew = [0] * len(self.scope["year"])
            co2_intensity_tech = [0] * len(self.scope["year"])

        for y, year in enumerate(self.scope["year"]):

            if y + 1 == len(self.scope["year"]):
                end_str = "\n * "
            else:
                end_str = "\n \t * "

            print(
                "in "
                + str(year)
                + ", % of renewable: "
                + str(np.round(sum_renew[y] * 100, 0))
                + "%"
                + ", GHG intensity per kWh: "
                + str(int(np.sum(co2_intensity_tech[y] * self.mix[y])))
                + " g. CO2-eq.",
                end=end_str,
            )

            if any(True for x in ["BEV", "PHEV-d"] if x in self.scope["powertrain"]):

                index = self.get_index_vehicle_from_array(
                    powertrain=["BEV", "PHEV-d"], year=year, method="and"
                )

                self.A[
                    np.ix_(
                        np.arange(self.iterations),
                        [
                            self.inputs[i]
                            for i in self.inputs
                            if str(year) in i[0]
                            and "electricity supply for electric vehicles" in i[0]
                        ],
                        [
                            i
                            for i in self.car_indices
                            if str(year) in self.rev_inputs[i][0]
                            and any(
                                True
                                for x in ["BEV", "PHEV-d"]
                                if x in self.rev_inputs[i][0]
                            )
                        ],
                    )
                ] = (
                    array[self.array_inputs["electricity consumption"], :, index]
                    / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
                    * -1
                ).T.reshape(
                    (self.iterations, 1, -1)
                )

        if "FCEV" in self.scope["powertrain"]:

            index = self.get_index_vehicle_from_array(powertrain="FCEV")

            print(
                "{} is completed by {}.".format(
                    self.fuel_blends["hydrogen"]["primary"]["type"],
                    self.fuel_blends["hydrogen"]["secondary"]["type"],
                ),
                end="\n \t * ",
            )
            for y, year in enumerate(self.scope["year"]):
                if y + 1 == len(self.scope["year"]):
                    end_str = "\n * "
                else:
                    end_str = "\n \t * "
                print(
                    "in "
                    + str(year)
                    + " _________________________________________ "
                    + str(
                        np.round(
                            self.fuel_blends["hydrogen"]["secondary"]["share"][y] * 100,
                            0,
                        )
                    )
                    + "%",
                    end=end_str,
                )

                # Primary fuel share

                ind_A = [
                    i
                    for i in self.car_indices
                    if str(year) in self.rev_inputs[i][0]
                    and "FCEV" in self.rev_inputs[i][0]
                ]
                ind_array = [
                    x
                    for x in self.get_index_vehicle_from_array(year=year)
                    if x in index
                ]

                self.A[
                    :,
                    [
                        self.inputs[i]
                        for i in self.inputs
                        if str(year) in i[0]
                        and "fuel supply for hydrogen vehicles" in i[0]
                    ],
                    ind_A,
                ] = (
                    array[self.array_inputs["fuel mass"], :, ind_array]
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

        if "ICEV-g" in self.scope["powertrain"]:
            index = self.get_index_vehicle_from_array(powertrain="ICEV-g")

            print(
                "{} is completed by {}.".format(
                    self.fuel_blends["cng"]["primary"]["type"],
                    self.fuel_blends["cng"]["secondary"]["type"],
                ),
                end="\n \t * ",
            )

            for y, year in enumerate(self.scope["year"]):
                if y + 1 == len(self.scope["year"]):
                    end_str = "\n * "
                else:
                    end_str = "\n \t * "
                print(
                    "in "
                    + str(year)
                    + " _________________________________________ "
                    + str(
                        np.round(
                            self.fuel_blends["cng"]["secondary"]["share"][y] * 100,
                            0,
                        )
                    )
                    + "%",
                    end=end_str,
                )

                # Primary fuel share

                ind_A = [
                    i
                    for i in self.car_indices
                    if str(year) in self.rev_inputs[i][0]
                    and "ICEV-g" in self.rev_inputs[i][0]
                ]
                ind_array = [
                    x
                    for x in self.get_index_vehicle_from_array(year=year)
                    if x in index
                ]

                # Includes pump-to-tank gas leakage, as a fraction of gas input
                self.A[
                    :,
                    [
                        self.inputs[i]
                        for i in self.inputs
                        if str(year) in i[0] and "fuel supply for gas vehicles" in i[0]
                    ],
                    ind_A,
                ] = (
                    (array[self.array_inputs["fuel mass"], :, ind_array])
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * (
                        1
                        + array[
                            self.array_inputs["CNG pump-to-tank leakage"], :, ind_array
                        ]
                    )
                    * -1
                ).T

                # Gas leakage emission as methane
                self.A[
                    :,
                    self.inputs[
                        (
                            "Methane, fossil",
                            ("air",),
                            "kilogram",
                        )
                    ],
                    ind_A,
                ] = (
                    (array[self.array_inputs["fuel mass"], :, ind_array])
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * array[self.array_inputs["CNG pump-to-tank leakage"], :, ind_array]
                    * -1
                ).T

                # Fuel-based emissions from CNG, CO2
                # The share and CO2 emissions factor of CNG is retrieved, if used

                share_fossil = 0
                CO2_fossil = 0

                if self.fuel_blends["cng"]["primary"]["type"] == "cng":
                    share_fossil += self.fuel_blends["cng"]["primary"]["share"][y]
                    CO2_fossil = (
                        self.fuel_blends["cng"]["primary"]["CO2"]
                        * self.fuel_blends["cng"]["primary"]["share"][y]
                    )

                if self.fuel_blends["cng"]["secondary"]["type"] == "cng":
                    share_fossil += self.fuel_blends["cng"]["secondary"]["share"][y]
                    CO2_fossil += (
                        self.fuel_blends["cng"]["primary"]["CO2"]
                        * self.fuel_blends["cng"]["secondary"]["share"][y]
                    )

                self.A[
                    :,
                    self.inputs[("Carbon dioxide, fossil", ("air",), "kilogram")],
                    ind_A,
                ] = (
                    (array[self.array_inputs["fuel mass"], :, ind_array] * CO2_fossil)
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

                # Fuel-based CO2 emission from alternative cng
                # The share of non-fossil gas in the blend is retrieved
                # As well as the CO2 emission factor of the fuel

                share_non_fossil = 0
                CO2_non_fossil = 0

                if self.fuel_blends["cng"]["primary"]["type"] != "cng":
                    share_non_fossil += self.fuel_blends["cng"]["primary"]["share"][y]
                    CO2_non_fossil = (
                        share_non_fossil * self.fuel_blends["cng"]["primary"]["CO2"]
                    )

                if self.fuel_blends["cng"]["secondary"]["type"] != "cng":
                    share_non_fossil += self.fuel_blends["cng"]["secondary"]["share"][y]
                    CO2_non_fossil += (
                        self.fuel_blends["cng"]["secondary"]["share"][y]
                        * self.fuel_blends["cng"]["secondary"]["CO2"]
                    )

                self.A[
                    :,
                    self.inputs[
                        (
                            "Carbon dioxide, non-fossil",
                            ("air",),
                            "kilogram",
                        )
                    ],
                    ind_A,
                ] = (
                    (
                        (
                            array[self.array_inputs["fuel mass"], :, ind_array]
                            * CO2_non_fossil
                        )
                    )
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

        if [i for i in self.scope["powertrain"] if i in ["ICEV-d", "PHEV-d", "HEV-d"]]:
            index = self.get_index_vehicle_from_array(
                powertrain=["ICEV-d", "PHEV-d", "HEV-d"]
            )

            print(
                "{} is completed by {}.".format(
                    self.fuel_blends["diesel"]["primary"]["type"],
                    self.fuel_blends["diesel"]["secondary"]["type"],
                ),
                end="\n \t * ",
            )

            for y, year in enumerate(self.scope["year"]):
                if y + 1 == len(self.scope["year"]):
                    end_str = "\n * "
                else:
                    end_str = "\n \t * "
                print(
                    "in "
                    + str(year)
                    + " _________________________________________ "
                    + str(
                        np.round(
                            self.fuel_blends["diesel"]["secondary"]["share"][y] * 100,
                            0,
                        )
                    )
                    + "%",
                    end=end_str,
                )

                ind_A = [
                    i
                    for i in self.car_indices
                    if str(year) in self.rev_inputs[i][0]
                    and any(
                        x in self.rev_inputs[i][0]
                        for x in ["ICEV-d", "PHEV-d", "HEV-d"]
                    )
                ]

                ind_array = [
                    x
                    for x in self.get_index_vehicle_from_array(year=year)
                    if x in index
                ]

                # Fuel supply
                self.A[
                    :,
                    [
                        self.inputs[i]
                        for i in self.inputs
                        if str(year) in i[0]
                        and "fuel supply for diesel vehicles" in i[0]
                    ],
                    ind_A,
                ] = (
                    (array[self.array_inputs["fuel mass"], :, ind_array])
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

                # Fuel-based CO2 emission from conventional diesel
                share_fossil = 0
                CO2_fossil = 0
                if self.fuel_blends["diesel"]["primary"]["type"] == "diesel":
                    share_fossil = self.fuel_blends["diesel"]["primary"]["share"][y]
                    CO2_fossil = (
                        self.fuel_blends["diesel"]["primary"]["CO2"]
                        * self.fuel_blends["diesel"]["primary"]["share"][y]
                    )

                if self.fuel_blends["diesel"]["secondary"]["type"] == "diesel":
                    share_fossil += self.fuel_blends["diesel"]["secondary"]["share"][y]
                    CO2_fossil += (
                        self.fuel_blends["diesel"]["secondary"]["CO2"]
                        * self.fuel_blends["diesel"]["secondary"]["share"][y]
                    )

                self.A[
                    :,
                    self.inputs[("Carbon dioxide, fossil", ("air",), "kilogram")],
                    ind_A,
                ] = (
                    (array[self.array_inputs["fuel mass"], :, ind_array] * CO2_fossil)
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

                # Fuel-based SO2 emissions
                # Sulfur concentration value for a given country, a given year, as concentration ratio

                sulfur_concentration = self.get_sulfur_content(
                    self.country, "diesel", year
                )

                self.A[
                    :,
                    self.inputs[("Sulfur dioxide", ("air",), "kilogram")],
                    ind_A,
                ] = (
                    (
                        (
                            array[self.array_inputs["fuel mass"], :, ind_array]
                            * share_fossil  # assumes sulfur only present in conventional diesel
                            * sulfur_concentration
                            * (64 / 32)  # molar mass of SO2/molar mass of O2
                        )
                    )
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

                share_non_fossil = 0
                CO2_non_fossil = 0

                # Fuel-based CO2 emission from alternative diesel
                # The share of non-fossil fuel in the blend is retrieved
                # As well as the CO2 emission factor of the fuel
                if self.fuel_blends["diesel"]["primary"]["type"] != "diesel":
                    share_non_fossil += self.fuel_blends["diesel"]["primary"]["share"][
                        y
                    ]
                    CO2_non_fossil = (
                        share_non_fossil * self.fuel_blends["diesel"]["primary"]["CO2"]
                    )

                if self.fuel_blends["diesel"]["secondary"]["type"] != "diesel":
                    share_non_fossil += self.fuel_blends["diesel"]["secondary"][
                        "share"
                    ][y]
                    CO2_non_fossil += (
                        self.fuel_blends["diesel"]["secondary"]["share"][y]
                        * self.fuel_blends["diesel"]["secondary"]["CO2"]
                    )

                self.A[
                    :,
                    self.inputs[
                        (
                            "Carbon dioxide, non-fossil",
                            ("air",),
                            "kilogram",
                        )
                    ],
                    ind_A,
                ] = (
                    (
                        (
                            array[self.array_inputs["fuel mass"], :, ind_array]
                            * CO2_non_fossil
                        )
                    )
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

        # Non-exhaust emissions
        self.A[
            :,
            self.inputs[
                (
                    "treatment of road wear emissions, lorry",
                    "RER",
                    "kilogram",
                    "road wear emissions, lorry",
                )
            ],
            -self.number_of_cars :,
        ] = (
            array[self.array_inputs["road wear emissions"], :]
            + (0.333 * array[self.array_inputs["road dust emissions"], :])
        ) / (
            array[self.array_inputs["total cargo mass"], :] / 1000
        )
        self.A[
            :,
            self.inputs[
                (
                    "treatment of tyre wear emissions, lorry",
                    "RER",
                    "kilogram",
                    "tyre wear emissions, lorry",
                )
            ],
            -self.number_of_cars :,
        ] = (
            array[self.array_inputs["tire wear emissions"], :]
            + (0.333 * array[self.array_inputs["road dust emissions"], :])
        ) / (
            array[self.array_inputs["total cargo mass"], :] / 1000
        )

        # Brake wear emissions
        self.A[
            :,
            self.inputs[
                (
                    "treatment of brake wear emissions, lorry",
                    "RER",
                    "kilogram",
                    "brake wear emissions, lorry",
                )
            ],
            -self.number_of_cars :,
        ] = (
            array[self.array_inputs["brake wear emissions"], :]
            + (0.333 * array[self.array_inputs["road dust emissions"], :])
        ) / (
            array[self.array_inputs["total cargo mass"], :] / 1000
        )

        # Infrastructure: 5.37e-4 per gross tkm
        self.A[
            :,
            self.inputs[("market for road", "GLO", "meter-year", "road")],
            -self.number_of_cars :,
        ] = (
            (array[self.array_inputs["driving mass"], :] / 1000)
            * 5.37e-4
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
        ) * -1

        # Infrastructure maintenance
        self.A[
            :,
            self.inputs[
                ("market for road maintenance", "RER", "meter-year", "road maintenance")
            ],
            -self.number_of_cars :,
        ] = (
            1.29e-3 / (array[self.array_inputs["total cargo mass"], :] / 1000) * -1
        )

        # Exhaust emissions
        # Non-fuel based emissions
        self.A[:, self.index_emissions, -self.number_of_cars :] = (
            array[
                [
                    self.array_inputs[self.map_fuel_emissions[self.rev_inputs[x]]]
                    for x in self.index_emissions
                ]
            ]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        ).transpose([1, 0, 2])

        # End-of-life disposal and treatment

        if len(index_16t) > 0:
            self.A[
                :,
                self.inputs[
                    (
                        "treatment of used lorry, 16 metric ton",
                        "CH",
                        "unit",
                        "used lorry, 16 metric ton",
                    )
                ],
                index_16t,
            ] = (
                1
                / array[self.array_inputs["lifetime kilometers"], :, index_arr_16t]
                / (
                    array[self.array_inputs["total cargo mass"], :, index_arr_16t]
                    / 1000
                )
                * (array[self.array_inputs["gross mass"], :, index_arr_16t] / 1000 / 16)
            ).T

        if len(index_28t) > 0:
            self.A[
                :,
                self.inputs[
                    (
                        "treatment of used lorry, 28 metric ton",
                        "CH",
                        "unit",
                        "used lorry, 28 metric ton",
                    )
                ],
                index_28t,
            ] = (
                1
                / array[self.array_inputs["lifetime kilometers"], :, index_arr_28t]
                / (
                    array[self.array_inputs["total cargo mass"], :, index_arr_28t]
                    / 1000
                )
                * (array[self.array_inputs["gross mass"], :, index_arr_28t] / 1000 / 28)
            ).T

        if len(index_40t) > 0:
            self.A[
                :,
                self.inputs[
                    (
                        "treatment of used lorry, 40 metric ton",
                        "CH",
                        "unit",
                        "used lorry, 40 metric ton",
                    )
                ],
                index_40t,
            ] = (
                1
                / array[self.array_inputs["lifetime kilometers"], :, index_arr_40t]
                / (
                    array[self.array_inputs["total cargo mass"], :, index_arr_40t]
                    / 1000
                )
                * (array[self.array_inputs["gross mass"], :, index_arr_40t] / 1000 / 40)
            ).T

        # Battery EoL
        self.A[
            :,
            self.inputs[
                (
                    "market for used Li-ion battery",
                    "GLO",
                    "kilogram",
                    "used Li-ion battery",
                )
            ],
            -self.number_of_cars :,
        ] = (
            (
                array[self.array_inputs["energy battery mass"], :]
                * (1 + array[self.array_inputs["battery lifetime replacements"]])
            )
            / array[self.array_inputs["lifetime kilometers"]]
            / (array[self.array_inputs["total cargo mass"]] / 1000)
        )

        # Noise emissions
        self.A[:, self.index_noise, -self.number_of_cars :] = (
            array[
                [
                    self.array_inputs[self.map_noise_emissions[self.rev_inputs[x]]]
                    for x in self.index_noise
                ]
            ]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        ).transpose([1, 0, 2])

        # Emissions of air conditioner refrigerant r134a
        # Leakage assumed to amount to 0.94 kg per lifetime according to
        # https://treeze.ch/fileadmin/user_upload/downloads/Publications/Case_Studies/Mobility/544-LCI-Road-NonRoad-Transport-Services-v2.0.pdf

        if any(y < 2022 for y in self.scope["year"]):
            idx_cars_before_2022 = [
                self.inputs[i]
                for i in self.inputs
                if i[0].startswith("transport, freight, lorry")
                and "metric" not in i[0]
                and int(re.findall("([, ]+[0-9]+)", i[0])[-1].replace(", ", "")) < 2022
            ]
            index = self.get_index_vehicle_from_array(
                year=[i for i in self.scope["year"] if i < 2022]
            )

            self.A[
                :,
                self.inputs[
                    ("Ethane, 1,1,1,2-tetrafluoro-, HFC-134a", ("air",), "kilogram")
                ],
                idx_cars_before_2022,
            ] = (
                0.94
                / self.array.values[self.array_inputs["lifetime kilometers"], :, index]
                / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
                * -1
                * self.array.values[
                    self.array_inputs["cooling energy consumption"], :, index
                ]
            ).T

            self.A[
                :,
                self.inputs[
                    (
                        "market for refrigerant R134a",
                        "GLO",
                        "kilogram",
                        "refrigerant R134a",
                    )
                ],
                idx_cars_before_2022,
            ] = (
                (0.94 + 1.1)
                / self.array.values[self.array_inputs["lifetime kilometers"], :, index]
                / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
                * -1
                * self.array.values[
                    self.array_inputs["cooling energy consumption"], :, index
                ]
            ).T

        # Charging infrastructure
        # Plugin BEV trucks
        # The charging station has a lifetime of 24 years
        # Hence, we calculate the lifetime of the bus
        # We assume two trucks per charging station

        index = self.get_index_vehicle_from_array(
            powertrain=["BEV", "PHEV-d"],
        )

        self.A[
            np.ix_(
                np.arange(self.iterations),
                [
                    self.inputs[i]
                    for i in self.inputs
                    if "EV charger, level 3, plugin, 200 kW" in i[0]
                ],
                [
                    i
                    for i in self.car_indices
                    if any(
                        True for x in ["BEV", "PHEV-d"] if x in self.rev_inputs[i][0]
                    )
                ],
            )
        ] = (
            -1
            / (
                24
                * (2100 / array[self.array_inputs["electric energy stored"], :, index])
                * array[self.array_inputs["kilometers per year"], :, index]
                * (array[self.array_inputs["total cargo mass"], :, index] / 1000)
            )
        ).T.reshape(
            (self.iterations, 1, -1)
        )

        print("*********************************************************************")

    def set_inputs_in_A_matrix_for_export(self, array):
        """
        Fill-in the A matrix. Does not return anything. Modifies in place.
        Shape of the A matrix (values, products, activities).

        :param array: :attr:`array` from :class:`TruckModel` class
        """

        # assembly operation

        self.A[
            :,
            self.inputs[
                (
                    "assembly operation, for lorry",
                    "RER",
                    "kilogram",
                    "assembly operation, for lorry",
                )
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit" and "market" not in i[0]
            ],
        ] = (
            array[self.array_inputs["curb mass"]] * -1
        )

        # Glider/Frame

        self.A[
            :,
            self.inputs[
                (
                    "frame, blanks and saddle, for lorry",
                    "RER",
                    "kilogram",
                    "frame, blanks and saddle, for lorry",
                )
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit" and "market" not in i[0]
            ],
        ] = (
            array[self.array_inputs["glider base mass"]] * -1
        )

        # Suspension + Brakes
        self.A[
            :,
            self.inputs[
                ("suspension, for lorry", "RER", "kilogram", "suspension, for lorry")
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit" and "market" not in i[0]
            ],
        ] = (
            array[
                [
                    self.array_inputs["suspension mass"],
                    self.array_inputs["braking system mass"],
                ],
                :,
            ].sum(axis=0)
            * -1
        )

        # Wheels and tires
        self.A[
            :,
            self.inputs[
                (
                    "tires and wheels, for lorry",
                    "RER",
                    "kilogram",
                    "tires and wheels, for lorry",
                )
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["wheels and tires mass"], :] * -1
        )

        # Cabin
        self.A[
            :,
            self.inputs[("cabin, for lorry", "RER", "kilogram", "cabin, for lorry")],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["cabin mass"], :] * -1
        )

        # Exhaust
        self.A[
            :,
            self.inputs[
                (
                    "exhaust system, for lorry",
                    "RER",
                    "kilogram",
                    "exhaust system, for lorry",
                )
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["exhaust system mass"], :] * -1
        )

        # Electrical system
        self.A[
            :,
            self.inputs[
                (
                    "power electronics, for lorry",
                    "RER",
                    "kilogram",
                    "power electronics, for lorry",
                )
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["electrical system mass"], :] * -1
        )

        # Transmission (52% transmission shaft, 36% gearbox + 12% retarder)
        self.A[
            :,
            self.inputs[
                (
                    "transmission, for lorry",
                    "RER",
                    "kilogram",
                    "transmission, for lorry",
                )
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["transmission mass"], :] * 0.52 * -1
        )

        self.A[
            :,
            self.inputs[
                ("gearbox, for lorry", "RER", "kilogram", "gearbox, for lorry")
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["transmission mass"], :] * 0.36 * -1
        )

        self.A[
            :,
            self.inputs[
                ("retarder, for lorry", "RER", "kilogram", "retarder, for lorry")
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["transmission mass"], :] * 0.12 * -1
        )

        # Other components, for non-electric and hybrid trucks
        index = self.get_index_vehicle_from_array(
            powertrain=["ICEV-d", "PHEV-d", "HEV-d", "ICEV-g"]
        )
        ind_A = [
            self.inputs[i]
            for i in self.inputs
            if "duty truck" in i[0]
            and any(x in i[0] for x in ["ICEV-d", "PHEV-d", "HEV-d", "ICEV-g"])
            and i[2] == "unit"
        ]
        self.A[
            :,
            self.inputs[
                (
                    "other components, for hybrid electric lorry",
                    "RER",
                    "kilogram",
                    "other components, for hybrid electric lorry",
                )
            ],
            ind_A,
        ] = (array[self.array_inputs["other components mass"], :, index] * -1).T

        # Other components, for electric trucks
        index = self.get_index_vehicle_from_array(powertrain=["BEV", "FCEV"])
        ind_A = [
            self.inputs[i]
            for i in self.inputs
            if "duty truck" in i[0]
            and any(x in i[0] for x in ["BEV", "FCEV"])
            and i[2] == "unit"
        ]
        self.A[
            :,
            self.inputs[
                (
                    "other components, for electric lorry",
                    "RER",
                    "kilogram",
                    "other components, for electric lorry",
                )
            ],
            ind_A,
        ] = (array[self.array_inputs["other components mass"], :, index] * -1).T

        list_base_components_mass = [
            "glider base mass",
            "suspension mass",
            "braking system mass",
            "wheels and tires mass",
            "cabin mass",
            "electrical system mass",
            "other components mass",
            "transmission mass",
        ]

        self.A[
            :,
            self.inputs[
                ("Glider lightweighting", "GLO", "kilogram", "glider lightweighting")
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["lightweighting"], :]
            * np.sum(
                array[[self.array_inputs[x] for x in list_base_components_mass], :], 0
            )
            * -1
        )

        index_16t = [
            self.inputs[i]
            for i in self.inputs
            if any(x in i[0] for x in ("3.5t", "7.5t", "18t")) and i[2] == "unit"
        ]
        index_arr_16t = self.get_index_vehicle_from_array(size=["3.5t", "7.5t", "18t"])

        index_28t = [
            self.inputs[i]
            for i in self.inputs
            if any(x in i[0] for x in ("26t", "32t")) and i[2] == "unit"
        ]
        index_arr_28t = self.get_index_vehicle_from_array(size=["26t", "32t"])
        index_40t = [
            self.inputs[i]
            for i in self.inputs
            if any(x in i[0] for x in ("40t", "60t")) and i[2] == "unit"
        ]
        index_arr_40t = self.get_index_vehicle_from_array(size=["40t", "60t"])

        if len(index_16t) > 0:
            self.A[
                :,
                self.inputs[
                    (
                        "maintenance, lorry 16 metric ton",
                        "CH",
                        "unit",
                        "maintenance, lorry 16 metric ton",
                    )
                ],
                index_16t,
            ] = (
                -1
                * (array[self.array_inputs["gross mass"], :, index_arr_16t] / 1000 / 16)
            ).T

        if len(index_28t) > 0:
            self.A[
                :,
                self.inputs[
                    (
                        "maintenance, lorry 28 metric ton",
                        "CH",
                        "unit",
                        "maintenance, lorry 28 metric ton",
                    )
                ],
                index_28t,
            ] = (
                -1
                * (array[self.array_inputs["gross mass"], :, index_arr_28t] / 1000 / 28)
            ).T

        if len(index_40t) > 0:
            self.A[
                :,
                self.inputs[
                    (
                        "maintenance, lorry 40 metric ton",
                        "CH",
                        "unit",
                        "maintenance, lorry 40 metric ton",
                    )
                ],
                index_40t,
            ] = (
                -1
                * (array[self.array_inputs["gross mass"], :, index_arr_40t] / 1000 / 40)
            ).T

        # Powertrain components

        self.A[
            :,
            self.inputs[
                (
                    "market for converter, for electric passenger car",
                    "GLO",
                    "kilogram",
                    "converter, for electric passenger car",
                )
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["converter mass"], :] * -1
        )

        self.A[
            :,
            self.inputs[
                (
                    "market for electric motor, electric passenger car",
                    "GLO",
                    "kilogram",
                    "electric motor, electric passenger car",
                )
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["electric engine mass"], :] * -1
        )

        self.A[
            :,
            self.inputs[
                (
                    "market for inverter, for electric passenger car",
                    "GLO",
                    "kilogram",
                    "inverter, for electric passenger car",
                )
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["inverter mass"], :] * -1
        )

        self.A[
            :,
            self.inputs[
                (
                    "market for power distribution unit, for electric passenger car",
                    "GLO",
                    "kilogram",
                    "power distribution unit, for electric passenger car",
                )
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["power distribution unit mass"], :] * -1
        )

        self.A[
            :,
            self.inputs[
                (
                    "internal combustion engine, for lorry",
                    "RER",
                    "kilogram",
                    "internal combustion engine, for lorry",
                )
            ],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[
                [self.array_inputs[l] for l in ["combustion engine mass"]],
                :,
            ].sum(axis=0)
            * -1
        )

        self.A[
            :,
            self.inputs[("Ancillary BoP", "GLO", "kilogram", "Ancillary BoP")],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["fuel cell ancillary BoP mass"], :]
            * (1 + array[self.array_inputs["fuel cell lifetime replacements"]])
            * -1
        )

        self.A[
            :,
            self.inputs[("Essential BoP", "GLO", "kilogram", "Essential BoP")],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["fuel cell essential BoP mass"], :]
            * (1 + array[self.array_inputs["fuel cell lifetime replacements"]])
            * -1
        )

        self.A[
            :,
            self.inputs[("Stack", "GLO", "kilowatt", "Stack")],
            [
                self.inputs[i]
                for i in self.inputs
                if "duty truck" in i[0] and i[2] == "unit"
            ],
        ] = (
            array[self.array_inputs["fuel cell power"], :]
            * (1 + array[self.array_inputs["fuel cell lifetime replacements"]])
            * -1
        )

        # Start of printout

        print(
            "****************** IMPORTANT BACKGROUND PARAMETERS ******************",
            end="\n * ",
        )

        # Energy storage for electric trucks

        print(
            "The country of use is " + self.country,
            end="\n * ",
        )

        battery_tech = list(
            set(
                list(
                    self.background_configuration["energy storage"]["electric"].values()
                )
            )
        )
        battery_origin = self.background_configuration["energy storage"]["origin"]
        print(
            f"Energy batteries produced in {battery_origin} using {battery_tech}.",
            end="\n * ",
        )

        # Use the NMC inventory of Schmidt et al. 2019 for electric and hybrid trucks
        index = self.get_index_vehicle_from_array(
            powertrain=["BEV", "FCEV", "PHEV-d", "HEV-d"]
        )
        ind_A = [
            self.inputs[i]
            for i in self.inputs
            if "duty truck" in i[0]
            and any(x in i[0] for x in ["BEV", "FCEV", "PHEV-d", "HEV-d"])
            and i[2] == "unit"
        ]

        self.A[
            :, self.inputs[("Battery BoP", "GLO", "kilogram", "Battery BoP")], ind_A
        ] = (
            (
                array[self.array_inputs["battery BoP mass"], :, index]
                * (
                    1
                    + array[
                        self.array_inputs["battery lifetime replacements"], :, index
                    ]
                )
            )
            * -1
        ).T

        # We look into `background_configuration` to see what battery chemistry to
        # use for each bus
        for veh, battery_tech in self.background_configuration["energy storage"][
            "electric"
        ].items():
            pwt, s, y = veh
            if (
                pwt in self.scope["powertrain"]
                and s in self.scope["size"]
                and y in self.scope["year"]
            ):

                battery_cell_label = (
                    "Battery cell, " + battery_tech,
                    "GLO",
                    "kilogram",
                    "Battery cell",
                )

                idx = self.get_index_vehicle_from_array(
                    powertrain=[pwt], size=[s], year=[y], method="and"
                )

                ind_A = [
                    self.inputs[i]
                    for i in self.inputs
                    if "duty truck" in i[0]
                    and i[2] == "unit"
                    and pwt in i[0]
                    and s in i[0]
                    and str(y) in i[0]
                ]

                self.A[:, self.inputs[battery_cell_label], ind_A] = (
                    (
                        array[self.array_inputs["battery cell mass"], :, idx]
                        * (
                            1
                            + array[
                                self.array_inputs["battery lifetime replacements"],
                                :,
                                idx,
                            ]
                        )
                    )
                    * -1
                ).T

                # Fetch the overall input of electricity per kg of battery cell
                electricity_batt = self.find_inputs(
                    "kilowatt hour",
                    f"Battery cell, {battery_tech}",
                    "unit",
                    filter_activities=["NMC", "LFP", "LTO", "NCA"],
                )

                self.A[
                    np.ix_(
                        np.arange(self.iterations),
                        [
                            self.inputs[i]
                            for i in self.inputs
                            if str(y) in i[0]
                            and "electricity market for energy storage production"
                            in i[0]
                        ],
                        ind_A,
                    )
                ] = (
                    (
                        electricity_batt
                        * array[self.array_inputs["battery cell mass"], :, idx]
                        * (
                            1
                            + array[
                                self.array_inputs["battery lifetime replacements"],
                                :,
                                idx,
                            ]
                        )
                    )
                    * -1
                ).T[
                    :, None, :
                ]

        # zero out initial electricity input
        zeroed_out = []
        for battery_tech in self.background_configuration["energy storage"][
            "electric"
        ].values():
            if battery_tech not in zeroed_out:
                self.find_inputs(
                    "kilowatt hour",
                    f"Battery cell, {battery_tech}",
                    "unit",
                    zero_out_input=True,
                )
                zeroed_out.append(battery_tech)

        # Use the inventory of Wolff et al. 2020 for lead acid battery for non-electric and non-hybrid trucks

        ind_A = [
            self.inputs[i]
            for i in self.inputs
            if "duty truck" in i[0]
            and any(x in i[0] for x in ["ICEV-d", "ICEV-g"])
            and i[2] == "unit"
        ]
        index = self.get_index_vehicle_from_array(powertrain=["ICEV-d", "ICEV-g"])

        self.A[
            :,
            self.inputs[
                (
                    "lead acid battery, for lorry",
                    "RER",
                    "kilogram",
                    "lead acid battery, for lorry",
                )
            ],
            ind_A,
        ] = (
            (
                array[self.array_inputs["battery BoP mass"], :, index]
                * (
                    1
                    + array[
                        self.array_inputs["battery lifetime replacements"], :, index
                    ]
                )
            )
            * -1
        ).T

        self.A[
            :,
            self.inputs[
                (
                    "lead acid battery, for lorry",
                    "RER",
                    "kilogram",
                    "lead acid battery, for lorry",
                )
            ],
            ind_A,
        ] += (
            (
                array[self.array_inputs["battery cell mass"], :, index]
                * (
                    1
                    + array[
                        self.array_inputs["battery lifetime replacements"], :, index
                    ]
                )
            )
            * -1
        ).T

        # Fuel tank for diesel trucks
        index_A = [
            self.inputs[c]
            for c in self.inputs
            if any(ele in c[0] for ele in ["ICEV-d", "PHEV-d", "HEV-d"])
            and c[2] == "unit"
        ]
        index = self.get_index_vehicle_from_array(
            powertrain=["ICEV-d", "PHEV-d", "HEV-d"]
        )

        self.A[
            :,
            self.inputs[
                ("fuel tank, for diesel vehicle", "RER", "kilogram", "fuel tank")
            ],
            index_A,
        ] = (array[self.array_inputs["fuel tank mass"], :, index] * -1).T

        index_A = [
            self.inputs[c]
            for c in self.inputs
            if any(ele in c[0] for ele in ["ICEV-g"]) and c[2] == "unit"
        ]

        index = self.get_index_vehicle_from_array(powertrain="ICEV-g")
        self.A[
            :,
            self.inputs[
                (
                    "Fuel tank, compressed natural gas, 200 bar",
                    "RER",
                    "kilogram",
                    "Fuel tank, compressed natural gas, 200 bar",
                )
            ],
            index_A,
        ] = (array[self.array_inputs["fuel tank mass"], :, index] * -1).T

        if "hydrogen" in self.background_configuration["energy storage"]:
            # If a customization dict is passed
            hydro_tank_technology = self.background_configuration["energy storage"][
                "hydrogen"
            ]["type"]
        else:
            hydro_tank_technology = "aluminium"

        dict_tank_map = {
            "carbon fiber": (
                "Fuel tank, compressed hydrogen gas, 700bar",
                "GLO",
                "kilogram",
                "Fuel tank, compressed hydrogen gas, 700bar",
            ),
            "hdpe": (
                "Fuel tank, compressed hydrogen gas, 700bar, with HDPE liner",
                "RER",
                "kilogram",
                "Hydrogen tank",
            ),
            "aluminium": (
                "Fuel tank, compressed hydrogen gas, 700bar, with aluminium liner",
                "RER",
                "kilogram",
                "Hydrogen tank",
            ),
        }

        index_A = [
            self.inputs[c]
            for c in self.inputs
            if any(ele in c[0] for ele in ["FCEV"]) and c[2] == "unit"
        ]

        index = self.get_index_vehicle_from_array(powertrain="FCEV")
        self.A[
            :,
            self.inputs[dict_tank_map[hydro_tank_technology]],
            index_A,
        ] = (array[self.array_inputs["fuel tank mass"], :, index] * -1).T

        # End-of-life disposal and treatment

        if len(index_16t) > 0:
            self.A[
                :,
                self.inputs[
                    (
                        "treatment of used lorry, 16 metric ton",
                        "CH",
                        "unit",
                        "used lorry, 16 metric ton",
                    )
                ],
                index_16t,
            ] = (
                1
                * (array[self.array_inputs["gross mass"], :, index_arr_16t] / 1000 / 16)
            ).T

        if len(index_28t) > 0:
            self.A[
                :,
                self.inputs[
                    (
                        "treatment of used lorry, 28 metric ton",
                        "CH",
                        "unit",
                        "used lorry, 28 metric ton",
                    )
                ],
                index_28t,
            ] = (
                1
                * (array[self.array_inputs["gross mass"], :, index_arr_28t] / 1000 / 28)
            ).T

        if len(index_40t) > 0:
            self.A[
                :,
                self.inputs[
                    (
                        "treatment of used lorry, 40 metric ton",
                        "CH",
                        "unit",
                        "used lorry, 40 metric ton",
                    )
                ],
                index_40t,
            ] = (
                1
                * (array[self.array_inputs["gross mass"], :, index_arr_40t] / 1000 / 40)
            ).T

        # END of vehicle building

        self.A[
            :,
            [
                self.inputs[c]
                for c in self.inputs
                if "duty truck" in c[0] and c[2] == "unit"
            ],
            self.car_indices,
        ] = (
            -1
            / array[self.array_inputs["lifetime kilometers"]]
            / (array[self.array_inputs["total cargo mass"]] / 1000)
        )

        try:
            sum_renew, co2_intensity_tech = self.define_renewable_rate_in_mix()

        except AttributeError:
            sum_renew = [0] * len(self.scope["year"])
            co2_intensity_tech = [0] * len(self.scope["year"])

        for y, year in enumerate(self.scope["year"]):

            if y + 1 == len(self.scope["year"]):
                end_str = "\n * "
            else:
                end_str = "\n \t * "

            print(
                "in "
                + str(year)
                + ", % of renewable: "
                + str(np.round(sum_renew[y] * 100, 0))
                + "%"
                + ", GHG intensity per kWh: "
                + str(int(np.sum(co2_intensity_tech[y] * self.mix[y])))
                + " g. CO2-eq.",
                end=end_str,
            )

            if any(True for x in ["BEV", "PHEV-d"] if x in self.scope["powertrain"]):

                index = self.get_index_vehicle_from_array(
                    powertrain=["BEV", "PHEV-d"], year=year, method="and"
                )

                self.A[
                    np.ix_(
                        np.arange(self.iterations),
                        [
                            self.inputs[i]
                            for i in self.inputs
                            if str(year) in i[0]
                            and "electricity supply for electric vehicles" in i[0]
                        ],
                        [
                            i
                            for i in self.car_indices
                            if str(year) in self.rev_inputs[i][0]
                            and any(
                                True
                                for x in ["BEV", "PHEV-d"]
                                if x in self.rev_inputs[i][0]
                            )
                        ],
                    )
                ] = (
                    array[self.array_inputs["electricity consumption"], :, index]
                    / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
                    * -1
                ).T.reshape(
                    (self.iterations, 1, -1)
                )

        if "FCEV" in self.scope["powertrain"]:

            index = self.get_index_vehicle_from_array(powertrain="FCEV")

            print(
                "{} is completed by {}.".format(
                    self.fuel_blends["hydrogen"]["primary"]["type"],
                    self.fuel_blends["hydrogen"]["secondary"]["type"],
                ),
                end="\n \t * ",
            )
            for y, year in enumerate(self.scope["year"]):
                if y + 1 == len(self.scope["year"]):
                    end_str = "\n * "
                else:
                    end_str = "\n \t * "
                print(
                    "in "
                    + str(year)
                    + " _________________________________________ "
                    + str(
                        np.round(
                            self.fuel_blends["hydrogen"]["secondary"]["share"][y] * 100,
                            0,
                        )
                    )
                    + "%",
                    end=end_str,
                )

                # Primary fuel share

                ind_A = [
                    i
                    for i in self.car_indices
                    if str(year) in self.rev_inputs[i][0]
                    and "FCEV" in self.rev_inputs[i][0]
                ]
                ind_array = [
                    x
                    for x in self.get_index_vehicle_from_array(year=year)
                    if x in index
                ]

                self.A[
                    :,
                    [
                        self.inputs[i]
                        for i in self.inputs
                        if str(year) in i[0]
                        and "fuel supply for hydrogen vehicles" in i[0]
                    ],
                    ind_A,
                ] = (
                    array[self.array_inputs["fuel mass"], :, ind_array]
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

        if "ICEV-g" in self.scope["powertrain"]:
            index = self.get_index_vehicle_from_array(powertrain="ICEV-g")

            print(
                "{} is completed by {}.".format(
                    self.fuel_blends["cng"]["primary"]["type"],
                    self.fuel_blends["cng"]["secondary"]["type"],
                ),
                end="\n \t * ",
            )

            for y, year in enumerate(self.scope["year"]):
                if y + 1 == len(self.scope["year"]):
                    end_str = "\n * "
                else:
                    end_str = "\n \t * "
                print(
                    "in "
                    + str(year)
                    + " _________________________________________ "
                    + str(
                        np.round(
                            self.fuel_blends["cng"]["secondary"]["share"][y] * 100,
                            0,
                        )
                    )
                    + "%",
                    end=end_str,
                )

                # Primary fuel share

                ind_A = [
                    i
                    for i in self.car_indices
                    if str(year) in self.rev_inputs[i][0]
                    and "ICEV-g" in self.rev_inputs[i][0]
                ]
                ind_array = [
                    x
                    for x in self.get_index_vehicle_from_array(year=year)
                    if x in index
                ]

                # Includes pump-to-tank gas leakage, as a fraction of gas input
                self.A[
                    :,
                    [
                        self.inputs[i]
                        for i in self.inputs
                        if str(year) in i[0] and "fuel supply for gas vehicles" in i[0]
                    ],
                    ind_A,
                ] = (
                    (array[self.array_inputs["fuel mass"], :, ind_array])
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * (
                        1
                        + array[
                            self.array_inputs["CNG pump-to-tank leakage"], :, ind_array
                        ]
                    )
                    * -1
                ).T

                # Gas leakage emission as methane
                self.A[
                    :,
                    self.inputs[
                        (
                            "Methane, fossil",
                            ("air",),
                            "kilogram",
                        )
                    ],
                    ind_A,
                ] = (
                    (array[self.array_inputs["fuel mass"], :, ind_array])
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * array[self.array_inputs["CNG pump-to-tank leakage"], :, ind_array]
                    * -1
                ).T

                # Fuel-based emissions from CNG, CO2
                # The share and CO2 emissions factor of CNG is retrieved, if used

                share_fossil = 0
                CO2_fossil = 0

                if self.fuel_blends["cng"]["primary"]["type"] == "cng":
                    share_fossil += self.fuel_blends["cng"]["primary"]["share"][y]
                    CO2_fossil = (
                        self.fuel_blends["cng"]["primary"]["CO2"]
                        * self.fuel_blends["cng"]["primary"]["share"][y]
                    )

                if self.fuel_blends["cng"]["secondary"]["type"] == "cng":
                    share_fossil += self.fuel_blends["cng"]["secondary"]["share"][y]
                    CO2_fossil = (
                        self.fuel_blends["cng"]["primary"]["CO2"]
                        * self.fuel_blends["cng"]["secondary"]["share"][y]
                    )

                self.A[
                    :,
                    self.inputs[("Carbon dioxide, fossil", ("air",), "kilogram")],
                    ind_A,
                ] = (
                    (array[self.array_inputs["fuel mass"], :, ind_array] * CO2_fossil)
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

                # Fuel-based CO2 emission from alternative cng
                # The share of non-fossil gas in the blend is retrieved
                # As well as the CO2 emission factor of the fuel

                share_non_fossil = 0
                CO2_non_fossil = 0

                if self.fuel_blends["cng"]["primary"]["type"] != "cng":
                    share_non_fossil += self.fuel_blends["cng"]["primary"]["share"][y]
                    CO2_non_fossil = (
                        share_non_fossil * self.fuel_blends["cng"]["primary"]["CO2"]
                    )

                if self.fuel_blends["cng"]["secondary"]["type"] != "cng":
                    share_non_fossil += self.fuel_blends["cng"]["secondary"]["share"][y]
                    CO2_non_fossil += (
                        self.fuel_blends["cng"]["secondary"]["share"][y]
                        * self.fuel_blends["cng"]["secondary"]["CO2"]
                    )

                self.A[
                    :,
                    self.inputs[
                        (
                            "Carbon dioxide, non-fossil",
                            ("air",),
                            "kilogram",
                        )
                    ],
                    ind_A,
                ] = (
                    (
                        (
                            array[self.array_inputs["fuel mass"], :, ind_array]
                            * CO2_non_fossil
                        )
                    )
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

        if [i for i in self.scope["powertrain"] if i in ["ICEV-d", "PHEV-d", "HEV-d"]]:
            index = self.get_index_vehicle_from_array(
                powertrain=["ICEV-d", "PHEV-d", "HEV-d"]
            )

            print(
                "{} is completed by {}.".format(
                    self.fuel_blends["diesel"]["primary"]["type"],
                    self.fuel_blends["diesel"]["secondary"]["type"],
                ),
                end="\n \t * ",
            )

            for y, year in enumerate(self.scope["year"]):
                if y + 1 == len(self.scope["year"]):
                    end_str = "\n * "
                else:
                    end_str = "\n \t * "
                print(
                    "in "
                    + str(year)
                    + " _________________________________________ "
                    + str(
                        np.round(
                            self.fuel_blends["diesel"]["secondary"]["share"][y] * 100,
                            0,
                        )
                    )
                    + "%",
                    end=end_str,
                )

                ind_A = [
                    i
                    for i in self.car_indices
                    if str(year) in self.rev_inputs[i][0]
                    and any(
                        x in self.rev_inputs[i][0]
                        for x in ["ICEV-d", "PHEV-d", "HEV-d"]
                    )
                ]

                ind_array = [
                    x
                    for x in self.get_index_vehicle_from_array(year=year)
                    if x in index
                ]

                # Fuel supply
                self.A[
                    :,
                    [
                        self.inputs[i]
                        for i in self.inputs
                        if str(year) in i[0]
                        and "fuel supply for diesel vehicles" in i[0]
                    ],
                    ind_A,
                ] = (
                    (array[self.array_inputs["fuel mass"], :, ind_array])
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

                # Fuel-based CO2 emission from conventional diesel
                share_fossil = 0
                CO2_fossil = 0
                if self.fuel_blends["diesel"]["primary"]["type"] == "diesel":
                    share_fossil = self.fuel_blends["diesel"]["primary"]["share"][y]
                    CO2_fossil = (
                        self.fuel_blends["diesel"]["primary"]["CO2"]
                        * self.fuel_blends["diesel"]["primary"]["share"][y]
                    )

                if self.fuel_blends["diesel"]["secondary"]["type"] == "diesel":
                    share_fossil += self.fuel_blends["diesel"]["secondary"]["share"][y]
                    CO2_fossil += (
                        self.fuel_blends["diesel"]["secondary"]["CO2"]
                        * self.fuel_blends["diesel"]["secondary"]["share"][y]
                    )

                self.A[
                    :,
                    self.inputs[("Carbon dioxide, fossil", ("air",), "kilogram")],
                    ind_A,
                ] = (
                    (array[self.array_inputs["fuel mass"], :, ind_array] * CO2_fossil)
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

                # Fuel-based SO2 emissions
                # Sulfur concentration value for a given country, a given year, as concentration ratio

                sulfur_concentration = self.get_sulfur_content(
                    self.country, "diesel", year
                )

                self.A[
                    :,
                    self.inputs[("Sulfur dioxide", ("air",), "kilogram")],
                    ind_A,
                ] = (
                    (
                        (
                            array[self.array_inputs["fuel mass"], :, ind_array]
                            * share_fossil  # assumes sulfur only present in conventional diesel
                            * sulfur_concentration
                            * (64 / 32)  # molar mass of SO2/molar mass of O2
                        )
                    )
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

                share_non_fossil = 0
                CO2_non_fossil = 0

                # Fuel-based CO2 emission from alternative diesel
                # The share of non-fossil fuel in the blend is retrieved
                # As well as the CO2 emission factor of the fuel
                if self.fuel_blends["diesel"]["primary"]["type"] != "diesel":
                    share_non_fossil += self.fuel_blends["diesel"]["primary"]["share"][
                        y
                    ]
                    CO2_non_fossil = (
                        share_non_fossil * self.fuel_blends["diesel"]["primary"]["CO2"]
                    )

                if self.fuel_blends["diesel"]["secondary"]["type"] != "diesel":
                    share_non_fossil += self.fuel_blends["diesel"]["secondary"][
                        "share"
                    ][y]
                    CO2_non_fossil += (
                        self.fuel_blends["diesel"]["secondary"]["share"][y]
                        * self.fuel_blends["diesel"]["secondary"]["CO2"]
                    )

                self.A[
                    :,
                    self.inputs[
                        (
                            "Carbon dioxide, non-fossil",
                            ("air",),
                            "kilogram",
                        )
                    ],
                    ind_A,
                ] = (
                    (
                        (
                            array[self.array_inputs["fuel mass"], :, ind_array]
                            * CO2_non_fossil
                        )
                    )
                    / array[self.array_inputs["target range"], :, ind_array]
                    / (
                        array[self.array_inputs["total cargo mass"], :, ind_array]
                        / 1000
                    )
                    * -1
                ).T

        # Non-exhaust emissions
        self.A[
            :,
            self.inputs[
                (
                    "treatment of road wear emissions, lorry",
                    "RER",
                    "kilogram",
                    "road wear emissions, lorry",
                )
            ],
            self.car_indices,
        ] = (
            array[self.array_inputs["road wear emissions"], :]
            + (0.333 * array[self.array_inputs["road dust emissions"], :])
        ) / (
            array[self.array_inputs["total cargo mass"], :] / 1000
        )
        self.A[
            :,
            self.inputs[
                (
                    "treatment of tyre wear emissions, lorry",
                    "RER",
                    "kilogram",
                    "tyre wear emissions, lorry",
                )
            ],
            self.car_indices,
        ] = (
            array[self.array_inputs["tire wear emissions"], :]
            + (0.333 * array[self.array_inputs["road dust emissions"], :])
        ) / (
            array[self.array_inputs["total cargo mass"], :] / 1000
        )

        # Brake wear emissions
        self.A[
            :,
            self.inputs[
                (
                    "treatment of brake wear emissions, lorry",
                    "RER",
                    "kilogram",
                    "brake wear emissions, lorry",
                )
            ],
            self.car_indices,
        ] = (
            array[self.array_inputs["brake wear emissions"], :]
            + (0.333 * array[self.array_inputs["road dust emissions"], :])
        ) / (
            array[self.array_inputs["total cargo mass"], :] / 1000
        )

        # Infrastructure: 5.37e-4 per gross tkm
        self.A[
            :,
            self.inputs[("market for road", "GLO", "meter-year", "road")],
            self.car_indices,
        ] = (
            (array[self.array_inputs["driving mass"], :] / 1000)
            * 5.37e-4
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
        ) * -1

        # Infrastructure maintenance
        self.A[
            :,
            self.inputs[
                ("market for road maintenance", "RER", "meter-year", "road maintenance")
            ],
            self.car_indices,
        ] = (
            1.29e-3 / (array[self.array_inputs["total cargo mass"], :] / 1000) * -1
        )

        # Exhaust emissions
        # Non-fuel based emissions

        self.A[
            np.ix_(
                np.arange(self.iterations),
                self.index_emissions,
                self.car_indices,
            )
        ] = (
            array[
                [
                    self.array_inputs[self.map_fuel_emissions[self.rev_inputs[x]]]
                    for x in self.index_emissions
                ]
            ]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        ).transpose(
            [1, 0, 2]
        )

        # Battery EoL
        self.A[
            :,
            self.inputs[
                (
                    "market for used Li-ion battery",
                    "GLO",
                    "kilogram",
                    "used Li-ion battery",
                )
            ],
            -self.number_of_cars :,
        ] = array[self.array_inputs["energy battery mass"], :] * (
            1 + array[self.array_inputs["battery lifetime replacements"]]
        )

        # Noise emissions
        self.A[
            np.ix_(np.arange(self.iterations), self.index_noise, self.car_indices)
        ] = (
            array[
                [
                    self.array_inputs[self.map_noise_emissions[self.rev_inputs[x]]]
                    for x in self.index_noise
                ]
            ]
            / (array[self.array_inputs["total cargo mass"], :] / 1000)
            * -1
        ).transpose(
            [1, 0, 2]
        )

        # Emissions of air conditioner refrigerant r134a
        # Leakage assumed to amount to 0.94 kg per lifetime according to
        # https://treeze.ch/fileadmin/user_upload/downloads/Publications/Case_Studies/Mobility/544-LCI-Road-NonRoad-Transport-Services-v2.0.pdf
        # but banned after 2021 in the European Union (and assumed elsewhere too)

        if any(y < 2022 for y in self.scope["year"]):
            idx_cars_before_2022 = [
                self.inputs[i]
                for i in self.inputs
                if i[0].startswith("transport, freight, lorry")
                and "metric" not in i[0]
                and int(re.findall("([, ]+[0-9]+)", i[0])[-1].replace(", ", "")) < 2022
            ]
            index = self.get_index_vehicle_from_array(
                year=[i for i in self.scope["year"] if i < 2022]
            )

            self.A[
                :,
                self.inputs[
                    ("Ethane, 1,1,1,2-tetrafluoro-, HFC-134a", ("air",), "kilogram")
                ],
                idx_cars_before_2022,
            ] = (
                0.94
                / self.array.values[self.array_inputs["lifetime kilometers"], :, index]
                / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
                * -1
                * self.array.values[
                    self.array_inputs["cooling energy consumption"], :, index
                ]
            ).T

            self.A[
                :,
                self.inputs[
                    (
                        "market for refrigerant R134a",
                        "GLO",
                        "kilogram",
                        "refrigerant R134a",
                    )
                ],
                idx_cars_before_2022,
            ] = (
                (0.94 + 1.1)
                / self.array.values[self.array_inputs["lifetime kilometers"], :, index]
                / (array[self.array_inputs["total cargo mass"], :, index] / 1000)
                * -1
                * self.array.values[
                    self.array_inputs["cooling energy consumption"], :, index
                ]
            ).T

        # Charging infrastructure
        # Plugin BEV trucks
        # The charging station has a lifetime of 24 years
        # Hence, we calculate the lifetime of the bus
        # We assume two trucks per charging station

        index = self.get_index_vehicle_from_array(
            powertrain=["BEV", "PHEV-d"],
        )

        self.A[
            np.ix_(
                np.arange(self.iterations),
                [
                    self.inputs[i]
                    for i in self.inputs
                    if "EV charger, level 3, plugin, 200 kW" in i[0]
                ],
                [
                    i
                    for i in self.car_indices
                    if any(
                        True for x in ["BEV", "PHEV-d"] if x in self.rev_inputs[i][0]
                    )
                ],
            )
        ] = (
            -1
            / (
                24
                * (2100 / array[self.array_inputs["electric energy stored"], :, index])
                * array[self.array_inputs["kilometers per year"], :, index]
                * (array[self.array_inputs["total cargo mass"], :, index] / 1000)
            )
        ).T.reshape(
            (self.iterations, 1, -1)
        )

        print("*********************************************************************")

    def select_heat_supplier(self, heat_supplier):
        """
        The heat supply is an important aspect of direct air capture.
        Here, we can change the supplier of heat.
        :param heat_supplier: by default "waste heat". Must be one of "waste heat", "biomass heat",
        "natural gas heat", "market heat".
        :type heat_supplier: str
        :return:
        """

        d_heat_suppliers = {
            "waste heat": (
                "heat, from municipal waste incineration to generic market for heat district or industrial, other than natural gas",
                "CH",
                "megajoule",
                "heat, district or industrial, other than natural gas",
            ),
            "biomass heat": (
                "heat production, hardwood chips from forest, at furnace 1000kW, state-of-the-art 2014",
                "CH",
                "megajoule",
                "heat, district or industrial, other than natural gas",
            ),
            "natural gas heat": (
                "market group for heat, central or small-scale, natural gas",
                "RER",
                "megajoule",
                "heat, central or small-scale, natural gas",
            ),
            "market heat": (
                "market for heat, from steam, in chemical industry",
                "RER",
                "megajoule",
                "heat, from steam, in chemical industry",
            ),
        }

        air_capture = self.inputs[
            (
                "carbon dioxide, captured from atmosphere",
                "RER",
                "kilogram",
                "carbon dioxide, captured from the atmosphere",
            )
        ]

        all_inds = [self.inputs[i] for i in list(d_heat_suppliers.values())]

        # DAC
        heat_amount = self.A[
            np.ix_(range(self.A.shape[0]), all_inds, [air_capture])
        ].sum()

        # zero out the heat input
        self.A[np.ix_(range(self.A.shape[0]), all_inds, [air_capture])] = 0
        # find index of the new supplier and set the amount
        ind = self.inputs[d_heat_suppliers[heat_supplier]]
        self.A[np.ix_(range(self.A.shape[0]), [ind], [air_capture])] = heat_amount
