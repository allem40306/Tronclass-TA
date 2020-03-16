# coding=utf-8
import os
path = u"E:\\第2章作业-2"
if __name__ == '__main__':
    for root, dirs, files in os.walk(path):
        if path != root:
            print('root_dir:', root)  # 当前目录路径
            print('files:', files)  # 当前路径下所有非目录子文件

            stuInfo = os.path.split(root)[-1] + u"_"

            for fileItem in files:
                # 下载好作业后的预处理代码，重命名
                # os.rename(root + u"\\" + fileItem, root + u"\\" + stuInfo + fileItem)

                # 批改完作业后，将原始作业删除
                # if fileItem.find(u"页面") == -1:
                #     os.remove(root + u"\\" + fileItem)

                # 给批改好的作业重命名，按照作业名称+学号+姓名+原始文件名的方式
                # os.rename(root + u"\\" + fileItem, root + u"\\" + u"第2章作业-2_" + stuInfo + fileItem)
    pass