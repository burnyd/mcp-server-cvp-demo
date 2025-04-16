import argparse
import asyncio
import httpx
import os
import sys
import json
from dotenv import load_dotenv

async def get_env_vars():
    load_dotenv()
    cvp = os.environ.get("CVP")
    cvtoken = os.environ.get("CVPTOKEN")
    datadict = {}
    datadict['cvtoken'] = cvtoken
    datadict["cvp"] = cvp 

    return datadict

async def fetch(token: str, url: str) -> list[dict[str, any]]:
    headers = {
        "Accept": "application/json"
    }
    cookies = {
        "access_token": token
    }

    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(url, headers=headers, cookies=cookies)
            response.raise_for_status()
        except httpx.RequestError as exc:
            print(f"Request failed: {exc}", file=sys.stderr)
            sys.exit(1)

    parsed_objects = []
    for line in response.text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            parsed_objects.append(obj)
        except json.JSONDecodeError as e:
            print(f"Failed to parse line:\n{line}\nError: {e}", file=sys.stderr)

    return parsed_objects

async def main():
    cvdata = await get_env_vars()
    cvtoken = cvdata["cvtoken"]
    cvp = cvdata["cvp"]
    devices = await fetch(cvtoken, f"https://{cvp}/api/resources/inventory/v1/Device/all")
    try:
        print(json.dumps(devices, indent=2))
    except TypeError as e:
        error_message = f"Had an issue response to JSON: {str(e)}"
        print(f"[ERROR] {error_message}") # Debug print
        return json.dumps({"error": error_message})
    
    events = await fetch(cvtoken, f"https://{cvp}/api/resources/event/v1/Event/all")
    try:
        print(json.dumps(events, indent=2))
    except TypeError as e:
        error_message = f"Had an issue response to JSON: {str(e)}"
        print(f"[ERROR] {error_message}") # Debug print
        return json.dumps({"error": error_message})


if __name__ == "__main__":
    asyncio.run(main())
