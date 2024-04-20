#from telebot.util import quick_markup

#User status: 0 - privileged; 1 - normal; 2 - banned;
from models.Bot import Bot
from models.sql_pkg.sqlDB import sqlDB

name = str(input("Name of the bot:"))
token = str(input("Token of the bot:"))
path = str(input("Path where you wanna temporarily save music:"))

print("SQL:")
host = str(input("host(put localhost if it is local):"))
username = str(input("username:"))
password = str(input("password:"))




UniqueBot = Bot(name,token, path, sqlDB(host, username, password, "ytbot"))

print(UniqueBot.__str__())
@UniqueBot.Handler.message_handler(commands=['start', 'help'])
def send_welcome(message):
    UniqueBot.Handler.reply_to(message, f"""Hello, {message.from_user.first_name}! \nI will help you find music from Youtube. \n<b>My advantages:</b> \n -Fast\n -Send music instantly if it was uploaded into <a href='t.me/uniqueYTbotMusic'>my channel</a>\n -Highest quality\n -Metadata(Including Thumbnail, Author, etc) \n \n If you find any issue using this bot, <a href='t.me/superv1sor'>contact me</a>
                               \nKeep in mind, this is only <b>beta version</b>.Have Fun :)""", parse_mode="HTML")

@UniqueBot.Handler.message_handler(regexp="^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$")
def handle_link(message):
    UniqueBot.getUserData(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.text)

    ytLink, ytID = UniqueBot.handleLink(message.text)
    
    if ytLink != True:
        UniqueBot.Handler.reply_to(message, f"Please, send me Youtube Link. I don't download from any other website\n{message.text} <b>is not a YouTube link</b>", parse_mode="HTML")

    else:
        title, channelMsgID = UniqueBot.findSongByID(ytID)
        
        if channelMsgID != None:
            UniqueBot.Handler.forward_message(message.chat.id, UniqueBot.channel_id, channelMsgID) #Forwarding pre-downloaded audio
            UniqueBot.InitiatingSQL(message.from_user.id, message.from_user.username, title, ytID, None) #Adding request to SQL table
        else:
            #Filename contains video_id(example: d3bUq_cX31) -> We'll use it to find/name our audio file. But title will be scraped from youtube page and will be contained in metadata;
            filename, title = UniqueBot.DownloadSong(ytID)
            if title != None:
                try: 
                    audio = open(f'{UniqueBot.path}{filename}.mp3', "rb")
                    print(audio)
                    channelMsgID = UniqueBot.Handler.send_audio(UniqueBot.channel_id, audio, caption=f"<a href='https://youtu.be/{ytID}'>link</a> | <a href='t.me/UniqueYTBot'>via UniqueBot</a>", parse_mode="HTML", title = title)
                    
                    #We must open file two times, otherwise an error will be thrown, telling audio is an Empty-File; Might change later to just forward this message;
                    audio = open(f'{UniqueBot.path}{filename}.mp3', "rb")
                    UniqueBot.Handler.send_audio(message.chat.id, audio, title=title, caption=f"<a href='https://youtu.be/{ytID}'>link</a> | <a href='t.me/UniqueYTBot'>via UniqueBot</a>", parse_mode="HTML")
                 
                    #Saving our request into SQL database
                    UniqueBot.InitiatingSQL(message.from_user.id, message.from_user.username, title, ytID, channelMsgID.message_id)
                    UniqueBot.removeFile()
                except:
                    #Some unexpected errors might be thrown, let's just skip
                    pass
            else:
                #If the size is larger than >= 500MB
                UniqueBot.Handler.reply_to(message, "Video/Audio Size is too large")

@UniqueBot.Handler.message_handler(content_types=["text"])
def handle_message(message):
    songName = message.text
    UniqueBot.getUserData(message.from_user.id, message.from_user.first_name, message.from_user.last_name, songName)

    markup_layout = UniqueBot.findSongByName(songName)
    if markup_layout != {}:
        qck_markup = quick_markup(markup_layout, row_width=1)
        UniqueBot.Handler.reply_to(message, "<b>Here are some results:</b>", parse_mode="HTML", reply_markup=qck_markup)
    else:
        UniqueBot.Handler.reply_to(message, "Couldn't find any pre-downloaded song :(\n\nPlease try to download it passing YT link")

@UniqueBot.Handler.callback_query_handler(func=lambda call: True)
def handle_request(call):
    channel_msg_id = call.data
    title, ytID = UniqueBot.findSongByMsgID(channel_msg_id)
    if title != None and ytID != None:
        UniqueBot.Handler.forward_message(call.message.chat.id, UniqueBot.channel_id, channel_msg_id) #Forwarding pre-downloaded audio
        UniqueBot.InitiatingSQL(call.from_user.id, call.from_user.username, title, ytID, None) #Adding request to SQL table
    else:
        UniqueBot.Handler.send_message(call.message.chat.id, "Couldn't load the audio :( ")
 


UniqueBot.Handler.infinity_polling()
