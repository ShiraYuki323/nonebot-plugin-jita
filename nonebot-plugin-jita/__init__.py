from ssl import OP_NO_COMPRESSION
from nonebot.adapters.cqhttp import message
import xlrd
from .getdata import getjita,pregetjita,colgetjita
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot,Event, Message, bot
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.typing import T_State


ojita = on_command('ojita',priority=5)
opjita = on_command('opjita',priority=5)
col = on_command('col',priority=5)

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
    await opjita.finish(getval)    

@col.handle()
async def _(bot : Bot ,event: Event,state: T_State):
    args = str(event.get_message()).strip()    
    if args:        
        state["id"] = args

@col.got("id",prompt="想查询什么物品呢？")
async def hanlde_id(bot: Bot ,event: Event,state: T_State):
    gotid = state["id"]
    getval = await colgetjita(gotid)
    Message(getval)
    await col.finish(getval)   




