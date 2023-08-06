from itertools import product

import numexpr as ne
import numpy as np
import xarray as xr
import yaml
from prettytable import PrettyTable

from . import DATA_DIR
from .background_systems import BackgroundSystemModel
from .driving_cycles import get_standard_driving_cycle
from .energy_consumption import EnergyConsumptionModel
from .hot_emissions import HotEmissionsModel
from .noise_emissions import NoiseEmissionsModel
from .particulates_emissions import ParticulatesEmissionsModel

CARGO_MASSES = DATA_DIR / "payloads.yaml"

DEFAULT_MAPPINGS = {
    "electric": {"BEV", "PHEV-e"},
    "combustion": {
        "HEV-d",
        "ICEV-g",
        "ICEV-d",
        "PHEV-c-d",
    },
    "combustion_wo_cng": {"HEV-d", "ICEV-d", "PHEV-c-d"},
    "pure_combustion": {"ICEV-g", "ICEV-d"},
    "petrol": {"PHEV-c-p"},
    "cng": {"ICEV-g"},
    "fuel_cell": {"FCEV"},
    "hybrid": {"PHEV-e", "PHEV-c-d"},
    "combustion_hybrid": {"PHEV-c-d"},
    "electric_hybrid": {"PHEV-e"},
    "diesel": {"ICEV-d", "PHEV-c-d", "HEV-d"},
    "battery": {"BEV"},
}


def finite(array, mask_value=0):
    return np.where(np.isfinite(array), array, mask_value)


