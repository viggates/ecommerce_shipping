import json
from utils.dynamic_import import DynamicImport

class DictToObject:
    def __init__(self, dictionary):
        if not isinstance(dictionary, dict):
            self = dictionary
        for key, value in dictionary.items():
            if key != "body" and isinstance(value, dict):
                setattr(self, key, DictToObject(value))
            else:
                setattr(self, key, value)


def api(event, context):

    event = DictToObject(event)

    route = event.routeKey
    module_name = route.split()[1].split("/")[1]
    dynamic_object = DynamicImport("api", module_name)
    dynamic_class = dynamic_object.load_class()
    response = dynamic_class.load(event, context)
    return response
   
    """ 
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
