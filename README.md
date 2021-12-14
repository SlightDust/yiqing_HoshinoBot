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

群内发送`xx疫情`即可获取xx地区的疫情信息。  


# 日志
2021/12/14  代码写的很烂，但是能跑就行。  

# 鸣谢
[腾讯疫情Api](https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5)