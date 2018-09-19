# Hortonworks Schema Registry Python API

## Install

## Usage

### Create connection
```
In [1]: import pyhwschema

In [2]: conn = pyhwschema.Connect("kb1.ibm.dsb.no","9090").connect_url()
```

### Get latest version of schema with name test
```
In [3]: pyhwschema.SchemaLatest(conn,"test").get()
Out[3]: 
{u'description': u'Used for testing',
 u'id': 31,
 u'mergeInfo': None,
 u'name': u'test',
 u'schemaMetadataId': 10,
 u'schemaText': u'{"type":"record","namespace":"Testing","name":"Employee",
                   "fields":[{"name":"Name","type":"string"},{"name":"Surname","type":"string"},
                   {"name":"Age","type":"int"}]}',
 u'stateId': 5,
 u'timestamp': 1537358228278,
 u'version': 1}
```

### Get a schema by using schema id
```
In [6]: pyhwschema.SchemaId(conn,schema_id="31").get()
Out[6]: 
{u'description': u'Used for testing',
 u'id': 31,
 u'mergeInfo': None,
 u'name': u'test',
 u'schemaMetadataId': 10,
 u'schemaText': u'{"type":"record","namespace":"Testing","name":"Employee",
                   "fields":[{"name":"Name","type":"string"},{"name":"Surname","type":"string"},
                   {"name":"Age","type":"int"}]}',
 u'stateId': 5,
 u'timestamp': 1537358228278,
 u'version': 1}
```

### Create metadata for a new schema (new or existing group)
```
In [11]: pyhwschema.SchemaNewMeta(conn,schema_name="test",schema_group="test").create()
Out[11]: 10
```

### Create a new version of a schema
```
test_avro_schema='''{"type":"record",
                     "namespace":"Testing",
                     "name":"Employee",
                     "fields":
                             [{"name":"Name","type":"string"},
                              {"name":"Age","type":"int"}
                              ]
                     }'''
 
In [14]: pyhwschema.SchemaNew(conn, schema_name="test",schema_text=test_avro_schema).create()
Out[14]: 2
```

### Drop/delete version of schema
```
In [4]: pyhwschema.SchemaDropVersion(conn, schema_name="test", schema_id="1").drop()
Out[4]: 
{u'responseCode': 1101,
 u'responseMessage': u"Entity with id [SchemaVersionKey{schemaName='test', version=1}] not found."}

In [5]: pyhwschema.SchemaDropVersion(conn, schema_name="test", schema_id="1").drop()
Out[5]: {'responseMessage': 'Schema version 1 dropped from schema test', 'responseCode': 200}
```