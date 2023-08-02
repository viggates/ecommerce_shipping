import redis
import api.models as models
from api.helper import make_response
from api.schema import ShippingProvider

class ShippingProviderClass(object):

    model = models.Models(ShippingProvider)

    def load(self, event, context):
        if "GET /shipping_provider/providers/" in event.routeKey:
            return self.get_provider(event.pathParameters.provider_id)
        elif "POST /shipping_provider/providers/" in event.routeKey:
            return self.update_provider(event.pathParameters.provider_id, event.body)
        elif "DELETE /shipping_provider/providers/" in event.routeKey:
            return self.delete_provider(event.pathParameters.provider_id)
        else:
            print("None Matched for", event.routeKey)

    def get_provider(self, provider_id: int):
        provider = self.model.get(provider_id)
        if not provider:
            return make_response(404, '{"error": "Provider not found"}')
        else:
            return make_response(200, provider.json())

    def update_provider(self, provider_id, provider):
        provider = ShippingProvider.parse_obj(provider)
        if self.model.set(provider_id, provider.json()):
            return make_response(201, provider.json())
        else:
            return make_response(424, '{"error": "DB Failure"}')

    def delete_provider(self, provider_id):
        if self.model.delete(provider_id):
            return make_response(201, '{"message": "Provider deleted"}')
        else:
            return make_response(424, '{"error": "DB Failure"}')

#@app.delete("/providers/simulate/{package_id}")
def simulate_package_movementr(package_id: int):
    pass


