# 前言

写了很多的教程，不知道大家发现没有，很多时候写爬虫，并保存数据的时候，一直都是将数据保存至txt文件或者是Excel文件中。不知道你是否想过，在企业的开发过程 ，数据是保存在哪里的吗？数据是保存在数据库当中，常见的数据库有MySQL、Oracle、mongodb等等。我们今天要讲的数据库是MySQL。

# 关系型数据库

关系型数据库是是通过二维表来保存数据的，它的存储方式就是行列组成的表，每一列是一个字段，每一行是一条记录。表可以是某个实体的集合。而实体之间存在关系，这就需要表与表之间的关联关系来体现，如主键与外键的关联关系，多表组成一个数据库也就是关系型数据库。

## 准备工作

在开始之前，请确保已经安装好MySQL数据库，若未安装是无法使用的，安装方式，可以自行百度。

在windows安装pymysql的方式如下所示：

```
pip install pymysql
```

## 连接数据库

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

## 创建表

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

## 插入数据

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

## 删除数据

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

## 查询数据

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

## 更新数据

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

至此关于爬虫与MySQL结合的基本知识都介绍完毕了，希望各位小伙伴看完这篇文章之后对你们有所启发。

学完上面的内容之后，我们就来进入实战吧！

# 实战

学完之后有没有一种跃跃欲试的感觉，觉得自己就可以写一串爬虫与MySQL集合的代码了吧。如果你觉得可以，那么恭喜你，上面的内容，你基本上学会了。如果不行，那也没有关系，**啃书君**会手把手教你学会。怎么样学？看实战。

## 准备

本次爬虫需要用到的工具有requests、pymysql。安装方式如下：

```
pip install requests
pip install pymysql
```

## 当当网

今天实战的内容就是当当网近24小时的图书畅销榜。为什么选择写这个呢？因为我发现之前写的当当网爬虫失效了，今天更新一下，顺带把写代码过程中遇到的坑分享给大家，避免大家再次入坑。

## 网页分析

网站链接如下：

```
http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-24hours-0-0-1-1
```

打开网页之后，紧接着打开开发者工具并刷新页面，点开第一个数据包，如图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210213233656349.png)

通过观察Response Headers可以发现，该网页把编码格式设置为gb2312，接下来我们就可以使用requests库模拟浏览器向目标服务器发送请求。

具体代码如下所示：

```python
def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        html = response.content.decode('gb2312', 'ignore')
        return html
    except:
        print('连接失败')
```

既然从上面的图片我们知道了该网页的编码为gb2312，但是当我设置编码的为gb2312的时候依然还是报错了，报了一个UnicodeDecodeError这个错误，因此我在后面添加上'ignore'这个参数，忽略这个错误，进而得到正确的响应。

## 解析网页

得到网页的响应之后，想要获取其中的信息就不难了。这里我使用正则表达式来提取网页的信息。

如果对正则表达式不熟悉的小伙伴可以看我之前写的文章。

我们要获取的信息有下面这几个：

- 书籍名称
- 推荐率
- 作者姓名 
- 出版日期
- 出版社
- 价格

### 书籍名称

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210214103132852.png)

从上图所示，要获取书籍名称还是比较容易的，但是，这里有个注意点：如果书籍名称直接获取a标签的文本就有可能获取到`<span class="dot">...</span>`，但这个并不是我们想要的，所以可以直接从a标签的title属性中获取书籍名称。

具体代码如下所示：

```python
book_name_pattern = re.compile('<li>.*?<div class="name">.*?<a.*?title="(.*?)">.*?</a>.*?</div>', re.S)
book_names = re.findall(book_name_pattern, html)
```

### 推荐率

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210214104258421.png)

推荐率也是很容易后获取的，它位于属性class=“star”的div标签内下的a标签，只需要提取该a标签的文本即可。

具体代码如下所示：

```python
tuijian_pattern = re.compile('<div class="star">.*?<span class="tuijian">(.*?)</span>.*?</div>', re.S)
tuijians = re.findall(tuijian_pattern, html)
```

### 作者姓名

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210214110259983.png)

作者的姓名位于属性class=“publisher_info”的div标签下的a标签内，因此只需要获取a标签内的文本即可。

具体代码如下所示：

```python
author_pattern = re.compile('<li>.*?<div class="publisher_info">.*?<a.*?>(.*?)</a>', re.S)
authors = re.findall(author_pattern, html)
```

### 初版社与出版时间

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210214110934863.png)

如上图所示，出版时间与出版社都是位于属性class=“publisher_info”的div标签，出版社信息位于a标签内，而出版时间位于span标签内。这里同样也有一个陷阱，存在着两个相同的class，那么这里就要注意一下了，要添加上最开始的li标签就不会出错。具体代码如下所示：

```python
time_pattern = re.compile('<li>.*?<div class="publisher_info">.*?<span>(.*?)</span>', re.S)
publisher_time = re.findall(time_pattern, html)

publisher_pattern = re.compile('<li>.*?<div class="publisher_info">.*?<span>.*?</span>.*?<a.*?>(.*?)</a>', re.S)
publisher = re.findall(publisher_pattern, html)
```

### 书籍价格

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210214111818553.png)

书籍的价格位于class="price"的div标签内的p标签下的span标签，只需要获取到span标签的文本信息即可。

具体代码如下所示：

```python
 price_pattern = re.compile('<div class="price">.*?<span class="price_n">(.*?)</span>', re.S)
 prices = [price.replace('&yen;', '￥') for price in re.findall(price_pattern, html)]
```

获取到的价格前面会带&yen，这样的字符，因此需要做替换。

最后只需要对上面获取到的所有书数据进行打包并返回，代码如下所示：

```python
return zip(book_names, authors, tuijians, publisher_time, publisher, prices)
```

## 创建数据库与数据表

创建数据库与数据表的时候，可以进入MySQL的终端，或者是借助一些工具去创建，创建的代码如下：

```
# 创建数据库
create database dangdang default character set utf8


# 创建表格
CREATE TABLE IF NOT EXISTS book (id int auto_increment PRIMARY KEY, booknames VARCHAR(255) NOT NULL, authornames VARCHAR(255) NOT NULL, stars VARCHAR(255) NOT NULL, publishertime DATE NOT NULL, publisher VARCHAR(255) NOT NULL, price VARCHAR(255) NOT NULL)
```

大小写，无影响。

## 连接数据库并插入数据

具体代码 如下所示：

```python
def save_data(datas):
    host = 'localhost'
    user = 'root'
    password = '698350As?'
    port = 3306
    db = pymysql.connect(host=host, user=user, password=password, port=port, db='dangdang')
    cursor = db.cursor()
    sql = 'insert into book(booknames, authornames, stars, publishertime, publisher, price) values (%s, %s, %s, %s, %s, %s)'
    for data in datas:
        print(data)
        try:
            cursor.execute(sql, data)
            db.commit()
            print('插入成功')
        except:
            db.rollback()
            print('插入失败')
```

## 最后结果

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210214113106706.png)

所有的内容都成功的保存到了数据库中。

# 最后

没有什么事情是可以一蹴而就的，生活如此，学习亦是如此！

因此，哪里会有什么三天速成，七天速成，唯有坚持，方能成功！

**啃书君说**：

文章的每一个字都是我用心敲出来的，只希望对得起每一位关注我的人，为文章点个【**赞**】，让我知道，你们也在为自己的学习努力和拼搏着。

**路漫漫其修远兮，吾将上下而求索**。

我是**啃书君**，一个专注于学习的人，**你懂的越多，你不懂的越多**，更多精彩内容，我们下期再见！