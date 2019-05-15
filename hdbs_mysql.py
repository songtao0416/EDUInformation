# -*- coding: utf-8 -*-
# 将xls中的data数据转存到mysql中

import pymysql
import csv
import os
import re
import sys
import time
import xlrd
import base_list
import datetime

# 读取 总数据 表数据
def open_alldata(keyword,all_path):
    path = all_path
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)
    id_list = []
    web_list = []
    name_list = []
    name2_list = []
    time_list = []
    url_list = []
    data_list = []
    for i in range(0, int(sheet.nrows)):
        if sheet.cell(i, 2).value not in name_list:
            id_list.append(sheet.cell(i, 0).value)
            web_list.append(sheet.cell(i, 1).value)
            name_list.append(sheet.cell(i, 2).value)
            name2_list.append(sheet.cell(i, 3).value)
            time_list.append(sheet.cell(i, 4).value)
            url_list.append(sheet.cell(i, 5).value)
            data_list.append(sheet.cell(i, 6).value)
    print("%s数据all_data读取成功" % keyword)
    return id_list, web_list,name_list,name2_list,time_list,url_list,data_list

#  连接数据库
def content_sql():
    global db,cursor
    # 打开数据库连接
    db = pymysql.connect("sh-cdb-pk4znli4.sql.tencentcdb.com", "hdbs_education", "ThisNotPsw2019",  "hdbs_education" ,port = 63737, charset="utf8")
    # db = pymysql.connect("localhost", "root", "yst123456", "skd")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor= db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("SELECT VERSION()")
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
    # data = cursor.fetchall()
    print("Database version : %s " % data)
    return cursor

# db表删除数据
def del_sql():
    content_sql()  # 连接mysql
    date_list =['2000','']
    sql = "delete from originallink WHERE RELEASE_DATETIME <=  '%s'" %"2019"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 向数据库提交
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    pass


# db表插入数据  sql
def insert_sql_data(id_list, web_list,name_list,name2_list,time_list,url_list,data_list,sub_list, key_list):
    content_sql()  # 连接mysql
    # 获取当天爬取时间
    pq_time = str(datetime.date.today())
    # 插入中文时，%s 要改为'%s',且插入的列数量要和数据库相同
    i=0
    for i in range(1, len(id_list)):
        # sql = "INSERT INTO all_data VALUES ('0','%s','%s','%s','%s','%s','%s','%s','%s')" % (id_list[i], web_list[i], name_list[i],name2_list[i], time_list[i], url_list[i], data_list[i],keyword)
        sql = "INSERT INTO originallink (SOURCE,TITLE,SHORT_DESC,RELEASE_DATETIME,ORIGINAL_LINK,CONTENT,SUBJECT_TYPE,SEARCH_WORDS_NAME,SOURCE_REAL) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(web_list[i], name_list[i],name2_list[i], time_list[i], url_list[i], data_list[i], sub_list[i],key_list[i],pq_time)
        try:
            if len(data_list[i]) >= 100000:
                print("字数太多，超过10w")
                continue
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            if i % 100 == 0:
                time.sleep(1)
        except:
            # 如果发生错误则回滚
            print('*' * 20, "第%d条插入失败" % i, '*' * 20)
            db.rollback()
    print("*"*20,"在数据库中共插入%d条数据" % i, "*"*20)
    return i

# 将db_urls存入csv中，在读取url爬取data前进行去重
def csv_dburls():
    dbcsv_adds = '(URL)DB.csv'
    # 判断文件是否存在
    if (os.path.exists(dbcsv_adds)):
        os.remove(dbcsv_adds)
    else:
        print("(URL)DB文件不存在！")

    path = dbcsv_adds
    csvfile = open(path, 'a+', encoding='utf-8', newline='')
    dburl_writer = csv.writer(csvfile)
    dburl_writer.writerow(('URL编号', 'URL'))
    return dburl_writer

# 读取db中，所有url数据
def get_dburls():
    dburl_writer = csv_dburls()
    content_sql()  # 连接mysql
    sql = "SELECT ORIGINAL_LINK FROM originallink "
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        i = 1
        for row in results:
            db_url = (''.join(row))
            dburl_writer.writerow((i, db_url))
            i += 1
    except:
        print("数据库读取失败")
    print("(URL)DB表更新成功")

# 读取db中数据,对比筛掉重复数据,主要对比对象为"标题"
def get_dbdata():
    db_list = []
    content_sql()  # 连接mysql
    sql = "SELECT TITLE FROM originallink "
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            db_list.append(''.join(row))
    except:
        print("数据库读取失败")
    return db_list

# 函数集合，包括数据读取、数据去重、数据写入
def coon_sql(keywords, asub_list):
    db_list = get_dbdata()      #获取db中原有数据，目的去重
    id_list = []
    web_list = []
    name_list = []
    name2_list = []
    time_list = []
    url_list = []
    data_list = []
    sub_list = []
    key_list = []
    # 读取不同关键词表中的数据
    for i in range(1, len(keywords)):
        skeyword = keywords[i]
        sub_id = asub_list[i]
        print(skeyword)
        for keyword in skeyword:
            try:
                mkpath = os.getcwd() +'/'+ keyword + '--爬取结果'
                all_path = mkpath + '/（总数据）'+keyword+'.csv.xls'
                (aid_list, aweb_list, aname_list, aname2_list, atime_list, aurl_list, adata_list) = open_alldata(keyword, all_path)
                # 拼接不同关键词表中的数据,并进行去重
                for i in range(1, len(aname_list)):
                    if aname_list[i] not in db_list:
                        if aname_list[i] not in name_list:
                            name_list.append(aname_list[i])
                            name2_list.append(aname2_list[i])
                            id_list.append(aid_list[i])
                            web_list.append(aweb_list[i])
                            time_list.append(atime_list[i])
                            url_list.append(aurl_list[i])
                            data_list.append(adata_list[i])
                            sub_list.append(sub_id)
                            key_list.append(keyword)
            except:
                print("*" * 100,"%s读取错误，可能不存在xls表" % keyword)
    # 将list中的数据插入db
    todat_i = insert_sql_data(id_list, web_list, name_list, name2_list, time_list, url_list, data_list, sub_list, key_list)
    # 关闭数据库连接
    db.close()
    return todat_i

# 主函数
def hdbs_mysql():
    # 调用数据源中的关键词和主题标识码
    keywords = base_list.keywords
    asub_list =base_list.sub_list
    # 获取数据插入数据，返回插入数据的数量
    todat_i = coon_sql(keywords, asub_list)
    # 获取数据库中已存在的URLlist，并保存csv中，避免下次抓取
    get_dburls()
    return todat_i

# 删除数据库中记录
# del_sql()
# get_dburls()
# start = time.clock()
# # hdbs_mysql()
# end = time.clock()
# print("数据库写入用时:",end-start,"秒")