# 数据存储

在前面的几篇文章中，我分别总结了：

- 什么是爬虫
- requests模块总结
- 正则表达式提取数据
- XPath解析数据
- Beautiful Soup解析数据
- pyquery解析数据
- jsonpath提取json数据

在上面的几篇文章当中都有实战项目进行配合，帮助各位看我的文章的小伙伴可以亲切的感受到爬虫的乐趣。在实战的过程当中很多时候也会将数据保存起来放在Excel文件或者是文本文件当中，但是却没有对数据的存储做详细的介绍，因此本次文章我就打算为大家带来数据存储的保姆级教程！

## 文件存储

文件储存的形式多种多样，比如说保存成TXT存文本形式，也可以保存为JSON格式、CSV格式等等。

### TXT文本存储

将数据保存到TXT文件的操作是非常简单的，而且TXT文本几乎兼容任何平台，但是也是存在缺点的，那就是不利于检索。所以如果对检索数据的要求不高，追求第一的话，可以采用TXT文本存储。

#### 基本示例

爬取小说网，链接如下：

```
https://www.soxscc.com/BianShenJueSeShaoNv/1001322.html
```

首先可以使用requests将网页源码获取下来，然后使用pyquery解析库解析，提取其中的小说内容。

具体代码如下所示：

```python
import requests
from pyquery import PyQuery as pq


url = 'https://w、w.soxscc.com/BianShenJueSeShaoNv/1001322.html'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
}
html = requests.get(url, headers=headers).text
doc = pq(html)
text = doc('#con1001322').text()
file = open('都市仙尊.txt', 'w', encoding='utf-8')
file.write(text)
print('获取完毕')
```

通过pyquery将小说内容全部提取出来，然后利用Python提供的open( )方法打开文本文件，获取一个文件操作对象，这里赋值为file，接着利用file对象的write ()方法将提取的内容写入文本文件。

这里的open()方法的第一个参数即要保存的目标文件的名称，第二个参数为w，代表写入。另外还指定了文本的编码格式为utf-8。最后，还需要调用close()方法是来关闭文件内容。

运行程序，可以发现本地生成了一个`都市仙尊.txt`的文件，其内容如下所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210124154316532.png)

就是这样简单的将小说内容成功的保存成了文本形式。

#### 打开方式

在上面的示例中，open()方法的第二个参数设置成了w，这样写入文本时都是以写入的方式打开一个文件，如果文件已经存在，就将其覆盖，如果文件不存在，则创建新的文件。

关于文件的打开方式，其实还有其他几种，这里做简单的介绍。

- [ ] **r**：以只读的方式打开文件。文件的指针将会放在文件的开头。这是默认模式。
- [ ] **rb**：以二进制只读方式。文件指针将会放在文件的开头
- [ ] **r+**：以读写的方式打开一个文件。文件指针将放在文件的开头。
- [ ] **rb+**：以二进制读写方式打开一个文件。文件指针将会放在文件的开头。
- [ ] **w**：以写入方式打开一个文件。如果该文件已经存在，则将其覆盖。如果该文件不存在，则创建新的文件。
- [ ] **wb**：以二进制写入方式打开一个文件。如果该文件已经存在，则将其覆盖。如果该文件不存在，则创建新的文件。
- [ ] **w+**：以读写方式打开一个文件。如果该文件已经存在，则将其覆盖。如果该文件不存在，则创建新的文件。
- [ ] **wb+**：以二进制读写格式打开一个文件。如果该文件已经存在，则将其覆盖。如果该文件不存在，则创建新的文件。
- [ ] **a**：以追加方式打开一个文件。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容会被写入到已有内容之后。如果该文件不存在，则创建新的文件。
- [ ] **ab**：以二进制追加方式打开一个文件。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容会被写入到已有内容之后。如果该文件不存在，则创建新的文件。
- [ ] **a+**：以读写方式打开一个文件。如果文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果文件不存在，则创建新文件来读写。
- [ ] **ab+**：以二进制追加方式打开一个文件。如果该文件已存在，则文件指针将会放在文件的结尾。如果该文件不存在，则创建新文件用于读写。

