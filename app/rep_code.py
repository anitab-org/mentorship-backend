from http import HTTPStatus
#import requests as r
def main():
    if HTTPStatus.status_codes == 200:
        var = str(200)
        var.replace(var, "HTTPStatus.created")
        return var
    elif HTTPStatus.status_codes == 201:
        var = str(201)
        var.replace(var, "HTTPStatus.created")
        return var
    elif HTTPStatus.status_codes == 400:
        var = str(400)
        var.replace(var, "HTTPStatus.created")
        return var
    elif HTTPStatus.status_codes == 401:
        var = str(401)
        var.replace(var, "HTTPStatus.created")
        return var
    elif HTTPStatus.status_codes == 402:
        var = str(402)
        var.replace(var, "HTTPStatus.created")
        return var
    elif HTTPStatus.status_codes == 403:
        var = str(403)
        var.replace(var, "HTTPStatus.created")
        return var
    else:
        if HTTPStatus.status_codes == 404:
            var = str(404)
            var.replace(var, "HTTPStatus.created")
            return var