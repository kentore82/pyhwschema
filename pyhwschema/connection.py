# -*- coding: utf-8 -*-


class Connect(object):
    """Connection object to Hortonworks Schema Registry.

    Creates a connection string to be used in API calls to Schema Registry

    Attributes:
        api_host (str): Host of the Schemaregistry API endpoint eg. "my.host.no".
        api_port (str): Host of the Schemaregistry API endpoint eg. "9090".
        api_auth (None): Auth mechanism of the Schemaregistry API endpoint eg. "".
        api_ssl (bool): Host of the Schemaregistry API endpoint eg. True for https / False for http

    """
    def __init__(self, api_host, api_port, api_auth=None, api_ssl=False):
        self.api_host = api_host
        self.api_port = api_port
        self.api_auth = api_auth
        self.api_ssl = api_ssl

        if api_ssl:
            self.api_protocol = "https://"
        else:
            self.api_protocol = "http://"

    def connect_url(self):
        """Returns the connection-url.

        Returns:
            str: Returns the base url to be used in an api call.

        """

        return self.api_protocol+self.api_host+":"+self.api_port + "/api/v1/schemaregistry"

