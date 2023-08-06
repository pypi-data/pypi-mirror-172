import asyncio

from nonebot import logger, on_command
from nonebot.adapters.onebot.v11 import ActionFailed, Message, MessageSegment
from nonebot.exception import FinishedException
from nonebot.internal.matcher import Matcher
from nonebot.params import CommandArg

from .const import SCHALE_URL
from .data_bawiki import db_wiki_stu, recover_stu_alia, schale_to_gamekee
from .data_gamekee import (
    game_kee_calender,
    game_kee_page_url,
    get_game_kee_page,
    get_l2d,
    get_stu_cid_li,
)
from .data_schaledb import (
    draw_fav_li,
    schale_calender,
    schale_get_stu_dict,
    schale_get_stu_info,
)

handler_calender = on_command("ba日程表")


@handler_calender.handle()
async def _(matcher: Matcher, arg: Message = CommandArg()):
    arg: str = arg.extract_plain_text()

    await matcher.send("正在绘制图片，请稍等")
    try:
        if "schale" in (arg := arg.lower()):
            arg = arg.replace("schale", "").strip()
            servers = []

            if (not arg) or ("日" in arg) or ("j" in arg):
                servers.append(0)
            if (not arg) or ("国际服" in arg) or ("g" in arg):
                servers.append(1)

            await asyncio.gather(
                *[
                    matcher.send(x)
                    for x in (
                        await asyncio.gather(*[schale_calender(x) for x in servers])
                    )
                ]
            )
            await matcher.finish()
        else:
            await matcher.finish(await game_kee_calender())
    except (FinishedException, ActionFailed):
        raise
    except:
        logger.exception("绘制日程表图片出错")
        return await matcher.finish("绘制日程表图片出错，请检查后台输出")


async def send_wiki_page(sid, matcher: Matcher):
    url = game_kee_page_url(sid)
    await matcher.send(f"请稍等，正在截取Wiki页面……\n{url}")

    try:
        img = await get_game_kee_page(url)
    except:
        logger.exception(f"截取wiki页面出错 {url}")
        return await matcher.finish("截取页面出错，请检查后台输出")

    await matcher.finish(MessageSegment.image(img))


stu_schale = on_command("ba学生图鉴")


@stu_schale.handle()
async def _(matcher: Matcher, arg: Message = CommandArg()):
    arg = arg.extract_plain_text().strip()
    if not arg:
        return await matcher.finish("请提供学生名称")

    try:
        ret = await schale_get_stu_dict()
    except:
        logger.exception("获取学生列表出错")
        return await matcher.finish("获取学生列表表出错，请检查后台输出")

    if not ret:
        return await matcher.finish("没有获取到学生列表数据")

    if not (data := ret.get(await recover_stu_alia(arg))):
        return await matcher.finish("未找到该学生")

    stu_name = data["PathName"]
    await matcher.send(f"请稍等，正在截取SchaleDB页面～\n" f"{SCHALE_URL}?chara={stu_name}")

    try:
        img = MessageSegment.image(await schale_get_stu_info(stu_name))
    except:
        logger.exception(f"截取schale db页面出错 chara={stu_name}")
        return await matcher.finish("截取页面出错，请检查后台输出")

    await matcher.finish(img)


stu_rank = on_command("ba学生评价", aliases={"ba角评"})


@stu_rank.handle()
async def _(matcher: Matcher, arg: Message = CommandArg()):
    arg = arg.extract_plain_text().strip()
    if not arg:
        return await matcher.finish("请提供学生名称")

    try:
        im = await db_wiki_stu(await recover_stu_alia(arg))
    except:
        logger.exception(f"获取角评出错")
        return await matcher.finish("获取角评出错，请检查后台输出")

    await matcher.finish(im)


stu_wiki = on_command("ba学生wiki", aliases={"ba学生Wiki", "ba学生WIKI"})


@stu_wiki.handle()
async def _(matcher: Matcher, arg: Message = CommandArg()):
    arg = arg.extract_plain_text().strip()
    if not arg:
        return await matcher.finish("请提供学生名称")

    try:
        ret = await get_stu_cid_li()
    except:
        logger.exception("获取学生列表出错")
        return await matcher.finish("获取学生列表出错，请检查后台输出")

    if not ret:
        return await matcher.finish("没有获取到学生列表数据")

    if not (sid := ret.get(await recover_stu_alia(arg, True))):
        return await matcher.finish("未找到该学生")

    await send_wiki_page(sid, matcher)


fav = on_command("ba好感度", aliases={"ba羁绊", "bal2d", "baL2D", "balive2d", "baLive2D"})


@fav.handle()
async def _(matcher: Matcher, arg: Message = CommandArg()):
    arg = arg.extract_plain_text().strip()
    if not arg:
        return await matcher.finish("请提供学生名称或所需的羁绊等级")

    # 好感度等级
    if arg.isdigit():
        arg = int(arg)
        if arg > 9:
            return await matcher.finish("学生解锁L2D最高只需要羁绊等级9")
        if arg < 1:
            return await matcher.finish("学生解锁L2D最低只需要羁绊等级1")

        try:
            p = await draw_fav_li(arg)
        except:
            logger.exception("绘制图片出错")
            return await matcher.finish("绘制图片出错，请检查后台输出")

        return await matcher.finish(p)

    # 学生名称
    arg = await recover_stu_alia(arg)

    try:
        ret = await schale_get_stu_dict()
    except:
        logger.exception("获取学生列表出错")
        return await matcher.finish("获取学生列表表出错，请检查后台输出")

    if stu := ret.get(arg):
        if not (lvl := stu["MemoryLobby"]):
            return await matcher.finish("该学生没有L2D")

        im = MessageSegment.text(f'{stu["Name"]} 在羁绊等级 {lvl[0]} 时即可解锁L2D\nL2D预览：')
        if p := await get_l2d(await schale_to_gamekee(arg)):
            im += [MessageSegment.image(x) for x in p]
        else:
            im += (
                "没找到该学生的L2D看板\n"
                "可能原因：\n"
                "- GameKee页面爬取不到角色L2D图片\n"
                "- GameKee和插件没有收录该学生的L2D\n"
            )
        return await matcher.finish(im)

    return await matcher.finish("未找到学生")
