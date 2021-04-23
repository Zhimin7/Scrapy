# 前言

在上篇文章中，我为大家介绍了Ajax的分析和抓取方式，这其实也是javascript动态渲染页面的一种方式，通过直接分析Ajax，仍然可以通过requests来实现数据的获取。

不过javascript动态渲染页面不止Ajax这种。有些网站的分页部分可能是通过javascript生成的，并非原生的HTML代码，这其中并不包含Ajax请求。再有就是淘宝页面，它即使是Ajax获取的数据，但是其Ajax接口会含有很多的加密参数，我们获取下来之后很难通过Ajax请求来得到规律。

为了解决这个问题，Python提供了很多模拟浏览器运行的库，如selenium、splash、PyV8、Ghost等。本次内容，我将为大家分享selenium的用法。有了它们就不需要为动态渲染的页面而发愁了。

是不是内心会有一点点的小激动呢？

# selenium的安装

是不是会有很多小伙伴会认为这个安装有必要讲吗？不就是一个pip就可以搞定嘛，当然没有那么简单了。

selenium是一个自动化测试工具，利用它我们可以驱动浏览器执行特定的动作，如点击、下拉等操作。对于一些javascript渲染的页面来说，这招还是很有效的。

## pip 安装

安装方式：我推荐pip安装

```
pip install selenium
```

## 验证安装

进入Python命令交互模式，导入selenium包，如果没有报错，那么就说明安装成功。

```
C:\Users\admin>python
Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 23:11:46) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import selenium
>>>
```

但是这样还不够，但是这样还不够，因为我们需要用到浏览器（如Chrome、Firefox）来配合selenium工作。有了浏览器我们才能配合selenium进行页面抓取。

## ChromeDriver的安装

当然，首先得下载好Chrome浏览器，可以自行百度下载并安装。

随后安装ChromeDriver。因为只有安装了ChromeDriver之后，才能驱动Chrome浏览器完成相应的操作。

- **1、准备工作**

在这之前请务必确定已经安装成功Chrome浏览器。

- **2、查看版本**

点击Chrome设置——>点击关于Chrome，即可查看Chrome的版本。如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210207171628259.png)

这里我的浏览器版本号是88.0。

请记住Chrome的版本号，因为等一下选择ChromeDriver版本的时候需要用到。

## 下载ChromeDriver

下载网址如下：

```
http://npm.taobao.org/mirrors/chromedriver
```

选择与你的浏览器相符合的版本，如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210207172148153.png)

## 环境变量配置

将刚刚下载好的驱动解压出来，并将其放入Python的Scripts目录下即可。如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210207174314161.png)

## 验证安装

配置完成之后可以在命令行输入chromedriver命令，如果输入之后出现如下图所示的界面，则说明环境变量配置好了。

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210207174505353.png)

# selenium的基本使用介绍

## 简单示例

```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
```

那么接下来就是对上面的代码进行简单的分析。

`selenium.webdriver`提供了所有的webdriver实现，当前支持的webdriver有：Firefox、Chrome、IE和Remote。`Keys`类提供键盘支持，比如：F1、enter等等。

```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
```

接下来创建一个Chrome实例

```python
driver = webdriver.Chrome()
```

`driver.get()方法`将打开URL中填写的地址，webdriver将等待，直到页面完全加载完毕（其实是等待onload方法执行完毕），然后继续执行脚本。值得注意的是，如果页面使用了大量的Ajax加载，webdriver可能不知道什么时候加载完毕。

```python
driver.get("http://www.python.org")
```

下一行使用`assert`的方式确认标题是否含有`python`一词。当assert语句后面为False时，将会抛出异常。

```python
assert "Python" in driver.title
```

同时webdriver也提供了大量的查找页面元素的方法。，例如：find_element_by_*， *就是属性。

```python
elem = driver.find_element_by_name("q")
```

接下来发送一个关键字，这个方法类似于使用键盘输入关键字。特殊的按键可以使用Keys类来输入，该类是继承`selenium.webdriver.common.keys`，为了安全起见，需要先清除input输入框里面的内容，避免对搜索结果存在影响。

```python
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
```

提交页面之后，你会得到所有的结果。为了使特定的结果被找到，使用assert如下：

```python
assert "No results found." not in driver.page_source
```

最后关闭浏览器。值得注意的是close()方法只会关闭一个标签，因此，可以使用quit()方法代替close()方法，quit()方法是关闭整个浏览器。

```python
driver.close()
```

## 查找元素

在一个页面中有很多不同的策略可以定位一个元素。在你的项目中可以选择最合适的方法去查找元素。selenium提供的方法如下所示：

- find_element_by_id
- find_element_by_name
- find_element_by_xpath
- find_element_by_link_text
- find_element_by_partial_link_text
- find_element_by_tag_name
- find_element_by_class_name
- find_element_by_css_selector

一次查找多个元素（这些元素会返回一个list列表）

- find_elements_by_id
- find_elements_by_name
- find_elements_by_xpath
- find_elements_by_link_text
- find_elements_by_partial_link_text
- find_elements_by_tag_name
- find_elements_by_class_name
- find_elements_by_css_selector

## 等待页面加载完成

现在大多数的web应用程序是使用Ajax技术。当一个页面被加载到浏览器时，该页面内的元素可以在不同的时间点被加载。这使得定位元素变得困难，如果元素不再页面之中，会抛出ElementNotVisibleException 异常。使用waits，我们可以解决这个问题。waits提供了一些操作之间的间隔，主要是定位元素或针对该元素的任何操作。

selenium webdriver提供两种等待方式，一种是显示等待，一种是隐式等待。

