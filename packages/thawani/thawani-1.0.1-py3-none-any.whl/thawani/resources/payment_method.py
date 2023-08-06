from .base import Resource
from ..constants.url import URL


class PaymentMethod(Resource):
    def __init__(self, client=None):
        super(PaymentMethod, self).__init__(client)
        self.base_url = URL.PAYMENT_METHOD_URL

    def all(self, data={}, **kwargs):
        """"
        Fetch all customer

        Returns:
            Dictionary of Customers data
        """
        return super(PaymentMethod, self).all(data, **kwargs)
    
