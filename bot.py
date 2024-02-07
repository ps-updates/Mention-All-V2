from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import os
import asyncio
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

Bot=Client(
    "Mention All Bot",
    api_id = int(os.environ.get("API_ID")),
    api_hash = os.environ.get("API_HASH"),
    bot_token = os.environ.get("BOT_TOKEN")
   )

chatQueue = []

stopProcess = False

@Bot.on_message(filters.command(["mentionall", "all"]))
async def everyone(client, message):
    global stopProcess
    try:
        try:
            sender = await Bot.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except:
            has_permissions = message.sender_chat

        if has_permissions:
            if len(chatQueue) > 5:
                await message.reply("⛔️ | ɪ'ᴍ ᴀʟʀᴇᴀᴅʏ ᴡᴏʀᴋɪɴɢ ᴏɴ ᴍʏ ᴍᴀxɪᴍᴜᴍ ɴᴜᴍʙᴇʀ ᴏꜰ 5 ᴄʜᴀᴛꜱ ᴀᴛ ᴛʜᴇ ᴍᴏᴍᴇɴᴛ.\nᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ ꜱʜᴏʀᴛʟʏ.")
            else:
                if message.chat.id in chatQueue:
                    await message.reply("🚫 | ᴛʜᴇʀᴇ'ꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴏɴɢᴏɪɴɢ ᴘʀᴏᴄᴇꜱꜱ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ. ᴘʟᴇᴀꜱᴇ /stop ᴛᴏ ꜱᴛᴀʀᴛ ᴀ ɴᴇᴡ ᴏɴᴇ.")
                else:
                    chatQueue.append(message.chat.id)

                    if len(message.command) > 1:
                        inputText = ' '.join(message.command[1:])
                    else:
                        inputText = ""

                    membersList = []
                    async for member in Bot.get_chat_members(message.chat.id):
                        if member.user.is_bot == True:
                            pass
                        elif member.user.is_deleted == True:
                            pass
                        else:
                            membersList.append(member.user)

                    i = 0
                    lenMembersList = len(membersList)

                    if stopProcess:
                        stopProcess = False

                    while len(membersList) > 0 and not stopProcess:
                        j = 0
                        text1 = f"{inputText}\n\n"

                        try:
                            while j < 10:
                                user = membersList.pop(0)
                                if user.username == None:
                                    text1 += f"{user.mention} "
                                    j += 1
                                else:
                                    text1 += f"@{user.username} "
                                    j += 1

                            try:
                                await Bot.send_message(message.chat.id, text1)
                            except Exception:
                                pass

                            await asyncio.sleep(10)
                            i += 10

                        except IndexError:
                            try:
                                await Bot.send_message(message.chat.id, text1)
                            except Exception:
                                pass

                            i = i + j

                    if i == lenMembersList:
                        await message.reply(f"✅ | ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴍᴇɴᴛɪᴏɴᴇᴅ **ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏꜰ {i} ᴍᴇᴍʙᴇʀꜱ.**\n❌ | ʙᴏᴛꜱ ᴀɴᴅ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ ᴡᴇʀᴇ ɪɢɴᴏʀᴇᴅ.")
                    else:
                        await message.reply(f"✅ | ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴍᴇɴᴛɪᴏɴᴇᴅ **ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏꜰ {i} ᴍᴇᴍʙᴇʀꜱ**\n❌ | ʙᴏᴛꜱ ᴀɴᴅ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ ᴡᴇʀᴇ ɪɢɴᴏʀᴇᴅ.")

                    chatQueue.remove(message.chat.id)

        else:
            await message.reply("👮🏻 | ꜱᴏʀʀʏ, **ᴏɴʟʏ ᴀᴅᴍɪɴꜱ** ᴄᴀɴ ᴇxᴇᴄᴜᴛᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.")

    except FloodWait as e:
        await asyncio.sleep(e.value)
 

