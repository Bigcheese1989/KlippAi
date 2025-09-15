from typing import Tuple

import requests

from .config import KlipperConfig


def test_moonraker_connection(klipper: KlipperConfig) -> Tuple[bool, str]:
	try:
		headers = {}
		if klipper.api_key:
			headers["X-Api-Key"] = klipper.api_key
		resp = requests.get(f"{klipper.moonraker_url}/printer/info", headers=headers, timeout=5)
		resp.raise_for_status()
		return True, "ok"
	except Exception as e:
		return False, str(e)
