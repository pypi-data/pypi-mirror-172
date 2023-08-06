"""
@Project:pymysql
@File:Model.py
@Author:函封封
@Date:9:23
"""

import pymysql

# mysql操作
class Model():
    def __init__(self,database=None,user=None,password=None,host="localhost",port=3306,charset="utf8"):
        if not all([database, user, password, host, port, charset]):
            try:
                from setting import DATABASES
            except Exception:
                raise ValueError("setting DATABASES 不存在！")
            self.pymysql_con = pymysql.connect(**DATABASES)
        else:
            self.pymysql_con = pymysql.connect(database=database, user=user, password=str(password), host=host,port=port, charset=charset)
        self.mysql = self.pymysql_con.cursor() # 创建游标对象
        self.table_name = None  # 表名
        self.field = ["id",]  # 表字段

    # 获取数据库内所有的表
    def show_tables(self):
        sql = f"""show tables;"""
        self.mysql.execute(sql)
        data = self.mysql.fetchall()
        table_list = []
        for i in data:   # 元组转换为列表
            table_list.append(i[0])
        return table_list # 返回当前数据库内所有的表

    # 连接表 接收一个字符串类型的表名
    def link_table(self, table_name=None, field=None):
        self.table_name = table_name  # 将表名赋值给实例属性
        field_str = ""
        for i in field:
            field_str += i + ","  # 将所有的字段与字段类型以 “ , ” 拼接
            field_name = i.split()[0]  # 获取所有的字段名，不含字段类型
            self.field.append(field_name)  # 获取该表的所有的字段名

        table_list = self.show_tables()  # 获取数据库里所有的表
        for i in table_list:
            if self.table_name == i:  # 判断该表是否已存在
                print(f"——连接成功：{self.table_name}——")
                return True # 该表已存在！直接返回

        field_str = field_str.rstrip(",")  # 删除字符串最后的“,”
        sql = f"""
             create table {self.table_name}(
                id int primary key auto_increment,
                {field_str}
              );
         """
        self.mysql.execute(sql)
        print(f"——创建并连接成功：{self.table_name}——")
        return True

    # 查询数据
    def all(self,*args):
        if len(args) != 0:
            field = args
        else:
            field = self.field
        for i in field:
            assert i in self.field,f"{i} 该字段不存在！"
        select_field = ",".join(field)
        sql = f"""select {select_field} from {self.table_name};""" # 根据表名直接查询
        self.mysql.execute(sql)
        data = self.mysql.fetchall()
        result = []
        for i in data:  # 进行数据转换
            temp = {}
            for k,j in enumerate(field):# 每行数据 组成字典类型
                temp[j] = i[k]
            result.append(temp)
        return result # 最终返回查询集

    # 添加数据     接收所有的命名参数 即根据字段名传入对应数据
    def create(self,**kwargs):
        try:
            value_list = []
            for i in self.field:
                value = kwargs.get(i)
                if value != None:
                    value_list.append(f"'{value}'")
                else:
                    value_list.append(f"null")
            create_sql = ",".join(value_list)
            # id 字段为null ，默认自增
            sql = f"""
                insert into {self.table_name} values 
                ({create_sql});
            """
            self.mysql.execute(sql)
        except Exception as err:
            self.pymysql_con.rollback()
            print("错误信息：", err)
            return False
        else:
            self.pymysql_con.commit()
            return True

    # 修改数据    接收所有的命名参数 即根据字段名传入对应数据
    def update(self,**kwargs):
        try:
            pk = kwargs.get("id")
            assert pk,"缺少 id 字段"

            field = []
            temp = kwargs.keys()
            for i in self.field:
                if i in temp:
                    field.append(i)

            value_list = []
            for i in field:
                value = kwargs.get(i)
                if value != None:
                    value_list.append(f"{i}='{value}'")
                else:
                    value_list.append(f"{i}=null")

            update_sql = ",".join(value_list)

            sql = f"""
                    update {self.table_name} set {update_sql} where id = {pk};
                """
            self.mysql.execute(sql)
        except Exception as err:
            self.pymysql_con.rollback()
            print("错误信息：", err)
            return False
        else:
            self.pymysql_con.commit()
            return True

    # 删除数据的方法   接收所有的命名参数 即根据字段名传入对应数据
    def delete(self,**kwargs):
        try:
            field = []
            temp = kwargs.keys()
            for i in self.field:
                if i in temp:
                    field.append(i)

            value_list = []
            for i in field:
                value = kwargs.get(i)
                if value != None:
                    value_list.append(f"{i}='{value}'")
                else:
                    value_list.append(f"{i}=null")

            delete_sql = " and ".join(value_list)

            # 先查询满足条件的数据个数
            sql = f"""
                        select COUNT(id) from {self.table_name} where {delete_sql};
                """
            self.mysql.execute(sql)
            data = self.mysql.fetchall()
            delete_sum = data[0][0]

            # 删除数据
            sql = f"""
                    delete from {self.table_name} where {delete_sql};
                """
            self.mysql.execute(sql)
        except Exception as err:
            self.pymysql_con.rollback()
            print("错误信息：", err)
            return False
        else:
            self.pymysql_con.commit()
            return delete_sum

    # 过滤查询数据
    def filter(self, *args, **kwargs):
        try:
            field = []
            temp = kwargs.keys()
            for i in self.field:
                if i in temp:
                    field.append(i)

            value_list = []
            for i in field:
                value = kwargs.get(i)
                if value != None:
                    value_list.append(f"{i}='{value}'")
                else:
                    value_list.append(f"{i}=null")
            filter_sql = " and ".join(value_list)

            # 结果字段
            if len(args) != 0:
                result_field = args
            else:
                result_field = self.field
            select_field = ",".join(result_field)

            for i in result_field:
                assert i in self.field, f"{i} 该字段不存在！"
            sql = f"""
                select {select_field} from {self.table_name} where {filter_sql};
            """
            self.mysql.execute(sql)
        except Exception as e:
            print("错误信息：", e)
        else:
            data = self.mysql.fetchall()
            result = []
            for i in data:
                temp = {}
                for k,j in enumerate(result_field):
                    temp[j] = i[k]
                result.append(temp)
            # 返回查询集
            return result

    # 过滤获取数据  返回第一个数据
    def get(self,**kwargs):
        try:
            field = []
            temp = kwargs.keys()
            for i in self.field:
                if i in temp:
                    field.append(i)

            value_list = []
            for i in field:
                value = kwargs.get(i)
                if value != None:
                    value_list.append(f"{i}='{value}'")
                else:
                    value_list.append(f"{i}=null")
            get_sql = " and ".join(value_list)

            sql = f"""
                select * from {self.table_name} where {get_sql};
            """
            self.mysql.execute(sql)
        except Exception as err:
            print("错误信息：", err)
        else:
            data = self.mysql.fetchall()
            data = data[0]

            result = {}
            for k, j in enumerate(self.field):
                result[j] = data[k]
            return result
