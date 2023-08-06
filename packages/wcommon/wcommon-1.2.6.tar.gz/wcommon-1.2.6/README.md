# This is my common Python tool classes.


### /data/apps/public/conf.ini content like:
```
[mysql]
host=example.com
port=3306
user=username
passwd=password
database=test
charset=utf8mb4
```

### Find the localhost internal network ip:
```python
from wcommon import *
ip = getLocalIp()
hostname = getLocalHostname()
```

### Decode unusual json string:
```python
from wcommon import *
line = """
{
    name:'java',
    system:'linux'
}
"""
result = dejson(line)
# output result
{"name":"java","system":"linux"}
```

### Operate mysql data:
```python
mysql = Mysql(configuraion_file="/data/apps/public/conf.ini", section="mysql")
```
```python
# query
rows = mysql.query("select * from example_table where status = %s order by id desc limit %s",(1,10))
for row in rows:
    print(row)
```

```python
# bulk_insert
mysql.bulk_insert("test.person",["name","age"],[["mahuateng",40],["liyanhong",39]])
```

```python
# bulk_insert
mysql.bulk_insert2("test.person",[{"name":"ma2","age":40},{"name":"liyanhong2","age":39},{"name":"ren"}] )
```