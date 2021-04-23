# 前言

相信大家在很多的时候，在公众号上经常会看到很多关于购买股票或者是基金的课程，让大家学会理财。就是所谓钱生钱。买股票与基金靠的不是运气，而是长期以来的经验，特别是对数据的敏感程度，做出正确的决策，因此今天我就特定的将股票网站的数据爬取下来，让各位买股票的小伙伴做一个参考。

# 网页分析

爬取的网址如下：

```
https://xueqiu.com/
```

打开页面如下所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210215223052207.png)

现在，我要找的是沪A成交额的数据，如何查找呢？如下所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210215223213638.png)

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210215223244159.png)

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210215223308119.png)

按着上图的顺序依次下来你就会来到我要寻找的数据的位置了。

说句题外话，刚刚打开页面的时候看到茅台的价格这么高，着实吓到了我，虽然我不买股票，但是偶尔也会跟一下基金。现在看来，我还是蛮后悔年前没有买白酒的。

好了，言归正传。现在对该网页进行分析。首先打开开发者工具。如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210215223953727.png)

从上图可以看到，数据并不在响应中，所以初步判断，数据是动态加载出来的。

那么接下来可以先点击XHR，再重新刷新页面。结果如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210215224234767.png)

通过上图分析XHR数据，可以精准的确定，该数据就是通过动态加载出来的，并且可以知道数据类型是json。

分析之后，我们也可以发现这个是第一页的数据，接下来依次点击第二页，第三页，它们的URL如下所示：

```
# 第一页
https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size=30&order=desc&order_by=amount&exchange=CN&market=CN&type=sha&_=1613400107752

# 第二页
https://xueqiu.com/service/v5/stock/screener/quote/list?page=2&size=30&order=desc&order_by=amount&exchange=CN&market=CN&type=sha&_=1613400455501

# 第三页
https://xueqiu.com/service/v5/stock/screener/quote/list?page=3&size=30&order=desc&order_by=amount&exchange=CN&market=CN&type=sha&_=1613400541459
```

通过分析它们的URL地址，不难发现，page值就是代表着每一页。至此，网页基本分析完毕，可以开始写代码了。

# 获取json数据

向目标网站发送URL请求，获取响应信息。具体代码如下所示：

```python
def get_json(url):
    response = requests.get(url, headers=headers)
    json_data = response.json()
    return json_data
```

可以将返回值进行打印，运行结果如下所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210215232154388.png)

# 获取数据

我们需要获取的数据主要有以下几点：

- 股票代码
- 股票名称
- 当前价
- 涨跌额
- 涨跌幅
- 年初至今
- 成交量
- 成交额
- 换手率
- 市营率
- 股息率
- 市值

这些数据都是保存在json中，那要获取就不难了，在之前的文章中我也有写过关于获取json数的库**jsonpath**的讲解，不熟悉的小伙伴可以自己去文章，并学习。

具体代码如下所示：

```python
def get_info(json_data):
    # 股票代码
    symbol = jsonpath.jsonpath(json_data, '$..symbol')
    # 股票名称
    name = jsonpath.jsonpath(json_data, '$..name')
    # 当前价
    current = jsonpath.jsonpath(json_data, '$..current')
    # 涨跌额
    chg = jsonpath.jsonpath(json_data, '$..chg')
    # 涨跌幅
    percent = [str(i) + '%' for i in jsonpath.jsonpath(json_data, '$..percent')]
    # 年初至今
    current_year_percent = [str(i) + '%' for i in jsonpath.jsonpath(json_data, '$..current_year_percent')]
    # 成交量
    volume = jsonpath.jsonpath(json_data, '$..volume')
    # 成交额
    amount = jsonpath.jsonpath(json_data, '$..amount')
    # 换手率
    turnover_rate = [str(i) + '%' for i in jsonpath.jsonpath(json_data, '$..turnover_rate')]
    # 市盈率
    pe_ttm = [str(i) + '%' for i in jsonpath.jsonpath(json_data, '$..pe_ttm')]
    # 股息率
    dividend_yield = [str(i) + '%' for i in jsonpath.jsonpath(json_data, '$..dividend_yield')]
    # 市值
    market_capital = jsonpath.jsonpath(json_data, '$..market_capital')
    df = pd.DataFrame(
        {
            '股票代码': symbol,
            '股票名称': name,
            '当前价': current,
            '涨跌额': chg,
            '涨跌幅': percent,
            '年初至今': current_year_percent,
            '成交量': volume,
            '成交额':amount,
            '换手率':turnover_rate,
            '市盈率':pe_ttm,
            '股息率':dividend_yield,
            '市值':market_capital
        }
    )
    return df
```

# 保存数据

保存数据的时候需要与翻页一起操作，将数据保存到data文件夹下的csv文件内，具体代码如下所示：

```python
def main():
    df = pd.DataFrame(columns=['股票代码','股票名称','当前价','涨跌额','年初至今', '成交量', '成交额', '换手率', '市盈率','股息率', '市值'])
    for page in range(1,54):
        print(f'正在下载第{page}页')
        time.sleep(0.5)
        url = f'https://xueqiu.com/service/v5/stock/screener/quote/list?page={page}&size=30&order=desc&order_by=amount&exchange=CN&market=CN&type=sha&_=1613400107752'
        json_data = get_json(url)
        df1 = get_info(json_data)
        df = pd.concat([df, df1])
        df = df.reset_index(drop=True)
    df.to_csv('../data/沪A成交额.csv',mode='a', encoding='utf-8-sig')
```

这里需要注意时间，要有一段睡眠时间，防止被反爬。

# 数据分析

## 查看数据

```python
data = pd.read_csv('沪A成交额.csv')
data
```

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210216001818720.png)

## 成交量图表

## 获取前30条数据

```python
df = data.dropna()
df1 = df[['股票名称','成交量']]
df2 = df1.iloc[:30]
df2
```

## 成交量可视化

```python
c = (
        Bar(init_opts=opts.InitOpts(width='1500px', height='660px', page_title='股票可视化')).add_xaxis(list(df2['股票名称'].values))
    .add_yaxis('股票成交量情况',list(df2['成交量'].values))
    .set_global_opts(
        title_opts=opts.TitleOpts(title='成交量图表'),
        datazoom_opts=opts.DataZoomOpts()
    )
    .render('data.html')
    )
```

运行结果如下所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210216011233098.png)

# 最后

**啃书君说**：

文章的每一个字都是我用心敲出来的，只希望对得起每一位关注我的人，为文章点个【**赞**】，让我知道，你也在为自己的学习努力和拼搏着。

**路漫漫其修远兮，吾将上下而求索**。

我是**啃书君**，一个专注于学习的人，**你懂的越多，你不懂的越多**。更多精彩内容，我们下期再见！