"""MIDAS upgrade module for Market Agents.

Author: Stephan Balduin <stephan.balduin@offis.de>

"""
import logging
from typing import Any, Dict, Tuple

from midas.util.upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class MarketAgentsModule(UpgradeModule):
    """Market agents upgrade module for MIDAS 1.0."""

    def __init__(self):
        super().__init__(
            module_name="marketagents",
            default_scope_name="midasmv",
            default_sim_config_name="MarketAgents",
            default_import_str=("midas.modules.qmarket_agents.simulator:MarketAgentSim"),
            default_cmd_str=("%(python)s -m midas.modules.qmarket_agents.simulator %(addr)s"),
            log=LOG,
        )

        self.models = {}
        self.agent_unit_model_map = {}
        self.sensors = []
        self.actuators = []

    def check_module_params(self, module_params: Dict[str, Any]):
        """Check the module params and provide default values."""
        module_params.setdefault("start_date", self.scenario.base.start_date)
        module_params.setdefault("module_name_unit_models", "der")

    def check_sim_params(self, module_params):
        """Check the params for a certain simulator instance."""
        self.sim_params.setdefault("start_date", module_params["start_date"])
        self.sim_params.setdefault("module_name_unit_models", module_params["module_name_unit_models"])
        self.sim_params.setdefault("mapping", {})

        if self.scenario.base.no_rng:
            self.sim_params["seed"] = self.scenario.create_seed()
        else:
            self.sim_params.setdefault("seed", self.scenario.create_seed())

    def start_models(self):
        """Start all models defined in the mapping of a certain simulator."""
        if not self.sim_params["mapping"]:
            self.sim_params["mapping"] = _create_default_mapping()

        model_ctr = 0
        model_name = "MarketAgentModel"
        agent_bus_map = self.scenario.create_shared_mapping(self, "agent_bus_map")
        der_mapping = self._find_der_mapping()

        for unit_model, bus, uidx in self.sim_params["mapping"]:
            model_key = self.scenario.generate_model_key(self, model_name.lower(), model_ctr)
            unit_key, unit_full_id = self._find_unit_model(unit_model, bus, uidx)

            params = {
                "s_max": der_mapping[unit_full_id]["sn_mva"],
                "unit_type": unit_model,
                "start_date": self.sim_params["start_date"],
                "step_size": self.sim_params["step_size"],
            }
            full_id = self.start_model(model_key, model_name, params)
            agent_bus_map[model_key] = (full_id, bus)
            self.agent_unit_model_map[model_key] = (unit_key, unit_full_id)
            model_ctr += 1

            self.sensors.append({
                "sensor_id": f"{full_id}.last_offer_price",
                "observation_space": (
                    "Box(low=-10, high=10, shape=(1,), dtype=np.double)" 
                )
            })
            self.sensors.append({
                "sensor_id": f"{full_id}.last_offer_amount",
                "observation_space": (
                    "Box(low=-100, high=100, shape=(1,), dtype=np.double)" 
                )
            })
            self.sensors.append({
                "sensor_id": f"{full_id}.profit",
                "observation_space": (
                    "Box(low=-1000, high=1000, shape=(1,), dtype=np.double)" 
                )
            })
            self.actuators.append({
                "actuator_id": f"{full_id}.q_price_per_mvarh_eur",
                "action_space": (
                    "Box(low=-10, high=10, shape=(1,), dtype=np.double)" 
                )
            })

    def _find_der_mapping(self):
        mappings = self.scenario.get_shared_mappings()
        key = f"{self.sim_params['module_name_unit_models']}_{self.scope_name}"

        for name, mapping in mappings.items():
            if key in name and "eid_mapping" in name:
                return mapping

        return {}

    def _find_unit_model(self, unit_model, bus, uidx) -> Tuple[str, str]:
        der_models = self.scenario.find_models(self.sim_params["module_name_unit_models"])

        candidates = []
        key = f"{unit_model.lower()}_{bus}"
        for model_key in der_models:
            if key in model_key:
                candidates.append(model_key)

        if not candidates:
            LOG.error(
                "No unit model with name '%s', bus '%d', and index '%d' " "found!",
                unit_model,
                bus,
                uidx,
            )
            raise ValueError("No unit model found for mapping: " f"[{unit_model}, {bus}, {uidx}]")

        return candidates[uidx], der_models[candidates[uidx]].full_id

    def connect(self):
        mod_ctr = 0
        ict_mappings = self.scenario.get_ict_mappings()

        for market_agent_key, (unit_model_key, _) in self.agent_unit_model_map.items():
            if self.scenario.base.with_ict:
                # provides a list of mapping, that ict can use to see
                # where to connect between the entities if initial data
                # is needed, it can be given. if not given, it is not
                # needed
                ict_mappings.append(
                    {
                        "sender": unit_model_key,
                        "receiver": market_agent_key,
                        "sender_before_ict": True,
                        "receiver_before_ict": False,
                        "attrs": [("schedule", "schedule")],
                    }
                )
                ict_mappings.append(
                    {
                        "sender": market_agent_key,
                        "receiver": unit_model_key,
                        "sender_before_ict": False,
                        "receiver_before_ict": True,
                        "attrs": [("set_q_schedule", "schedule")],
                        "initial_data": ["set_q_schedule"],
                    }
                )
            else:
                self.connect_entities(unit_model_key, market_agent_key, ["schedule"])
                self.connect_entities(
                    market_agent_key,
                    unit_model_key,
                    [("set_q_schedule", "schedule")],
                    time_shifted=True,
                    initial_data={"set_q_schedule": None},
                )
            mod_ctr += 1

    def connect_to_db(self):
        db_key = self.scenario.find_first_model("store", "database")[0]
        for agent_key in self.agent_unit_model_map:
            self.connect_entities(agent_key, db_key, ["set_q_schedule", "reactive_power_offer"])

    def get_sensors(self):
        for sensor in self.sensors:
            self.scenario.sensors.append(sensor)

    def get_actuators(self):
        for act in self.actuators:
            self.scenario.actuators.append(act)

def _create_default_mapping():
    unit_map = [["PV", 2, 0], ["PV", 3, 0], ["PV", 2, 1], ["PV", 3, 1]]
    return unit_map
