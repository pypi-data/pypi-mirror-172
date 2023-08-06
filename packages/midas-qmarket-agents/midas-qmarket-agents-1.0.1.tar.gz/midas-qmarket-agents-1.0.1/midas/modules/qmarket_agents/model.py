"""This module contains the market agent model for the qmarket
Author: Torge Wolff <torge.wolff@offis.de>

"""
import logging
import math
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

LOG = logging.getLogger(__name__)


class MarketAgentModel:
    def __init__(
        self,
        sid: str,
        eid: str,
        unit_type: str,
        s_max: float,
        start_date: str,
        step_size: int = 15 * 60,
        date_fmt: str = "%Y-%m-%d %H:%M:%S%z",
    ):
        self.sid: str = sid
        self.eid: str = eid
        self.unit_type: str = unit_type
        self.s_max: float = s_max
        self.step_size: int = step_size
        self.start_dt: datetime = datetime.strptime(start_date, date_fmt)
        self.now_dt: datetime = self.start_dt
        self.next_offer_dt: datetime = self.now_dt + timedelta(seconds=self.step_size)
        self.last_offer_dt: Optional[datetime] = None
        self.reactive_power_offer = None
        self.set_q_schedule: pd.DataFrame = pd.DataFrame()
        internal_schedule_columns: list = [
            "p_mw",
            "q_mvar",
            "q_min",
            "q_max",
            "q_offer",
            "sent_q_offer",
            "q_target",
        ]
        self.internal_schedule: pd.DataFrame = pd.DataFrame(columns=internal_schedule_columns)

        # Inputs
        self.sim_time: int = 0
        self.schedule: pd.DataFrame = pd.DataFrame()
        self.place_offer_state: bool = True
        self.q_set: Optional[float] = None
        self.q_price_per_mvarh_eur = 0

        # Outputs

    def step(self):

        if self.place_offer_state:
            LOG.debug(
                "(%s) performing 'place offer' state at %s.",
                self.eid,
                self.now_dt,
            )
            self._place_offer()
        else:
            LOG.debug(
                "(%s) performing 'create schedule' state at %s.",
                self.eid,
                self.now_dt,
            )
            self._create_schedule()

        self.now_dt = self.start_dt + timedelta(seconds=self.sim_time)

    def _place_offer(self):
        LOG.debug("(%s) received schedule: %s.", self.eid, self.schedule.to_json())
        self.set_q_schedule = pd.DataFrame()

        if self.schedule.empty:
            LOG.warning("(%s) Schedule is empty, cannot create offer!", self.eid)
            self.reactive_power_offer = {}
            return

        schedule_update = {
            "p_mw": self.schedule["p_mw"].loc[self.next_offer_dt] * -1,
            "q_mvar": self.schedule["q_mvar"].loc[self.next_offer_dt] * -1,
            "sent_q_offer": False,
            "q_min": None,
            "q_max": None,
            "q_offer": None,
            "q_target": None,
        }

        self.internal_schedule = pd.concat(
            [
                self.internal_schedule,
                pd.DataFrame(schedule_update, index=pd.to_datetime([self.next_offer_dt])),
            ]
        )

        self._calculate_q_min_and_q_max()
        self._calculate_linear_q_price()

        # Distinguish offer between positive and negative reactive power
        q_min = self.internal_schedule["q_min"].loc[self.next_offer_dt]
        q_max = self.internal_schedule["q_max"].loc[self.next_offer_dt]
        assert q_min <= 0
        assert q_max >= 0
        # Assumption: agents can submit only a single offer
        self.reactive_power_offer = {
            "agent_id": f"{self.sid}.{self.eid}",
            "q_min": q_min,
            "q_max": q_max,
            "q_price": self.q_price_per_mvarh_eur,
        }

        self.internal_schedule.at[self.next_offer_dt, "sent_q_offer"] = True
        LOG.debug(
            "(%s) Q_Offer: %s for time %s",
            self.eid,
            self.reactive_power_offer,
            self.next_offer_dt,
        )

        self.last_offer_dt = self.next_offer_dt
        self.next_offer_dt += timedelta(seconds=self.step_size)
        LOG.debug(
            "(%s) Created offer for %s. Next offer will be created at %s",
            self.eid,
            self.last_offer_dt,
            self.next_offer_dt,
        )

    def _create_schedule(self):
        LOG.debug("(%s)_Q_set: %s", self.eid, self.q_set)

        self.set_q_schedule = pd.DataFrame()
        if self.q_set is None:
            self.q_set = 0.0
            LOG.warning(
                "(%s) Q setpoint is None! Is interpreted as 0.0.",
                self.eid,
            )

        q_max = self.internal_schedule["q_max"].loc[self.last_offer_dt]
        try:
            q_target = self.q_set / q_max
        except ZeroDivisionError:
            q_target = 0.0
        # TODO: abs: only one direction possible
        tmp_schedule = {"q_set_mvar": self.q_set}
        self.set_q_schedule = pd.DataFrame(tmp_schedule, index=pd.to_datetime([self.last_offer_dt])).tz_convert(
            tz="Europe/Berlin"
        )
        self.internal_schedule.at[self.last_offer_dt, "q_target"] = q_target

    def _calculate_q_min_and_q_max(self):
        """Calculate q_min and q_max by s_max of each unit"""
        p_mw_next_15 = self.internal_schedule["p_mw"].loc[self.next_offer_dt]
        q_max = math.sqrt(max(self.s_max**2 - p_mw_next_15**2, 0))
        self.internal_schedule.at[self.next_offer_dt, "q_max"] = q_max
        self.internal_schedule.at[self.next_offer_dt, "q_min"] = q_max * -1

    def _calculate_linear_q_price(self):
        """Calculate linear price with fixed value."""
        # TODO: Search for different prices per unit type and make non-static.

        # The unit is EUR/MVArh
        # https://bit.ly/3edHkXT
        # (BMWK Studie Zukuenftige Bereitstellung von Blind Leistung und anderen Massnahmen fuer die Netzsicherheit)
        # p. 109
        if self.q_price_per_mvarh_eur == 0:
            self.q_price_per_mvarh_eur = 0.52