### JSON文件存储

JSON，全称是javascript Object Notation，也就是javascript对象标记，它通过对象和数组来表示数据，构造简洁但是结构化程度高，是一种轻量级的数据交互格式。

#### 对象和数组

- [ ] **对象**：它在javascript中是使用花括号{ }包裹起来的内容，数据结构为{key1:value1,key2:value2,...}的键值对结构。
- [ ] **数组**：数组在javascript中是方括号[ ]包裹起来的内容，数据结构为["java","python","C++"]的索引结构

#### 读取JSON

Python为我们提供了简单易用的JSON库来实现JSON文件的读写操作，我们可以调用json库的loads()方法将JSON文本字符串JSON对象，可以通过dumps()方法将JSON对象转为文本字符串。

例如，这里有一段JSON形式的字符串，它是str类型，我们用Python将其转为可操作的数据结构。

具体代码如下所示：

```python
import json

string = '''
{ "store": {
    "book": [ 
      { "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95
      },
      { "category": "fiction",
        "author": "Evelyn Waugh",
        "title": "Sword of Honour",
        "price": 12.99
      },
      { "category": "fiction",
        "author": "Herman Melville",
        "title": "Moby Dick",
        "isbn": "0-553-21311-3",
        "price": 8.99
      },
      { "category": "fiction",
        "author": "J. R. R. Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "0-395-19395-8",
        "price": 22.99
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    }
  }
}
'''
print(type(string))
data = json.loads(string)
print(data)
print(type(data))
```

运行结果：

```
<class 'str'>
{'store': {'book': [{'category': 'reference', 'author': 'Nigel Rees', 'title': 'Sayings of the Century', 'price': 8.95}, {'category': 'fiction', 'author': 'Evelyn Waugh', 'title': 'Sword of Honour', 'price': 12.99}, {'category': 'fiction', 'author': 'Herman Melville', 'title': 'Moby Dick', 'isbn': '0-553-21311-3', 'price': 8.99}, {'category': 'fiction', 'author': 'J. R. R. Tolkien', 'title': 'The Lord of the Rings', 'isbn': '0-395-19395-8', 'price': 22.99}], 'bicycle': {'color': 'red', 'price': 19.95}}}
<class 'dict'>
```

这里使用loads()方法将字符串转为JSON对象。由于最外层是大括号，所以最终的类型是字典类型。

值得注意的是，JSON的数据需要用**双引号**来包围，不能使用单引号。

否则会出现JSON解析错误提示。

如果json文本中读取内容，假如这里有一个data.json这个文件，其内容就是上面所定义的json字符串，我们可以将文本内容读出，再通过json.loads()方法将其转换为Python的JSON对象。

具体代码如下所示：

```python
import json

with open('data.json', 'r') as file:
    text_json = file.read()
data_json = json.loads(text_json)
print(data_json)
print(type(data_json))
```

运行上面的代码你会发现，逻辑其实是一样的。

#### 写入JSON

另外，可以调用dumps()方法，可以将JSON对象转换为字符串。

具体代码如下所示：

```python
import json

string = '''
{ "store": {
    "book": [ 
      { "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95
      },
      { "category": "fiction",
        "author": "Evelyn Waugh",
        "title": "Sword of Honour",
        "price": 12.99
      },
      { "category": "fiction",
        "author": "Herman Melville",
        "title": "Moby Dick",
        "isbn": "0-553-21311-3",
        "price": 8.99
      },
      { "category": "fiction",
        "author": "J. R. R. Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "0-395-19395-8",
        "price": 22.99
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    }
  }
}
'''
with open('data2.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(string, ensure_ascii=False))
```

### csv文件存储

CSV，全称为Comma-Separated Values，中文可以叫做逗号分隔值或字符分隔值，其文件以纯文件形式存储表格数据。该文件是一个字符序列，可以由任意数目的记录组成，记录间以某种换行符号分隔。每条记录由字段组成，字段间的分隔符是其他字符或字符串，最常见的逗号或制表符。不过所有记录都有完全相同的字段序列，相当于一个结构化表的纯文本形式。

