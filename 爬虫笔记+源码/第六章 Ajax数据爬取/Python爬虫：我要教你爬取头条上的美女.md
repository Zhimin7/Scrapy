![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/79.jpg)

觉得上面的小姐姐漂亮的，可以举个爪子。

今天就来教大家来爬取头条上的美女。

但是，不要着急，在学爬虫之前，大家需要先学会分析Ajax请求。

# 前言

有时候我们会用requests抓取页面的时候，得到的结果可能和浏览器中看到的不一样：在浏览器中可以看到正常显示的页面数据，但是使用requests得到的结果并没有。这是因为requests获取的是原始的HTML文档，而浏览器中的页面则是经过javascript处理数据后生成的结果，这些数据的来源有多种，可能通过Ajax加载的，可能是包含在HTML文档当中，也有可能是经过javascript特定算法计算后生成的。

对于第一种情况：Ajax加载数据是一种异步加载方式，原始的农业面最初是不会包含这些数据的，原始页面加载完成之后，会再向服务器请求某个接口的数据，然后数据就会被处理从而呈现到网页上，这就是一个Ajax请求。

按照目前web的发展形式，这种页面会越来越多。网页的原始HTML中不会包含任何的数据，数据是通过Ajax统一加载后呈现出来的，这样在web开发上可以做到前后分离，而且降低了服务器直接渲染页面带来的压力。

因此，直接利用requests来获取原始HTML，是无法获取到有效的数据的，这时需要分析网页后台向接口发送的Ajax请求，如果可以用requests来模拟Ajax请求，那么就可以正常抓取数据了。

# 什么是Ajax

Ajax是异步的javascript和xml。它不是一门编程语言，而是利用javascript保证页面不被刷新，URL不变的情况下与服务器交换数据并更新部分网页的技术。

对于传统的网页来说，要想更新数据就必须刷新整个页面，但是有了Ajax之后，便可以在页面不全部刷新的情况下更新内容。在这个过程中实际上是在后台与服务器进行了数据的交换，获取到数据之后，再利用javascript改变网页，这样页面就会刷新了。

# Ajax分析方法

这里以微博为例，我们知道拖动刷新的内容由Ajax加载，而且页面的URL没有任何变化，那么应该去哪里查看这些Ajax请求呢？

## 查看请求

这里还需要借助浏览器的开发者工具，下面以Chrome浏览器为例子进行简单的介绍。

首先，打开微博的首页随便点击任意一条微博，随后在页面中点击鼠标右键，从弹出的快捷键菜单中选择“检查”选项，此时就会弹出开发者工具，如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210203211011051.png)

此时在element选项卡中便会观察到网页的源代码。不过这个不是我们需要寻找的内容，切换到network选项卡，随后重新刷新页面，可以发现这里多出了不少的条目，如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210203211413423.png)

这里是页面加载过程中浏览器与服务器之间发送请求和接收响应的所有内容。

Ajax其实是特殊的请求类型，它叫做xhr。在下面的图片中，我们可以看到以big为开头的请求，其类型type为xhr，其实这个就是Ajax请求。

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210203214533354.png)

鼠标点击该请求的时候，右侧可以看到该请求的Request Headers、URL和Response Headers等信息。其中Request Headers中有个信息为`x-requested-with: XMLHttpRequest`，这个就是标记此请求就是Ajax请求。如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210203214829849.png)

随后点击一下preview，即可看到响应内容，它是json格式的数据，这里的Chrome为我们自动做了解析，点击内容即可展开和收起相应的内容。如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210203215322848.png)

由于里面的内容较多，我将它复制下来，比较容易观察。

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210203215935690.png)

从上面的图片可以观察到，返回的内容其实是评论者的昵称、评论内容、评论时间以及点赞数。

另外，我们也可以切换到该页面URL的请求，查看它的Response是什么，如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210204141648643.png)

经过观察，其实很容易发现，这里的代码非常简单，除了简单的HTML代码之外，其他的都是javascript。所以说，我们看到的微博页面的数据并不是原始的页面返回的，而是后来执行javascript后，再次向后台发送的Ajax请求，浏览器拿到数据之后做进一步的渲染。

## 过滤请求

接下来利用浏览器中的开发者工具进行筛选，可以将Ajax请求全部筛选出来。在请求的上方有一层筛选栏，直接点击XHR，此时在下方显示的所有请求便都是Ajax请求了，如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210204161941147.png)

接下来，不断的滑动页面，可以看到页面底部有一条条新的微博评论被刷出，而开发者工具下方也会有一个个Ajax请求出现，这样我们就可以捕捉到所有的Ajax请求了。如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210204162317947.png)

