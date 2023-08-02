ecommerce_shipping

This project is designed to run on serverless

How to run

Install serverless
==================

npm i -g serverless

References
==========
1. https://www.sentinelone.com/blog/aws-lambda-with-python/?utm_source=gdn-paid&utm_medium=paid-display&utm_campaign=cloud-launch-ppc&utm_term=&campaign_id=20183238684&ad_id=&gclid=CjwKCAjwq4imBhBQEiwA9Nx1BrtfQmSzYr_SutptrO0oeEs3mD9PCqymzTqNbKdcIbCNn-k8Wh9XohoCBM4QAvD_BwE
2. https://www.serverless.com/blog/serverless-python-packaging/

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

