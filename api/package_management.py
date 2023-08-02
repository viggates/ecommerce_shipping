from datetime import datetime

from pydantic import BaseModel
import api.models as models
from api.helper import make_response
from api.schema import Package
import boto3

from api.sns import SnsWrapper

AWS_REGION = "us-east-1"
sns_res = boto3.resource("sns", region_name=AWS_REGION)

sns_wrapper=SnsWrapper(sns_res)

packages=[]
subscribers=[]

class PackageManagementClass(object):

    model = models.Models(Package)

    def load(self, event, context):
        if "GET /package_management/packages/" in event.routeKey:
            return self.get_package(event.pathParameters.package_id)
        elif "POST /package_management/packages/" in event.routeKey:
            return self.create(event.pathParameters.package_id, event.body)
        elif "DELETE /package_management/packages/" in event.routeKey:
            return self.delete_package(event.pathParameters.package_id)
        else:
            print("None Matched for", event.routeKey)

    def create(self, package_id, package):
        package = Package.parse_obj(package)
        if self.model.set(package.id, package.json()):
            return make_response(201, package.json())
        else:
            return make_response(424, '{"error": "DB Failure"}')

    def get_package(self, package_id):
        package = self.model.get(package_id)
        if not package:
            return make_response(404, '{"error": "Package not found"}')
        else:
            return make_response(200, package.json())

    def delete_package(self, package_id):
        if self.model.delete(package_id):
            return make_response(201, '{"message": "Packaged removed"}')
        else:
            return make_response(424, '{"error": "DB Failure"}')

#@app.put("/packages/",response_model=Package)
async def update(package: Package):
    if model.update(package.id, package.json()):
        return package
    else:
        return raise_http(424, "DB failure")

#@app.delete("/packages/{id}")
def delete_package(id: int):
    if model.delete(id):
        return {"message": "Packaged removed"}
    else:
        return raise_http(424, "DB failure")

#@app.put("/packages/{id}/{status}")
async def set_status(id:int, status:str):
    package = model.get(id)
    package.prev_status = package.curr_status
    package.curr_status = status
    if model.update(id, package.json()):
        sns_wrapper.publish_message("status_notification_channel",package.curr_status,{"timestamp":datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        return package, 200
    else:
        return raise_http(404, "Package not found")