它比Excel文件更加简洁，XLS文本是电子表格，它包含了文本、数值、公式和格式等内容 ，而CSV中不包含这些内容，就是特定字符字符分隔的纯文本，结构简单清晰，所以，有时候用CSV来保存数据是比较方便的。

- **写入**

先看一个简单的例子：

```python
import csv

with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'name', 'age'])
    writer.writerow(['10001', 'Mike', 20])
    writer.writerow(['10002', 'Bob', 23])
    writer.writerow(['10003', 'Jordan', 25])
```

接下来就对上面的代码做简单的概述：

首先打开data.csv文件，然后指定打开模式为w（即写入），newline参数为空，否则会出现多出一个空行，获得文件句柄，随后调用csv库的writer()方法初始化写入对象，传入该句柄，然后调用writerow()方法传入每行的数据即可完成写入。

如果想要修改列与列之间的分隔符，只需要传入一个delimiter参数。

```python
writer = csv.writer(file, delimiter=' ')
```

另外，还可以调用writerows()方法同时写入多行，此时参数就需要为二维列表。

具代码如下所示：

```python
import csv

with open('data1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'name', 'age'])
    writer.writerows([['10001', 'Mike', 20],['10002', 'Bob', 22], ['10003', 'Jordan', 21]])
```

运行上面的代码你会发现，运行结果与上面是一样的。

但是一般情况下，爬虫爬取的都是结构化数据，我们一般会用字典来表示。在CSV库中也提供了字典的写入方式，具体代码如下所示：

```python
import csv


with open('data2.csv', 'w', newline='') as file:
    fieldnames = ['id','name','age']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'id':'10001', 'name':'Mike','age':20})
    writer.writerow({'id':'10002', 'name':'Bob','age':22})
    writer.writerow({'id':'10003','name':'Jordan', 'age':21})
```

另外，如果想要追加写入的话，可以修改文件的打开模式，即将open()函数的第二个参数改为a，代码如下：

```python
import csv

with open('data2.csv', 'a') as file:
    fieldnames = ['id','name','age']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writerow({'id':'10004', 'name':'Durant','age':25})
```

- **读取**

我们同样可以通过CSV库来读取CSV文件。例如，将刚才写入的文件内容读取出来，具体代码如下所示：

```python
import csv

with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
```

另外，如果接触过pandas的话，可以利用read_csv()方法将数据从CSV读读取出来，例如：

```python
import pandas as pd

df = pd.read_csv('data.csv')
print(df)
```

### 关系型数据库存储

关系型数据库是基于关系型数据库，而关系模型是通过二维表来保存的，但是它的存储方式就是行列组成的表，每一列是一个字段，每行是一条记录。表可以是某个实体的集合，而实体之间存在关系，这就需要表与表之间的关联关系来体现，如主键外键的关联关系。多个表组成一个数据库，也就是关系型数据库。

关系型数据库有SQLite，MySQL，Oracle，SQL Server，DB2等，下面重点讲解MySQL的用法。

#### 准备工作

在开始之前，请确保已经安装好MySQL数据库并保证它可以正常运行，而且需要安装好PyMySQL。

安装MySQL可以自行百度。

安装PyMySQL的方法如下所示：

```
pip install pymysql
```

#### 连接数据库

首先尝试一下连接数据库。当假设MySQL运行在本地，运行端口为3306。

具体代码如下所示：

```python
import pymysql


host = 'localhost'
user = 'root'
password = '密码'
port = 3306
db = pymysql.connect(host=host, user=user, password=password, port=port)
cursor = db.cursor()
cursor.execute('select version()')
data = cursor.fetchone()
print('database version:',data)
cursor.execute('create database spiders default character set utf8')
db.close()
print('创建成功')
```

接下来对上面的代码做简单的解释：

首先通过pymysql的connect()方法声明一个MySQL连接对象db，此时需要传入MySQL运行时的host（即IP）。由于MySQL在本地运行，所以传入的是localhost，如果MySQL运行在远程，则需要传入公网的IP地址。

