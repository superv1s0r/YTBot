def addSongRequest(ytID: str, TeleID: int, songName: str, ChannelMsgID):
    if ChannelMsgID != None:
        return """
        INSERT INTO request (video_id, songName, TeleID, channel_msg_id)
        VALUES ("{YT_ID}", "{SONG_NAME}", {Tele_ID}, {ChannelMsgID} );""".format(YT_ID=ytID, Tele_ID=TeleID, SONG_NAME=songName, ChannelMsgID = ChannelMsgID)
    else:
        return """
        INSERT INTO request (video_id, songName, TeleID)
        VALUES ("{YT_ID}", "{SONG_NAME}", {Tele_ID});""".format(YT_ID=ytID, Tele_ID=TeleID, SONG_NAME=songName)

def findSongByID(ytID: str):
    return f"""
    SELECT songName, channel_msg_id FROM request WHERE video_id = "{ytID}" AND channel_msg_id != 'NULL';"""

def findSongByName(songName: str):
    return f"""
    SELECT songName, channel_msg_id from request WHERE songName LIKE '%{songName}%' AND channel_msg_id != 'NULL';"""

def findSongByMsgID(channel_msg_id: str):
    return f"""
    SELECT songName, channel_msg_id FROM request WHERE channel_msg_id = {channel_msg_id};""" 


def addUser(TeleID, Username):
    return """
    INSERT INTO user (TeleID, Username, Preference) VALUES ({TELEID}, "{USERNAME}", "");""".format(TELEID=TeleID, USERNAME=Username)
    
def findUser(TeleID):
    return """
    SELECT * FROM user WHERE TeleID = {TELEID}""".format(TELEID=TeleID)
     
def updateUserInfo(TeleID, Username, Preference):
    return """
    UPDATE user Username = '{USERNAME}', Preference = '{PREFERENCE}' WHERE TeleID = {TELEID}""".format(USERNAME=Username, PREFERENCE=Preference, TELEID=TeleID)
    
   
def createTables():
    return """
    CREATE TABLE request (video_id PRIMARY KEY NOT NULL VARCHAR(50), sognName VARCHAR(50), TeleID INT, channel_msg_id INT);
    CREATE TABLE user (TeleID PRIMARY KEY NOT NULL INT, Username VARCHAR(50) NOT NULL, Preference VARCHAR(50));
    """ 