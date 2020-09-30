# -*- coding: utf-8 -*-
import pytest, os, json

from .context import pyhwschema


# Get config
config_path = os.path.join(os.path.dirname(__file__), "./config.json")

with open(config_path, 'r') as f:
    config = json.load(f)


class TestClass(object):
    pytest.host = config["hwsr_host"]
    pytest.port = config["hwsr_port"]
    pytest.schema_name = "pyhwschema_test"
    pytest.connect = pyhwschema.Connect(api_host=pytest.host, api_port=pytest.port).connect_url()
    pytest.base_url = "http://{0}:{1}/api/v1/schemaregistry".format(pytest.host, pytest.port)
    pytest.api_url = pytest.base_url + "/schemas/" + pytest.schema_name + "/versions/latest?branch=MASTER"
    pytest.avro_schema = '''{"type":"record","namespace":"Testing","name":"Employee","fields":
                            [{"name":"Name","type":"string"},{"name":"Surname","type":"string"},
                            {"name":"Age","type":"int"}]}'''

    def test_base_url(self):
        assert pytest.base_url == pyhwschema.HwSchema(connection=pytest.connect).api_url()

    def test_latest_schema_api_url(self):
        assert pytest.api_url == pyhwschema.SchemaLatest(connection=pytest.connect, schema_name=pytest.schema_name)\
            .api_url()

    def test_create_SchemaNewMeta(self):
        out = pyhwschema.SchemaNewMeta(connection=pytest.connect, schema_name=pytest.schema_name,
                                       schema_group=pytest.schema_name, schema_meta_description="Used for testing",
                                       schema_compatibility="NONE", schema_validationlevel="LATEST").create()
        assert type(out) == int

    def test_create_SchemaNew(self):
        out = pyhwschema.SchemaNew(connection=pytest.connect, schema_text=pytest.avro_schema,
                                   schema_name=pytest.schema_name, schema_description="Used for testing",
                                   schema_branch="MASTER", schema_enable=True).create()

        assert out == 1

    def test_SchemaLatest(self):
        test_keys = [u'description',
                     u'stateId',
                     u'schemaMetadataId',
                     u'schemaText',
                     u'version',
                     u'timestamp',
                     u'mergeInfo',
                     u'id',
                     u'name']

        schema = pyhwschema.SchemaLatest(connection=pytest.connect, schema_name=pytest.schema_name).get()
        keys = schema.keys()

        assert list(set(sorted(test_keys))) == list(set(sorted(keys)))

    def test_SchemaMetaData(self):
        """Test if returned dict keys are what we expect"""
        expected_dict_keys = [u'evolve',
                              u'description',
                              u'schemaGroup',
                              u'type',
                              u'compatibility',
                              u'validationLevel',
                              u'name']

        schema_meta_data = pyhwschema.SchemaMetaData(connection=pytest.connect,
                                                     schema_name=pytest.schema_name).get()['schemaMetadata'].keys()
        assert list(set(sorted(expected_dict_keys))) == list(set(sorted(schema_meta_data)))

    def test_SchemaDelete(self):
        """Test if a schema is successfully deleted"""
        out = pyhwschema.SchemaDelete(connection=pytest.connect, schema_name=pytest.schema_name).delete()
        assert out in [200, 1101]

