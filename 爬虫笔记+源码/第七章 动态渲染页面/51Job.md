# 前言

在上一篇文章中，为大家分享了selenium的使用方法，因此今天这篇文章为大家带了的就是关于selenium的实战项目。

本次项目的内容是爬取51job的招聘信息，希望接下来的内容对你找工作有所帮助。

# 项目准备

本次项目涉及到的库比较多，需要各位小伙伴们先做好准备：

- requests
- selenium
- lxml
- csv
- pandas
- matplotlib

安装方式应该不需要我再概述了吧。

# 网页分析

当所有必要内容都准备好了之后，就要开始分析网页了。

网站链接如下：

```
https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=
```

打开的页面，如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210220204245152.png)

从上面的网址来看，它存在的参数特别多，能不能像百度一样，把后面的参数去掉呢？

那我们就来试试，删除参数之后的链接如下所示：

```
https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,1.html
```

将链接复制到浏览器，打开的页面如下所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210220204920708.png)

经过观察发现，和之前的页面并无区别。

## 关于动态渲染

该网页经过分析之后发现，如果直接使用requests向目标网址发送请求，可以发现有些动态加载的数据无法加载出来，可能导致爬虫出错，因此这里使用selenium自动测试工具，模拟发送请求，并加载数据。

## 关于翻页

经过测试，发现该职位下一共有81页的职位，因此需要获取到每一页的链接，所以，在这里又需要来观察不同页面的链接规律了。

```
# 第一页
https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,1.html
# 第二页
https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,2.html
# 第三页
https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,3.html
```

想必聪明的小伙伴们都发现了，URL的变化规律了吧。

只需要通过简单的for循环就可以解决了。

# 需求分析与功能实现

## 详情页分析

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210220210009422.png)

每一个招聘信息，我们都需要点击进去，才能看到每个招聘岗位的详细信息。里面的内容才是我们真正需要的，如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210220210622043.png)

**那么应该如何获取详情页的URL呢？**

首先打开开发者工具，使用选择器进行选择即可，如下图所示：

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210220211036167.png)

你会发现详情页的URL都放在了class属性为j_joblist的div标签下的div标签下的a标签，只需要提取a标签的href属性即可。

具体代码如下所示：

```python
def get_link():
    link_lists = []	# 保存详情页URL
    browser = webdriver.Chrome()
    for page in range(1, 82):
        browser.get(f'https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,{page}.html')
        wait = WebDriverWait(browser, 5)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.j_joblist')))
        # print(button)
        joblists = browser.find_elements_by_xpath('//div[@class="j_joblist"]/div/a')
        # print(joblists)
        for joblist in joblists:
            con_link = joblist.get_attribute('href')
            link_lists.append(con_link)
    browser.quit()
    return link_lists
```

接下来，我就对上面的几行代码做简单的分析。

```python
wait = WebDriverWait(browser, 5)
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.j_joblist')))
# print(button)
joblists = browser.find_elements_by_xpath('//div[@class="j_joblist"]/div/a')
```

这里首先引入WebDriverWait这个对象，指定最长的等待时间，然后调用它的until()方法，传入等待条件，譬如：这里传入了element_to_be_clickable，代表节点出现的意思，其参数是节点的定位元组。

## 获取详情数据

当我们将81页的详情页的链接都拿到手之后，只需通过requests向这些URL发送请求即可。

我们要在详情页中提取的数据主要有：

- 岗位名称
- 薪资
- 工作经验
- 学历
- 招聘人数
- 工作地点
- 福利

具体代码如下所示：

```python
def get_data(url_lists):

    with open('data_all3.csv', 'a', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['链接', '岗位名称', '薪资', '工作经验', '学历','招聘人数','工作地点','福利'])
    job_information = []
    for i, url in enumerate(url_lists):
        datalist = []
        headers = {
            'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
        }
        time.sleep(0.5)
        response = requests.get(url, headers=headers)
        # print(response.status_code)
        try:
            html = response.content.decode('gbk')
            # print(html)
            data = etree.HTML(html)
            datalist.append(url)    # 存入岗位连接
            title = data.xpath('//div[@class="cn"]/h1/@title')[0]  # 岗位名称
            # print(title)

            datalist.append(title)
            salary = data.xpath('//div[@class="cn"]/strong/text()')[0]
            datalist.append(salary)
            # print(datalist)
            information = data.xpath('//p[@class="msg ltype"]/@title')[0] # 地点、学历、人数
            information = re.sub(r'\s+', '', information)
            experience = information.split('|')[1]  # 工作经验
            # print(experience)
            datalist.append(experience)
            education = information.split('|')[2]   # 学历
            datalist.append(education)
            num = information.split('|')[3] # 招聘人数
            datalist.append(num)
            place = data.xpath('//p[@class="fp"]/text()')[0]
            # print(place)
            datalist.append(place)
            treament = ' '.join(data.xpath('//span[@class="sp4"]/text()'))  # 福利
            datalist.append(treament)
            # job_info = '\n'.join(data.xpath('//div[@class="bmsg job_msg inbox"]/p/text()'))
            # datalist.append(job_info)
            # print(treament)
            # print(job_info)
            print(f'第{i}条')
            print(datalist)
            with open('data_all3.csv', 'a' ,encoding='utf-8-sig', newline='') as csvfile:
                writer  = csv.writer(csvfile)
                writer.writerow(datalist)
```

# 结果展示

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/image-20210220213459108.png)

经过半个小时的抓取，终于抓到3779条招聘信息了。

我直接一句**好家伙**！！

Python的职位这么多吗？

# 可视化观察

## 学历统计

![](https://routing-ospf.oss-cn-beijing.aliyuncs.com/%E5%AD%A6%E5%8E%86%E7%BB%9F%E8%AE%A1.png)

因为有些公司并没有指定学历，因此会出现，招几人的结果。

不过从上面，我们也可以看出，目前Python的岗位还是本科生是居多的，其次是大专，最后是硕士。

## 工作经验统计

![工作经验统计](https://routing-ospf.oss-cn-beijing.aliyuncs.com/%E5%B7%A5%E4%BD%9C%E7%BB%8F%E9%AA%8C%E7%BB%9F%E8%AE%A1.png)

有些公司并没有指定工作经验，因此会出现学历在这边。

不过从上面已经可以看出，目前的企业最需要的拥有3-4年工作时间的程序员，如果你已经有了3-4年的工作经验的话，那是很容易可以找到使你满意的工作的。

# 最后

没有什么事情是可以一蹴而就的，生活如此，学习亦是如此！

因此，哪里会有什么三天速成，七天速成的说法呢？

唯有坚持，方能成功！

**啃书君说：**

文章的每一个字都是我用心敲出来的，只希望对得起每一位关注我的人。在文章末尾点个【**赞**】，让我知道，你也在自己的未来拼搏和努力着。

**路漫漫其修远兮，吾将上下而求索**。

我是**啃书君**，一个专注于学习的人，**你懂的越多，你不懂的越多**，更多精彩内容，我们下期再见！

