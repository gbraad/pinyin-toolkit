#!/usr/bin/python
#-*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# This is a plugin for Anki: http://ichi2.net/anki/
# It is part of the Pinyin Toolkit plugin.
#
# This file is modifed from the version 1.0 of the:
# Kanji Graph Plugin by Anton Zolotkov <azolotkov@gmail.com>
# And has been hacked to work for Chinese
#
# License:     GNU GPL
# ---------------------------------------------------------------------------


try:
    from matplotlib.figure import Figure
except UnicodeEncodeError:
    # haven't tracked down the cause of this yet, but reloading fixes it
    from matplotlib.figure import Figure

from ankiqt.ui.graphs import GraphWindow, AdjustableFigure
import anki.utils
from anki.hooks import wrap,addHook

import hooks

import pinyin.utils

hanziGrades = [
    (u'Non-HSK', u''),
    (u'HSK Basic', u'一七万三上下不且世业东丢两个中丰为主举久么义之乐九也习书买乱了事二云互五些交产亮亲人亿什今介从他代以们件任休会伟但位低住体何作你使例侯便信俩倍倒候借假做停健傅像儿元先克全八公六共关兴其典内再冒写农冬决况冷净准凉几出刀分切划刚初利别刮到刻前剩力办加务动助努劳包化北医十千午半单卖南占卡危厂历原去参又友双反发取变口句只叫可史右号吃各合同名后向吗吧听吹呀告呐员呢周和咖咱咳哈响哥哪哭唱商啊啡啤啦喂喊喜喝嗯嗽嘛嘴器四回因团园困围国图圆在地场坏坐块坚城基堂墙增声处备复夏外多夜够大天太夫头女奶她好如妈妹始姐姑姓娘子字学孩它安完定宜实客室宴家容宿寄富寒对导封将小少尤就尺局层屋展山岁工左差己已市布师希带帮常帽干平年幸广床应店府度座庭康建开弟张当录彩影往很得心必志忘忙快念忽态怎怕思急总息您情惯想愉意感愿慢懂成我或戴户房所手才打扬批找技把报抬抱抽拉拍拾拿持挂指挤挺换掉掌排接推提握搞搬摆播操擦支收改放政故教敢散数整文斤新方旁旅族日旧早时明易星春昨是晚晨晴暖更最月有朋服望朝期本术机杂李村束条来杯板极果查树校样根桌桔桥检棵椅楚楼概橘次欢歌正步死段母每比毛民气水永求汉江汤汽没河治法注泳洗活派流浅济海消深清渴游湖满漂演澡火灯点炼烦烧热然照熟爬爱父爸片牛物特猪玩现班球理瓶生用电男画界留疼病痛白百的目直相省看真眼着睛睡知短矮研破础确碗碰磁示礼社祖祝神票福离秋种科租究空穿突窗立站章笑笔第等答简算篇篮米精糖系紧累红级纪纸练组细织绍经结给继绩续绿羊翻老考者而联肉育胜能脏脚脱脸腿自舍舒舞般船色艺节花苦英苹茶草药菜蓝蕉虽蛋行街衣表袜被装西要见观视览觉角解言计认讨让记讲许论设访评识诉词译试话该语误说请读课谁调谅谈谊谢象负责贵赛赢走起足跑跟路跳践踢身躺车轻较辅辆输辛边过迎运近还这进远连迟退送适通遇遍道那邮部都酒酸里重钟钢钱铅银错锻长门问间闻阳阴附院除险难集雨雪零需青静非面鞋音页须顾顿预领题颜风飞食饭饱饺饿馆首香马驾验骑高鱼鸡麻黄齐'),
    (u'HSK Elementary', u'丈与专丝严临丽乎乏乒乓乘乡争于井亩享京仅仍仔付令仪仰价份仿企伍众优伙伞传伤伯估伸似余佛供依侵促俗保修俱倡值偏偷傍催傲傻允兄充光免兔党入兵具养册军冠冰冲冻减凡击列则创判制刷刺剧剪副割劝功励劲势勇勺匹区升卜卫印即却卷厅厉压厌厕厘厚厨县叉及叔受叠古另召台叶司吊吐吓否吨吩含启吵吸呆味呼命咐咬咽品哇哎哲哼善喷嗓嘿嚷固圈土圾址均坡垃型埋堆堵塑塔填境墨壁士壶央失夹夺奇奋奖套妇妙妻委姨姻婚嫂孔存季守宝宣害宽宾密察寸寻射尊尖尝尽尾居届属岛岸崇巧巨巩巴巾币帝席幅并庄庆序底庙延异弃弄式引弯弱弹强形彻征待律微德忆忍怒怜性怪恋恐恢恨恳悄悉悔悟悠悲惊惹愁愤慌慕慰懒戏战戚扁扇扎扑扔托扛扣执扩扫扭扮扰扶承抄抓投抖抗折抢护披担拆拐拒拔拖招拜拣拥拦择括拼按挑挖挡挥挨捆捉捕捞损捡捧据掀授掏探控措描插援搁搭摇摔摘撒撕撞攻效敌救敬敲斗料斜断施旗无既昏映显晒晓普景暂暑暗曾替朗木未朴朵杀杆材松构析林枪架某染柴柿标株格案桶梁梦梨梯械棉森植榜模欠欺款歇歉止此武歪殊毕毫毯汗池污沉沙油沿泛泥泪泼洋洒洞测浓浪浮涂涨液淡混添渐渠渡温港湿源滑滚滴漏漠激灭灰灵灾炮烂烈烟烤烫煤煮熊燃燥爷版牌牙牲牵牺犯状狗独狮狼猜猫献猴率玉王环玻珠璃瓜甜甩田由略疑疲瘦登皂皇皮盆益盐盒盖盗盘盼盾睁瞧矛石矿码砍硬碎碑磨禁秀私秒秘秩积称移程稍稳稻稼穷窄竞竟童端竹符筑策筷签管箭箱类粉粒粗粘粮糊糕糟素紫繁纠纤约纷纺线终绕绝统绢绪绳维综编缩缺罐网置美羡群羽翅耐耳聊职聪肃肚肝肠肤肥肩肯肺胃胆背胖胡胳胸脆脉脑脖脾腐腰膀膊臭至致舌航良艰苯范荣获菌萝营落著蔬薄藏虎虑虚虫蛇蜂蜜血补衫衬袋袖裙裤规触警订训议讯证诗诚详谓豆貌贡败货质购贯贴贸费贺资赔赞赶趁超越趟趣跃跌距跨跪踩蹲躲转轮软辉辟达迅迈违迫述迷迹追逃选透逐递途逗逛速造逢逼遭遵避邀邻郊郎配酱醉醋醒采释野量金针钓钻铁铃铜铺锅锐键镜闪闭闯闲闹阅阔队防阵阶阿际陆降限陪随隔雄雷雾露靠革顶项顺颗飘餐饼馒骂骄骗骨鬼鲜鸟鹅麦默鼓鼻龄龙'),
    (u'HSK Intermediate', u'丁丑丘丙丛丧串丸乖乙予亏亚亡亭仇仓仗伊伴伺佩佳侧侨侮俄俏俯倘倚倦债倾偶偿僚僵兑兰兼兽冤冶凑凝凭凳凶凿刊删削剖剥劣勃勉勤勾匀匆匙华协博卧卵卸厢叙叭叹吞吻吼呵咙咸哀哆哗哟哦哨唇唤售喇喉喘喽嗦嘱噢囱圣坑坝坟坦垂垄垫垮域培堤塌塞墓墟壤壮壳夸奈奔奠奥奴妥妨姥姿威娃娱娶婆婴婶媳嫁嫌嫩孙孤宁宅宇宏宗官宙审宪宫宵寂寓寞寡寿尔尘尚屁屈屿岗岩峡峰崖崭巷帐帘帜幕幢幻幼库废廊廓弓归彼径徒御循忠怀怖怨恰恶患悦悬惕惜惦惨惭愈愚愧慎慧憾截扒扯抑抛抵抹押拢拧拨拳拴挣挫振挽捏捷掠掩揉揪揭搂搅搓搜摄摊摧摩撑撤攀敏斥斯旋旦旬旱昆晃晕晰智暴曲末朽权枉枕枝枯柄柏柔柜柱柳核栽桃档桩梅梳棋棍棒棚椒楞横欣歼残殖殿毁毅毒氏氓氛氧汇沟沸沾泌泡波泽洁洪浆浇浑浴浸涉涌润淆淋淹渔渣溅溉溜溶滥滩漆漫潮灌灸灿炉炒炸烁烛焊焦焰煌煎熬燕爆爹牢牧犹狂狠狡狱猎猛猾猿珍琴瓣瓦瓷甘甚甭甲申畅畔番疆疗疯疾症痕癌皱盏监盛盟盯盲眉眠眯督瞎瞒瞪矩砖砸碍碱秧稀税稚稿窑窜窟窿竭笼筋筐筒籍粥粪粱索纯纱纲纵纹绑络缓缘缚缝缸罚罢罩罪署翁翘耀耍耕耗耽聚肌股肿胀胁胞胶腔腾膏膨舅舰舱艘艳芽苍苗若茅荐荒菠萄葡蒙蒸蓬蔑虾蚀蚊蚕蛙蜡蝇蝴蝶蠢衡衰衷袍袭袱裁裂裕裹譬讶讽诊诞询诬诵谋谜谣谦谨谷豪豫财贫贱赏赚赠赤趴踊踏蹄蹈蹬躁轨载辈辑辜辞辣辩辱返逝逮逻遗遥遮酬酷鉴钉钞钥钩铝铲铸锁锈锡锣镇镑闷阂阻陈陌陡陵陷隐障隶雇雕震霉霜顷顽颂额颤饥饮饰饲饶驮驴驶驻驼骆骚骤魂鲸鸣鸭鸽黎齿'),
    (u'HSK Advanced', u'丹乃乌乔乞乳亢亦仁仆仙伏伐伪伶佣侄侈侍侣侦俊俐俘俭储僻兆兜兢冈凄凌凤凯凰凸凹函刁刃刑刨券刹剂剃剑劈劫勒勘勿匠匪卑卓厦叁叛叨叮叼吁吉君吟呈呕呜呻咋咏咨哄哑唆唐唠唯唾啃啄啥啸喻嗅嘉嘲噪嚼囊坊坛坯垒垦埠堕堡堪塘壹夕奉奏奢奸妄妆妒妖姆姜娇媒嫉孕孝宰寇寨寺尸尼尿屉屎屏屑屠屡履屯岂岔岭峻崩嵌川州巡巫帅帆帖幽庞庸廉弊弥弦彰役徊徐徘徽忌忧怠怯恒恩恭恼悼惋惑惠惧惩惫惰慈慨慷憋戒抚抠抡拄拇拌拓拘拙拟拱拽挎挚挟挠挪捅捌捍捎捐捣捶捻掂掐掘掰掷掺揍揽搀搏携摸撇撵擅攒敞敷斑斧斩旨旷旺昂昌昧昼晋晌晤晶晾暄暮曰杏杜杠杨杰枚枣柒柠柬栋栏栗桂桅框桐桑桨梗梢梧棕棱棺椭榆榨榴榷槐槽樱橡檬欲歧歹殃殴毙氢氮汁汛汞汪汰汹沃沏沛沥沫沼泄泉泊泣泰泻津洲洽浊浩涕涛涝涤淀淇淘淫渗渺湾溃溪滋滔滞滤滨潜潦潭澄瀑灶炊炎炕炭烘烹熄熏熔爪爽犁犬狈狐狭狸猖玖玫玲珊珑琢瑚瑞瑰畏畜畴疏疙疤疫疮痒痪痰痴痹瘟瘤瘩瘫瘸皆盈眨眶睦睬睹瞥瞩瞻砂砌硅硫碌碟碧碳磋磕磷祥祸禽禾秃秆秉秤秽稠穆穗穴窃窝竖竿笆笋笛笨筛筝筹箩篱簸籽粹糠絮纳绅绒绘绞绣绵绷绸缀缎缔缠缴罕罗羞羿翔翠翼耸耻聋聘肆肖肢肪肾脂脊腊腥腮腹膛膜膝臂臣舆舟舵舶艇艾芒芝芦芬芭芳芹苏茂茄茎茧茫荔荡荷莫莲菇菊萌萍董葫葬葱葵蒂蒜蓄蔓蔗蔼蔽蕴蕾薪薯藤蘑虏虹蚁蚂蛛蛮蛾蜓蜘蜻蝉蝗融螺衅衍衔袄裳覆誉誓讥讹讼诈诧诫诱诸诽谎谐谗谤谬谱谴豁豌贝贞贤贩贪贬贰贷贼贿赂赋赌赖赴趋跺踌踪蹋蹦蹭躇躬轧轰轿辐辖辙辨辫辰辽迁逆逊遣邦邪郁郑鄙酌酗酝酶酿钙钦钮钳铀铭链销锋锌锤锦锯锹镁镰镶闸闺阀阁阐陋陶隆隘隙隧雀雁雅雌雹霍霞霸靴鞠鞭韧韵颁颇颈颊频颖颠饪馈馋驰驱驳骡髦魄魔鲁鸦鹊鹰鹿鼠龟黑'),
  ]

