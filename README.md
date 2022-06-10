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
2022/01/13  改为图片发送，谢谢小夏！[#2](https://github.com/SlightDust/yiqing_HoshinoBot/pull/2) [@N-zi](https://github.com/N-zi/)  
2022/01/18  现在可以获取具体风险地区；图片会自动调整大小了；针对直辖市和特别行政区有了更清晰的描述  
2022/01/18  优化风险地区排版[#3](https://github.com/SlightDust/yiqing_HoshinoBot/pull/3) [@daseinem](https://github.com/daseinem/)  
2022/03/07  修复不能查询吉林市的问题。使用 `疫情 吉林市` 查询  
2022/03/16  `中国 全国 国内`都可以匹配查询全国疫情  
2022/03/29  现在可以查询到省级无症状感染者的数据；取消了风险等级的显示，因为都是“点击查看详情”  
2022/04/18  原api出错，更换api  
2022/06/10  图片中添加一句免责声明  

# 免责声明
数据来源：  
[腾讯疫情Api（原）](https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5)  
[腾讯疫情Api（新）](https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail,diseaseh5Shelf)  
[风险等级Api（post）](https://wechat.wecity.qq.com/api/PneumoniaTravelNoAuth/queryAllRiskLevel)
