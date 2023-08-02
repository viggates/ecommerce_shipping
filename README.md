ecommerce_shipping

This project is designed to run on serverless

How to run

Install serverless
==================

npm i -g serverless


Assumptions
===========
1. Have a mysql DB running locally
2. Have a standalone redis DB running locally
3. They can be configured in api/models.py

Shipping Provider
=================

serverless invoke local --function shipping --data '{"routeKey": "POST /shipping_provider/providers/{provider_id}", "pathParameters": {"provider_id": "3"}, "body": {"id": 3, "name": "new123", "address" : "33333 newstreer", "phone": "666-7777"}}'


serverless invoke local --function shipping --data '{"routeKey": "GET /shipping_provider/providers/{provider_id}", "pathParameters": {"provider_id": "3"}}'


serverless invoke local --function shipping --data '{"routeKey": "DELETE /shipping_provider/providers/{provider_id}", "pathParameters": {"provider_id": "3"}}'


Package Management
==================


serverless invoke local --function shipping --data '{"routeKey": "POST /package_management/packages/{package_id}", "pathParameters": {"package_id": "2"}, "body": {"id": 2, "name": "package2", "email" : "package@hello.com", "curr_status": "Ordered", "prev_status": "None"}}'


serverless invoke local --function shipping --data '{"routeKey": "GET /package_management/packagess/{package_id}", "pathParameters": {"package_id": "2"}}'


serverless invoke local --function shipping --data '{"routeKey": "DELETE /package_management/packages/{package_id}", "pathParameters": {"package_id": "2"}}'

====