class HanziGraphHook(hooks.Hook):    
    # Returns the Hanzi Figure object for the plot

    def hanziData(self, graphwindow, days=30):
        # Retrieve information about the card contents that were first answered on each day
        mids = self.mw.deck.s.column0('select id from models where tags like "%s"', self.config.modelTag)
        rows = self.mw.deck.s.all("""
        select value, firstAnswered from cards, fields, facts
        where
        cards.reps > 0 and
        cards.factId = fields.factId
        and cards.factId = facts.id
        and facts.modelId in %s
        order by firstAnswered
        """ % anki.utils.ids2str(mids))
        
        # Retrieve all the card contents that the user has seen at least once
        allhanzi = self.deck.s.column0("""
        select value from cards, fields
        where
        cards.reps > 0 and
        cards.factId = fields.factId
        """)
        
        # Use the statistics engine to generate the data for graphing
        x, y, gradeys = hanziDailyStats(allhanzi, rows, days)
        # TODO: use gradeys
        
        # Setup the graph we will fill with the information
        figure = Figure(figsize=(graphwindow.width, graphwindow.height), dpi=graphwindow.dpi)
        graph = figure.add_subplot(111)
        graph.set_xlim(xmin=-days, xmax=0)
        
        # Set the minimum y value to be the smallest number of characters
        # in the range. Otherwise, if the number of hanzi you know didn't go
        # up too much in the given range, you'll get pretty much a rectangle
        # of a graph, which is not very useful
        if len(y) > 1:
            lastcount = y[len(y) - 1]
            firstcount = y[0] 
            
            padding = (lastcount - firstcount) / 10
            graph.set_ylim(ymin=max(0, firstcount - padding), ymax=lastcount + padding)

        # Add the final graph to the window
        graphwindow.filledGraph(graph, days, "#fdce51", x, y)
        
        return figure

    def setupHanziGraph(self, graphwindow):
        # Append our own graph at the end
        extragraph = ankiqt.ui.graphs.AdjustableFigure(graphwindow.parent, 'hanzi', lambda days: self.hanziData(graphwindow, days), graphwindow.range)
        extragraph.addWidget(QtGui.QLabel("<h1>Unique Hanzi Learned</h1>"))
        self.vbox.addWidget(extragraph)
        self.widgets.append(extragraph)
    