### 显式等待

它指定要查找的节点，然后指定一个最长的等待时间，如果规定时间内加载出来了这个节点，就返回查找的节点；如果规定时间内没有加载出该节点，就抛出超时异常。

接下来，我们就用一个简单的例子来表示：

首先打开京东并打开开发者工具。如下图所示：

![image-20210216161222066](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210216161222066.png)

如上图，我们需要寻找id为key的节点和class为button的节点。具体代码如下所示：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


broswer = webdriver.Chrome()
broswer.get('https://www.jd.com/')
wait = WebDriverWait(broswer, 20)
input_q = wait.until(EC.presence_of_element_located((By.ID, 'key')))
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.button')))
print(input_q, button)
```

接下来对上面代码进行简单的说明，首先引入WebDriverWait这个对象，并指定最长时间，然后调用它的until()方法，传入要等待的条件expected_conditions，比如这里传入了presence_of_element_located这个条件，代表节点出现的意思，其参数是节点定位的元组，也就是ID为key的搜索框。

这样做到的效果是，在10秒如果ID为key的节点成功加载出来，就返回该节点；如果超过20秒还没有加载出来就会抛出异常。

运行代码之后，网速不错的话，是可以成功加载出来的。

输出结果如下：

```python
<selenium.webdriver.remote.webelement.WebElement (session="54576c743c2ef8ec50ae1e02e826f5c0", element="cc0ff331-146f-4756-b738-82eb65016c41")> <selenium.webdriver.remote.webelement.WebElement (session="54576c743c2ef8ec50ae1e02e826f5c0", element="d38b49d7-550b-4619-bee9-f268ff7b4bf9")>
```

可以看到，控制台成功输出了两个节点，它们都是WebElement类型。

### 隐式等待

当使用隐式等待执行测试的时候，如果Selenium没有在DOM中找到节点，将继续等待，超出设定时间后，则抛出找不到节点的异常。换句话说，当查找节点而节点并没有出现的时候，隐式等待将等待一段时间再查找DOM，默认时间是0，示例如下：

```python
from selenium import webdriver


browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.get('https://www.jd.com/')
input_q = browser.find_element_by_class_name('button')
print(input_q)
```

这里的implicitly_wait()方法实现了隐式等待。

隐式等待的效果其实没有那么好，因为我们只规定了一个固定时间，而页面的加载时间会受到网络条件的影响。

## 等待条件

关于等待条件，其实还有很多，比如判断标题内容，判断某个节点是否出现了某文字等。具体如下表所示：

|                等待条件                |            含义            |
| :------------------------------------: | :------------------------: |
|                title_is                |        标题是某内容        |
|             title_contains             |       标题包含某内容       |
|       present_of_element_located       | 节点加载出来，传入定位元组 |
|     visibility_of_element_located      |   节点可见，传入定位元组   |
|             visibility_of              |     可见，传入节点对象     |
|    present_of_all_elements_located     |      所有节点加载出来      |
|     text_to_be_present_in_element      |    某节点文本包含某文字    |
|  text_to_be_present_in_element_value   |     某个节点包含某文字     |
| frame_to_be_available_and_switch_to_it |         加载并切换         |
|    invisibility_of_element_located     |         节点不可见         |

## 前进和后退

平常使用的浏览器都有前进和后退的功能，Selenium也可以完成这个操作，它使用back()方法后退，使用forward()方法前进，具体代码如下所示：

```python
import time
from selenium import webdriver


browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.get('https://www.taobao.com')
browser.get('https://www.jd.com')

browser.back()
time.sleep(2)
browser.forward()
```

这里我们连续访问了三个页面，然后调用back()方法返回第二个页面，等待2秒之后，再次进入第三个页面。

## Cookie

使用Selenium，还可以方便的对Cookies进行操作，例如获取、添加、删除Cookies等。具体代码如下所示：

```python
from selenium import webdriver


browser = webdriver.Chrome()
browser.get('https://www.zhihu.com')
print(browser.get_cookies())
# browser.add_cookie({'aa':'aa','bb':'bb'})
# print(browser.get_cookies())
browser.delete_all_cookies()
print(browser.get_cookies())
```

在这里需要注意一点，在增加cookie的时候，长度需要与你获取的cookie的长度相同。当全部cookie删除的时候，获取到的cookie就为空。

## 异常处理

在使用selenium的时候，难免会遇到一些异常，例如超时、节点未找到的错误等等。一旦出现此类错误，程序便无法运行下去了。这里我们可以使用try except语句来捕获异常。

具体代码如下所示：

```python
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException


browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
except TimeoutException:
    print('超时')

try:
    browser.find_element_by_id('aa')
except NoSuchElementException:
    print('未找到节点')
finally:
    browser.close()
```

这里我们使用的是try except来捕获异常。比如，我们对find_element_by_id()查找节点的方法捕获NoSuchElementException的异常。一旦出现了这样的错误，就进行异常处理，程序就不会中断了。

本次的分享到这里就结束了。

# 最后

没有什么事情是可以一蹴而就的，生活如此，学习亦是如此。因此，哪里会有什么三天速成、七天速成的说法呢？唯有坚持，方能成功！

**啃书君说**：

文章的每一个字都是我用心敲出来的，只希望对得起每一位关注我的人。在文章末尾给我点个【**赞**】，让我知道，你也在为自己的学习拼搏和努力着。

**路漫漫其修远兮，吾将上下而求索**。

我是**啃书君**，一个专注于学习的人，**你懂的越多，你不懂的越多**，更多精彩内容，我们下期再见！

