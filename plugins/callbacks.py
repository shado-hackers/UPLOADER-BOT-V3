import os
from functions.display_progress import progress_for_pyrogram, humanbytes
from plugins.config import Config
from plugins.dl_button import ddl_call_back
from plugins.youtube_dl_button import youtube_dl_call_back
from plugins.settings.settings import OpenSettings
from plugins.translation import Translation
from pyrogram import Client, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.database.database import db
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




@Client.on_callback_query()
async def button(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=Translation.START_TEXT.format(update.from_user.mention),
            reply_markup=Translation.START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=Translation.HELP_TEXT,
            reply_markup=Translation.HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=Translation.ABOUT_TEXT,
            reply_markup=Translation.ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    elif query.data == "openSettings":
        await query.answer()
        await OpenSettings(query.message)

    elif update.data == "showThumbnail":
        thumbnail = await db.get_thumbnail(update.from_user.id)
        if not thumbnail:
            await update.answer("You didn't set any custom thumbnail!", show_alert=True)
        else:
            await update.answer()
            await bot.send_photo(update.message.chat.id, thumbnail, "Custom Thumbnail",
                               reply_markup=types.InlineKeyboardMarkup([[
                                   types.InlineKeyboardButton("Delete Thumbnail",
                                                              callback_data="deleteThumbnail")
                               ]]))
    elif query.data == "deleteurlthumbnail":
        await db.set_lazy_thumbnail(query.from_user.id, None)
        await query.answer("**Okay baby, I deleted your custom thumbnail for url downloading. Now I will apply default thumbnail. ☑**", show_alert=True)
        await query.message.delete(True)
    elif query.data == "deleteThumbnail":
        await db.set_thumbnail(query.from_user.id, None)
        await query.answer("**Okay sweetie, I deleted your custom thumbnail for direct renaming. Now I will apply default thumbnail. ✅️**", show_alert=True)
        await query.message.delete(True)

    elif query.data == "triggerUploadMode":
        await query.answer("Thank You ")
        upload_as_doc = await db.get_upload_as_doc(query.from_user.id)
        if upload_as_doc:
            await db.set_upload_as_doc(query.from_user.id, False)
        else:
            await db.set_upload_as_doc(query.from_user.id, True)
        await OpenSettings(query.message)
    elif "close" in query.data:
        await query.message.delete(True)
    elif "|" in update.data:
        await youtube_dl_call_back(bot, update)
    elif "=" in update.data:
        await ddl_call_back(bot, update)

    else:
        await update.message.delete()