def hanziGrade(hanzi):
    from anki.stats import isKanji
    
    # Despite the name, this function works for Hanzi too:
    if not isKanji(hanzi):
        return None
    
    for grade, hanzis in hanziGrades:
        if hanzi in hanzis:
            return grade
    
    # Default to Non-HSK
    return hanziGrades[0][0]


def organizeHanziByGrade(allhanzi):
    # Create a set of Hanzi for each grade
    hanziByGrade = dict([(grade, set([])) for grade, _hanzis in hanziGrades])
    for hanzi in "".join(allhanzi):
        grade = hanziGrade(hanzi)
        if grade:
            # If this character was actually Hanzi, add it to the graded set
            hanziByGrade[grade].add(hanzi)
    
    return hanziByGrade

def hanziDailyStats(allhanzi, rows, daysInRange):
# This function returns a tuple (days, cumulativeTotal, cumulativesByGrade) where:
#  days is a list of day indexes, negative, with 0 representing today
#  cumulativeTotal is a list containing, for the corresponding day, the number
#    of hanzi that the user has "learned" up until the day
#  cumulativesByGrade is a dictionary of lists containing the same information, but
#    broken down by grade

    # Holds, for each day, the set constructued by appending values of all fields
    # for the cards that were first answered on the given day and removing duplicates
    firstLearnedByDay = {}
    endOfDay = time.time()
    for (value, firstAnswered) in rows:
        # FIXME: this doesn't account for midnightOffset
        day = int((firstAnswered - endOfDay) / 86400.0)
        firstLearnedByDay[day] = firstLearnedByDay.get(day, set()).update(set(value))

    # Compute the hanzi counts by grade
    hanziCountsByGradeByDay = {}
    for grade, hanziSet in organizeHanziByGrade(allhanzi).items():
        # Create an entry for this grade:
        thisGradeHanziCountsByDay = {}
        hanziCountsByGradeByDay[grade] = thisGradeHanziCountsByDay
      
        # Run time forward:
        for day, firstLearnedToday in sorted(firstLearnedByDay.items(), pinyin.utils.byFirst):
            # Obtain the set of hanzi learned today in this grade and add that amount to the learned amount
            learnedTodaySet = hanziSet.intersection(firstLearnedToday)
            thisGradeHanziCountsByDay[day] = thisGradeHanziCountsByDay.get(day, 0) + len(learnedTodaySet)
            
            # Remove the hanzi learned today from consideration in later time steps
            hanziSet.difference_update(learnedTodaySet)
  
    # Compute the total hanzi counts
    totalHanziCountsByDay = {}
    for grade, hanziCountsByDay in hanziCountsByGradeByDay.items():
        for day, hanziCount in hanziCountsByDay.items():
            totalHanziCountsByDay[day] = totalHanziCountsByDay.get(day, 0) + hanziCount
    
    # Convert the data into a format usable by the graphing platform
    days = [day for day in sorted(totalHanziCountsByDay.keys()) if day >= -daysInRange]
    cumulativeTotal = list(cumulative([totalHanziCountsByDay[day] for day in days]))
    cumulativesByGrade = {}
    for grade, hanziCountsByDay in hanziCountsByGradeByDay.items():
        cumulativesByGrade[grade] = list(cumulative([hanziCountsByDay.get(day, 0) for day in days]))
    
    return days, cumulativeTotal, cumulativesByGrade
    
    
if __name__ == "__main__":
  print "This is a plugin for Anki and cannot be run independently."
  print "Please download the latest version of Anki from http://ichi2.net/anki/"
  print "and copy this file into your ~/.anki/plugins directory."

"""
else:  # disabled as broke and generates exception; to fix we need to pass the arguments required for gaph building
  self.hanziGraph = HanziGraphHook(hooks.Hook) 
  self.mw = mw
  mw.addHook("init", self.hanziGraph) #also broken
  """