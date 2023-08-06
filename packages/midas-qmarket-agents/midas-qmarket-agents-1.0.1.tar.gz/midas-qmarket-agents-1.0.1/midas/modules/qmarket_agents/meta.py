META = {
    "type": "time-based",
    "models": {
        "MarketAgentModel": {
            "public": True,
            "params": ["eid", "unit_type", "s_max", "start_date", "step_size"],
            "attrs": [
                "schedule",
                "reactive_power_offer",
                "q_set",
                "set_q_schedule",
                "last_offer_price",
                "last_offer_amount",
                "last_profit",
            ],
        },
    },
}