@Bot.on_message(filters.command(["remove","clean"]))
async def remove(client, message):
  global stopProcess
  try: 
    try:
      sender = await Bot.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      bot = await Bot.get_chat_member(message.chat.id, "self")
      if bot.status == ChatMemberStatus.MEMBER:
        await message.reply("🕹 | ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ.")  
      else:  
        if len(chatQueue) > 5 :
          await message.reply("⛔️ | ɪ'ᴍ ᴀʟʀᴇᴀᴅʏ ᴡᴏʀᴋɪɴɢ ᴏɴ ᴍʏ ᴍᴀxɪᴍᴜᴍ ɴᴜᴍʙᴇʀ ᴏꜰ 5 ᴄʜᴀᴛꜱ ᴀᴛ ᴛʜᴇ ᴍᴏᴍᴇɴᴛ.\nᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ ꜱʜᴏʀᴛʟʏ.")
        else:  
          if message.chat.id in chatQueue:
            await message.reply("🚫 | ᴛʜᴇʀᴇ'ꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴏɴɢᴏɪɴɢ ᴘʀᴏᴄᴇꜱꜱ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ. ᴘʟᴇᴀꜱᴇ /stop ᴛᴏ ꜱᴛᴀʀᴛ ᴀ ɴᴇᴡ ᴏɴᴇ.")
          else:  
            chatQueue.append(message.chat.id)  
            deletedList = []
            async for member in Bot.get_chat_members(message.chat.id):
              if member.user.is_deleted == True:
                deletedList.append(member.user)
              else:
                pass
            lenDeletedList = len(deletedList)  
            if lenDeletedList == 0:
              await message.reply("👻 | ɴᴏ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ ᴅᴇᴛᴇᴄᴛᴇᴅ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ.")
              chatQueue.remove(message.chat.id)
            else:
              k = 0
              processTime = lenDeletedList*10
              temp = await Bot.send_message(message.chat.id, f"🚨 | ᴛᴏᴛᴀʟ ᴏꜰ {lenDeletedList} ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇᴛᴇᴄᴛᴇᴅ.\n⏳ | ᴇꜱᴛɪᴍᴀᴛᴇᴅ ᴛɪᴍᴇ : {processTime} ꜱᴇᴄᴏɴᴅꜱ ꜰʀᴏᴍ ɴᴏᴡ.")
              if stopProcess: stopProcess = False
              while len(deletedList) > 0 and not stopProcess:   
                deletedAccount = deletedList.pop(0)
                try:
                  await Bot.ban_chat_member(message.chat.id, deletedAccount.id)
                except Exception:
                  pass  
                k+=1
                await asyncio.sleep(10)
              if k == lenDeletedList:  
                await message.reply(f"✅ | ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ᴀʟʟ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ ꜰʀᴏᴍ ᴛʜɪꜱ ᴄʜᴀᴛ.")  
                await temp.delete()
              else:
                await message.reply(f"✅ | ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ {k} ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ ꜰʀᴏᴍ ᴛʜɪꜱ ᴄʜᴀᴛ.")  
                await temp.delete()  
              chatQueue.remove(message.chat.id)
    else:
      await message.reply("👮🏻 | ꜱᴏʀʀʏ, **ᴏɴʟʏ ᴀᴅᴍɪɴꜱ** ᴄᴀɴ ᴇxᴇᴄᴜᴛᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.")  
  except FloodWait as e:
    await asyncio.sleep(e.value)                               
        
@Bot.on_message(filters.command(["stop","cancel"]))
async def stop(client, message):
  global stopProcess
  try:
    try:
      sender = await Bot.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if not message.chat.id in chatQueue:
        await message.reply("🤷🏻‍♀️ | ᴛʜᴇʀᴇ ɪꜱ ɴᴏ ᴏɴɢᴏɪɴɢ ᴘʀᴏᴄᴇꜱꜱ ᴛᴏ ꜱᴛᴏᴘ.")
      else:
        stopProcess = True
        await message.reply("🛑 | ꜱᴛᴏᴘᴘᴇᴅ.")
    else:
      await message.reply("👮🏻 | ꜱᴏʀʀʏ, **ᴏɴʟʏ ᴀᴅᴍɪɴꜱ** ᴄᴀɴ ᴇxᴇᴄᴜᴛᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ.")
  except FloodWait as e:
    await asyncio.sleep(e.value)

@Bot.on_message(filters.command(["admins","staff"]))
async def admins(client, message):
  try: 
    adminList = []
    ownerList = []
    async for admin in Bot.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
      if admin.privileges.is_anonymous == False:
        if admin.user.is_bot == True:
          pass
        elif admin.status == ChatMemberStatus.OWNER:
          ownerList.append(admin.user)
        else:  
          adminList.append(admin.user)
      else:
        pass   
    lenAdminList= len(ownerList) + len(adminList)  
    text2 = f"**GROUP STAFF - {message.chat.title}**\n\n"
    try:
      owner = ownerList[0]
      if owner.username == None:
        text2 += f"👑 ᴏᴡɴᴇʀ\n└ {owner.mention}\n\n👮🏻 ᴀᴅᴍɪɴꜱ\n"
      else:
        text2 += f"👑 ᴏᴡɴᴇʀ\n└ @{owner.username}\n\n👮🏻 ᴀᴅᴍɪɴꜱ\n"
    except:
      text2 += f"👑 ᴏᴡɴᴇʀ\n└ <i>ʜɪᴅᴅᴇɴ</i>\n\n👮🏻 ᴀᴅᴍɪɴꜱ\n"
    if len(adminList) == 0:
      text2 += "└ <i>ᴀᴅᴍɪɴꜱ ᴀʀᴇ ʜɪᴅᴅᴇɴ</i>"  
      await Bot.send_message(message.chat.id, text2)   
    else:  
      while len(adminList) > 1:
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"├ {admin.mention}\n"
        else:
          text2 += f"├ @{admin.username}\n"    
      else:    
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"└ {admin.mention}\n\n"
        else:
          text2 += f"└ @{admin.username}\n\n"
      text2 += f"✅ | **ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏꜰ ᴀᴅᴍɪɴꜱ** : {lenAdminList}\n❌ | ʙᴏᴛꜱ ᴀɴᴅ ʜɪᴅᴅᴇɴ/ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴꜱ ᴡᴇʀᴇ ɪɢɴᴏʀᴇᴅ."  
      await Bot.send_message(message.chat.id, text2)           
  except FloodWait as e:
    await asyncio.sleep(e.value)       

