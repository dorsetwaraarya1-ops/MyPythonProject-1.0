
[
  {
    "device": {
      "id": "device-123",
      "type": "sensor"
    },
    "ts": 1625097600000,
    "telemetry": {
      "temperature": 25.4,
      "humidity": 48
    }
  }
]



[
  {
    "deviceId": "device-123",
    "timestamp": "2021-07-01T00:00:00Z",
    "measurements": {
      "temp": 25.4,
      "hum": 48
    }
  }
]
[
  {
    "device_id": "device-123",
    "timestamp": 1625097600000,
    "temperature": 25.4,
    "humidity": 48
  }# main.py
# Converts data-1.json and data-2.json into the unified format (data-result.json)

import json
from datetime import datetime
from pathlib import Path
import sys

BASE = Path(__file__).parent

def iso_to_milliseconds(iso_string):
    """Convert ISO datetime string (e.g. '2021-07-01T00:00:00Z') to milliseconds since epoch."""
    dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
    return int(dt.timestamp() * 1000)

def transform_data1(msg):
    """
    Transform one message from data-1.json style into the unified format.
    Unified format fields: device_id, timestamp, temperature, humidity
    """
    device_id = msg["device"]["id"]
    ts = int(msg["ts"])  # already milliseconds
    telemetry = msg["telemetry"]

    return {
        "device_id": device_id,
        "timestamp": ts,
        "temperature": telemetry["temperature"],
        "humidity": telemetry["humidity"]
    }

def transform_data2(msg):
    """
    Transform one message from data-2.json style into the unified format.
    Needs ISO timestamp → milliseconds conversion.
    """
    device_id = msg["deviceId"]
    ts = iso_to_milliseconds(msg["timestamp"])
    measurements = msg["measurements"]

    return {
        "device_id": device_id,
        "timestamp": ts,
        "temperature": measurements["temp"],
        "humidity": measurements["hum"]
    }

def load_json(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_json(obj, p: Path):
    with p.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    p1 = BASE / "data-1.json"
    p2 = BASE / "data-2.json"
    p_expected = BASE / "data-result.json"

    try:
        d1 = load_json(p1)
        d2 = load_json(p2)
        expected = load_json(p_expected)
    except FileNotFoundError as e:
        print("❌ File not found:", e)
        sys.exit(1)

    msg1 = d1[0]
    msg2 = d2[0]
    expected_obj = expected[0]

    out1 = transform_data1(msg1)
    out2 = transform_data2(msg2)

    save_json(out1, BASE / "unified-from-data1.json")
    save_json(out2, BASE / "unified-from-data2.json")

    print("✅ Transformed output from data-1.json:")
    print(json.dumps(out1, indent=2, ensure_ascii=False))

    print("\n✅ Transformed output from data-2.json:")
    print(json.dumps(out2, indent=2, ensure_ascii=False))

    ok1 = out1 == expected_obj
    ok2 = out2 == expected_obj
    print(f"\nComparison → data-1 match: {ok1}, data-2 match: {ok2}")

    if ok1 and ok2:
        print("\n🎉 SUCCESS: both transformed outputs match data-result.json")
        sys.exit(0)
    else:
        print("\n⚠️ ERROR: one or both outputs do not match expected format")
        print("\nExpected (data-result.json):")
        print(json.dumps(expected_obj, indent=2, ensure_ascii=False))
        sys.exit(1)

]
{
  "device_id": "device-123",
  "timestamp": 1625097600000,
  "temperature": 25.4,{
  "device_id": "device-123",
  "timestamp": 1625097600000,
  "temperature": 25.4,
  "humidity": 48
}
  "humidity": 48
}
