import xmltodict
import ssl
import aiohttp
import xlrd

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
ssl._create_default_https_context = ssl._create_unverified_context


workbook = xlrd.open_workbook()#你的表格绝对位置如r'C:\Users\Administrator\Desktop\yourbot\trans.xlsx'
tab = workbook.sheet_by_name("物品与技能")
length = tab.nrows  

async def getmkt(id)->dict:
    try:       
        url = (f"https://api.evemarketer.com/ec/marketstat?usesystem=30000142&typeid={id}")
        async with aiohttp.ClientSession() as Session:
            async with Session.get(url=url,headers=headers) as rep:
                context = await rep.read()
        dexml = xmltodict.parse(context)
        jitabuy = float(dexml['exec_api']['marketstat']['type']['buy']['max'])
        jitasell = float(dexml['exec_api']['marketstat']['type']['sell']['min'])
        jita = {'buy':jitabuy,'sell':jitasell}
        return jita
    except:
        url = (f"https://www.ceve-market.org/tqapi/marketstat?typeid={id}&usesystem=30000142")
        async with aiohttp.ClientSession() as Session:
            async with Session.get(url=url,headers=headers) as rep:
                context = await rep.read()
        dexml = xmltodict.parse(context)
        jitabuy = float(dexml['evec_api']['marketstat']['type']['buy']['max'])
        jitasell = float(dexml['evec_api']['marketstat']['type']['sell']['min'])
        jita = {'buy':jitabuy,'sell':jitasell}
        return jita

async def GetItem(CnItem):
    num = 0 
    for i in range(length):
        row = tab.row_values(i)
        if CnItem in row[1]:
            ItemId = str(row[2]).replace(".0","")
            ItemName = str(row[1])
            ItemDir={'id':ItemId,'name':ItemName}
            return ItemDir
        else:
            num = num + 1
            if(num == 21085):
                return "表内无此物品"

async def PGetItem(CnItem):
    num = 0
    for i in range(length):
        row = tab.row_values(i)
        if CnItem == row[1]:
            ItemId = str(row[2]).replace(".0","")
            ItemName = str(row[1])
            ItemDir={'id':ItemId,'name':ItemName}
            return ItemDir
        else:
            num = num + 1
            if(num == 21085):
                return "表内无此物品"

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
                return (f"{item['name']}\njitabuy:\n{jitabuy} ISK\njitasell:\n{jitasell} ISK")
        else:
            return "无法查询此物品,表内可能没有此物品"
    except Exception as e:
        return e

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
        return e