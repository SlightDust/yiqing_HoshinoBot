# yiqing_HoshinoBot
一个适用于HoshinoBot的新冠肺炎疫情获取插件

# 安装和使用方法：
和一般hoshino插件一样  

1. 在hoshino/modules下clone本仓库`git clone https://github.com/SlightDust/yiqing_HoshinoBot.git`  
2. 在hoshino/config/\_\_bot\_\_.py中加入
```
MODULES_ON = {
...
'yiqing_HoshinoBot',  # 疫情
}
```
3. 重启hoshino

群内发送`xx 疫情` 或 `疫情 xx`即可查询xx地区的疫情信息。  

更换图片字体的话最方便的方法是直接把字体文件放进来，重命名为simhei.ttf，不用动代码，方便下次pull。  

# 日志
2021/12/14  代码写的很烂，但是能跑就行。  
2022/01/11  ~~用很多try except~~修复无法获取数据的问题。今天腾讯悄悄改了api响应，导致插件炸了。~~腾讯你坏事做尽~~  
2022/01/13  改为图片发送，谢谢小夏！  

# 免责声明
数据来源：[腾讯疫情Api](https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5)