# -*- coding: utf-8 -*-
import pytest

from .context import pyhwschema


class TestClass(object):
    pytest.host = "docker1.kb.test"
    pytest.schema_name = "Vegstengning"
    pytest.connect = pyhwschema.Connect(api_host=pytest.host, api_port="9090").connect_url()
    pytest.base_url = "http://{0}:9090/api/v1/schemaregistry".format(pytest.host)
    pytest.api_url = pytest.base_url + "/schemas/" + pytest.schema_name + "/versions/latest?branch=MASTER"
    pytest.avro_schema = '''{"type":"record","namespace":"Testing","name":"Employee","fields":
                            [{"name":"Name","type":"string"},{"name":"Surname","type":"string"},
                            {"name":"Age","type":"int"}]}'''

    def test_base_url(self):
        assert pytest.base_url == pyhwschema.HwSchema(connection=pytest.connect).api_url()

    def test_latest_schema_api_url(self):
        assert pytest.api_url == pyhwschema.SchemaLatest(connection=pytest.connect, schema_name=pytest.schema_name).api_url()

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

        assert test_keys == keys

    def test_SchemaMetaData(self):
        """Test if returned dict keys are what we expect"""
        expected_dict_keys = [u'evolve',
                              u'description',
                              u'schemaGroup',
                              u'type',
                              u'compatibility',
                              u'validationLevel',
                              u'name']

        schema_meta_data = pyhwschema.SchemaMetaData(connection=pytest.connect, schema_name=pytest.schema_name).get()['schemaMetadata'].keys()
        assert expected_dict_keys == schema_meta_data

