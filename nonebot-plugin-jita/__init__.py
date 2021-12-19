import re
from ssl import OP_NO_COMPRESSION
from nonebot.plugin import on
from pydantic.main import prepare_config
import xlrd
from .config import getmkt
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot,Event, Message, bot
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.typing import T_State


ojita = on_command('ojita',priority=5)
opjita = on_command('opjita',priority=5)


@ojita.handle()
async def _(bot : Bot ,event: Event,state: T_State):
    args = str(event.get_message()).strip()    
    if args:        
        state["id"] = args
    
@ojita.got("id",prompt="想查询什么物品呢？")
async def hanlde_id(bot: Bot ,event: Event,state: T_State):
    gotid = state["id"]
    getval = await getjita(gotid)
    await ojita.finish(getval)    


@opjita.handle()
async def _(bot : Bot ,event: Event,state: T_State):
    args = str(event.get_message()).strip()    
    if args:        
        state["id"] = args


@opjita.got("id",prompt="想查询什么物品呢？")
async def hanlde_id(bot: Bot ,event: Event,state: T_State):
    gotid = state["id"]
    getval = await pregetjita(gotid)
    await ojita.finish(getval)    

async def getjita(gotid):
    num = 0 
    gotid = str(gotid)
    workbook = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\qqbot\trans.xlsx')
    tab = workbook.sheet_by_name("物品与技能")
    length = tab.nrows   
    for i in range(length):
        row = tab.row_values(i)
        if gotid in row[1]:
            inid = row[2]
            ltem = row[1]
            inid = str(inid)
            inid = inid.replace(".0","")
            all = await getmkt(inid)
            if(all['buy'] == 0.00 and all['sell'] == 0.00 ):
                return (f"{ltem}\n该物品买卖价格均为0")
            else:          
                jitabuy = format(all['buy'],',')     
                jitasell = format(all['sell'],',')         
                return (f"{ltem}\njitabuy:\n{jitabuy} ISK\njitasell:\n{jitasell} ISK")
        else:
            num = num + 1
            if(num == 21085):
                return("无法查询此物品,表内可能没有此物品") 

async def pregetjita(gotid):
    num = 0 
    gotid = str(gotid)
    workbook = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\qqbot\trans.xlsx')
    tab = workbook.sheet_by_name("物品与技能")
    length = tab.nrows   
    for i in range(length):
        row = tab.row_values(i)
        if gotid == row[1]:
            inid = row[2]
            ltem = row[1]
            inid = str(inid)
            inid = inid.replace(".0","")
            all = await getmkt(inid)
            if(all['buy'] == 0.00 or all['sell'] == 0.00 ):
                return ("该物品买卖价格均为0")
            else:          
                jitabuy = format(all['buy'],',')     
                jitasell = format(all['sell'],',')         
                return (f"{ltem}\njitabuy:\n{jitabuy} ISK\njitasell:\n{jitasell} ISK")
        else:
            num = num + 1
            if(num == 21085):
                #print("无法查询此物品") 
                return("无法查询此物品,请检查物品名称是否完整") 