连接成功之后，再调用cursor()获取到MySQL的操作游标，利用游标来执行MySQL语句。这里我们执行了两条SQL语句，直接用execute()方法执行即可。第一句是获取MySQL的版本信息，然后调用fetchone()方法获取第一条数据，也就是版本号。第二句SQL执行创建数据库名为spiders，默认编码是utf-8。

如何查看是否创建成功，可以参考下面的方法。

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210127101538358.png)

从上图可以看到databases里面成功创建了一个数据库：spiders。

#### 创建表

一般来说，创建数据库的操作只需要执行一次就可以了。

接下来要操作数据库还需要额外指定一个参数db。

接下来，创建一个数据表students，此时需要执行创建表SQL语句即可。这里指定三个字段，如下表所示：

| 字段名 | 含义 |  类型   |
| :----: | :--: | :-----: |
|   id   | 学号 | varchar |
|  name  | 姓名 | varchar |
|  age   | 年龄 |   int   |

创建students表的具体代码如下所示：

```python
import pymysql

host = 'localhost'
user = 'root'
password = '密码'
port = 3306
db = pymysql.connect(host=host, user=user, password=password, port=port, db='spiders')
cursor = db.cursor()
sql = 'create table if not exists students (id varchar(255) not null, name varchar(255) not null, age int not null, primary key (id))'
cursor.execute(sql)
db.close()
print('创建成功')
```

运行之后，我们便创建了一个名为students的数据表。

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210127101809792.png)

从上图可以看到，我们成功的创建了数据表：students。

同样的，也可以查看该表的字段有哪些，如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210127102213288.png)

#### 插入数据

下一步就是向数据库中插入数据了，例如这里爬取了一个学生的信息，学号为2020001，名字为Bob，年龄是18，那么应该怎么样将数据插入数据库呢？

具体代码如下所示：

```python
import pymysql

host = 'localhost'
user = 'root'
password = '密码'
port = 3306

data = {
    'id':'2020001',
    'name':'Bob',
    'age':18
}
table = 'students'
keys = ','.join(data.keys())    # id,name,age
values = ','.join(['%s']*len(data)) # %s,%s,%s

db = pymysql.connect(host=host, user=user, password=password, port=port, db='spiders')
cursor = db.cursor()

sql = 'insert into {table}({keys}) values ({values})'.format(table=table, keys=keys, values=values)
try:
    if cursor.execute(sql, tuple(data.values())):
        print('插入成功')
        db.commit()
except:
    print('插入失败')
    db.rollback()
db.close()
```

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210127105235459.png)

从上面的代码以及图片可以看到，成功的将数据插入到了students表当中。

在上面的代码中值得注意的是，需要执行db对象的commit()方法才可以实现数据插入，这个方法才是真正将语句提交到数据库执行的方法，对于数据的插入、更新、删除操作，都需要调用该方法才能生效。

接下来，我们加一层异常处理，如果执行失败，则调用rollback()执行数据回滚，相当于什么都没有发生过。

#### 删除数据

删除操作相对简单，直接用delete语句即可，只需要指定要删除的表名和删除的条件。

在删除之前，我们可以再往数据库里面多插入几条数据，在插入的时候要注意，id是主键，因此不能重复。

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210127133759690.png)

如上图所示：我们额外的插入了3条数据。

删除数据的代码如下所示：

```python
import pymysql


host = 'localhost'
user = 'root'
password = '密码'
port = 3306
table = 'students'
condition = 'age > 20'
db = pymysql.connect(host=host, user=user, password=password, port=port, db='spiders')
cursor = db.cursor()
sql = 'delete from {table} where {condition}'.format(table=table, condition=condition)
try:
    cursor.execute(sql)
    db.commit()
    print('删除成功')
except:
    db.rollback()
    print('删除失败')


db.close()
```

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210127134351372.png)

看了上面的图片之后相信你就明白了，代码的含义了吧。条件是删除年龄大于20岁的学生，并执行该语句。