至此，我们基本上可以分析出Ajax请求的一些详细信息了，接下来只需要用程序模拟这些Ajax请求，就可以轻松的获取到我们需要的信息了。

# 实战

## 分析Ajax爬取今日头条小姐姐

### 准备工作

在项目开始之前，请确保已经安装好requests库，如果没有安装，请参考下面的安装方法：

```
pip install requests
```

### 抓取分析

在抓取之前，首先要分析抓取的逻辑。打开今日头条的首页：https://www.toutiao.com/

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210204164335008.png)

在左上角有一个搜索接口，这里尝试抓取美女图片，所以输入“美女”二字搜索一下，如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210204164514400.png)

这时打开开发者工具并刷新整个页面，你会发现在network选项卡中会出现大量的数据请求信息。点击第一个请求，并点击response选项，搜索“写真”，遗憾的事情发生了，里面没有出现任何的关于写真的字眼。

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210204165528623.png)

因此，可以初步判断这些内容是由Ajax加载的，然后利用javascript渲染出来，接下来切换到XHR选项卡，查看有没有Ajax请求，如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210204165922797.png)

不出所料，这里果然出现了一些比较常规的Ajax请求，看看它的结果是否包含了页面中的相关数据。

点击data字段展开，发现这里许多条数据。点击第一条展开，发现有article_url字段和title字段与网页内容基本符合。

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210204170447594.png)

切换回headers选项卡，观察URL和headers信息，如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210204174933637.png)

可以看到这是一个get请求，请求的URL参数有:**aid**、**app_name**、**offset**、**format**、**keyword**、**autoload**、**count**、**en_qc**、**cur_tab**、**from**、**pd**、**timestamp**、**_signature**

继续下滑网页，你会发现在XHR选项卡中会出现越来越多的符合条件的Ajax请求。

如下所示：

```
https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=0&format=json&keyword=%E7%BE%8E%E5%A5%B3&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1612428382721&_signature=_02B4Z6wo00f015gKQTwAAIDAKPut9b7JdoeYL0WAAIYhGfqDyZWOUeA.JwSONVd37BCTuUrJwE1gIOy3vdsi5j5EDUTmLQeASGQij2uMyxRGe3E8Peoo2hzHzz5RwATyAVC1zu18zMfLZ5S3a

https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=20&format=json&keyword=%E7%BE%8E%E5%A5%B3&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1612429526639&_signature=_02B4Z6wo00d01lR4bAgAAIDB5ImAw3OJbZpUXWiAAPUUQO2SS7CFcMRjXUZZEIHjqP2egcZBSpXYmI6hWj.iKGkzEg0JBWChgQPoggOPf63cZGszmYGGuZdc1vbIO9gVPQmgwTOGo6qCxbjK94


https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=40&format=json&keyword=%E7%BE%8E%E5%A5%B3&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1612429531243&_signature=_02B4Z6wo00d01GfNiKwAAIDD1zxkZOf0K2hn6IwAAHnwQO2SS7CFcMRjXUZZEIHjqP2egcZBSpXYmI6hWj.iKGkzEg0JBWChgQPoggOPf63cZGszmYGGuZdc1vbIO9gVPQmgwTOGo6qCxbjKdd


https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset=60&format=json&keyword=%E7%BE%8E%E5%A5%B3&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis&timestamp=1612429538566&_signature=_02B4Z6wo00d01tH81gwAAIDBYQ06xI8rJLrR2dKAANRxQO2SS7CFcMRjXUZZEIHjqP2egcZBSpXYmI6hWj.iKGkzEg0JBWChgQPoggOPf63cZGszmYGGuZdc1vbIO9gVPQmgwTOGo6qCxbjK95
```

   

通过观察，可以发现变化的内容有`offset`,`timestamp`和`_signature`    。

timestamp指的是时间戳，而_signature指的是签名认证。我自己也看了很多的教程，大多数关于这个 _signature的破解其实是js的逆向。本来我也想要写用js逆向来破解这个 _signature，但是想到大家对于js逆向的方法可能不熟悉，毕竟我还没有写过该类文章，因此就不用这个方法了。经过测试发现不添加 _signature这个参数，对于获取json响应并无影响。

并且通过分析该Ajax请求可以发现，里面有`image_list`字段，如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210205115210249.png)

将这三个URL地址依次复制到浏览器之后可以发现，正是图片的URL地址，但是需要注意的是这个并不是高清大图的URL地址。

那问题就出现了，如何获取高清大图的URL地址呢？

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210205120518378.png)

如上图所示，可以依次点击URL地址，点击进去之后就会发现里面的都是高清大图的美女图片了。如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210205120925324.png)

那接下来就可以来看看json数据内的URL和高清大图的URL存在着什么样的区别。

