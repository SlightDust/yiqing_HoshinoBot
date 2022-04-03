import json
from sys import path_importer_cache
import hoshino
from hoshino import Service, priv
from hoshino import aiorequests
from hoshino.util import FreqLimiter
from PIL import Image, ImageDraw, ImageFont
import io
import os
import base64

flmt = FreqLimiter(5)
url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"  # 腾讯api

sv = Service(
    name='疫情数据',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # False隐藏
    enable_on_default=True,  # 是否默认启用
)


# ============================================ #


async def get_yiqing_data(area: str) -> str:
    # 应该不会有人闲到写全称吧
    if area == "内蒙古自治区":
        area = "内蒙古"
    elif area == "宁夏回族自治区":
        area = "宁夏"
    elif area == "新疆维吾尔自治区":
        area = "新疆"
    elif area == "西藏自治区":
        area = "西藏"
    elif area == "广西壮族自治区":
        area = "广西"
    type_ = ""  # 标记是省还是市
    result = {}
    msg = ""
    raw_data = await aiorequests.get(url=url)
    raw_data = await raw_data.json()
    if raw_data['ret'] != 0:
        print('ret不为0，疑似有问题')
    data = json.loads(raw_data['data'])
    tree = data['areaTree']
    all_province = tree[0]['children']

    # 先最特殊情况
    if area in ("中国", "全国", "国内"):
        data.pop("areaTree")
        msg += f"中国疫情：\n"
        msg += f"现存确诊（含港澳台）{data['chinaTotal']['nowConfirm']}(+{data['chinaAdd']['confirm']})\n"
        msg += f"现存无症状{data['chinaTotal']['noInfect']}(+{data['chinaAdd']['noInfect']})\n"
        msg += f"境内现存确诊{data['chinaTotal']['localConfirmH5']}(" \
               + ("+" if data['chinaAdd']['localConfirmH5'] > 0 else "") \
               + f"{data['chinaAdd']['localConfirmH5']})"  # localConfirm和localConfirmH5不一样，页面显示的是H5
        msg += "\n"
        msg += f"累计确诊{data['chinaTotal']['confirm']}\n"
        msg += f"累计治愈{data['chinaTotal']['heal']}\n"
        msg += f"累计死亡{data['chinaTotal']['dead']}\n"
        return msg
    elif area == "吉林市":
        for province in all_province:
            if province['name'] == "吉林":
                for city in province['children']:
                    if city['name'] == "吉林":
                        result = city
                        type_ = "(市)"
    else:
        # 移除“市”
        if area[-1] == "市":
            area = area[0:-1]
        # 先找省
        if area[-1] == "省":
            # 针对指定为省份的查询
            for province in all_province:
                if province['name'] == area[0:-1]:
                    province.pop('children')
                    result = province
                    type_ = "(省)"
        else:
            # 不会优化，两个for嗯找，能跑就行
            for province in all_province:
                if province['name'] == area and "省" not in area:
                    # 没有写“省”字，但要找的确实是一个省
                    province.pop('children')
                    result = province
                    type_ = "(省)"
                    break
                for city in province['children']:
                    if city['name'] == area:
                        result = city
                        type_ = "(市)"
    if area in ['北京', '天津', '重庆', '上海']:
        type_ = "(直辖市)"
    elif area in ['香港', '澳门']:
        type_ = "(特别行政区)"
    msg += f"{result['name']}{type_}疫情：\n"
    msg += f"现存确诊：{result['total']['nowConfirm']}" + (
        f"(+{result['today']['confirm']})" if result['today']['confirm'] > 0 else "")
    msg += "\n"
    if type_ != "(市)": # api里新增了wzz和wzz_add字段，但是二级行政区恒为0
        try:
            msg += f"现存无症状：{result['total']['wzz']}" +(
                f"(+{result['today']['wzz_add']})" if result['today']['wzz_add'] > 0 else "")
            msg += "\n"
        except:
            pass
    msg += f"累计确诊：{result['total']['confirm']}\n"
    try:
        msg += f"累计死亡：{result['total']['dead']} ({result['total']['deadRate']}%)\n"
    except:
        msg += f"累计死亡：{result['total']['dead']} ({(result['total']['dead'] / result['total']['confirm'] * 100):.2f}%)\n"
    try:
        msg += f"累计治愈：{result['total']['heal']} ({result['total']['healRate']}%)\n"
    except:
        msg += f"累计治愈：{result['total']['heal']} ({(result['total']['heal'] / result['total']['confirm'] * 100):.2f}%)\n"
    msg += f"当前地区信息今日已更新\n最后更新时间：\n{data['lastUpdateTime']}\n" if result['today']['isUpdated'] else "！当前地区信息今日无更新\n"

    if type_ in ["(省)","(特别行政区)"]:  # 没有获取到风险等级
        return msg

    try:  # 不知道稳不稳，先用try包一下
        url_risk_area = "https://wechat.wecity.qq.com/api/PneumoniaTravelNoAuth/queryAllRiskLevel"
        payload_json = {"args": {"req": {}}, "service": "PneumoniaTravelNoAuth", "func": "queryAllRiskLevel",
                        "context": {"userId": "a"}}
        risk_area_data = await aiorequests.post(url=url_risk_area, json=payload_json)
        risk_area_data = await risk_area_data.json()
        risk_area_data = risk_area_data['args']['rsp']
        mediumRiskAreaList = risk_area_data['mediumRiskAreaList']
        highRiskAreaList = risk_area_data['highRiskAreaList']
        
        
        # （吉林市上面没移除“市”）
        if area[-1] == "市":
            area = area[0:-1]
        
        msg += '\n中风险地区：\n'
        mid_risk_msg = ''
        for i in mediumRiskAreaList:
            for j in i['list']:
                if j['cityName'] in [area, area + "市"]:
                    mid_risk_msg += f"  {j['areaName']} {j['communityName']}\n"
        if len(mid_risk_msg) > 0:
            mid_risk_msg = mid_risk_msg.replace('、', '\n  ')
            msg += mid_risk_msg + '\n'
        else:
            msg += '  N/A\n'

        msg += '高风险地区：\n'
        high_risk_msg = ''
        for i in highRiskAreaList:
            for j in i['list']:
                if j['cityName'] in [area, area + "市"]:
                    high_risk_msg += f"  {j['areaName']} {j['communityName']}\n"
        if len(high_risk_msg) > 0:
            high_risk_msg = high_risk_msg.replace('、', '\n  ')
            msg += high_risk_msg + '\n'
        else:
            msg += '  N/A\n'
            
        return msg
    except:
        return msg


