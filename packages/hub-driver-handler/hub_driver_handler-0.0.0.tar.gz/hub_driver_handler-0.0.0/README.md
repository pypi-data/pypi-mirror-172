# hub-driver-handler Package

## standard file structure
```
+ drivers/
   + DRIVER_ID/
      + __init__.py
      + handler.py
      + ANYFILES...
   + DRIVER_ID2/...
   + __init__.py
   + requirements.txt
+ .dockerignore
+ app.py
+ Dockerfile
```
- drivers/DRIVER_ID/\_\_init\_\_.py is required and might be empty.
- environment variable 'HUB_FUNCTION_NAME' is required to notify the results to the IoT-hub.

## drivers/\_\_init\_\_.py
```
import drivers.DRIVER_ID.handler
...
```
- add each drivers for import.

## handler.py
```
class DRIVER_ID(object):
    def __init__(self, event):
        # store required data from event
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __del__(self):
        pass

    def get_status(self):
        ...
        return result
    
    def ANY_COMMAND(self):
        ...
        return result
    
    ...
```
- implement your driver code in this file.
- event["request"]["command_id"] will be invoked.

## .dockerignore
```
**/__pycache__
**/.pytest_cache
*.pyc
```
- this is the best practice.

## app.py
```
from hub_driver_handler.handler import handler

def lambda_handler(event, context):
    driver_id = event.get("driver_id") or context.function_name
    return handler(event, driver_id)
```
- this code expected 'driver_id' will be passed from the IoT-hub for multiple drivers support.
- if only one driver and driver_id is not equal to lambda function name, set driver_id explicitly.

## Dockerfile
```
FROM public.ecr.aws/lambda/python:3.9

COPY app.py ./
COPY drivers/ ./drivers

RUN python3.9 -m pip install --upgrade pip
RUN python3.9 -m pip install hub-driver-handler -t .
RUN python3.9 -m pip install -r drivers/requirements.txt -t .

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
```