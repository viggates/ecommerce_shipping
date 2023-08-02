from datetime import datetime

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
        elif "PUT /package_management/packages/" in event.routeKey:
            return self.set_status(event.pathParameters.package_id, event.pathParameters.status)
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

    def set_status(self, package_id, status):
        package = self.model.get(package_id)
        package.prev_status = package.curr_status
        package.curr_status = status
        if self.model.update(package_id, package.json()):
            sns_wrapper.publish_message("status_notification_channel",package.curr_status,{"timestamp":datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
            return make_response(201, package.json())
        else:
            return make_response(404, '{"error": "Package not found"}')



