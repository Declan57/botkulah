# credits Alfiananda
# ported for SPARKZZZ by @vishnu175
import asyncio
import os
import time

from telethon.tl.types import DocumentAttributeFilename
from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.utils import progress


@register(outgoing=True, pattern=r"^\.ssvideo(?: |$)(.*)")
async def ssvideo(framecap):
    reply_message = await framecap.get_reply_message()
    if not (reply_message.media or framecap.reply_to_msg_id):
        await framecap.edit("`reply to a video..`")
        return
    try:
        frame = int(framecap.pattern_match.group(1))
        if frame > 10:
            return await framecap.edit("`hey..dont put that much`")
    except BaseException:
        return await framecap.edit("`Please input number of frame!`")
    if (reply_message.photo
            or (DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
                in reply_message.media.document.attributes)
            or (DocumentAttributeFilename(file_name="sticker.webp")
                in reply_message.media.document.attributes)
            ):
        return await framecap.edit("`Unsupported files..`")
    c_time = time.time()
    await framecap.edit("`Downloading media..`")
    ss = await bot.download_media(
        reply_message,
        "anu.mp4",
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, framecap, c_time, "[DOWNLOAD]")
        ),
    )
    try:
        await framecap.edit("`Proccessing..`")
        command = f"vcsi -g {frame}x{frame} {ss} -o ss.png "
        os.system(command)
        await framecap.client.send_file(
            framecap.chat_id,
            "ss.png",
            reply_to=framecap.reply_to_msg_id,
        )
        await framecap.delete()
        os.system("rm -rf *.png")
        os.system("rm -rf *.mp4")
    except BaseException as e:
        os.system("rm -rf *.png")
        os.system("rm -rf *.mp4")
        return await framecap.edit(f"{e}")


CMD_HELP.update({
    "ssvideo":
    "`.ssvideo` <grid>"
    "\nUsage: Capture video frames by <grid> x <grid>."
    "\n*max grid is 10."
})
