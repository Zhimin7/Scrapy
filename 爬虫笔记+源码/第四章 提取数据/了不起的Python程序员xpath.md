# 什么是Xpath

XPath，全称XML Path Language，即XML路径语言，它是在XML语言中查找信息的语言。它最初是用来搜寻XML文档的，但是它同样适用于HTML文档的搜索。

# Xpath选取节点

Xpath，使用路径表达式在XML文档中选取节点。节点是通过路径或者是step来选取的。

**下面列出了最有用的路径表达式**：

|  表达式  |                           描述                           |
| :------: | :------------------------------------------------------: |
| nodename |                  选取此节点的所有子节点                  |
|    /     |                       从根节点选取                       |
|    //    | 从匹配选择的当前节点选择文档中的节点，而不考虑他们的位置 |
|    .     |                       选取当前节点                       |
|    ..    |                   选取当前节点的父节点                   |
|    @     |                         选取属性                         |

# 准备工作

接下来我将举一个例子，带你简单了解Xpath的用法。

在使用Xpath之前，首先应该安装lxml这个库，安装方式如下所示：

```
pip install lxml
```

# 简单案例

## 匹配节点

```html
<?xml version="1.0" encoding="ISO-8859-1"?>

<bookstore>

<book>
  <title lang="eng">Harry Potter</title>
  <price>29.99</price>
</book>

<book>
  <title lang="eng">Learning XML</title>
  <price>39.95</price>
</book>

</bookstore>
```

看到上面的xml文档了吗？我们接下来就将列出一些路径表达式，以及表达式的结果：

|   路径表达式    |                             结果                             |
| :-------------: | :----------------------------------------------------------: |
|    bookstore    |                选取bookstore元素的所有子节点                 |
|   /bookstore    |                     选取根元素bookstore                      |
| bookstore/book  |                选取bookstore下的所有book元素                 |
|     //book      |        选取所有的book子元素，而不管它们在文档中的位置        |
| bookstore//book | 选取属于bookstore元素的后代所有book元素，而不管它们位于bookstore之下的什么位置 |
|     //@lang     |                    选取名为lang的所有属性                    |

那怎么样通过Python代码来实现呢？请看下面的代码展示：

```python
from lxml import etree


html = etree.parse('./test.html', etree.HTMLParser())

bookstore = html.xpath('//bookstore')
print(bookstore)

book = html.xpath('//bookstore/book')
print(book)

book = html.xpath('//book')
print(book)

lang = html.xpath('//@lang')
print(lang)
```

运行结果如下：

```
[<Element bookstore at 0x295815f2e40>]
[<Element book at 0x295815f2e80>, <Element book at 0x295815f2f40>]
[<Element book at 0x295815f2e80>, <Element book at 0x295815f2f40>]
['en', 'eng', 'eng']
```

那接下来我就对上面的代码做简单的说明：

首先导入lxml包中的etree模块，通过方法parse()，对html代码进行解析，返回_ElementTree对象（注明：我将上面的HTML代码放入了test.html文件中），然后接下来就可以使用xpath语法了。

在匹配节点的时候，你会发现，每一次我都是在前面放上两个`//`，这是因为bookstore或者是book不是该HTML代码中的根节点，所以我们需要匹配当前文档中的节点，而不考虑它们所在的位置。但是你从上面的HTML代码来看bookstore的确是根节点没有错，但是xpath需要标准的HTML代码

## 谓语

谓语就是用来查找某个特定节点或者包含某个指定值的节点，谓语被嵌在方括号中。

在下面的表格中，我列出了带有谓语的一些路径表达式，如下表所示：

|        路径表达式         |                          结果                          |
| :-----------------------: | :----------------------------------------------------: |
|    /bookstore/book[1]     |       选取属于根节点bookstore下的第一个book节点        |
|  /bookstore/book[last()]  |      选取属于根节点bookstore下的最后一个book节点       |
| /bookstore/book[last()-1] |     选取属于根节点bookstore下的倒数第二个book节点      |
|      //title[@lang]       |            选取所有名为lang属性的title元素             |
|   //title[@lang='eng']    |       选取所有名为lang属性的元素，且属性值为eng        |
| /bookstore/book[price>35] | 选取bookstore节点的所有book节点，其中price元素值大于35 |

## 选取未知节点

Xpath可以通过通配符来选取未知的xml元素。

| 通配符 |        描述        |
| :----: | :----------------: |
|   *    |  匹配任何元素节点  |
|   @*   |  匹配任何属性节点  |
| node() | 匹配任何类型的节点 |

在下面的表格中，我列出了一些路径表达式，以及表达式的结果：