@Bot.on_message(filters.command("bots"))
async def bots(client, message):  
  try:    
    botList = []
    async for bot in Bot.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
      botList.append(bot.user)
    lenBotList = len(botList) 
    text3  = f"**BOT LIST - {message.chat.title}**\n\n🤖 ʙᴏᴛꜱ\n"
    while len(botList) > 1:
      bot = botList.pop(0)
      text3 += f"├ @{bot.username}\n"    
    else:    
      bot = botList.pop(0)
      text3 += f"└ @{bot.username}\n\n"
      text3 += f"✅ | **ᴛᴏᴛᴀʟ ɴᴜᴍʙᴇʀ ᴏꜰ ʙᴏᴛꜱ**: {lenBotList}"  
      await Bot.send_message(message.chat.id, text3)
  except FloodWait as e:
    await asyncio.sleep(e.value)

@Bot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    text = "Hey {},\nᴍʏ ɴᴀᴍᴇ ɪꜱ **ᴍᴇɴᴛɪᴏɴ ᴀʟʟ**. ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ɢᴇᴛ ᴇᴠᴇʀʏᴏɴᴇ'ꜱ ᴀᴛᴛᴇɴᴛɪᴏɴ ʙʏ ᴍᴇɴᴛɪᴏɴɪɴɢ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ.\n\nɪ ʜᴀᴠᴇ ꜱᴏᴍᴇ ᴀᴅᴅɪᴛɪᴏɴᴀʟ ᴄᴏᴏʟ ꜰᴇᴀᴛᴜʀᴇꜱ ᴀɴᴅ ᴀʟꜱᴏ ɪ ᴄᴀɴ ᴡᴏʀᴋ ɪɴ ᴄʜᴀɴɴᴇʟꜱ.\n\nᴅᴏɴ'ᴛ ꜰᴏʀɢᴇᴛ ᴛᴏ ᴊᴏɪɴ ᴍʏ [ᴄʜᴀɴɴᴇʟ](https://telegram.me/ps_updates) ᴛᴏ ʀᴇᴄɪᴇᴠᴇ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴏɴ ᴀʟʟ ᴛʜᴇ ʟᴀᴛᴇꜱᴛ ᴜᴘᴅᴀᴛᴇꜱ.\n\nᴜꜱᴇ /help ᴛᴏ ꜰɪɴᴅ ᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀɴᴅ ᴛʜᴇ ᴜꜱᴇ ᴏꜰ ᴛʜᴇᴍ."
    user = message.from_user
    await db.add_user(client, message)                
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton("🗯 Updates Channel", url='https://t.me/TGBotsCode')
    ]])
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=text.format(user.mention), reply_markup=button)       
    else:
        await message.reply_text(text=text.format(user.mention), reply_markup=button, disable_web_page_preview=True)  


@Bot.on_message(filters.command("help"))
async def help(client, message):
  text = "ʜᴇʏ, ʟᴇᴛ'ꜱ ʜᴀᴠᴇ ᴀ Qᴜɪᴄᴋ ʟᴏᴏᴋ ᴀᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅꜱ.\n\n**ᴄᴏᴍᴍᴀɴᴅꜱ**:\n- /all <input>: <i>ᴍᴇɴᴛɪᴏɴ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ</i>\n- /remove: <i>ʀᴇᴍᴏᴠᴇ ᴀʟʟ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛꜱ.</i>\n- /admins: <i>ᴄʜᴇᴄᴋ ʟɪꜱᴛ ᴏꜰ ᴀᴅᴍɪɴꜱ/ ɢʀᴏᴜᴘ ꜱᴛᴀꜰꜰ.</i>\n- /bots: <i>ɢᴇᴛ ᴛʜᴇ ᴀʟʟ ʙᴏᴛ ʟɪꜱᴛ ᴏꜰ ᴛʜᴇ ᴄʜᴀᴛ.</i>\n- /stop: <i>ꜱᴛᴏᴘ ᴀɴ ᴏɴ ɢᴏɪɴɢ ᴘʀᴏᴄᴇꜱꜱ.</i>\n\nɪꜰ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ Qᴜᴇꜱᴛɪᴏɴꜱ ᴏɴ ʜᴏᴡ ᴛᴏ ᴜꜱᴇ ᴍᴇ, ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ᴀꜱᴋ ɪɴ ᴍʏ [ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ](https://telegram.me/ps_discuss)"
  button = InlineKeyboardMarkup([
  [
  InlineKeyboardButton("✖️ ᴄʟᴏꜱᴇ ✖️", callback_data="close")]
  ])
  await Bot.send_message(message.chat.id, text, disable_web_page_preview=True)
  
@Bot.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    if data == "close":
        try:
            await query.message.delete()
        except:
            pass  

print("Mention All is alive!")  
Bot.run()