class TruckModel:

    """
    This class represents the entirety of the vehicles considered, with useful attributes, such as an array that stores
    all the vehicles parameters.

    :ivar array: multi-dimensional numpy-like array that contains parameters' value(s)
    :vartype array: xarray.DataArray
    :ivar mappings: Dictionary with names correspondence
    :vartype mappings: dict
    :ivar ecm: instance of :class:`EnergyConsumptionModel` class for a given driving cycle
    :vartype ecm: coarse.energy_consumption.EnergyConsumptionModel

    """

    def __init__(
        self,
        array,
        mappings=None,
        cycle="Urban delivery",
        country=None,
        fuel_blend=None,
        energy_storage=None,
        payload=None,
        energy_target={2025: 0.85, 2030: 0.7, 2050: 0.6},
        energy_consumption=None,
        target_range=None,
    ):

        self.array = array
        self.mappings = mappings or DEFAULT_MAPPINGS
        self.bs = BackgroundSystemModel()

        self.country = country or "RER"

        with open(DATA_DIR / "fuel_specs.yaml", "r", encoding="utf-8") as stream:
            self.fuel_specs = yaml.safe_load(stream)

        self.fuel_blend = self.define_fuel_blends(fuel_blend)
        self.cycle = cycle

        self.energy_target = energy_target

        self.energy_storage = {
            "electric": {
                x: "NMC-622"
                for x in product(
                    ["BEV", "PHEV-e", "HEV-d", "FCEV"],
                    self.array.coords["size"].values,
                    self.array.year.values,
                )
            },
            "origin": "CN",
        }
        self.energy_storage.update(energy_storage or {})

        self.set_battery_preferences()

        target_ranges = {
            "Urban delivery": 150,
            "Regional delivery": 400,
            "Long haul": 800,
        }

        self["target range"] = target_range or target_ranges[self.cycle]

        self.energy_consumption = energy_consumption or None

        print(
            "{} driving cycle is selected. \nVehicles will be designed to achieve a minimal range of {} km.".format(
                cycle, target_range or target_ranges[self.cycle]
            )
        )

        print("")

        self.ecm = EnergyConsumptionModel(
            cycle=cycle, size=self.array.coords["size"].values
        )

        self.set_cargo_mass_and_annual_mileage(payload)

    def __call__(self, key):
        """
        This method fixes a dimension of the `array` attribute given a powertrain technology selected.

        Set up this class as a context manager, so we can have some nice syntax

        .. code-block:: python

            with class('some powertrain') as cpm:
                cpm['something']. # Will be filtered for the correct powertrain

        On with block exit, this filter is cleared
        https://stackoverflow.com/a/10252925/164864

        :param key: A powertrain type, e.g., "FCEV"
        :type key: str
        :return: An instance of `array` filtered after the powertrain selected.

        """
        self.__cache = self.array
        self.array = self.array.sel(powertrain=key)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.array = self.__cache
        del self.__cache

    def __getitem__(self, key):
        """
        Make class['foo'] automatically filter for the parameter 'foo'
        Makes the model code much cleaner

        :param key: Parameter name
        :type key: str
        :return: `array` filtered after the parameter selected
        """

        return self.array.sel(parameter=key)

    def __setitem__(self, key, value):
        self.array.loc[{"parameter": key}] = value

    # Make it easier/more flexible to filter by powertrain types
    def __getattr__(self, key):
        if key in self.mappings:
            return self.mappings[key]

    def set_all(self, electric_utility_factor: float = None):
        """
        This method runs a series of other methods to obtain the tank-to-wheel energy requirement,
        efficiency of the vehicle, costs, etc.

        :meth:`set_component_masses()`, :meth:`set_vehicle_masses()` and :meth:`set_power_parameters()` and
         :meth:`set_energy_stored_properties` relate to one another.
        `powertrain_mass` depends on `power`, `curb_mass` is affected by changes in `powertrain_mass`,
        `combustion engine mass`, `electric engine mass`. `energy battery mass` is influenced
        by the `curb mass` but also
        by the `target range` the truck has. `power` is also varying with `curb_mass`.

        The current solution is to loop through the methods until the change in payload between
        two iterations is
        inferior to 0.1%. It is then assumed that the trucks are correctly sized.

        :returns: Does not return anything. Modifies ``self.array`` in place.

        """

        diff = 1.0
        arr = np.array([])

        self["is_compliant"] = True
        self["is_available"] = True

        print("Finding solutions for trucks...")

        while abs(diff) > 0.001 or np.std(arr[-10:]) > 0.05 or len(arr) < 7:

            old_payload = self["available payload"].sum().values

            self.set_vehicle_masses()
            self.set_power_parameters()
            self.set_component_masses()
            self.set_auxiliaries()
            self.set_fuel_cell_parameters()
            self.calculate_ttw_energy()
            self.set_share_recuperated_energy()
            self.set_battery_fuel_cell_replacements()
            self.set_energy_stored_properties()

            if len(self.array.year.values) > 1:
                # if there are vehicles after 2020, we need to ensure CO2 standards compliance
                # return an array with non-compliant vehicles
                non_compliant_vehicles = self.adjust_combustion_power_share()
                arr = np.append(arr, non_compliant_vehicles.sum())
            else:
                arr = np.append(arr, [0])
                non_compliant_vehicles = 0

            self.set_vehicle_masses()

            diff = (self["available payload"].sum().values - old_payload) / self[
                "available payload"
            ].sum()

        self.adjust_cost()
        self.set_electric_utility_factor(electric_utility_factor)
        self.set_electricity_consumption()
        self.set_costs()
        self.set_particulates_emission()
        self.set_noise_emissions()
        self.set_hot_emissions()
        self.create_PHEV()
        self.drop_hybrid()

        self.array.values = np.clip(self.array.values, 0, None)

        print("")
        print("'-' vehicle with driving mass superior to the permissible gross weight.")
        print("'*' vehicle that does not comply with the set energy reduction target.")
        print("'/' vehicle not available for the specified year.")

        self["is_compliant"] *= self["driving mass"] < self["gross mass"]

        # If the number of remaining non-compliant vehicles is not zero, then
        if len([y for y in self.array.year.values if y > 2020]) > 0:

            l_pwt = [
                p for p in self.array.powertrain.values if p in ["ICEV-d", "ICEV-g"]
            ]

            if len(l_pwt) > 0:

                self.array.loc[
                    dict(
                        powertrain=l_pwt,
                        parameter="is_compliant",
                        year=[y for y in self.array.year.values if y > 2020],
                    )
                ] = np.logical_not(non_compliant_vehicles).astype(int)

        # Indicate vehicles not available before 2020
        l_pwt = [
            p
            for p in self.array.powertrain.values
            if p in ["BEV", "FCEV", "PHEV-d", "HEV-d"]
        ]

        if len(l_pwt) > 0:

            self.array.loc[
                dict(
                    powertrain=l_pwt,
                    parameter="is_available",
                    year=[y for y in self.array.year.values if y < 2020],
                )
            ] = 0

        t = PrettyTable(
            ["Payload (in tons)"] + self.array.coords["size"].values.tolist()
        )

        for pt in self.array.coords["powertrain"].values:
            for y in self.array.coords["year"].values:

                row = [pt + ", " + str(y)]

                # indicate vehicles with lower cargo
                # as a result of curb mass being too large
                vals = np.asarray(
                    [
                        np.round(v[2][0])
                        if (v[0][0] - v[1][0]) > 0
                        else f"-{np.round(v[2][0])}-"
                        for v in (
                            self.array.sel(
                                parameter=["gross mass", "driving mass", "cargo mass"],
                                powertrain=pt,
                                year=y,
                            )
                            / 1000
                        ).values.tolist()
                    ]
                )

                # indicate vehicles that do not comply with energy target
                vals = np.where(
                    self.array.sel(
                        parameter="is_compliant",
                        powertrain=pt,
                        year=y,
                        value="reference"
                        if "reference" in self.array.coords["value"]
                        else 0,
                    ).values,
                    vals,
                    [str(v) + "*" for v in vals],
                )

                # indicate vehicles that are not commercially available
                vals = np.where(
                    self.array.sel(
                        parameter="is_available",
                        powertrain=pt,
                        year=y,
                        value="reference"
                        if "reference" in self.array.coords["value"]
                        else 0,
                    ).values,
                    vals,
                    "/",
                )

                t.add_row(row + vals.tolist())
        print(t)

    def set_cargo_mass_and_annual_mileage(self, payload):

        """Set the cargo mass and annual mileage of the vehicles."""

        with open(CARGO_MASSES, "r", encoding="utf-8") as stream:
            generic_payload = yaml.safe_load(stream)

        payload = payload or generic_payload

        for s in self.array.coords["size"].values:
            if "payload" in payload:
                if self.cycle in payload["payload"]:
                    if s in payload["payload"][self.cycle]:
                        self.array.loc[dict(size=s, parameter="cargo mass")] = payload[
                            "payload"
                        ][self.cycle][s]

            if "annual mileage" in payload:
                if self.cycle in payload["annual mileage"]:
                    if s in payload["annual mileage"][self.cycle]:
                        self.array.loc[
                            dict(size=s, parameter="kilometers per year")
                        ] = payload["annual mileage"][self.cycle][s]

    def set_battery_preferences(self):

        for key, val in self.energy_storage["electric"].items():
            pwt, size, year = key

            if (
                val is not None
                and pwt in self.array.coords["powertrain"].values
                and size in self.array.coords["size"].values
                and year in self.array.coords["year"].values
            ):

                cell_params = self.array.loc[
                    dict(
                        powertrain=pwt,
                        size=size,
                        year=year,
                        parameter=[
                            f"battery cell energy density, {val.split('-')[0].strip()}",
                            f"battery cell mass share, {val.split('-')[0].strip()}",
                            f"battery cycle life, {val.split('-')[0].strip()}",
                        ],
                    )
                ]

                self.array.loc[
                    dict(
                        powertrain=pwt,
                        size=size,
                        year=year,
                        parameter=[
                            "battery cell energy density",
                            "battery cell mass share",
                            "battery cycle life",
                        ],
                    )
                ] = cell_params.values

    def adjust_combustion_power_share(self):
        """
        If the exhaust CO2 emissions exceed the targets defined in `self.emission_target`,
        compared to 2020, we decrement the power supply share of the combustion engine.

        :returns: `is_compliant`, whether all vehicles are compliant or not.
        """

        list_target_years = [2020] + list(self.energy_target.keys())
        list_target_vals = [1] + list(self.energy_target.values())
        # years under target
        actual_years = [y for y in self.array.year.values if y > 2020]

        if len(actual_years) > 0:

            l_pwt = [
                p for p in self.array.powertrain.values if p in ["ICEV-d", "ICEV-g"]
            ]

            if len(l_pwt) > 0:

                fc = (
                    self.array.loc[:, l_pwt, "fuel mass", :]
                    / self.array.loc[:, l_pwt, "target range", :]
                ).interp(year=list_target_years, kwargs={"fill_value": "extrapolate"})

                fc[:, :, :, :] = (
                    fc[:, :, 0, :].values
                    * np.array(list_target_vals).reshape((-1, 1, 1, 1))
                ).transpose(1, 2, 0, 3)

                years_after_last_target = [
                    y for y in actual_years if y > list_target_years[-1]
                ]

                list_years = list_target_years + actual_years
                list_years = list(set(list_years))
                fc = fc.interp(year=list_years, kwargs={"fill_value": "extrapolate"})

                if (
                    len(years_after_last_target) > 0
                    and list_target_years[-1] in fc.year.values
                ):
                    fc.loc[dict(year=years_after_last_target)] = fc.loc[
                        dict(year=list_target_years[-1])
                    ].values[:, :, None, :]

                fc = fc.loc[dict(year=actual_years)]

                arr = (
                    fc.values
                    < (
                        self.array.loc[:, l_pwt, "fuel mass", actual_years]
                        / self.array.loc[:, l_pwt, "target range", actual_years]
                    ).values
                )

                if arr.sum() > 0:
                    new_shares = self.array.loc[
                        dict(
                            powertrain=l_pwt,
                            parameter="combustion power share",
                            year=actual_years,
                        )
                    ] - (arr * 0.02)
                    self.array.loc[
                        dict(
                            powertrain=l_pwt,
                            parameter="combustion power share",
                            year=actual_years,
                        )
                    ] = np.clip(new_shares, 0.6, 1)
                return arr
            else:
                return np.array([])
        else:
            return np.array([])

    def adjust_cost(self):
        """
        This method adjusts costs of energy storage over time, to correct for the overly optimistic linear
        interpolation between years.

        """

        n_iterations = self.array.shape[-1]
        n_year = len(self.array.year.values)

        # If uncertainty is not considered, teh cost factor equals 1.
        # Otherwise, a variability of +/-30% is added.

        if n_iterations == 1:
            cost_factor = 1

            # reflect a scaling effect for fuel cells
            # according to
            # FCEV trucks should cost the triple of an ICEV-d in 2020
            cost_factor_fcev = 5
        else:
            if "reference" in self.array.value.values.tolist():
                cost_factor = np.ones((n_iterations, 1))
                cost_factor_fcev = np.full((n_iterations, 1), 5)
            else:
                cost_factor = np.random.triangular(0.7, 1, 1.3, (n_iterations, 1))
                cost_factor_fcev = np.random.triangular(3, 5, 6, (n_iterations, 1))

        # Correction of hydrogen tank cost, per kg
        if "FCEV" in self.array.powertrain.values.tolist():
            self.array.loc[:, ["FCEV"], "fuel tank cost per kg", :, :] = np.reshape(
                (1.078e58 * np.exp(-6.32e-2 * self.array.year.values) + 3.43e2)
                * cost_factor_fcev,
                (1, 1, n_year, n_iterations),
            )

            # Correction of fuel cell stack cost, per kW
            self.array.loc[:, ["FCEV"], "fuel cell cost per kW", :, :] = np.reshape(
                (3.15e66 * np.exp(-7.35e-2 * self.array.year.values) + 2.39e1)
                * cost_factor_fcev,
                (1, 1, n_year, n_iterations),
            )

        # Correction of energy battery system cost, per kWh
        l_pwt = [
            p
            for p in self.array.powertrain.values
            if p in ["BEV", "PHEV-e", "PHEV-c-d"]
        ]

        if len(l_pwt) > 0:
            self.array.loc[:, l_pwt, "energy battery cost per kWh", :, :] = np.reshape(
                (2.75e86 * np.exp(-9.61e-2 * self.array.year.values) + 5.059e1)
                * cost_factor,
                (1, 1, n_year, n_iterations),
            )

        # Correction of power battery system cost, per kW
        l_pwt = [
            p
            for p in self.array.powertrain.values
            if p in ["ICEV-d", "ICEV-g", "PHEV-c-d", "FCEV", "HEV-d"]
        ]

        if len(l_pwt) > 0:
            self.array.loc[:, l_pwt, "power battery cost per kW", :, :] = np.reshape(
                (8.337e40 * np.exp(-4.49e-2 * self.array.year.values) + 11.17)
                * cost_factor,
                (1, 1, n_year, n_iterations),
            )

        # Correction of combustion powertrain cost for ICEV-g
        if "ICEV-g" in self.array.powertrain.values:
            self.array.loc[
                :,
                ["ICEV-g"],
                "combustion powertrain cost per kW",
                :,
                :,
            ] = np.reshape(
                (5.92e160 * np.exp(-0.1819 * self.array.year.values) + 26.76)
                * cost_factor,
                (1, 1, n_year, n_iterations),
            )

    def drop_hybrid(self):
        """
        This method drops the powertrains `PHEV-c-p`, `PHEV-c-d` and `PHEV-e` as they were only used to create the
        `PHEV` powertrain.
        :returns: Does not return anything. Modifies ``self.array`` in place.
        """
        l_pwt = [
            p for p in self.array.powertrain.values if p not in ["PHEV-c-d", "PHEV-e"]
        ]
        self.array = self.array.sel(powertrain=l_pwt)

    def set_electricity_consumption(self):
        """
        This method calculates the total electricity consumption for BEV and plugin-hybrid vehicles
        :returns: Does not return anything. Modifies ``self.array`` in place.
        """
        l_pwt = [p for p in self.array.powertrain.values if p in ["BEV", "PHEV-e"]]

        for pt in l_pwt:
            self.array.loc[dict(powertrain=pt, parameter="electricity consumption")] = (
                self.array.loc[dict(powertrain=pt, parameter="TtW energy")]
                / self.array.loc[
                    dict(powertrain=pt, parameter="battery charge efficiency")
                ]
            ) / 3600

    def calculate_ttw_energy(self):
        """
        This method calculates the energy required to operate auxiliary services as well
        as to move the vehicle. The sum is stored under the parameter label "TtW energy" in :attr:`self.array`.

        """
        self.energy = xr.DataArray(
            np.zeros(
                (
                    len(self.array.coords["size"]),
                    len(self.array.coords["powertrain"]),
                    9,
                    len(self.array.coords["year"]),
                    len(self.array.coords["value"]),
                    self.ecm.cycle.shape[0],
                )
            ).astype("float32"),
            coords=[
                self.array.coords["size"],
                self.array.coords["powertrain"],
                [
                    "auxiliary energy",
                    "motive energy",
                    "motive energy at wheels",
                    "recuperated energy",
                    "recuperated energy at wheels",
                    "transmission efficiency",
                    "engine efficiency",
                    "power load",
                    "negative motive energy",
                ],
                self.array.coords["year"],
                self.array.coords["value"],
                np.arange(self.ecm.cycle.shape[0]),
            ],
            dims=["size", "powertrain", "parameter", "year", "value", "second"],
        )

        motive_power, recuperated_power, distance = self.ecm.motive_energy_per_km(
            driving_mass=self["driving mass"],
            rr_coef=self["rolling resistance coefficient"],
            drag_coef=self["aerodynamic drag coefficient"],
            frontal_area=self["frontal area"],
            recuperation_efficiency=self["recuperation efficiency"],
            motor_power=self["electric power"],
        )

        self.energy.loc[dict(parameter="auxiliary energy")] = (
            self["auxiliary power demand"].values[..., None] / 1000
        )

        self.energy.loc[dict(parameter="motive energy at wheels")] = np.clip(
            motive_power.T, 0, self["power"].values[..., None]
        )

        self.energy.loc[dict(parameter="negative motive energy")] = (
            np.clip(motive_power.T, None, 0) * -1
        )

        self.energy.loc[dict(parameter="recuperated energy at wheels")] = (
            np.clip(recuperated_power.T, 0, self["electric power"].values[..., None])
            * -1
        )

        self.energy.loc[dict(parameter="power load")] = (
            motive_power.T + recuperated_power.T
        ) / self["combustion power"].values[..., None]

        l_pwt = [
            p for p in self.array.powertrain.values if p in ["BEV", "FCEV", "PHEV-e"]
        ]

        idx = [i for i, j in enumerate(self.array.powertrain.values) if j in l_pwt]

        if len(l_pwt) > 0:

            self.energy.loc[dict(parameter="power load", powertrain=l_pwt)] = (
                motive_power.T[:, idx, ...] + recuperated_power.T[:, idx, ...]
            ) / self.array.sel(parameter="electric power", powertrain=l_pwt).values[
                ..., None
            ]

        self.energy.loc[dict(parameter="power load")] = np.clip(
            self.energy.loc[dict(parameter="power load")], 0, 1
        )

        self.energy.loc[dict(parameter="transmission efficiency")] = np.clip(
            np.interp(
                self.energy.loc[dict(parameter="power load")],
                [0, 0.025, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                [0, 0.6, 0.75, 0.85, 0.88, 0.91, 0.91, 0.91, 0.91, 0.91, 0.91, 0.91],
            ),
            0.2,
            1,
        )

        # dirty correction for BEVs and FCEVs
        # to reach 90-93% efficiency
        # as documented in
        # https://www.research-collection.ethz.ch/bitstream/handle/20.500.11850/121450/1/2539-07.pdf

        l_pwt = [
            p
            for p in self.array.powertrain.values
            if p in ["ICEV-d", "HEV-d", "PHEV-c-d", "ICEV-g"]
        ]

        if len(l_pwt) > 0:

            self.energy.loc[
                dict(
                    parameter="engine efficiency",
                    powertrain=l_pwt,
                )
            ] = np.clip(
                np.interp(
                    self.energy.loc[dict(parameter="power load", powertrain=l_pwt)],
                    [0, 0.025, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                    [
                        0,
                        0.2,
                        0.25,
                        0.32,
                        0.385,
                        0.41,
                        0.42,
                        0.42,
                        0.42,
                        0.42,
                        0.42,
                        0.42,
                    ],
                ),
                0.2,
                1,
            )

        # Correction for CNG trucks
        if "ICEV-g" in self.array.powertrain.values:
            self.energy.loc[
                dict(parameter="engine efficiency", powertrain="ICEV-g")
            ] *= 1 - self.array.sel(
                parameter="CNG engine efficiency correction factor",
                powertrain="ICEV-g",
            )

        # correction for BEVs and FCEVs
        l_pwt = [
            p for p in self.array.powertrain.values if p in ["BEV", "FCEV", "PHEV-e"]
        ]
        if len(l_pwt) > 0:
            self.energy.loc[
                dict(
                    parameter=["engine efficiency", "transmission efficiency"],
                    powertrain=l_pwt,
                )
            ] = self.array.loc[
                dict(
                    parameter=["engine efficiency", "transmission efficiency"],
                    powertrain=l_pwt,
                )
            ].values[
                ..., None
            ]

        self.energy.loc[dict(parameter="motive energy")] = (
            self.energy.loc[dict(parameter="motive energy at wheels")]
            / self.energy.loc[dict(parameter="transmission efficiency")]
        )

        self.energy.loc[dict(parameter="motive energy")] = np.clip(
            self.energy.loc[dict(parameter="motive energy")],
            1,
            self["power"].values[..., None],
        )

        self.energy.loc[dict(parameter="motive energy")] /= self.energy.loc[
            dict(parameter="engine efficiency")
        ]

        self.energy.loc[dict(parameter="recuperated energy")] = np.clip(
            (
                self.energy.loc[dict(parameter="recuperated energy at wheels")]
                * (
                    self.energy.loc[dict(parameter="transmission efficiency")]
                    * self.array.loc[dict(parameter="battery charge efficiency")]
                    * self.array.loc[dict(parameter="battery discharge efficiency")]
                )
            ),
            self["electric power"].values[..., None] * -1,
            0,
        )

        self.energy = self.energy.fillna(0)
        self.energy *= np.isfinite(self.energy)

        self["TtW energy"] = (
            self.energy.sel(
                parameter=["motive energy", "auxiliary energy", "recuperated energy"]
            )
            .sum(dim=["second", "parameter"])
            .T
            / distance
        ).T

        self["TtW efficiency"] = np.nanmean(
            np.where(
                self.energy.loc[dict(parameter="power load")] == 0,
                np.nan,
                (
                    self.energy.loc[dict(parameter="transmission efficiency")]
                    * self.energy.loc[dict(parameter="engine efficiency")]
                ),
            ),
            axis=-1,
        )

        # Correction for electric motors
        l_pwt = [p for p in self.array.powertrain.values if p in ["BEV", "PHEV-e"]]

        if len(l_pwt) > 0:
            self.array.loc[
                dict(parameter="TtW efficiency", powertrain=l_pwt)
            ] *= self.array.sel(
                parameter="battery discharge efficiency", powertrain=l_pwt
            )
            self.array.loc[
                dict(parameter="TtW energy", powertrain=l_pwt)
            ] /= self.array.sel(
                parameter="battery discharge efficiency", powertrain=l_pwt
            )

        # Correction for fuel cell stack efficiency
        if "FCEV" in self.array.powertrain.values:
            self.array.loc[
                dict(parameter="TtW efficiency", powertrain=["FCEV"])
            ] *= self.array.sel(
                parameter="fuel cell system efficiency", powertrain=["FCEV"]
            ) * self.array.sel(
                parameter="battery discharge efficiency", powertrain=["FCEV"]
            )
            self.array.loc[
                dict(parameter="TtW energy", powertrain=["FCEV"])
            ] /= self.array.sel(
                parameter="fuel cell system efficiency", powertrain=["FCEV"]
            ) * self.array.sel(
                parameter="battery discharge efficiency", powertrain=["FCEV"]
            )

        self["auxiliary energy"] = (
            self.energy.sel(parameter="auxiliary energy").sum(dim="second").T / distance
        ).T

        pwt = [
            p
            for p in self.array.powertrain.values
            if p not in ["BEV", "PHEV-e", "FCEV"]
        ]

        self.array.loc[
            dict(parameter="engine efficiency", powertrain=pwt)
        ] = np.nanmean(
            np.where(
                self.energy.loc[dict(parameter="power load", powertrain=pwt)] == 0,
                np.nan,
                self.energy.loc[dict(parameter="engine efficiency", powertrain=pwt)],
            ),
            axis=-1,
        )

        self.array.loc[
            dict(parameter="transmission efficiency", powertrain=pwt)
        ] = np.nanmean(
            np.where(
                self.energy.loc[dict(parameter="power load", powertrain=pwt)] == 0,
                np.nan,
                self.energy.loc[
                    dict(parameter="transmission efficiency", powertrain=pwt)
                ],
            ),
            axis=-1,
        )

        # override of TtW energy, provided by the user
        if self.energy_consumption:
            for key, val in self.energy_consumption.items():
                pwt, size, year = key
                if val is not None:
                    self.array.loc[
                        dict(
                            powertrain=pwt, size=size, year=year, parameter="TtW energy"
                        )
                    ] = val

                    self.energy.loc[
                        dict(
                            powertrain=pwt,
                            size=size,
                            year=year,
                            parameter="motive energy",
                        )
                    ] = (
                        val * distance / self.energy.shape[-1]  # kj/km  # km  # seconds
                    ).reshape(
                        1, -1
                    )

        self["TtW energy, combustion mode"] = self["TtW energy"] * (
            self["combustion power share"] > 0
        )
        self["TtW energy, electric mode"] = self["TtW energy"] * (
            self["combustion power share"] == 0
        )

    def set_fuel_cell_parameters(self):
        """
        Specific setup for fuel cells, which are mild hybrids.
        Must be called after :meth:`.set_power_parameters`.
        """

        if "FCEV" in self.array.coords["powertrain"].values:
            with self("FCEV"):
                self["fuel cell system efficiency"] = (
                    self["fuel cell stack efficiency"]
                    / self["fuel cell own consumption"]
                )
                self["fuel cell power share"] = self["fuel cell power share"].clip(
                    min=0, max=1
                )
                self["fuel cell power"] = (
                    self["power"]
                    * self["fuel cell power share"]
                    * self["fuel cell own consumption"]
                )

                # our basic fuel cell mass is based on a car fuel cell with 800 mW/cm2
                # and 1.02 kg/kW
                # the cell power density is adapted for truck use
                # it is decreased comparatively to that of a passenger car
                # to reflect increased durability
                self["fuel cell stack mass"] = (
                    1.02
                    * self["fuel cell power"]
                    * (800 / self["fuel cell power area density"])
                )
                self["fuel cell ancillary BoP mass"] = (
                    self["fuel cell power"]
                    * self["fuel cell ancillary BoP mass per power"]
                )
                self["fuel cell essential BoP mass"] = (
                    self["fuel cell power"]
                    * self["fuel cell essential BoP mass per power"]
                )

                self["battery power"] = self["fuel cell power"] * (
                    1 - self["fuel cell power share"]
                )
                self["battery cell mass"] = (
                    self["battery power"] / self["battery cell power density"]
                )
                self["battery BoP mass"] = self["battery cell mass"] * (
                    1 - self["battery cell mass share"]
                )

    def set_auxiliaries(self):
        """
        Calculates the power needed to operate the auxiliary services of the vehicle (heating, cooling).

        The demand for heat and cold are expressed as a fraction of the heating and cooling capacities

        .. note:

            Auxiliary power demand (W) = Base auxiliary power (W) +
            (Heating demand (dimensionless, between 0 and 1) * Heating power (W)) +
            (Cooling demand (dimensionless, between 0 and 1) * Cooling power (W))

        """
        self["auxiliary power demand"] = (
            self["auxilliary power base demand"]
            + self["heating thermal demand"] * self["heating energy consumption"]
            + self["cooling thermal demand"] * self["cooling energy consumption"]
        )

    def set_battery_fuel_cell_replacements(self):
        """
        This methods calculates the number of replacement batteries needed to match the vehicle lifetime.
        Given the chemistry used, the cycle life is known. Given the lifetime kilometers and the kilometers per charge,
        the number of charge cycles can be inferred.

        If the battery lifetime surpasses the vehicle lifetime, 100% of the burden of the battery production
        is allocated to the vehicle. Also, the number of replacement is rounded up. This means that the entirety
        of the battery replacement is allocated to the vehicle (and not to its potential second life).

        """
        # Number of replacement of battery is rounded *up*

        list_electric = [
            pwt for pwt in ["BEV"] if pwt in self.array.coords["powertrain"].values
        ]

        self.array.loc[
            dict(parameter="battery lifetime replacements", powertrain=list_electric)
        ] = finite(
            np.ceil(
                np.clip(
                    (
                        # number of charge cycles needed divided by the expected cycle life
                        (
                            self.array.loc[
                                dict(
                                    parameter="lifetime kilometers",
                                    powertrain=list_electric,
                                )
                            ]
                            * (
                                self.array.loc[
                                    dict(
                                        parameter="TtW energy", powertrain=list_electric
                                    )
                                ]
                                / 3600
                            )
                        )
                        / self.array.loc[
                            dict(
                                parameter="electric energy stored",
                                powertrain=list_electric,
                            )
                        ]
                        / self.array.loc[
                            dict(
                                parameter="battery cycle life", powertrain=list_electric
                            )
                        ]
                    )
                    - 1,
                    1,
                    None,
                )
            )
        )

        # The number of fuel cell replacements is based on the average distance driven
        # with a set of fuel cells given their lifetime expressed in hours of use.
        # The number is replacement is rounded *up* as we assume no allocation of burden
        # with a second life

        if "FCEV" in self.array.coords["powertrain"].values:
            with self("FCEV") as pt:
                pt["fuel cell lifetime replacements"] = np.ceil(
                    np.clip(
                        (
                            pt["lifetime kilometers"]
                            / (
                                pt.ecm.cycle.sum(axis=0)
                                / pt.ecm.cycle.shape[0]
                                * pt["fuel cell lifetime hours"].T
                            )
                        )
                        - 1,
                        0,
                        5,
                    )
                )

    def set_vehicle_masses(self):
        """
        Define ``curb mass``, ``driving mass``, and ``cargo mass``.

            * `curb mass <https://en.wikipedia.org/wiki/Curb_weight>`__ is the mass of the vehicle and fuel, without people or cargo.
            * ``cargo mass`` is the mass of the cargo and passengers.
            * ``driving mass`` is the ``curb mass`` plus ``cargo mass``.

        .. note::
            driving mass = cargo mass + driving mass

        """

        # Base components, common to all powertrains
        base_components = [
            "glider base mass",
            "suspension mass",
            "braking system mass",
            "wheels and tires mass",
            "cabin mass",
            "electrical system mass",
            "other components mass",
            "transmission mass",
        ]

        self["curb mass"] = self[base_components].sum(axis=2) * (
            1 - self["lightweighting"]
        )

        curb_mass_includes = [
            "fuel mass",
            "charger mass",
            "converter mass",
            "inverter mass",
            "power distribution unit mass",
            # Updates with set_components_mass
            "combustion engine mass",
            # Updates with set_components_mass
            "electric engine mass",
            # Updates with set_components_mass
            "exhaust system mass",
            "fuel cell stack mass",
            "fuel cell ancillary BoP mass",
            "fuel cell essential BoP mass",
            "battery cell mass",
            "battery BoP mass",
            "fuel tank mass",
        ]
        self["curb mass"] += self[curb_mass_includes].sum(axis=2)

        self["total cargo mass"] = (
            self["average passengers"] * self["average passenger mass"]
        ) + self["cargo mass"]

        self["driving mass"] = (
            self["curb mass"]
            + self["cargo mass"]
            + (self["average passengers"] * self["average passenger mass"])
        )

        self["available payload"] = (
            self["gross mass"]
            - self["curb mass"]
            - (self["average passengers"] * self["average passenger mass"])
        )

        self["cargo mass"] = np.clip(self["cargo mass"], 0, self["available payload"])

        self["capacity utilization"] = np.clip(
            (self["cargo mass"] / self["available payload"]), 0, 1
        )

    def set_power_parameters(self):
        """Set electric and combustion motor powers based on input parameter ``power to mass ratio``."""
        # Convert from W/kg to kW
        self["power"] = np.clip(
            self["power to mass ratio"] * self["curb mass"] / 1000, 0, 450
        )
        self["combustion power share"] = self["combustion power share"].clip(
            min=0, max=1
        )
        self["combustion power"] = self["power"] * self["combustion power share"]
        self["electric power"] = self["power"] * (1 - self["combustion power share"])

    def set_component_masses(self):
        self["combustion engine mass"] = (
            self["combustion power"] * self["engine mass per power"]
            + self["engine fixed mass"]
        )
        self["electric engine mass"] = np.clip(
            (24.56 * np.exp(0.0078 * self["electric power"])), 0, 600
        ) * (self["electric power"] > 0)

        self["transmission mass"] = (self["gross mass"] / 1000) * self[
            "transmission mass per ton of gross weight"
        ]

        self["inverter mass"] = (
            self["electric power"] * self["inverter mass per power"]
            + self["inverter fix mass"]
        )

    def set_share_recuperated_energy(self):
        """Calculate the share of recuperated energy, over the total negative motive energy"""

        self["share recuperated energy"] = (
            (
                self.energy.loc[dict(parameter="recuperated energy at wheels")].sum(
                    dim="second"
                )
                * -1
            )
            * self["engine efficiency"]
            * self["transmission efficiency"]
        ) / self.energy.loc[dict(parameter="negative motive energy")].sum(dim="second")

        if "PHEV-d" in self.array.powertrain.values:
            self.array.loc[
                dict(powertrain="PHEV-c-d", parameter="share recuperated energy")
            ] = self.array.loc[
                dict(powertrain="PHEV-e", parameter="share recuperated energy")
            ]

    def set_electric_utility_factor(self, uf: float = None) -> None:
        """
        The electric utility factor
        is the share of km driven in battery-depleting mode
        over the required range autonomy.
        Scania's PHEV tractor can drive 60 km in electric mode
        :return:
        """
        if "PHEV-e" in self.array.coords["powertrain"].values:

            range = (
                self.array.loc[
                    dict(parameter="electric energy stored", powertrain="PHEV-d")
                ]
                * self.array.loc[dict(parameter="battery DoD", powertrain="PHEV-e")]
            ) / (
                self.array.loc[dict(parameter="TtW energy", powertrain="PHEV-e")]
                / 1000
                / 3.6
            )

            if uf is None:
                self.array.loc[
                    dict(powertrain="PHEV-e", parameter="electric utility factor")
                ] = (
                    range
                    / self.array.loc[
                        dict(powertrain="PHEV-e", parameter="target range")
                    ]
                )
            else:
                self.array.loc[
                    dict(powertrain="PHEV-e", parameter="electric utility factor")
                ] = uf

    def create_PHEV(self):
        """PHEV-p/d is the range-weighted average between PHEV-c-p/PHEV-c-d and PHEV-e."""

        if "PHEV-e" in self.array.coords["powertrain"].values:
            self.array.loc[{"powertrain": "PHEV-d"}] = (
                self.array.loc[{"powertrain": "PHEV-e"}]
                * self.array.loc[
                    {"powertrain": "PHEV-e", "parameter": "electric utility factor"}
                ]
            ) + (
                self.array.loc[{"powertrain": "PHEV-c-d"}]
                * (
                    1
                    - self.array.loc[
                        {"powertrain": "PHEV-e", "parameter": "electric utility factor"}
                    ]
                )
            )

            self.array.loc[
                {"powertrain": "PHEV-d", "parameter": "electric utility factor"}
            ] = self.array.loc[
                {"powertrain": "PHEV-e", "parameter": "electric utility factor"}
            ]

            self.energy.loc[
                dict(
                    parameter=[
                        "auxiliary energy",
                        "motive energy",
                        "motive energy at wheels",
                        "recuperated energy",
                        "recuperated energy at wheels",
                        "transmission efficiency",
                        "engine efficiency",
                        "power load",
                        "negative motive energy",
                    ],
                    powertrain=["PHEV-d"],
                )
            ] = (
                self.array.loc[
                    dict(parameter="electric utility factor", powertrain=["PHEV-e"])
                ]
                * self.energy.loc[
                    dict(
                        parameter=[
                            "auxiliary energy",
                            "motive energy",
                            "motive energy at wheels",
                            "recuperated energy",
                            "recuperated energy at wheels",
                            "transmission efficiency",
                            "engine efficiency",
                            "power load",
                            "negative motive energy",
                        ],
                        powertrain=["PHEV-e"],
                    )
                ]
            ).values.transpose(
                0, 1, 4, 2, 3, 5
            ) + (
                (
                    1
                    - self.array.loc[
                        dict(parameter="electric utility factor", powertrain="PHEV-e")
                    ]
                )
                * self.energy.loc[
                    dict(
                        parameter=[
                            "auxiliary energy",
                            "motive energy",
                            "motive energy at wheels",
                            "recuperated energy",
                            "recuperated energy at wheels",
                            "transmission efficiency",
                            "engine efficiency",
                            "power load",
                            "negative motive energy",
                        ],
                        powertrain=["PHEV-c-d"],
                    )
                ]
            ).values.transpose(
                0, 3, 4, 1, 2, 5
            )

            # We store the tank-to-wheel energy consumption
            # in combustion and electric mode separately
            self.array.loc[
                dict(parameter="TtW energy, combustion mode", powertrain="PHEV-d")
            ] = self.array.loc[dict(parameter="TtW energy", powertrain="PHEV-c-d")]

            self.array.loc[
                dict(parameter="TtW energy, electric mode", powertrain="PHEV-d")
            ] = self.array.loc[dict(parameter="TtW energy", powertrain="PHEV-e")]

    def set_energy_stored_properties(self):
        """
        First, fuel mass is defined. It is dependent on the range required.
        Then batteries are sized, depending on the range required and the energy consumption.
        :return:
        """
        d_map_fuel = {
            "ICEV-d": "diesel",
            "HEV-d": "diesel",
            "PHEV-c-d": "diesel",
            "ICEV-g": "cng",
            "FCEV": "hydrogen",
        }

        for pt in [
            pwt
            for pwt in ["ICEV-d", "HEV-d", "PHEV-c-d", "ICEV-g"]
            if pwt in self.array.coords["powertrain"].values
        ]:

            # calculate the average LHV based on fuel blend
            fuel_type = d_map_fuel[pt]
            primary_fuel_share = self.fuel_blend[fuel_type]["primary"]["share"]
            primary_fuel_lhv = self.fuel_blend[fuel_type]["primary"]["lhv"]
            secondary_fuel_share = self.fuel_blend[fuel_type]["secondary"]["share"]
            secondary_fuel_lhv = self.fuel_blend[fuel_type]["secondary"]["lhv"]

            blend_lhv = (np.array(primary_fuel_share) * primary_fuel_lhv) + (
                np.array(secondary_fuel_share) * secondary_fuel_lhv
            )

            self.array.loc[dict(powertrain=pt, parameter="fuel mass")] = (
                self.array.loc[dict(powertrain=pt, parameter="target range")]
                * (self.array.loc[dict(powertrain=pt, parameter="TtW energy")] / 1000)
            ) / blend_lhv.reshape((-1, 1))

            self.array.loc[dict(powertrain=pt, parameter="oxidation energy stored")] = (
                self.array.loc[dict(powertrain=pt, parameter="fuel mass")]
                * blend_lhv.reshape((-1, 1))
            ) / 3.6

            if pt == "ICEV-g":
                # Based on manufacturer data
                # We use a four-cylinder configuration
                # Of 320L each
                # A cylinder of 320L @ 200 bar can hold 57.6 kg of CNG
                nb_cylinder = np.ceil(
                    self.array.loc[dict(powertrain=pt, parameter="fuel mass")] / 57.6
                )

                self.array.loc[dict(powertrain=pt, parameter="fuel tank mass")] = (
                    (0.018 * np.power(57.6, 2)) - (0.6011 * 57.6) + 52.235
                ) * nb_cylinder

            else:
                # From Wolff et al. 2020, Sustainability, DOI: 10.3390/su12135396.
                # We adjusted though the intercept from the original function (-54)
                # because we size here trucks based on the range autonomy
                # a low range autonomy would produce a negative fuel tank mass
                self.array.loc[dict(powertrain=pt, parameter="fuel tank mass")] = (
                    17.159
                    * np.log(
                        self.array.loc[dict(powertrain=pt, parameter="fuel mass")]
                        * (1 / 0.832)
                    )
                    - 30
                )

        for pt in [
            pwt
            for pwt in ["ICEV-d", "HEV-d", "PHEV-c-d", "ICEV-g"]
            if pwt in self.array.coords["powertrain"].values
        ]:
            self.array.loc[
                dict(powertrain=pt, parameter="battery power")
            ] = self.array.loc[dict(powertrain=pt, parameter="electric power")]
            self.array.loc[dict(powertrain=pt, parameter="battery cell mass")] = (
                self.array.loc[dict(powertrain=pt, parameter="battery power")]
                / self.array.loc[
                    dict(powertrain=pt, parameter="battery cell power density")
                ]
            )
            self.array.loc[
                dict(powertrain=pt, parameter="battery cell mass share")
            ] = np.clip(
                self.array.loc[
                    dict(powertrain=pt, parameter="battery cell mass share")
                ],
                0,
                1,
            )

            self.array.loc[
                dict(powertrain=pt, parameter="battery BoP mass")
            ] = self.array.loc[dict(powertrain=pt, parameter="battery cell mass")] * (
                1
                - self.array.loc[
                    dict(powertrain=pt, parameter="battery cell mass share")
                ]
            )

        for pt in [
            pwt
            for pwt in ["BEV", "PHEV-e"]
            if pwt in self.array.coords["powertrain"].values
        ]:
            self.array.loc[dict(powertrain=pt, parameter="electric energy stored")] = (
                (
                    self.array.loc[dict(powertrain=pt, parameter="target range")]
                    * (
                        self.array.loc[dict(powertrain=pt, parameter="TtW energy")]
                        / 1000
                    )
                )
                / self.array.loc[dict(powertrain=pt, parameter="battery DoD")]
                / 3.6
            )

            self.array.loc[dict(powertrain=pt, parameter="battery cell mass")] = (
                self.array.loc[dict(powertrain=pt, parameter="electric energy stored")]
                / self.array.loc[
                    dict(powertrain=pt, parameter="battery cell energy density")
                ]
            )

            self.array.loc[dict(powertrain=pt, parameter="energy battery mass")] = (
                self.array.loc[dict(powertrain=pt, parameter="battery cell mass")]
                / self.array.loc[
                    dict(powertrain=pt, parameter="battery cell mass share")
                ]
            )

            self.array.loc[dict(powertrain=pt, parameter="battery BoP mass")] = (
                self.array.loc[dict(powertrain=pt, parameter="energy battery mass")]
                - self.array.loc[dict(powertrain=pt, parameter="battery cell mass")]
            )

        if "FCEV" in self.array.coords["powertrain"].values:

            self.array.loc[dict(powertrain="FCEV", parameter="fuel mass")] = (
                self.array.loc[dict(powertrain="FCEV", parameter="target range")]
                * (
                    self.array.loc[dict(powertrain="FCEV", parameter="TtW energy")]
                    / 1000
                )
            ) / self.array.loc[dict(powertrain="FCEV", parameter="LHV fuel MJ per kg")]

            self.array.loc[
                dict(powertrain="FCEV", parameter="oxidation energy stored")
            ] = (
                self.array.loc[dict(powertrain="FCEV", parameter="fuel mass")]
                * 120
                / 3.6
            )

            # Based on manufacturer data
            # We use a four-cylinder configuration
            # Of 650L each
            # A cylinder of 650L @ 700 bar can hold 14.4 kg of H2
            nb_cylinder = np.ceil(
                self.array.loc[dict(powertrain="FCEV", parameter="fuel mass")] / 14.4
            )

            self.array.loc[dict(powertrain="FCEV", parameter="fuel tank mass")] = (
                (
                    -0.1916
                    * np.power(
                        14.4,
                        2,
                    )
                )
                + (14.586 * 14.4)
                + 10.805
            ) * nb_cylinder

            # Fuel cell buses do also have a battery, which capacity
            # corresponds roughly to 6% of the capacity contained in the
            # H2 tank

            self.array.loc[
                dict(powertrain="FCEV", parameter="electric energy stored")
            ] = 20 + (
                self.array.loc[dict(powertrain="FCEV", parameter="fuel mass")]
                * 120
                / 3.6
                * 0.06
            )

            self.array.loc[dict(powertrain="FCEV", parameter="battery cell mass")] = (
                self.array.loc[
                    dict(powertrain="FCEV", parameter="electric energy stored")
                ]
                / self.array.loc[
                    dict(powertrain="FCEV", parameter="battery cell energy density")
                ]
            )

            self.array.loc[dict(powertrain="FCEV", parameter="energy battery mass")] = (
                self.array.loc[dict(powertrain="FCEV", parameter="battery cell mass")]
                / self.array.loc[
                    dict(powertrain="FCEV", parameter="battery cell mass share")
                ]
            )

            self.array.loc[dict(powertrain="FCEV", parameter="battery BoP mass")] = (
                self.array.loc[dict(powertrain="FCEV", parameter="energy battery mass")]
                - self.array.loc[dict(powertrain="FCEV", parameter="battery cell mass")]
            )

    def set_costs(self):

        glider_components = [
            "glider base mass",
            "suspension mass",
            "braking system mass",
            "wheels and tires mass",
            "cabin mass",
        ]

        self["glider cost"] = np.clip(
            ((38747 * np.log(self[glider_components].sum(dim="parameter"))) - 252194),
            33500,
            110000,
        )

        # Discount glider cost for 40t and 60t trucks because of the added trailer mass

        for size in [
            s for s in ["40t", "60t"] if s in self.array.coords["size"].values
        ]:
            self.array.loc[dict(parameter="glider cost", size=size)] *= 0.7

        self["lightweighting cost"] = (
            self["glider base mass"]
            * self["lightweighting"]
            * self["glider lightweighting cost per kg"]
        )
        self["electric powertrain cost"] = (
            self["electric powertrain cost per kW"] * self["electric power"]
        )
        self["combustion powertrain cost"] = (
            self["combustion power"] * self["combustion powertrain cost per kW"]
        )

        self["fuel cell cost"] = self["fuel cell power"] * self["fuel cell cost per kW"]

        self["power battery cost"] = (
            self["battery power"] * self["power battery cost per kW"]
        )
        self["energy battery cost"] = (
            self["energy battery cost per kWh"] * self["electric energy stored"]
        )
        self["fuel tank cost"] = self["fuel tank cost per kg"] * self["fuel mass"]
        # Per ton-km
        self["energy cost"] = (
            self["energy cost per kWh"]
            * self["TtW energy"]
            / 3600
            / (self["cargo mass"] / 1000)
        )

        # For battery, need to divide cost of electricity in battery by efficiency of charging
        for pt in [
            pwt
            for pwt in ["BEV", "PHEV-e"]
            if pwt in self.array.coords["powertrain"].values
        ]:
            self.array.loc[
                dict(powertrain=pt, parameter="energy cost")
            ] /= self.array.loc[
                dict(powertrain=pt, parameter="battery charge efficiency")
            ]

        self["component replacement cost"] = (
            self["energy battery cost"] * self["battery lifetime replacements"]
            + self["fuel cell cost"] * self["fuel cell lifetime replacements"]
        )

        to_markup = [
            "combustion powertrain cost",
            "component replacement cost",
            "electric powertrain cost",
            "energy battery cost",
            "fuel cell cost",
            "fuel tank cost",
            "glider cost",
            "lightweighting cost",
            "power battery cost",
        ]

        self[to_markup] *= self["markup factor"]

        # calculate costs per km:
        self["lifetime"] = self["lifetime kilometers"] / self["kilometers per year"]
        i = self["interest rate"]
        lifetime = self["lifetime"]
        amortisation_factor = ne.evaluate("i + (i / ((1 + i) ** lifetime - 1))")

        purchase_cost_list = [
            "battery onboard charging infrastructure cost",
            "combustion exhaust treatment cost",
            "combustion powertrain cost",
            "electric powertrain cost",
            "energy battery cost",
            "fuel cell cost",
            "fuel tank cost",
            "glider cost",
            "heat pump cost",
            "lightweighting cost",
            "power battery cost",
        ]

        self["purchase cost"] = self[purchase_cost_list].sum(axis=2)

        # per ton-km
        self["amortised purchase cost"] = (
            self["purchase cost"]
            * amortisation_factor
            / (self["cargo mass"] / 1000)
            / self["kilometers per year"]
        )

        # per km
        self["adblue cost"] = (
            self["adblue cost per kg"] * 0.06 * self["fuel mass"]
        ) / self["target range"]
        self["maintenance cost"] = self["maintenance cost per km"]
        self["maintenance cost"] += self["adblue cost"]
        self["maintenance cost"] /= self["cargo mass"] / 1000

        self["insurance cost"] = (
            self["insurance cost per year"]
            / (self["cargo mass"] / 1000)
            / self["kilometers per year"]
        )

        self["toll cost"] = self["toll cost per km"] / (self["cargo mass"] / 1000)

        # simple assumption that component replacement occurs at half of life.
        km_per_year = self["kilometers per year"]
        com_repl_cost = self["component replacement cost"]
        cargo = self["cargo mass"] / 1000

        self["amortised component replacement cost"] = ne.evaluate(
            "(com_repl_cost * ((1 - i) ** lifetime / 2) * amortisation_factor) / km_per_year / cargo"
        )

        self["total cost per km"] = (
            self["energy cost"]
            + self["amortised purchase cost"]
            + self["maintenance cost"]
            + self["insurance cost"]
            + self["toll cost"]
            + self["amortised component replacement cost"]
        )

    def set_particulates_emission(self):
        """
        Calculate the emission of particulates according to
        https://www.eea.europa.eu/ds_resolveuid/6USNA27I4D

        and further disaggregated in:
        https://doi.org/10.1016/j.atmosenv.2020.117886

        for:

        - brake wear
        - tire wear
        - road wear
        - re-suspended road dust

        by considering:

        - vehicle mass
        - driving situation (urban, rural, motorway)

        into the following fractions:

        - PM 2.5
        - PM 10

        Emissions are subdivided in compartments: urban, suburban and rural.

        """

        list_param = [
            "tire wear emissions",
            "brake wear emissions",
            "road wear emissions",
            "road dust emissions",
        ]

        pem = ParticulatesEmissionsModel(
            cycle_name=self.ecm.cycle_name,
            cycle=self.ecm.cycle,
            mass=self["driving mass"],
        )

        res = pem.get_abrasion_emissions()

        self[list_param] = res

        # brake emissions are discounted by the use of regenerative braking
        self["brake wear emissions"] *= 1 - self["share recuperated energy"]

    def set_hot_emissions(self):
        """
        Calculate hot pollutant emissions based on ``driving cycle``.
        The driving cycle is passed to the :class:`HotEmissionsModel` class and :meth:`get_emissions_per_powertrain`
        return emissions per substance per second of driving cycle.
        :return: Does not return anything. Modifies ``self.array`` in place.
        """
        hem = HotEmissionsModel(self.ecm.cycle_name, self.ecm.cycle)

        list_direct_emissions = [
            "Hydrocarbons direct emissions, urban",
            "Carbon monoxide direct emissions, urban",
            "Nitrogen oxides direct emissions, urban",
            "Particulate matters direct emissions, urban",
            "Methane direct emissions, urban",
            "NMVOC direct emissions, urban",
            "Dinitrogen oxide direct emissions, urban",
            "Ammonia direct emissions, urban",
            "Benzene direct emissions, urban",
            "Ethane direct emissions, urban",
            "Propane direct emissions, urban",
            "Butane direct emissions, urban",
            "Pentane direct emissions, urban",
            "Hexane direct emissions, urban",
            "Cyclohexane direct emissions, urban",
            "Heptane direct emissions, urban",
            "Ethene direct emissions, urban",
            "Propene direct emissions, urban",
            "1-Pentene direct emissions, urban",
            "Toluene direct emissions, urban",
            "m-Xylene direct emissions, urban",
            "o-Xylene direct emissions, urban",
            "Formaldehyde direct emissions, urban",
            "Acetaldehyde direct emissions, urban",
            "Benzaldehyde direct emissions, urban",
            "Acetone direct emissions, urban",
            "Methyl ethyl ketone direct emissions, urban",
            "Acrolein direct emissions, urban",
            "Styrene direct emissions, urban",
            "PAH, polycyclic aromatic hydrocarbons direct emissions, urban",
            "Arsenic direct emissions, urban",
            "Selenium direct emissions, urban",
            "Zinc direct emissions, urban",
            "Copper direct emissions, urban",
            "Nickel direct emissions, urban",
            "Chromium direct emissions, urban",
            "Chromium VI direct emissions, urban",
            "Mercury direct emissions, urban",
            "Cadmium direct emissions, urban",
            "Hydrocarbons direct emissions, suburban",
            "Carbon monoxide direct emissions, suburban",
            "Nitrogen oxides direct emissions, suburban",
            "Particulate matters direct emissions, suburban",
            "Methane direct emissions, suburban",
            "NMVOC direct emissions, suburban",
            "Dinitrogen oxide direct emissions, suburban",
            "Ammonia direct emissions, suburban",
            "Benzene direct emissions, suburban",
            "Ethane direct emissions, suburban",
            "Propane direct emissions, suburban",
            "Butane direct emissions, suburban",
            "Pentane direct emissions, suburban",
            "Hexane direct emissions, suburban",
            "Cyclohexane direct emissions, suburban",
            "Heptane direct emissions, suburban",
            "Ethene direct emissions, suburban",
            "Propene direct emissions, suburban",
            "1-Pentene direct emissions, suburban",
            "Toluene direct emissions, suburban",
            "m-Xylene direct emissions, suburban",
            "o-Xylene direct emissions, suburban",
            "Formaldehyde direct emissions, suburban",
            "Acetaldehyde direct emissions, suburban",
            "Benzaldehyde direct emissions, suburban",
            "Acetone direct emissions, suburban",
            "Methyl ethyl ketone direct emissions, suburban",
            "Acrolein direct emissions, suburban",
            "Styrene direct emissions, suburban",
            "PAH, polycyclic aromatic hydrocarbons direct emissions, suburban",
            "Arsenic direct emissions, suburban",
            "Selenium direct emissions, suburban",
            "Zinc direct emissions, suburban",
            "Copper direct emissions, suburban",
            "Nickel direct emissions, suburban",
            "Chromium direct emissions, suburban",
            "Chromium VI direct emissions, suburban",
            "Mercury direct emissions, suburban",
            "Cadmium direct emissions, suburban",
            "Hydrocarbons direct emissions, rural",
            "Carbon monoxide direct emissions, rural",
            "Nitrogen oxides direct emissions, rural",
            "Particulate matters direct emissions, rural",
            "Methane direct emissions, rural",
            "NMVOC direct emissions, rural",
            "Dinitrogen oxide direct emissions, rural",
            "Ammonia direct emissions, rural",
            "Benzene direct emissions, rural",
            "Ethane direct emissions, rural",
            "Propane direct emissions, rural",
            "Butane direct emissions, rural",
            "Pentane direct emissions, rural",
            "Hexane direct emissions, rural",
            "Cyclohexane direct emissions, rural",
            "Heptane direct emissions, rural",
            "Ethene direct emissions, rural",
            "Propene direct emissions, rural",
            "1-Pentene direct emissions, rural",
            "Toluene direct emissions, rural",
            "m-Xylene direct emissions, rural",
            "o-Xylene direct emissions, rural",
            "Formaldehyde direct emissions, rural",
            "Acetaldehyde direct emissions, rural",
            "Benzaldehyde direct emissions, rural",
            "Acetone direct emissions, rural",
            "Methyl ethyl ketone direct emissions, rural",
            "Acrolein direct emissions, rural",
            "Styrene direct emissions, rural",
            "PAH, polycyclic aromatic hydrocarbons direct emissions, rural",
            "Arsenic direct emissions, rural",
            "Selenium direct emissions, rural",
            "Zinc direct emissions, rural",
            "Copper direct emissions, rural",
            "Nickel direct emissions, rural",
            "Chromium direct emissions, rural",
            "Chromium VI direct emissions, rural",
            "Mercury direct emissions, rural",
            "Cadmium direct emissions, rural",
        ]

        l_y = []
        for y in self.array.year.values:
            if 2000 <= y < 2005:
                l_y.append(3)
            if 2005 <= y < 2008:
                l_y.append(4)
            if 2008 <= y < 2012:
                l_y.append(5)
            if y >= 2012:
                l_y.append(6)

        l_pwt = [
            p
            for p in self.array.powertrain.values
            if p in ["ICEV-d", "PHEV-c-d", "HEV-d"]
        ]

        if len(l_pwt) > 0:
            self.array.loc[
                dict(
                    powertrain=l_pwt,
                    parameter=list_direct_emissions,
                )
            ] = hem.get_emissions_per_powertrain(
                powertrain_type="diesel",
                euro_classes=l_y,
                lifetime_km=self.array.loc[
                    dict(
                        powertrain=l_pwt,
                        parameter="lifetime kilometers",
                    )
                ],
                energy_consumption=self.energy.sel(
                    powertrain=l_pwt,
                    parameter=[
                        "motive energy",
                        "auxiliary energy",
                        "recuperated energy",
                    ],
                ).sum(dim="parameter"),
            )

        # For CNG vehicles
        if "ICEV-g" in self.array.powertrain.values:
            self.array.loc[
                dict(powertrain="ICEV-g", parameter=list_direct_emissions)
            ] = np.squeeze(
                hem.get_emissions_per_powertrain(
                    powertrain_type="cng",
                    euro_classes=l_y,
                    lifetime_km=self.array.loc[
                        dict(
                            powertrain="ICEV-g",
                            parameter="lifetime kilometers",
                        )
                    ],
                    energy_consumption=self.energy.sel(
                        powertrain=["ICEV-g"],
                        parameter=[
                            "motive energy",
                            "auxiliary energy",
                            "recuperated energy",
                        ],
                    ).sum(dim="parameter"),
                ),
                axis=1,
            )

    def set_noise_emissions(self):
        """
        Calculate noise emissions based on ``driving cycle``.
        The driving cycle is passed to the :class:`NoiseEmissionsModel` class and :meth:`get_sound_power_per_compartment`
        returns emissions per compartment type ("rural", "non-urban" and "urban") per second of driving cycle.

        Noise emissions are not differentiated by size classes at the moment, but only by powertrain "type"
        (e.g., combustion, hybrid and electric)

        :return: Does not return anything. Modifies ``self.array`` in place.
        """
        nem = NoiseEmissionsModel(self.ecm.cycle_name)

        list_noise_emissions = [
            "noise, octave 1, day time, urban",
            "noise, octave 2, day time, urban",
            "noise, octave 3, day time, urban",
            "noise, octave 4, day time, urban",
            "noise, octave 5, day time, urban",
            "noise, octave 6, day time, urban",
            "noise, octave 7, day time, urban",
            "noise, octave 8, day time, urban",
            "noise, octave 1, day time, suburban",
            "noise, octave 2, day time, suburban",
            "noise, octave 3, day time, suburban",
            "noise, octave 4, day time, suburban",
            "noise, octave 5, day time, suburban",
            "noise, octave 6, day time, suburban",
            "noise, octave 7, day time, suburban",
            "noise, octave 8, day time, suburban",
            "noise, octave 1, day time, rural",
            "noise, octave 2, day time, rural",
            "noise, octave 3, day time, rural",
            "noise, octave 4, day time, rural",
            "noise, octave 5, day time, rural",
            "noise, octave 6, day time, rural",
            "noise, octave 7, day time, rural",
            "noise, octave 8, day time, rural",
        ]

        l_pwt_combustion = [
            p
            for p in self.array.powertrain.values
            if p in ["ICEV-g", "ICEV-d", "PHEV-c-d"]
        ]

        l_pwt_electric = [
            p for p in self.array.powertrain.values if p in ["BEV", "FCEV", "PHEV-e"]
        ]

        l_size_medium = [
            s
            for s in self.array.coords["size"].values
            if s in ["3.5t", "7.5t", "18t", "26t"]
        ]

        l_size_heavy = [
            s for s in self.array.coords["size"].values if s in ["32t", "40t", "60t"]
        ]

        if len(l_pwt_combustion) > 0 and len(l_size_medium) > 0:
            cycle = get_standard_driving_cycle(self.cycle, size=l_size_medium)

            self.array.loc[
                dict(
                    powertrain=l_pwt_combustion,
                    parameter=list_noise_emissions,
                    size=l_size_medium,
                )
            ] = nem.get_sound_power_per_compartment("combustion", "medium", cycle)

        if len(l_pwt_combustion) > 0 and len(l_size_heavy) > 0:

            cycle = get_standard_driving_cycle(self.cycle, size=l_size_heavy)

            self.array.loc[
                dict(
                    powertrain=l_pwt_combustion,
                    parameter=list_noise_emissions,
                    size=l_size_heavy,
                )
            ] = nem.get_sound_power_per_compartment(
                powertrain_type="combustion", category="heavy", cycle=cycle
            )

        if len(l_pwt_electric) > 0 and len(l_size_medium) > 0:
            cycle = get_standard_driving_cycle(self.cycle, size=l_size_medium)

            self.array.loc[
                dict(
                    powertrain=l_pwt_electric,
                    parameter=list_noise_emissions,
                    size=l_size_medium,
                )
            ] = nem.get_sound_power_per_compartment("electric", "medium", cycle)

        if len(l_pwt_electric) > 0 and len(l_size_heavy) > 0:
            cycle = get_standard_driving_cycle(self.cycle, size=l_size_heavy)

            self.array.loc[
                dict(
                    powertrain=l_pwt_electric,
                    parameter=list_noise_emissions,
                    size=l_size_heavy,
                )
            ] = nem.get_sound_power_per_compartment("electric", "heavy", cycle)

        if "HEV-d" in self.array.powertrain.values and len(l_size_medium) > 0:
            cycle = get_standard_driving_cycle(self.cycle, size=l_size_medium)

            self.array.loc[
                dict(
                    powertrain=["HEV-d"],
                    parameter=list_noise_emissions,
                    size=l_size_medium,
                )
            ] = nem.get_sound_power_per_compartment("hybrid", "medium", cycle)

        if "HEV-d" in self.array.powertrain.values and len(l_size_heavy) > 0:
            cycle = get_standard_driving_cycle(self.cycle, size=l_size_heavy)

            self.array.loc[
                dict(
                    powertrain=["HEV-d"],
                    parameter=list_noise_emissions,
                    size=l_size_heavy,
                )
            ] = nem.get_sound_power_per_compartment("hybrid", "heavy", cycle)

    def calculate_cost_impacts(self, sensitivity=False, scope=None):
        """
        This method returns an array with cost values per vehicle-km, sub-divided into the following groups:

            * Purchase
            * Maintentance
            * Component replacement
            * Energy
            * Total cost of ownership

        :return: A xarray array with cost information per vehicle-km
        :rtype: xarray.core.dataarray.DataArray
        """

        if scope is None:
            scope = {
                "size": self.array.coords["size"].values.tolist(),
                "powertrain": self.array.coords["powertrain"].values.tolist(),
                "year": self.array.coords["year"].values.tolist(),
            }
        else:
            scope["size"] = scope.get("size", self.array.coords["size"].values.tolist())
            scope["powertrain"] = scope.get(
                "powertrain", self.array.coords["powertrain"].values.tolist()
            )
            scope["year"] = scope.get("year", self.array.coords["year"].values.tolist())

        list_cost_cat = [
            "purchase",
            "maintenance",
            "insurance",
            "toll",
            "component replacement",
            "energy",
            "total",
        ]

        response = xr.DataArray(
            np.zeros(
                (
                    len(scope["size"]),
                    len(scope["powertrain"]),
                    len(list_cost_cat),
                    len(scope["year"]),
                    len(self.array.coords["value"].values),
                )
            ),
            coords=[
                scope["size"],
                scope["powertrain"],
                list_cost_cat,
                scope["year"],
                self.array.coords["value"].values.tolist(),
            ],
            dims=["size", "powertrain", "cost_type", "year", "value"],
        )

        response.loc[:, :, list_cost_cat, :, :] = self.array.sel(
            powertrain=scope["powertrain"],
            size=scope["size"],
            year=scope["year"],
            parameter=[
                "amortised purchase cost",
                "maintenance cost",
                "insurance cost",
                "toll cost",
                "amortised component replacement cost",
                "energy cost",
                "total cost per km",
            ],
        ).values

        if not sensitivity:
            return response * (self.array.sel(parameter="cargo mass") > 100)
        else:
            return response / response.sel(value="reference")

    def get_share_biodiesel(self):
        """Returns average share of biodiesel according to historical IEA stats"""
        share_biofuel = np.squeeze(
            np.clip(
                self.bs.biodiesel.sel(country=self.country)
                .interp(
                    year=self.array.coords["year"].values,
                    kwargs={"fill_value": "extrapolate"},
                )
                .values,
                0,
                0.2,
            )
        )
        return share_biofuel

    def get_share_biomethane(self):
        """Returns average share of biomethane according to historical IEA stats"""
        share_biofuel = np.squeeze(
            np.clip(
                self.bs.biomethane.sel(country=self.country)
                .interp(
                    year=self.array.coords["year"].values,
                    kwargs={"fill_value": "extrapolate"},
                )
                .values,
                0,
                1,
            )
        )
        return share_biofuel

    def get_share_biofuel(self):

        try:
            region = self.bs.region_map[self.country]["RegionCode"]
        except KeyError:
            print(
                "No biofuel share could be found for {}. Hence, EU average is used.".format(
                    self.country
                )
            )
            region = "EUR"
        scenario = "SSP2-Base"

        share_biofuel = (
            self.bs.biofuel.sel(
                region=region,
                value=0,
                fuel_type="Biomass fuel",
                scenario=scenario,
            )
            .interp(
                year=self.array.coords["year"].values,
                kwargs={"fill_value": "extrapolate"},
            )
            .values
        )
        return share_biofuel

    def find_fuel_shares(self, fuel_blend, fuel_type):

        default_fuels = {
            "diesel": {
                "primary": "diesel",
                "secondary": "biodiesel - cooking oil",
                "all": [
                    "diesel",
                    "biodiesel - cooking oil",
                    "biodiesel - algae",
                    "biodiesel - palm oil",
                    "biodiesel - rapeseed oil",
                    "synthetic diesel - energy allocation",
                ],
            },
            "cng": {
                "primary": "cng",
                "secondary": "biogas - sewage sludge",
                "all": ["cng", "biogas - sewage sludge", "syngas", "biogas - biowaste"],
            },
            "hydrogen": {
                "primary": "electrolysis",
                "secondary": "smr - natural gas",
                "all": [
                    "electrolysis",
                    "smr - natural gas",
                    "smr - natural gas with CCS",
                    "smr - biogas",
                    "smr - biogas with CCS",
                    "coal gasification",
                    "wood gasification",
                    "wood gasification with CCS",
                ],
            },
        }

        if fuel_type in fuel_blend:
            primary = fuel_blend[fuel_type]["primary"]["type"]

            try:
                # See of a secondary fuel type has been specified
                secondary = fuel_blend[fuel_type]["secondary fuel"]["type"]
            except KeyError:
                # A secondary fuel has not been specified, set one by default
                # Check first if the default fuel is not similar to the primary fuel

                if default_fuels[fuel_type]["secondary"] != primary:
                    secondary = default_fuels[fuel_type]["secondary"]
                else:
                    secondary = [
                        f for f in default_fuels[fuel_type]["all"] if f != primary
                    ][0]

            primary_share = fuel_blend[fuel_type]["primary"]["share"]
            secondary_share = 1 - np.array(primary_share)

        else:
            primary = default_fuels[fuel_type]["primary"]
            secondary = default_fuels[fuel_type]["secondary"]

            if primary == "electrolysis":
                secondary_share = np.zeros_like(self.array.year.values)
            else:
                if fuel_type == "diesel":
                    if self.country in self.bs.biodiesel.country.values:
                        secondary_share = self.get_share_biodiesel()
                    else:
                        secondary_share = self.get_share_biofuel()
                elif fuel_type == "cng":
                    if self.country in self.bs.biomethane.country.values:
                        secondary_share = self.get_share_biomethane()
                    else:
                        secondary_share = self.get_share_biofuel()
                else:
                    secondary_share = self.get_share_biofuel()

            primary_share = 1 - np.array(secondary_share)

        return primary, secondary, primary_share, secondary_share

    def define_fuel_blends(self, fuel_blend=None):
        """
        This function defines fuel blends from what is passed in `fuel_blend`.
        It populates a dictionary `self.fuel_blends` that contains the respective shares, lower heating values
        and CO2 emission factors of the fuels used.

        Source for LHV: https://www.bafu.admin.ch/bafu/en/home/topics/climate/state/data/climate-reporting/references.html

        :return:
        """

        if fuel_blend is None:
            fuel_blend = dict()

        fuel_types = ["diesel", "cng", "hydrogen"]

        fuel_to_powertrains_map = {
            "diesel": ["ICEV-d", "HEV-d", "PHEV-d"],
            "cng": ["ICEV-g"],
            "hydrogen": ["FCEV"],
        }

        for fuel_type in fuel_types:
            if any(
                i in self.array.powertrain.values
                for i in fuel_to_powertrains_map[fuel_type]
            ):
                (
                    primary,
                    secondary,
                    primary_share,
                    secondary_share,
                ) = self.find_fuel_shares(fuel_blend, fuel_type)
                if not isinstance(primary_share, np.ndarray):
                    primary_share = np.squeeze(np.array([primary_share]))
                if not isinstance(secondary_share, np.ndarray):
                    secondary_share = np.squeeze(np.array([secondary_share]))

                fuel_blend[fuel_type] = {
                    "primary": {
                        "type": primary,
                        "share": np.array(primary_share).reshape(-1)
                        if primary_share.ndim == 0
                        else primary_share,
                        "lhv": self.fuel_specs[primary]["lhv"],
                        "CO2": self.fuel_specs[primary]["co2"],
                    },
                    "secondary": {
                        "type": secondary,
                        "share": np.array(secondary_share).reshape(-1)
                        if secondary_share.ndim == 0
                        else secondary_share,
                        "lhv": self.fuel_specs[secondary]["lhv"],
                        "CO2": self.fuel_specs[secondary]["co2"],
                    },
                }

        return fuel_blend