|  路径表达式  |              结果               |
| :----------: | :-----------------------------: |
| /bookstore/* | 选取bookstore节点下的所有子节点 |
|     //*      |      选取文档中的所有节点       |
| //title[@*]  |    选取所有带属性的title元素    |

看到这里，想必各位小伙伴对Xpath已经有了较为简单的了解了，但是还需要和Python进行结合才是我们的目的，因此我将导入下面的案例，为大家剖析xpath语法与Python的结合。

# 案例导入

现在通过实例来xpath对网页解析的过程

```python
from lxml import etree


text = '''
<div>
    <ul>
        <li class="item-0"><a href="link1.html">first-item</a></li>
        <li class="item-1"><a href="link2.html"></a>second-item</li>
        <li class="item-inactive"><a href="link3.html">third-item</a></li>
        <li class="item-1"><a href="link4.html">fourth-item</a></li>
        <li class="item-0"><a href="link5.html">fifith-item</a></li>
    

</div>
'''
html = etree.HTML(text)
result = etree.tostring(html)
print(result.decode('utf-8'))
```

这里首先通过lxml这个库导入etree这个模块，然后声明一段HTML文本，调用HTML类进行初始化，这就成功构造了xpath对象。

细心的读者朋友应该会发现我上面的代码片段中标签**ul**是没有闭合的，但是运行之后你会发现运行结果是闭合的，并且还自动添加了**html**和**body**标签。

这是因为我们调用了**tostring( )**方法帮助我们将HTML文本进行修正，但是要注意的是**tostring( )**方法`返回的结果是byte类型`，因此这里调用了tostring( )方法即可输出修正后的HTML代码。使用decode( )方法可以将byte类型的数据转成str类型的数据。

当然，etree这个模块也可以直接读取文本文件进行解析，具体代码如下所示：

```python
from lxml import etree


html = etree.parse('./test.html', etree.HTMLParser())
result = etree.tostring(html)
print(result.decode('utf-8'))
```

其中文件test.html的内容就是上面示例的HTML代码。

## 获取所有的节点

我们一般会使用 // 开头的Xpath规则来选取所有符合要求的节点，假如我需要获取所有的节点，示例代码如下所示：

```python
from lxml import etree


html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//*')
print(result)
```

首先对上面的代码做简单的说明，这里的 * 代表匹配全部，所以所有的节点都会获取到，返回值是一个列表。

每个元素是Element类型，其中后面跟的就是节点的名称。

运行结果如下所示：

```
[<Element html at 0x1a0334c39c0>, <Element body at 0x1a0334c3a80>, <Element div at 0x1a0334c3ac0>, <Element ul at 0x1a0334c3b00>, <Element li at 0x1a0334c3b40>, <Element a at 0x1a0334c3bc0>, <Element li at 0x1a0334c3c00>, <Element a at 0x1a0334c3c40>, <Element li at 0x1a0334c3c80>, <Element a at 0x1a0334c3b80>, <Element li at 0x1a0334c3cc0>, <Element a at 0x1a0334c3d00>, <Element li at 0x1a0334c3d40>, <Element a at 0x1a0334c3d80>]

```

从上面的运行结果你会发现，html、body、div、ul、li等等节点。

## 获取指定节点

例如，在这里我要获取到所有的li节点，那该怎么办呢？其实很简单，具体代码示例如下所示：

```python
from lxml import etree


html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li')
print(result)

```

通过上面的几个例子，不知道大家有没有明白节点的含义。

其实节点的含义你可以理解为当前的html文档开始的地方。

如果上面的代码你修改一段，变成这样：

```python
result = html.xpath('/li')
```

运行之后你会发现列表是空的，因为该文档的的子节点中没有 li 这个节点，li 是该文档的子孙节点，而该文档的子节点是html。

所以，你将代码这样修改：

```python
result = html.xpath('/html')
# 另一种写法
result = html.xpath('.')
```

运行之后你会惊喜的发现，成功获取到了html节点。

## 子节点与子孙节点

通过/或//即可查好元素的子节点或者是子孙节点，假如你想要选择 li 节点下的所有 a 节点可以这样实现，具体代码如下所示：

```python
from lxml import etree


html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li/a')
print(result)
```

先对上面的代码做简要的说明：//li表示获取所有的li节点，/a表示获取 li 节点下的子节点 a 。

或者也可以这样写，你可以先获取到所有的 ul 节点，再获取 ul 节点下的所有**子孙节点** a 节点。

具体示例代码如下所示：

```python
from lxml import etree


html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//ul//a')	# 注意//a
print(result)

```

运行上面的代码你会发现结果是相同的。

## 获取父节点

通过上面的几个例子，想必应该知道何为子节点与子孙节点。那么如何寻找父节点呢？这里可以通过 .. 来实现。

比如，我现在要选中href属性为link4.html的a节点，然后再获取其父节点，再获取其class属性。看着内容好多，那就要一个一个来，不要着急。

具体代码示例如下所示：

```python
from lxml import etree


html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//a[@href="link4.html"]/../@class')
print(result)
```

运行结果

```python
['item-1']
```

## 属性的匹配

在选取数据的时候，可以使用@符号进行属性的过滤，比如：这里通过选取 li 标签属性class为item-0的节点，可以这样实现：

```python
from lxml import etree


html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li[@class="item-0"]')
print(result)
```

你可以试着运行上面的代码，你会发现匹配到了两个正确的结果。

## 文本获取

在整个HTML文档中肯定会有很多的文本内容，有些恰恰是我们需要的，那么应该如何获取这些文本内容呢？

接下来可以尝试使用text( )方法获取节点中的文本。

具体代码实例如下所示：

```python
from lxml import etree


html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li[@class="item-0"]/a/text()')
print(result)
```

试着运行上面的代码，你会发现，已经获取到了所有class属性为item-0的 li 节点下的文本。

## 获取标签属性值

在编写爬虫的过程中，很多时候我们需要的数据可能是属性值，那就要学会如何来获取我们想要的属性值了。

例如，我想要获取 li 节点下的a节点的所有href属性，具体代码示例如下所示：

```python
from lxml import etree


html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li/a/@href')
print(result)
```

通过@href就获取到了该节点的href属性值，当然，它们都是以列表的形式返回。

## 属性多值的匹配

在编写前端代码的时候，有些节点为了方便可能就会存在多个值，那么就要使用contains函数了，例如：

```python
from lxml import etree

text = '''
<li class="li li-first"><a href="link.html">first item</a></li>

'''
html = etree.HTML(text)
result = html.xpath('//li[contains(@class, "li")]/a/text()')
print(result)

```



要是你说我怎么记得住这些函数，那好，还可以这样写。

具体代码示例如下：

```python
from lxml import etree

text = '''
<li class="li li-first"><a href="link.html">first item</a></li>

'''
html = etree.HTML(text)
result = html.xpath('//li[@class="li li-first"]/a/text()')
print(result)
```

看出区别了吗？

运行上面的两段代码，你会发现结果是一样的。

## 多属性匹配

另外，我们写写爬虫的时候会遇到另一种情况，那就是在一个标签内存在多个属性。那此时可以用and操作符来连接

具体代码示例如下所示：

```python
from lxml import etree

text = '''
<li class="li li-first" name="item"><a href="link.html">first item</a></li>

'''
html = etree.HTML(text)
result = html.xpath('//li[contains(@class, "li") and @name="item"]/a/text()')
print(result)
```

## xpath运算符的简单介绍

从上面的示例你应该知道了，and是xpath的运算符，xpath的运算符也是比较多的，那么接下来对xpath运算符做简单的介绍。

| 运算符 |                       描述                        |
| :----: | :-----------------------------------------------: |
|   or   |                        或                         |
|  and   |                        与                         |
|   \|   | 计算两个节点集，//li \| //a 获取li和a元素的节点集 |
|   +    |                       加法                        |
|   -    |                       减法                        |
|   *    |                       乘法                        |
|  div   |                       除法                        |
|   =    |                       等于                        |
|   !=   |                      不等于                       |
|   <    |                       小于                        |
|   >    |                       大于                        |
|   >=   |                     大于等于                      |
|   <=   |                     小于等于                      |
|  mod   |                     计算余数                      |

## 按序选择

有时候，我们编写爬虫的时候可能会匹配到几个相同的 li 节点，但是，我只需要第一个或者最后一个就可以了。那这时该怎么样处理那？

这时可以通过索引的方式，传入指定的索引，获取指定节点。

具体代码示例如下所示：

```python
from lxml import etree

text = '''
<div>
    <ul>
        <li class="item-0"><a href="link1.html">first-item</a></li>
        <li class="item-1"><a href="link2.html"></a>second-item</li>
        <li class="item-inactive"><a href="link3.html">third-item</a></li>
        <li class="item-1"><a href="link4.html">fourth-item</a></li>
        <li class="item-0"><a href="link5.html">fifith-item</a></li>
    </ul>

</div>
'''
html = etree.HTML(text)
# 获取第一个li节点
result = html.xpath('//li[1]/a/text()')
print(result)
# 获取最后一个li节点
result = html.xpath('//li[last()]/a/text()')
print(result)
# 获取位置小于3的li节点
result = html.xpath('//li[position()<3]/a/text()')
print(result)
# 获取倒数第三个li节点
result = html.xpath('//li[last()-2]/a/text()')
print(result)
```

上述内容所描述的是xpath的在爬虫应用中常见使用方法，如果各位小伙伴想要继续深入学习的话，可以参考w3c进行学习，网址如下：

```
https://www.w3school.com.cn/xpath/xpath_syntax.asp
```

# 最后

没有什么事情是可以一蹴而就的，生活如此，学习亦是如此！

因此，哪里有什么三天速成，七天速成，唯有坚持，方能成功！

**啃书君说**：

文章的每一个字都是我用心敲出来的，只希望对得起每一位关注我的人。点个【赞】与【在看】，让我知道，你们也在为自己的学习拼搏和努力着。

**路漫漫其修远兮，吾将上下而求索**。

我是**啃书君**，一个专注于学习的人，**你懂的越多，你不懂的越多**，更多精彩内容我们下期再见！

