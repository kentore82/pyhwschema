from __future__ import print_function
import requests
from avro.schema import parse


class HwSchema(object):
    def __init__(self, connection):
        self.connection = connection

    def api_url(self):
        return self.connection

    def get(self):
        """Returns a dict with latest schema information.

        Gives back a dictionary with schema info

        Returns:
            dict: from GET request
        """

        response = requests.get(self.api_url())

        return response.json()

    def put(self, payload):
        """Returns a dict with POST response information.

        Gives back a dictionary with POST request response info

        Returns:
            dict: from POST request
        """
        response = requests.post(self.api_url(), json=payload)
        return response.json()


class SchemaLatest(HwSchema):

    def __init__(self, connection, schema_name, schema_branch="MASTER"):
        HwSchema.__init__(self, connection)
        self.schema_name = schema_name
        self.schema_branch = schema_branch

    def api_url(self):
        return self.connection + "/schemas/" + self.schema_name + "/versions/latest?branch=" + self.schema_branch

    def put(self, *arg):
        raise AttributeError("'SchemaLatest' object has no attribute 'put'")


class SchemaId(HwSchema):

    def __init__(self, connection, schema_id="0", schema_branch="MASTER"):
        HwSchema.__init__(self, connection)
        self.schema_id = schema_id
        self.schema_branch = schema_branch

    def api_url(self):
        return self.connection + "/schemas/versionsById/" + self.schema_id

    def put(self, *arg):
        raise AttributeError("'SchemaId' object has no attribute 'put'")


class SchemaNewMeta(HwSchema):

    def __init__(self, connection, schema_name="test", schema_group="test", schema_meta_description="Used for testing"):
        HwSchema.__init__(self, connection)
        self.schema_name = schema_name
        self.schema_group = schema_group
        self.schema_meta_description = schema_meta_description

    def api_url(self):
        return self.connection + "/schemas"

    def get(self):
        raise AttributeError("'SchemaNewMeta' object has no attribute 'get'")

    def create(self):
        payload = {"type": "avro",
                   "schemaGroup": self.schema_group,
                   "name": self.schema_name,
                   "description": self.schema_meta_description,
                   "compatibility": "BACKWARD",
                   "validationLevel": "LATEST"}

        return self.put(payload)


class SchemaNew(HwSchema):

    def __init__(self, connection, schema_text, schema_name="test", schema_description="Used for testing"):
        HwSchema.__init__(self, connection)
        self.schema_name = schema_name
        self.schema_text = schema_text
        self.schema_description = schema_description

    def api_url(self):
        return self.connection + "/schemas/" + self.schema_name + "/versions"

    def get(self):
        raise AttributeError("'SchemaNew' object has no attribute 'get'")

    def create(self):
        # verify valid Avro schema
        try:
            parse(self.schema_text)
        except AssertionError as error:
            print(error)

        payload = {"description": self.schema_description,
                   "schemaText": self.schema_text}

        return self.put(payload)


class SchemaDropVersion(HwSchema):

    def __init__(self, connection, schema_name="test", schema_id="1"):
        HwSchema.__init__(self, connection)
        self.schema_name = schema_name
        self.schema_id = schema_id

    def api_url(self):
        return self.connection + "/schemas/" + self.schema_name + "/versions/" + self.schema_id

    def get(self):
        raise AttributeError("'SchemaNew' object has no attribute 'get'")

    def put(self, *arg):
        raise AttributeError("'SchemaDrop' object has no attribute 'put'")

    def drop(self):
        response = requests.delete(self.api_url())
        try:
            return response.json()
        except:
            return {"responseCode": response.status_code, "responseMessage":
                "Schema version {0} dropped from schema {1}".format(self.schema_id, self.schema_name)}
