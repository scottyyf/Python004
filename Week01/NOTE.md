## 学习笔记


## bs4
beatiful soup处理页面，获取页面数据

由于bs是全页面检索的，所以速度比较慢。

bs的markup参数，支持字符串以及file like的方式（即直接open（file， 'r'））
#### 解析器：

* 标准库 html.parser 

| header | header | usage | desc
| ------ | ------ | ----- | -- |
| 标准库 | html.parser | bs(markup, 'html.parser') | adviced |
| lxml | lxml | bs(markup, 'lxml') | c needed |
| xml, lxml-xml | bs(markup, 'xml' | c needed |
| html5lib | html5lib | bs(markup, 'html5lib') | too slow |

* bs_info的一些可用方法
    - bs_info 可直接调用tag，将其作为自己的对象，它将返回该tag的字串
    - tag.string将获取对象的text内容
    - tag['var'] 将获取tag的attrbute内容

* 遍历
   - find_all， 返回tag下对应的attr的列表
   - find 返回tag下的列表的第一项

* tag的父节点
  - tag.parent将返回父节点

#### find_all
* find_all
    - 支持正则表达式。 查找所有以**b** 开头的标签
     ```
     for tag in bs.find_all(re.compile(r'^b')):  
     ```

    - 支持多个查找。查找以a b 为tag的标签
     ```
     bs.find_all(['a', 'b'])
     ```

    - 自定义tag。
     ```
     def has_class_but_no_id(tag):
         return all(tag.has_attr('class'), not tag.has_atr('id'))

     bs.find_all(has_class_but_no_id)
     ```

bs.find_all(), 第一个参数可是是tag名， 方法，也可以是id=‘link’这种attr, 也可以是re, 获取全部（即True）
```
bs.find_all('a')
bs.find_all(id='link2')
bs.find_all(href=re.compile('elsie'))
bs.find_all(id=True) 这个将查找所有有id属性的tag
bs.find_all(attrs={'id': 'link2'}) 推荐用这种方法咯
```

注意对于class属性，将使用class_='a'。一定要加下划线

查找text是特定值的tag
```
bs.find_all(string='Elsie')
bs.find_all(string=['scott', 'tom' ])
bs.find_all(string=re.compile('Dormouse'))
```

支持限定查找数量。只返回查找到的两个
```
bs.find_all('a', limit=2)
```

支持只在子节电中查找，默认是子孙节电中查找
```
bs.find_all('a', recursive=False)
```

get_text(), 获取文本内容，对于多个文本的，则append到字符后面， 对于当个文本，则返回该文本内容
```
bs.get_test()
bs.find('a', class_='var').get_text()
bs.get_test("|", strip=True) 处理文本
```

get(),可获取属性的值
```
bs.find('a').get('class') 将获取class的值
```
