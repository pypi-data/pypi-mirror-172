"""Mosaik interface for the MarketAgentSim.

Author: Torge Wolff <torge.wolff@offis.de>
"""

import json
import logging
from typing import Any, Dict, List, Optional

import mosaik_api
import pandas as pd

from .meta import META
from .model import MarketAgentModel

LOG = logging.getLogger(__name__)


class MarketAgentSim(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.sid: Optional[str] = None
        self.step_size: int = 60 * 15
        self.models: dict = {}
        self.eid_prefix: str = "MarketAgentModel_"
        self.entities: dict = {}
        self.last_time: int = -self.step_size
        self.place_offer_state: bool = True

    def init(self, sid: str, **sim_params):
        """
        Called exactly ones after the simulator has been started.
        :return: the meta dict (set by mosaik_api.Simulator)
        """
        self.sid = sid
        self.eid_prefix = sim_params.get("eid_prefix", self.eid_prefix)

        return self.meta

    def create(
        self,
        num: int,
        model: str,
        unit_type: str,
        s_max: float,
        start_date: str,
        step_size: int,
    ):
        """
        Initialize the simulation model instance (entity)
        :return: a list with information on the created entity
        """
        next_eid = len(self.models)
        entities = []

        for i in range(next_eid, next_eid + num):
            eid = f"{self.eid_prefix}{unit_type}_{i}"
            # prefix = self.eid_prefix + unit_type + "_"
            # eid = "%s%d" % (prefix, i)
            new_model = MarketAgentModel(
                sid=self.sid,
                eid=eid,
                unit_type=unit_type,
                s_max=s_max,
                start_date=start_date,
                step_size=step_size,
            )
            self.models[eid] = new_model
            entities.append({"eid": eid, "type": model})

        return entities

    def step(self, time: int, inputs: Dict[str, Any], max_advance: int = 0) -> int:
        """Perform a simulation step"""
        LOG.debug("At step %s received inputs: %s", time, inputs)

        for eid, attrs in inputs.items():
            self.models[eid].time = time
            self.models[eid].place_offer_state = self.place_offer_state

            for attr, src_ids in attrs.items():
                if attr == "schedule":

                    for schedule in src_ids.values():
                        if schedule is None:
                            continue
                        if not isinstance(schedule, pd.DataFrame):
                            if not isinstance(schedule, str) and len(schedule.keys()) == 1:
                                schedule = list(schedule.values())[0]
                            try:
                                schedule = pd.read_json(schedule).tz_localize("UTC")
                            except ValueError:
                                LOG.info("MarketAgents: Failed to load: '%s' (type=%s)", schedule, type(schedule))
                                continue

                        self.models[eid].schedule = schedule
                        break
                elif attr == "q_price_per_mvarh_eur":
                    self.models[eid].q_price_per_mvarh_eur = list(src_ids.values())[0]
                elif attr == "q_set":
                    q_set = deserialize_q_set(src_ids, f"{self.sid}.{eid}")
                    self.models[eid].q_set = q_set

        for eid, model in self.models.items():
            LOG.debug("Stepping model with eid '%s'", eid)
            model.step()

        if self.place_offer_state:
            self.place_offer_state = False
        else:
            self.place_offer_state = True
        wakeup_time = time + self.step_size // 2
        LOG.debug("Set wakeup time in step %d.", wakeup_time)
        return wakeup_time

    def get_data(self, outputs: Dict[str, List[str]]):
        """Returns the requested outputs (if feasible)"""
        data = {}
        for eid, attrs in outputs.items():
            data[eid] = {}
            for attr in attrs:
                if attr == "set_q_schedule":
                    value = self.models[eid].set_q_schedule
                    if value is None or value.empty:
                        value = "{}"  # Empty dataframe as json
                    else:
                        value = value.to_json()
                elif attr == "reactive_power_offer":
                    value = json.dumps(self.models[eid].reactive_power_offer)
                elif attr == "last_offer_amount":
                    value = self.models[eid].q_set
                elif attr == "last_offer_price":
                    value = self.models[eid].q_price_per_mvarh_eur
                elif attr == "profit":
                    value = abs(self.models[eid].q_set) * self.models[eid].q_price_per_mvarh_eur
                else:
                    raise ValueError("Unknown output attribute: %s" % attr)

                data[eid][attr] = value
        LOG.debug(f"Gathered outputs: {data}")
        return data


def deserialize_q_set(src_ids, full_id):
    # extract q_set values from market operator
    for value in src_ids.values():
        if not value:
            q_set = 0.0
        else:
            q_set = value.get(full_id, 0.0)
            if q_set == 0.0:
                if len(value) == 1:
                    # Maybe ict simulator is used -> dict within dict
                    data = list(value.values())[0]
                    if isinstance(data, dict):
                        q_set = data.get(full_id, 0.0)
                    else:
                        q_set = value.get(full_id, 0.0)
                if q_set == 0.0:
                    LOG.debug("q_set is 0.0 for %s", full_id)
    return q_set


if __name__ == "__main__":
    mosaik_api.start_simulation(MarketAgentSim())