def image_draw(msg):
    fontpath = font_path = os.path.join(os.path.dirname(__file__), 'simhei.ttf')
    font1 = ImageFont.truetype(fontpath, 16)
    width, height = font1.getsize_multiline(msg.strip())
    img = Image.new("RGB", (width + 20, height + 20), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), msg, fill=(0, 0, 0), font=font1)
    b_io = io.BytesIO()
    img.save(b_io, format="JPEG")
    base64_str = 'base64://' + base64.b64encode(b_io.getvalue()).decode()
    return base64_str


@sv.on_suffix("疫情")
@sv.on_prefix("疫情")
async def yiqing(bot, ev):
    # 冷却器检查
    if not flmt.check(ev['user_id']):
        await bot.send(ev, f"查询冷却中，请{flmt.left_time(ev['user_id']):.2f}秒后再试~", at_sender=True)
        return
    area = ev.message.extract_plain_text()
    try:
        msg = await get_yiqing_data(area)
        flmt.start_cd(ev['user_id'])
    except Exception as e:
        if str(e) == "'name'":
            msg = "无法查询该地区疫情"
        else:
            msg = f"查询{area}数据失败：{e}"
            repr(e)
        flmt.start_cd(ev['user_id'], 3)
    if len(msg) < 30:
        await bot.send(ev, msg)
    else:
        pic = image_draw(msg)
        await bot.send(ev, f'[CQ:image,file={pic}]')


@sv.on_fullmatch('疫情帮助')
async def yiqing_help(bot, ev):
    help_msg = "输入xx[省市]疫情，获取xx地区的疫情信息。xx只可输入一级或二级行政区名。"
    await bot.send(ev, help_msg)
