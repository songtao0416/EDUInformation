import os, sys
dirPath = os.getcwd()
print('移除前test目录下有文件：%s' %os.listdir(dirPath))
#判断文件是否存在
if(os.path.exists("tets.csv")):
    os.remove("tets.csv")
    print('移除后test 目录下有文件：%s' %os.listdir(dirPath))
else:
    print("要删除的文件不存在！")