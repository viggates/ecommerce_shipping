def make_response(status_code, message):
    response = dict()
    response["statusCode"] = status_code
    response["body"] = message
    return response
