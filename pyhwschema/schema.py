from __future__ import print_function
import sys
import json
import requests
# Avro lib is different in between Python 2 and 3
if sys.version_info[0] < 3:
    from avro.schema import parse
else:
    from avro.schema import Parse as parse


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

    def get_string(self):
        """Returns a string representation of the schema.

        Gives back a schema string

        Returns:
            str: from GET request
        """

        response = requests.get(self.api_url())

        return response.json()[u'schemaText']

    def get_dict(self):
        """Returns a dict representation of the schema.

        Gives back a schema dict

        Returns:
            dict: from GET request
        """

        response = requests.get(self.api_url())

        return json.loads(response.json()[u'schemaText'])

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

    def __init__(self, connection, schema_name="test", schema_group="test", schema_meta_description="Used for testing",
                 schema_compatibility="NONE", schema_validationlevel="LATEST"):
        HwSchema.__init__(self, connection)
        self.schema_name = schema_name
        self.schema_group = schema_group
        self.schema_meta_description = schema_meta_description
        self.schema_compatibility = schema_compatibility
        self.schema_validationlevel = schema_validationlevel

    def api_url(self):
        return self.connection + "/schemas"

    def get(self):
        raise AttributeError("'SchemaNewMeta' object has no attribute 'get'")

    def get_string(self):
        raise AttributeError("'SchemaNewMeta' object has no attribute 'get_string'")

    def get_dict(self):
        raise AttributeError("'SchemaNewMeta' object has no attribute 'get_dict'")

    def create(self):
        payload = {"type": "avro",
                   "schemaGroup": self.schema_group,
                   "name": self.schema_name,
                   "description": self.schema_meta_description,
                   "compatibility": self.schema_compatibility,
                   "validationLevel": self.schema_validationlevel}

        return self.put(payload)


class SchemaNew(HwSchema):

    def __init__(self, connection, schema_text, schema_name="test", schema_description="Used for testing",
                 schema_branch="MASTER"):
        HwSchema.__init__(self, connection)
        self.schema_name = schema_name
        self.schema_text = schema_text
        self.schema_description = schema_description
        self.schema_branch = schema_branch

    def api_url(self):
        return self.connection + "/schemas/" + self.schema_name + "/versions?branch=" + self.schema_branch

    def get(self):
        raise AttributeError("'SchemaNew' object has no attribute 'get'")

    def get_string(self):
        raise AttributeError("'SchemaNew' object has no attribute 'get_string'")

    def get_dict(self):
        raise AttributeError("'SchemaNew' object has no attribute 'get_dict'")

    def create(self):
        # verify valid Avro schema
        try:
            parse(self.schema_text)
        except AssertionError as error:
            print(error)

        payload = {"description": self.schema_description,
                   "schemaText": self.schema_text}

        return self.put(payload)


class SchemaNewBranch(HwSchema):

    def __init__(self, connection, schema_name="test", branch_name="test", schema_description="Used for testing"):
        HwSchema.__init__(self, connection)
        self.branch_name = branch_name
        self.schema_name = schema_name
        self.schema_description = schema_description

        url = self.connection + "/schemas/" + self.schema_name + "/versions/latest?branch=MASTER"
        response = requests.get(url)
        self.version_id = response.json()

    def api_url(self):
        return self.connection + "/schemas/versionsById/" + str(self.version_id["id"]) + "/branch"

    def get(self):
        raise AttributeError("'SchemaNew' object has no attribute 'get'")

    def get_string(self):
        raise AttributeError("'SchemaNew' object has no attribute 'get_string'")

    def get_dict(self):
        raise AttributeError("'SchemaNew' object has no attribute 'get_dict'")

    def create(self):
        payload = {"description": self.schema_description,
                   "name": self.branch_name}

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

    def get_string(self):
        raise AttributeError("'SchemaDropVersion' object has no attribute 'get_string'")

    def get_dict(self):
        raise AttributeError("'SchemaDropVersion' object has no attribute 'get_dict'")

    def drop(self):
        response = requests.delete(self.api_url())
        try:
            return response.json()
        except:
            return {"responseCode": response.status_code, "responseMessage":
                "Schema version {0} dropped from schema {1}".format(self.schema_id, self.schema_name)}


class SchemaMetaData(HwSchema):

    def __init__(self, connection, schema_name):
        HwSchema.__init__(self, connection)
        self.schema_name = schema_name

    def api_url(self):
        return self.connection + "/schemas/" + self.schema_name

    def get_string(self):
        """Returns a string representation of the schema metadata.

        Gives back a meta string

        Returns:
            str: from GET request
        """

        response = requests.get(self.api_url())

        return json.dumps(response.json()['schemaMetadata'])

    def get_dict(self):
        """Returns a dict representation of the schema metadata.

        Gives back a schema dict

        Returns:
            dict: from GET request
        """

        response = requests.get(self.api_url())

        return response.json()['schemaMetadata']

    def put(self, *arg):
        raise AttributeError("'SchemaLatest' object has no attribute 'put'")


class SchemaGetVersions(HwSchema):

    def __init__(self, connection, schema_name, branch="MASTER"):
        HwSchema.__init__(self, connection)
        self.schema_name = schema_name
        self.schema_branch = branch

    def api_url(self):
        return self.connection + "/schemas/" + self.schema_name + "/versions?branch=" + self.schema_branch

    def get_string(self):
        """Returns a string representation of the schema metadata.

        Gives back a meta string

        Returns:
            str: from GET request
        """

        response = requests.get(self.api_url())

        response_list = response.json()["entities"]

        version_tuples = map(lambda x: {"version": x["version"], "id": x["id"]}, response_list)

        return json.dumps(version_tuples)

    def get_dict(self):
        """Returns a dict representation of the schema metadata.

        Gives back a schema dict

        Returns.:
            dict: from GET request
        """

        response = requests.get(self.api_url())

        response_list = response.json()["entities"]

        version_tuples = map(lambda x: {"version": x["version"], "id": x["id"]}, response_list)

        return version_tuples

    def put(self, *arg):
        raise AttributeError("'SchemaLatest' object has no attribute 'put'")

