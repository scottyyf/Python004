# 学习笔记

## pandas
an excel in python

* dataframe
* series

## dataframe
pd初始化

1. 使用dict初始化：使用dict作为参数给pd初始化时，key将作为每一列的标题；
dict的value，需要长度一致
```
df = pd.DataFrame({'name': ['a'], 'age': [22]})
```

2. 默认情况下，pd将会给列默认的1, 2 。。的列名称
```
df = pd.DataFrame([[1,2,3], ['a', 'b', 'c']])
```

3. 可使用key-value给pd加上对应的列和行名称
```
df = pd.DataFrame([1,2], index=['a','b'], columns=['name'])
```

## series
series可理解为一列的数据，pd将自动给这个单列加上索引index，以提高查询速率

1. create
```
se = pd.Series([1,2,3])
```

## 使用
* max(), min(), describe()都是针对单列进行的比较。这些比较只支持数字和None的比较。 如果没有指定列，那么就会将所有能比的列都比较然后分别显示出来

* describe(): 将对每一列做数据统计
* agg将对指定列和指定函数 做操作运算 : 聚合. 显示的结果进行了合并
```
df.agg({'age': [mix, max], 'sex': [mean]})
```

* transform('mix'),  显示的结果不进行合并
```
df.groupby('group').transform('mean')
```



* df.isnull() :  是否由空值
* df.ffill(axis=0): 用前一行的值取补全
* df.filena(value='xx')： 用xx替代None
* df.dropna() 删除na的行
* df.drop_dumplicates() 去重

* df.head(n), df.tail(n) , se.head(n), se.tail(n) 查看前|后几行

* df.shape() 返回行数与列数， 如果指定了某一列，则返回行数

* df['age'], df[['age', 'name']] 返回一列多多列

* df['age'] > 35 将返回age这行是否大于35的结果，bool类型
* df['age'].isin([1,2, 4]) 枚举结果
* df['age'].notna() 返回age列不为None的结果，bool类型
* df.loc[df['age']>35, 'name'] 返回age大于35的所有name列。这里是一个子列
。


默认是对列的操作： df[1:3] 1到3列
loc是对行单操作: df[1:2] 1到2行

使用了行和列进行匹配，那么则需要使用loc或iloc函数，这个函数逗号前是比较的行，逗号后面是选择的列

如果需要指定多少行，多少列则使用iloc
```
df.iloc[1:2, 3:4]
```

还可以进行赋值
```
 df.iloc[1:2, 3:4] = ‘anon’
```


* df[df['age'] > 35]  返回age大于35的行数据
* df[(df['age'] > 35) & (df['name'] == 'scott')]

1. 比较大小： 比较列中的大小
```
df = pd.DataFrame([[11,22,33], ['allen', 'willson', 'james']],
                  colums=['age', 'name])
df['age'].max()
```

* 增加新列
```
df['new_col'] = [xxx]
```

* 重命名列 不改变原来的值
```
ret = df.rename(columns={'star': 'start'})
ret = df.rename(columns=str.lower)
```

* 计算
mean， max， min， median, sum

* groupby('sex') 以sex进行分组后，再求每列的平均值
```
df[['sex', 'age']].groupby('sex').mean()
```

df.groupby('sex')['age'].mean() sex分组后求age的平均值。分解如下
```
groupby将df分成两个子df
age则应用到每个子df中
mean求平均值
```

```
df.groupby('sex').groups()
length = df.groupby('sex').count()
for a, b in df.groupby('sex'):
    print(a)
    print(b)
```

*  排序
    - df.sort_values(by='age'): 排序
    - df.sort_values(by=['age','class'], ascending=True) 升序排列

* 合并data: concat 将用一个轴（行或列）进行表的合入
```
pd.concat([pd1, pd2], axis=0) # 0,1 可选， 0为向下穿过行， 1为水平穿过列
```

* 数据透视表， 展开
```
df.stack()
df.unstack()
```

* 其他

    - pd['age'].str.lower()
    - pd['age'].str.split(',')
    - pd['name'].str.contains('bob') 是否包含这个字符
    - pd['name'].str.len()
    - pd['name'].replace({'male': 'M, 'female': 'F'}) 查找并更改male的值为M
    - pd['age'].replace([4,5,8], 1000)

    - df.drop('a', axis=1) 删除列
    - df.drop('a', axis=0) 删除行
    - df.T  行列互换

* read_csv
* read_excel to_excel
* read_table
* read_sql

1. excel

* pd.read_excel(file, sheet_name='sheet0')
* pd.info() 统计excel的信息： 列名， 多少行， 多少列， 每列的类型

1. csv

* read. pd默认将列的第一个单元格字符作为key，可通过key获取一整个列的数据
```
df = pd.read_csv(csv_file)
df[key]
```

* 设置表头
```
df.columns = ['star', 'vote', 'shorts']
```

* 获取特定的行，列数据
   - 获取特定行
   ```
   df[1:3]
   ```

   - 获取特定列
   ```
   df[:, ['star']]
   ```

## padans to python
* pd.to_dict()
* se.to_list()

## 数据透视
布局如下：
```
        --       --     --   VALUES
     -    -     -   -   -   - COLUMNS
|  |
|  |            aggfunc
|  |
INDEX
```

```
pd.pivot_table(df_data, values='salary', columns='group',
               index='age'
               ,aggfunc='count', margins=True
              ).reset_index()
```

## 数据拼接
* 1 vs 1
```
pd.merge(df1, df2)
```

* many vs 1
```
pd.merge(df1, df2i, on='group') 以group列为连接列进行拼接， 返回一个新的dataframe
```

* many vs many
```
pd.merge(df1, df2)
```

* not columns
```
pd.merge(df1, df2, left_on='age', right_on='salary')
```

## 纵向拼接  ****重要
直接附加 pd.concat


## to_*
1. df1.to_excel(shname, tb_name, index=False, columns=['a','b'], na_rep=0)
2. df1.to_csv()

## 绘图
```
import matplotlib.pyplot as plt

plt(df.index, df['a'], color='#FFAA00',marker='D')
plt.show()
```

美化
```
import seaborn as sns
plt(df.index, df['a'], color='#FFAA00',marker='D')
plt.show()

sns.set_style('darkgrid')
plt.scatter(df.index, df['a'])
plt.show()
```
