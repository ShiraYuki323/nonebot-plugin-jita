import xmltodict
import ssl
import aiohttp

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
ssl._create_default_https_context = ssl._create_unverified_context

async def getmkt(id):
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