```
json数据内的URL
http://p1-tt.byteimg.com/list/190x124/pgc-image/183b0a981cf04498958beb194613fe43

高清大图的URL
https://p6-tt.byteimg.com/origin/pgc-image/183b0a981cf04498958beb194613fe43?from=pc
```

通过观察上面的两个URL，其实区别也不是很大，只需要替换一些字符就可以了。

## 功能需求与实现

### 获取json数据

获取json数据倒不是特别难，主要是构造URL参数，具体代码如下所示：

```python
def get_page(offset):
    global headers
    headers = {
        'cookie': 'tt_webid=6925326312953529869; s_v_web_id=verify_kkqm44un_jaeWrYZ1_CnOS_4Xuz_BNoi_lE3QmTQ37uHC; csrftoken=280e107c397cea753911229202dc0c3d; ttcid=45904355bfa4470f9543c9cdeb94869f30; tt_webid=6925326312953529869; csrftoken=280e107c397cea753911229202dc0c3d; __ac_signature=_02B4Z6wo00f01Coh3wgAAIDDmtAzwcHMKowqBduAAGqaWRSmr26jOpvMaDLR3MsdEfPZTRN9mxTbUMgGifTuVJdj6FgWrIu6yKXVS3Dsp.wz3Pxl9vgfeguqCWDdZ4ocFVxb4JgkNBJTefPR41; __tasessionId=pyia55cn11612433914121; MONITOR_WEB_ID=2264d055-a390-4e4b-9b1f-4a3e2a6ac47c; tt_scid=pcBhM4miMb3tReqLN21gkwPxqHE92TFulL0hVtP4mdhm0UL1X0v0T1r158U8hVOua37f',
        'referer': 'https://www.toutiao.com/search/?keyword=%E7%BE%8E%E5%A5%B3',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    params = {
        'aid':'24',
        'app_name':'web_search',
        'offset':offset,
        'format':'json',
        'keyword':'美女',
        'autoload':'true',
        'count':'20',
        'en_qc':'1',
        'cur_tab':'1',
        'from':'search_tab',
        'pd':'synthesis',
        'timestamp':int(time.time())
    }
    url = 'https://www.toutiao.com/api/search/content/?'
    try:
        response = requests.get(url, headers=headers, params=params)
        response.content.decode('utf-8')
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('连接失败', e)
```

### 获取图片地址

经过上面的分析发现，json内部的图片链接并不是高清大图，所以在这里需要获取高清大图时需要做简单的字符串替换。

具体代码如下所示：

```python
def get_info(json):
    new_img_lists = []
    image_lists = jsonpath.jsonpath(json, '$.data[*].image_list..url')
    for image_list in image_lists:
        new_img_list = image_list.replace('p1', 'p6').replace('p3', 'p6').replace('list','origin').replace('/190x124', '')
        new_img_lists.append(new_img_list)
    return new_img_lists
```

### 保存图片

保存图片的时候只需要向上面获取到的图片地址依次发送请求即可。具体代码如下所示：

```python
def save_img(new_image_lists):
    global name
    for image in new_image_lists:
        print('-------正在获取第{}张----------'.format(name))
        data = requests.get(image, headers=headers).content
        with open(f'../image/{name}.jpg', 'wb') as f:
            f.write(data)
        name += 1
```

### 结果展示

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210205133702942.png)

### 关于翻页

其实翻页问题相当的好解决，通过对上面Ajax的接口就可以发现offset其实就是实现翻页效果的参数，每一次都是20的倍数，因此只需要传递offset的偏移量即可。

具体代码如下所示：

```python
def main(offset):
    json = get_page(offset)
    # print(type(json))
    new_image_lists = get_info(json)
    save_img(new_image_lists)


if __name__ == '__main__':
    pool = Pool()
    groups = [i * 20 for i in range(4)] # 0 20 40
    pool.map(main, groups)	# 传递偏移量
    pool.close()
    pool.join()
```

### 最后结果

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210205134901040.png)

通过上图以及代码可以知道，我只传递了3个偏移量，就获取到了229张的美女图片。

以上就是今天分享的所有内容了。

本篇文章告诉了大家：什么是Ajax？、如何查看与过滤Ajax请求。希望各位小伙伴以后遇到类似的问题可以举一反三，加强练习。

# 最后

**来自啃书君警告**：

`美女虽好，切莫贪杯`，要是自己的ip被封了就得不偿失了。

**啃书君说**：

没有一件事是可以一蹴而就的，哪有什么三天速成，七天速成，没有坚持何来成功！生活如此，学习亦是如此！

文章的每一个字，都是我用心敲出来的，只希望对得起每一位关注我的人。

在文章末尾点个赞与在看，让我知道，你们也在为自己的学习拼搏和努力着。

