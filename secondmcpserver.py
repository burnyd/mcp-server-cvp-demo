from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import sys, os , json
from dotenv import load_dotenv


# Initialize FastMCP server
mcp = FastMCP("CVP MCP Server")

#async function to return creds 
async def get_env_vars():
    load_dotenv()
    cvp = os.environ.get("CVP")
    cvtoken = os.environ.get("CVPTOKEN")
    datadict = {}
    datadict['cvtoken'] = cvtoken
    datadict["cvp"] = cvp 

    return datadict

#Function to fetch data get request wise from CVP. 
async def get_request_cvp(token: str, url: str) -> dict[str, Any] | None:
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

    headers = {
        "Accept": "application/geo+json"
    }
    cookies = {
        "access_token": token
    }
    parsed_objects = []
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0, cookies=cookies)
            response.raise_for_status()
            if response.status_code == 204:
                print("Received empty response (204 No Content) from SuzieQ API for")
        except Exception:
            return None
    for line in response.text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            parsed_objects.append(obj)
        except json.JSONDecodeError as e:
            print(f"Failed to parse line:\n{line}\nError: {e}", file=sys.stderr)

    return(parsed_objects)

#Get inventory tool returns inventory
@mcp.tool()
async def get_inventory() -> str:
    """Gets the inventory of devices from CVP"""
    cvdata = await get_env_vars()
    cvtoken = cvdata["cvtoken"]
    cvp = cvdata["cvp"]
    devices = await get_request_cvp(cvtoken, f"https://{cvp}/api/resources/inventory/v1/Device/all")
    try:
        return json.dumps(devices, indent=2)
    except TypeError as e:
        error_message = f"Had an issue response to JSON: {str(e)}"
        print(f"[ERROR] {error_message}") # Debug print
        return json.dumps({"error": error_message})

#Get events returns all the events from CVP 
@mcp.tool()
async def get_events() -> str:
    """Gets All of the events from CVP"""
    cvdata = await get_env_vars()
    cvtoken = cvdata["cvtoken"]
    cvp = cvdata["cvp"]
    events = await get_request_cvp(cvtoken, f"https://{cvp}/api/resources/event/v1/Event/all")
    try:
        return json.dumps(events, indent=2)
    except TypeError as e:
        error_message = f"Had an issue response to JSON: {str(e)}"
        print(f"[ERROR] {error_message}") # Debug print
        return json.dumps({"error": error_message})