from __future__ import annotations

import argparse

from cloudlayer.factory import get_adapter
from src import config


PAYLOADS = [
    {
        "temp_c": 50,
        "vibration_mm_s": 10,
        "pressure_kpa": 200,
        "hours_since_service": 1000,
        "load_pct": 70,
        "ambient_humidity": 50,
    },
    {
        "temp_c": 30,
        "vibration_mm_s": 5,
        "pressure_kpa": 150,
        "hours_since_service": 500,
        "load_pct": 40,
        "ambient_humidity": 40,
    },
    {
        "temp_c": 80,
        "vibration_mm_s": 20,
        "pressure_kpa": 300,
        "hours_since_service": 5000,
        "load_pct": 90,
        "ambient_humidity": 80,
    },
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True)
    args = parser.parse_args()

    cfg = config.load()
    adapter = get_adapter(cfg)

    for i, payload in enumerate(PAYLOADS, 1):
        print(f"=== SMOKE {i} ===")
        print(adapter.invoke(args.endpoint, payload))


if __name__ == "__main__":
    main()
