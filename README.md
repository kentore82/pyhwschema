# Hortonworks Schema Registry Python API

## Install
> `pip2.7 install pyhwschema`

## Usage

### Create connection
```
In [1]: import pyhwschema

In [2]: conn = pyhwschema.Connect("<schema_reg_host>","9090").connect_url()
```

### Get latest version of schema from MASTER branch with name test
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
### Get metadata for schema with name test
```
In [5]: pyhwschema.SchemaMetaData(conn,"test").get_dict()
Out[5]: 
{u'compatibility': u'BACKWARD',
 u'description': u'',
 u'evolve': True,
 u'name': u'test',
 u'schemaGroup': u'test-group',
 u'type': u'avro',
 u'validationLevel': u'LATEST'}
```

### Get latest version of schema with name test as string
```
In [8]: pyhwschema.SchemaLatest(conn,"test").get_string()
Out[8]: u'{"type":"record","namespace":"Testing","name":"Employee","fields":
[{"name":"Name","type":"string"},{"name":"Age","type":"int"}]}'
```

### Get latest version of schema with name test as dict
```
In [9]: pyhwschema.SchemaLatest(conn,"test").get_dict()
Out[9]: 
{u'fields': [{u'name': u'Name', u'type': u'string'},
  {u'name': u'Age', u'type': u'int'}],
 u'name': u'Employee',
 u'namespace': u'Testing',
 u'type': u'record'}

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
In [11]: pyhwschema.SchemaNewMeta(conn, schema_name="test", schema_group="test", 
                                  schema_meta_description="Used for testing",
                                  schema_compatibility="NONE", schema_validationlevel="LATEST").create()
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
 
In [14]: pyhwschema.SchemaNew(conn, schema_name="test",schema_text=test_avro_schema, 
                              schema_branch="MASTER", schema_description="Used for testing").create()
Out[14]: 2
```

### Create a new branch off a schema MASTER
```
pyhwschema.SchemaNewBranch(conn, schema_name="test", branch_name="test-branch", 
                           schema_description="Used for dev").create()
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

### Get all versions for a schema
```
In[9]: pyhwschema.SchemaGetVersions(conn, schema_name="test4", branch="testfork").get()
Out[9]: 
{u'entities': [{u'description': u'dgf',
   u'id': 108,
   u'mergeInfo': None,
   u'name': u'test4',
   u'schemaMetadataId': 15,
   u'schemaText': u'{...}',
   u'stateId': 1,
   u'timestamp': 1556878680184,
   u'version': 2},
  {u'description': u'test4',
   u'id': 107,
   u'mergeInfo': None,
   u'name': u'test4',
   u'schemaMetadataId': 15,
   u'schemaText': u'{...}',
   u'stateId': 5,
   u'timestamp': 1556877928952,
   u'version': 1}]}
```
