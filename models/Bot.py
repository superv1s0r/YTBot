import re 
from typing import Optional
import requests
import yt_dlp
import telebot
from bs4 import BeautifulSoup
import yt_dlp
from models.sql_pkg.sqlDB import sqlDB
import models.sql_pkg.SQLrequests as SQLrequests 
import os as Command
class Bot:
    def __init__(self, botName: str, botID: str, path: str, SQL_db: sqlDB): 
        self.__botName = botName
        self.__botID = botID
        self.__path = path
        self.__Handler = telebot.TeleBot(self.botID, parse_mode=None)
        self.__SQL_db = SQL_db
        self.__channel_id = <INPUT_YOUR_CHANNEL_ID>
  
        self.createTables()



    @property
    def botName(self) -> str: 
        return self.__botName
    @botName.setter
    def botName(self, value) -> None:
        self.__botName = value
    @property
    def botID(self) -> str: 
        return self.__botID
    @botID.setter
    def botID(self, value) -> None:
        self.__botID = value
    @property
    def path(self): 
        return self.__path    
    @path.setter
    def path(self, value):
        self.__path = value
    @property
    def Handler(self): 
        return self.__Handler
    @Handler.setter
    def Handler(self, value):
        self.__botName = value
    @property
    def SQL_db(self) -> sqlDB:
        """The SQL_db property."""
        return self.__SQL_db
    @SQL_db.setter
    def SQL_db(self, value) -> None:
        self.__SQL_db = value

    @property
    def channel_id(self) -> int:
        """The channel_id property."""
        return self.__channel_id
    @channel_id.setter
    def channel_id(self, value) -> None:
        self.__channel_id = value


    def __str__(self):
        return "Bot {NAME} with Telegram ID: {ID}".format(NAME = self.botName, ID = self.botID)

    def handleLink(self, link: str):
        #By default we'll consider that we're dealing with non-YT link
        #When we found it is indeed a YT link, it'll turn to True statement
        #And we'll return it
        YTLink = False 
        yt_ID = ""
    
        #As there are two types of link patterns, one match will suffice
        HandlerType1 = re.search(r"https://([A-Za-z]+(\.[A-Za-z]+)+)/watch\?v=[A-Za-z0-9]+", link)
        HandlerType2 = re.search(r"https://[A-Za-z]+\.be/[A-Za-z0-9]+", link)

        if HandlerType1 != None and YTLink == False:
            yt_ID_Array = re.split("\?v=", link)
            yt_ID = yt_ID_Array[1]
            YTLink = True

        elif HandlerType2 != None and YTLink == False:
            
            yt_ID_Array = re.split("\.be/", link)
            yt_ID = yt_ID_Array[1]
            YTLink = True

        return YTLink, yt_ID

    def createTables(self) -> bool:

        return self.SQL_db.execute_query(SQLrequests.createTables())
    


    def DownloadSong(self, link: str) -> tuple[str|None, str|None]:

        link = f"https://youtube.com/watch?v={link}"
        pageData = requests.get(link)
        soup = BeautifulSoup(pageData.text, "html.parser")
        
        # Getting video data
        dataObtained = soup.find_all(name="title")[0]
        title = str(dataObtained)
        title = title.replace("<title>","")
        title = title.replace("</title>","")
        title = title.replace(" - YouTube","")
        title = title.replace(":", "")
        #Extracting Filesize of Video
        info = yt_dlp.YoutubeDL({}).extract_info(link, download=False)

        if info == None:
            return None, None

        if info['formats'][-1]['filesize'] != None:

            filesize = info['formats'][-1]['filesize'] / 1048576
        #If file size is superior to 500MB we're not going to download it
        else:
            filesize = 1000

        if filesize >= 500:
            return " "," "
        else:
            ydl_opts = {
                    'outtmpl': f'{self.path}{info["id"]}.%(ext)s',
                    'noplaylist': True,
                    'quiet': True,
                    'restrictfilenames': True,
                    'format': 'worstvideo[ext=mp4]+bestaudio[ext=mp3]/best',
                    'postprocessors': [{
                        'key': 'FFmpegMetadata',
                        'add_metadata': True,
                    },
                    {
                    'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '0'
                    },
                    ]
            } 
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download(link)
        return info['id'], title
   

    def InitiatingSQL(self, TeleID: str, Username: str, songTitle: str, songID: str, channelMsgID: str):
        try:
            SQL_UserCheck_query = SQLrequests.findUser(TeleID)
            SQL_UserCheck_response = self.SQL_db.read_query(SQL_UserCheck_query)

            #If user is not in our database
            if SQL_UserCheck_response == []:
                SQL_UserAdd_query = SQLrequests.addUser(TeleID, Username)
                self.SQL_db.execute_query(SQL_UserAdd_query)

            #We're gonna add Song data to the request table regardless of previous queries
            SQL_AddSong_query = SQLrequests.addSongRequest(songID, TeleID, songTitle, channelMsgID)

            self.SQL_db.execute_query(SQL_AddSong_query)

            return True
        except:
            print("Couldn't save query")
            return False
    def findSongByID(self, ytID: str):
        channel_msgID = None
        title = None
        
        SQL_SongCheck_query = SQLrequests.findSongByID(ytID)
        SQL_SongCheck_response = self.SQL_db.read_query(SQL_SongCheck_query)
        if SQL_SongCheck_response != []:
            title = SQL_SongCheck_response[0][0]
            channel_msgID = SQL_SongCheck_response[0][1]
        #print(f"TITLE: {title} AND ID: {channel_msgID}")
        #print("Couldn't execute query to find song")
        
        return title, channel_msgID

    def findSongByName(self, songName: str):
        markup = {}
        SQL_SongCheck_query = SQLrequests.findSongByName(songName)
        SQL_SongCheck_response = self.SQL_db.read_query(SQL_SongCheck_query)
        if SQL_SongCheck_response != []:
            for i in range(0, len(SQL_SongCheck_response)):
                print(SQL_SongCheck_response[i][0])
                markup[SQL_SongCheck_response[i][0]] = {"callback_data": SQL_SongCheck_response[i][1]}
        
            markup["Donate☕"] = {"url": "https://www.paypal.com/donate/?hosted_button_id=8J2VX7847ZBGQ"}
        return markupYoutube b

    def findSongByMsgID(self, channel_msgID: str):
        ytID = None
        title = None
        
        SQL_SongCheck_query = SQLrequests.findSongByMsgID(channel_msgID)
        SQL_SongCheck_response = self.SQL_db.read_query(SQL_SongCheck_query)
        if SQL_SongCheck_response != []:
            title = SQL_SongCheck_response[0][0]
            ytID = SQL_SongCheck_response[0][1]
        #print(f"TITLE: {title} AND ID: {channel_msgID}")
        #print("Couldn't execute query to find song")
        
        return title, ytID

    
    def getUserData(self, TeleID: str, first_name: str, last_name: str, url: str):
        print(f"ID:{TeleID}; Names: {first_name}, {last_name} requested {url}")

    def removeFile(self):
        try:
            Command.system(f"rm -rf {self.path}")
            return True
        except:
            return False

