import json
import boto3
import os
from decimal import Decimal

HUB_FUNCTION_NAME = os.environ.get('HUB_FUNCTION_NAME', '')

def handler(event, driver_name):
    if isinstance(event, str):
        driver_event = json.loads(event)
    elif isinstance(event, dict):
        driver_event = event
    else:
        raise Exception(f"unsupported payload: {type(event)}")

    try:
        # command_param = driver_event["request"]["command_params"]
        # #### command_ids = driver_event["request"]["command_ids"]
        command_id = driver_event["request"]["command_id"]

        components = f'drivers.{driver_name}.handler.{driver_name}'.split('.')
        print(components)
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)

        with mod(driver_event) as client:
            ## for c in command_ids:
            ##    cmd = getattr(client, c)
            ##    ret = cmd()
            ##    driver_event["result"].append({"function": c, "result": ret})
            cmd = getattr(client, command_id)
            ret = cmd()
            driver_event["result"] = {"function": command_id, "result": ret}

    except Exception as e:
        driver_event["result"] = e

    result = {
        "message_log_id": driver_event["message_log_id"],
        "result": driver_event["result"],
        "source": driver_event["thing_dest_address"],
        "service_id": driver_event["service_id"],
    }

    if HUB_FUNCTION_NAME:
        client = boto3.client("lambda")
        sts = client.invoke(
            FunctionName=HUB_FUNCTION_NAME,
            InvocationType="Event",
            Payload=to_json(result),
        )
        res = sts['Payload'].read()
        print(res)

    return result

def decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def to_json(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, default=decimal_default_proc)
