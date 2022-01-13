import xmltodict
from aiohttp import ClientSession
from aiohttp import TCPConnector
from .evedata import eved
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}


eve_types = eved.eve_types
listLen = len(eve_types)
async def getmkt(id)->dict:
    try:
        url = (f"https://www.ceve-market.org/tqapi/marketstat?typeid={id}&usesystem=30000142")
        async with ClientSession(connector=TCPConnector(verify_ssl=False)) as Session:
            async with Session.get(url=url,headers=headers) as rep:
                context = await rep.read()
        dexml = xmltodict.parse(context)
        jitabuy = float(dexml['evec_api']['marketstat']['type']['buy']['max'])
        jitasell = float(dexml['evec_api']['marketstat']['type']['sell']['min'])
        jita = {'buy':jitabuy,'sell':jitasell}
        return jita           
    except Exception as e:
        print(e)
        url = (f"https://api.evemarketer.com/ec/marketstat?usesystem=30000142&typeid={id}")
        async with ClientSession(connector=TCPConnector(verify_ssl=False)) as Session:
            async with Session.get(url=url,headers=headers) as rep:
                context = await rep.read()
        dexml = xmltodict.parse(context)
        jitabuy = float(dexml['exec_api']['marketstat']['type']['buy']['max'])
        jitasell = float(dexml['exec_api']['marketstat']['type']['sell']['min'])
        jita = {'buy':jitabuy,'sell':jitasell}
        return jita   

async def GetItem(CnItem):
    if CnItem in ('PLEX','plex','伊甸币'):
        return {'id':'44992','name':'伊甸币'}
    else:
        num = 0
        for i in eve_types:
            if CnItem in eve_types[i][0]:
                ItemId = i
                ItemName = eve_types[i][0]
                ItemDir={'id':ItemId,'name':ItemName}
                #print(ItemDir)
                return ItemDir
            else:
                num = num+1
                if num == listLen:
                    return "表内无此物品"

async def PGetItem(CnItem):
    num = 0
    for i in eve_types:
        if CnItem == eve_types[i][0]:
            ItemId = i
            ItemName = eve_types[i][0]
            ItemDir={'id':ItemId,'name':ItemName}
            return ItemDir
        else:
            num = num+1
            if num == listLen:
                return "表内无此物品"
async def colgetitem(CnItem):
    num = 0
    a = 0
    colall = []
    for i in eve_types:
        if CnItem in eve_types[i][0]:
            a = a +1
            if a <= 6:
                ItemId = i
                ItemName = eve_types[i][0]
                ItemDir={'id':ItemId,'name':ItemName}
                colall.append(ItemDir)
        else:
            num = num +1
            if num == listLen:
                colall.append('null')         
    return colall  
async def getjita(GetCnItem):
    try:       
        item = await GetItem(GetCnItem)
        if item != "表内无此物品":
            jitamkt = await getmkt(item['id'])
            if(jitamkt['buy'] == 0.00 and jitamkt['sell'] == 0.00 ):
                return (f"{item['name']}\n该物品买卖价格均为0")
            else:
                jitabuy = format(jitamkt['buy'],',')     
                jitasell = format(jitamkt['sell'],',') 
                if item['id'] == '44992':
                    plexjitabuy = format((jitamkt['buy']*500),',')     
                    plexjitasell = format((jitamkt['sell']*500),',') 
                    return (f"{item['name']}\njitabuy:\n{jitabuy} ISK\njitasell:\n{jitasell} ISK\n{item['name']}*500\njitabuy:\n{plexjitabuy} ISK\njitasell:\n{plexjitasell} ISK")   
                else:
                    pass                         
                return (f"{item['name']}\njitabuy:\n{jitabuy} ISK\njitasell:\n{jitasell} ISK")
        else:
            return "无法查询此物品,表内可能没有此物品"
    except Exception as e:
        return ('出错啦！错误是：' +str(e))

async def pregetjita(GetCnItem):
    try:
        item = await PGetItem(GetCnItem)
        if item != "表内无此物品":
            jitamkt = await getmkt(item['id'])
            if(jitamkt['buy'] == 0.00 and jitamkt['sell'] == 0.00 ):
                return (f"{item['name']}\n该物品买卖价格均为0")
            else:          
                jitabuy = format(jitamkt['buy'],',')     
                jitasell = format(jitamkt['sell'],',')         
                return (f"{item['name']}\njitabuy:\n{jitabuy} ISK\njitasell:\n{jitasell} ISK")
        else:
            return "无法查询此物品,请检查物品名称是否完整"
    except Exception as e:
        return ('出错啦！错误是：' +str(e))

async def colgetjita(GetCnItem):
    try:
        colv = []
        num  = -1
        wn = 1
        item = await colgetitem(GetCnItem)
        if item[0]!='null':
            while wn <= 6:
                wn = wn + 1
                num = num+1
                jitamkt = await getmkt(item[num]['id'])      
                jitabuy = jitamkt['buy']  
                jitasell = jitamkt['sell']      
                col = {'name':f'{item[num]["name"]}','buy':jitabuy,'sell':jitasell}
                colv.append(col)
            allbuy = format((colv[0]['buy'] + colv[1]['buy'] + colv[2]['buy'] + colv[3]['buy'] + colv[4]['buy'] + colv[5]['buy']),',')
            allsell = format((colv[0]['sell'] + colv[1]['sell'] + colv[2]['sell'] + colv[3]['sell'] + colv[4]['sell'] + colv[5]['sell']),',')
            all = (f"一堆物品的价格：\n{colv[0]['name']}\nbuy:{format(colv[0]['buy'],',')}\nsell:{format(colv[0]['sell'],',')}\n{colv[1]['name']}\nbuy:{format(colv[1]['buy'],',')}\nsell:{format(colv[1]['sell'],',')}\n{colv[2]['name']}\nbuy:{format(colv[2]['buy'],',')}\nsell:{format(colv[2]['sell'],',')}\n{colv[3]['name']}\nbuy:{format(colv[3]['buy'],',')}\nsell:{format(colv[3]['sell'],',')}\n{colv[4]['name']}\nbuy:{format(colv[4]['buy'],',')}\nsell:{format(colv[4]['sell'],',')}\n{colv[5]['name']}\nbuy:{format(colv[5]['buy'],',')}\nsell:{format(colv[5]['sell'],',')}\n总价:\nbuy:{allbuy}\nsell:{allsell}")
            return all
        else:
            return "无法查询此物品,表内可能没有此物品"
    except Exception as e:
        return ('出错啦！错误是：' +str(e) + '\n可能是你需要查询的物品不足6个')
