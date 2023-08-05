# PyMysqlModel

#### 介绍
基于 pymysql 的模型创建及使用
内置 create、all、update、delete、filter、get 等常用方法

#### 软件架构
软件架构说明


#### 安装教程

1.  xxxx
2.  xxxx
3.  xxxx

#### 使用说明

```python


import os
from pathlib import Path


from PyMysqlModel.Model import Model

student = Model(database="pymysqlmodel",user="root",password=123)


table_name = "student_tb"
student_table_fields = [
    "name varchar (20)",  # 一个字符串为一个字段
    "age int",
    "gender enum('男','女')",
    "phone varchar(11)",
]
student.link_table(table_name,student_table_fields)

names = "张三"
ages = 18
genders = 1
phones = "17613355211"

# 添加数据
# flag = student.create(name=names,age=ages,gender=genders,phone=phones)
# print(flag)

# 获取所有数据
data = student.all() # 获取所有信息
for i in data:
    print(i)

# pk = 2
# names = "李四"
# ages = 21
# genders = 2
# phones = "17613355211"
# 修改数据
# flag = student.update(id=pk,name=names, age=ages, gender=genders, phone=phones)
# print(flag)


# 删除数据
pk = 3
names = "张三"
# flag = student.delete(id=pk)
# flag = student.delete(id=pk,name=names)
# print(flag)

# 查询
# 根据表字段进行过滤查询
ages = 18
data = student.filter(age=ages)
print("查询结果")
for i in data:
    print(i)


# 获取单条数据
names = "李四"
data = student.get(name=names)
print("查询单挑结果")
print(data)


```

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
