from .base import Resource
from ..constants.url import URL


class Checkout(Resource):
    def __init__(self, client=None):
        super(Checkout, self).__init__(client)
        self.base_url = URL.CHECKOUT_SESSION_URL

    def fetch(self, session_id, data={}, **kwargs):
        """"
        Fetch checkout session by session_id

        Args:
            session_id : Id for which session object has to be retrieved

        Returns:
            Order dict for given session Id
        """
        return super(Checkout, self).fetch(session_id, data, **kwargs)

    def create(self, data={}, **kwargs):
        """"
        Create Checkout from given dict

        Returns:
            Checkout Dict which was created
        """
        url = self.base_url
        return self.post_url(url, data, **kwargs)


    
    def all(self, data={}, **kwargs):
        """"
        Fetch all session

        Returns:
            Dictionary of Checkout data
        """
        return super(Checkout, self).all(data, **kwargs)