#### 查询数据

查询会用到select语句。

具体代码如下所示：

```python
import pymysql


host = 'localhost'
user = 'root'
password = '密码'
port = 3306
table = 'students'

db = pymysql.connect(host=host, user=user, password=password, port=port, db='spiders')
cursor = db.cursor()
sql = 'select * from students'
try:
    cursor.execute(sql)
    result = cursor.fetchall()
    print('results:', result)
    for row in result:
        print(row)
except:
    print('查询失败')
db.close()
```

运行结果：

```
results: (('2020001', 'Bob', 18), ('2020003', 'Mike', 16), ('2020004', 'Mark', 19))
('2020001', 'Bob', 18)
('2020003', 'Mike', 16)
('2020004', 'Mark', 19)
```

调用fetchall()方法可以将全部数据获取下来。

当然，也可以根据条件来获取数据，比如说接下来要获取小于19岁学生的信息。

具体代码如下所示：

```python
import pymysql


host = 'localhost'
user = 'root'
password = '密码'
port = 3306
table = 'students'

db = pymysql.connect(host=host, user=user, password=password, port=port, db='spiders')
cursor = db.cursor()
sql = 'select * from students where age < 19'
try:
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        print(row)
except:
    print('查询失败')
db.close()
```

运行结果：

```
('2020001', 'Bob', 18)
('2020003', 'Mike', 16)
```

#### 更新数据

上面讲完了删除、插入和查询，还剩下一个非常重要的操作那就是修改数据，修改数据需要用到update语句。

具体代码如下所示：

```python
import pymysql


host = 'localhost'
user = 'root'
password = '698350As?'
port = 3306
table = 'students'

db = pymysql.connect(host=host, user=user, password=password, port=port, db='spiders')
cursor = db.cursor()
sql = 'update students set age = %s where name = %s'
try:
    cursor.execute(sql, (20, 'Bob'))
    db.commit()
    print('修改成功')
except:
    db.rollback()
    print('修改失败')
db.close()	
```

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210127140548668.png)

通过上面的图片你会发现成功的将Bob的年龄从18改成了20。

但是在抓取数据的过程中，大多数都是需要插入数据，我们更关心的是会不会出现重复的数据，如果出现了，我们希望的是更新数据，而不是再保存一个。那么就需要我们动态的构造SQL语句了。

具体方法如下所示：

```python
import pymysql


host = 'localhost'
user = 'root'
password = '698350As?'
port = 3306
table = 'students'

db = pymysql.connect(host=host, user=user, password=password, port=port, db='spiders')
cursor = db.cursor()
data = {
    'id':'2020001',
    'name':'Bob',
    'age':28
}
keys = ','.join(data.keys())
values = ','.join(['%s'] * len(data))
sql = 'insert into {table}({keys}) values ({values}) on duplicate key update'.format(table=table, keys=keys, values=values)
update = ','.join([" {key}= %s".format(key=key) for key in data])
sql+=update
try:
    if cursor.execute(sql, tuple(data.values())*2):
        print('更新成功')
        db.commit()
except:
    print('更新失败')
    db.rollback()
db.close()
```

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210127142058229.png)

这里其实是构造了一个插入语句，但是我们在后面加了on duplicate key update。这行代码的意思是如果主键已经存在，就执行更新操作。因此数据就不会被重复插入。

至此，关于关系型数据库MySQL的讲解到这里就结束了，在下一篇文章中就会重点讲解关于非关系型数据库，例如Redis和MongoDB。本次的文章篇幅有点大，就不再写实战内容，实战内容我会在写完非关系型数据库之后一并分享给大家！！

**啃书君说**：

文章的每一个字都是我用心敲出来的，只希望对得起每一位关注我的人。

点个**[在看]**，让我知道，你们也在为自己的学习拼搏和努力。

**路漫漫其修远兮，吾将上下而求索**。

我是**啃书君**，一个专注于学习的人，**你懂得越多，你不懂得越多**。更多精彩内容，我们下期再见！

