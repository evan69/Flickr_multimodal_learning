# Flickr图片数据集建立和处理程序

<font size = 4>

本仓库下个文件功能：

flickr\_crawl.py ： 用于爬取常用的形容词tag

pic\_crawl.py ： 用于下载图片 

参数：

- -s：下载有监督学习的图片
- -u：下载无监督学习的图片

tag\_crawl.py ： 用于获取已下载图片的全部tag

merge.py ： 用于合并所有文件夹下的全部图片tag文件tag\_data.txt

matGenerator.py ： 用于将图像特征提取的向量结果或者LDA提取文本模态的结果转化为.mat文件供matlab程序使用

run.py ： 运行LDA程序，将结果以及图像特征提取的结果处理成.mat文件

</font>