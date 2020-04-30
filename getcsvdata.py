import os
import csv
import sys
import datetime
import facebook
import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve 
import MySQLdb as db


class readcsvintocode:

    def readcsv(filename):  # 執行讀CSV與切CSV
        
        ifile = open(filename, "r")
        reader = csv.reader(ifile, delimiter="\t")
        next(reader)  # 跳過第一行(標題行)
        rownum = 0	
        a = []

        for row in reader :
            a.append (row)
        
        ifile.close()
        return a

    def readcsv2(filename):  # 執行讀CSV與切CSV
        
        ifile = open(filename, "r",encoding="utf-8")
        reader = csv.reader(ifile, delimiter=",")
        next(reader)  # 跳過第一行(標題行)
        rownum = 0
        a = []

        for row in reader :
            a.append (row)
        
        ifile.close()
        return a

    def getSOME(wantcutarrary , needcode):  # 選則需要的資料
        
        playersome = []
        for datalength in range(len(wantcutarrary)):
            playersome.append(wantcutarrary[datalength][needcode])
        return playersome
    

class getfbdata:
    def writecontext(token, fbid):
        order = 'posts'
        limitcount = '100'
        untiltime = (str(gettoday.year)+'-' + str(gettoday.month) + '-' + str(gettoday.day))
        url = ('https://graph.facebook.com/v2.12/' + fbid + '/' + order+'?access_token=' + token+'&limit=' + limitcount + '&until=' + untiltime)
        response = requests.get(url)
        html = json.loads(response.text)
        print(html)
        writetocsv = open('d:/python/fb'+str(gettoday.year)+'-' + str(gettoday.month) + '-' + str(gettoday.day)+'.csv', 'w', encoding="utf-8")
        csv_file = csv.writer(writetocsv)

        for index in range(len(html['data'])):
            try:
                print(html['data'][index]['message'])
                writetocsv.writelines(html['data'][index]['message']+"\n")
            except:
                print('none message')
                writetocsv.writelines('none message'+"\n")
        writetocsv.close()
    
    def writealldata(token, fbid, plteam, plname):
        HOST = "localhost"
        PORT = 3306
        USER = "scott"
        PASSWORD = "scott919086"
        DB = "nba_web_crawler"
        
        gettoday = datetime.datetime.now()
        graph = facebook.GraphAPI(access_token=token, version="2.12")
        profile = graph.get_object(id=str(fbid), fields='fan_count,name,talking_about_count,posts.limit(100){id,message,shares,updated_time,likes.summary(true)}')
        # friends = graph.get_connections(id=findid,  connection_name='friends')are
        # fanfollower = getfbdata.gethtml(fbid)
        # while fanfollower == ",":
        #     fanfollower = gethtml(fbid)

        writetocsv = open('D:\\python\\coldata\\'+str(gettoday.year)+'-' + str(gettoday.month) + '-' + str(gettoday.day)+'_'+str(fbid)+'_'+'FBfan_count.csv', 'w', encoding="utf-8")
        csv_file = csv.writer(writetocsv)
        # writetocsv.writelines('team :'+"\t"+'id :'+"\t"+'name :'+"\t"+'fan_count :'+"\t"+'fan_follower :'+"\t"+'fan_talking_about_count :'+"\t"+'postid :'+"\t"+'postmessage :'+"\t"+'postupdated_time :'+"\t"+'postshare :'+"\t"+'postlikes :'+"\n")
        writetocsv.writelines('team :'+"\t"+'id :'+"\t"+'name :'+"\t"+'fan_count :'+"\t"+"\t"+'fan_talking_about_count :'+"\t"+'postid :'+"\t"+'postmessage :'+"\t"+'postupdated_time :'+"\t"+'postshare :'+"\t"+'postlikes :'+"\n")

        for index in range(len(profile['posts']['data'])):
            try:
                evedayfancount = str(fbid) + str(gettoday.year) + str(gettoday.month) + str(gettoday.day)
                postsinformationid = str(profile['posts']['data'][index]["id"]) + str(gettoday.year) + str(gettoday.month) + str(gettoday.day)
                connection = db.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)
                dbhandler = connection.cursor()
                dbhandler.execute("""INSERT INTO `posts_message`(`postsid`, `postmessage`) VALUES ('""" + str(postid) + """','""" + str(profile['posts']['data'][index]["message"]) + """')""")
                connection.commit()
                dbhandler.execute("""INSERT INTO `post_information`(`postsinformationid`, `postid`, `postupdated_time`, `postshare`, `postlikes`) VALUES ('""" + str(postsinformationid) + """','""" + str(profile['posts']['data'][index]["id"]) + """','""" + str(profile['posts']['data'][index]["updated_time"]) + """',""" + str(profile['posts']['data'][index]["shares"]['count']) + """,""" + str(profile['posts']['data'][index]["likes"]["summary"]["total_count"]) + """)""")
                connection.commit()
                dbhandler.execute("""INSERT INTO `player_data_pagedat`(`every_day_fan_count`, `fan_count`, `fan_follower`, `fan_talking_about_count`) VALUES (""" + evedayfancount + """,""" + str(profile['fan_count']) + """,""" + '' + """,""" + str(profile['talking_about_count']) + """)""")
                connection.commit()
                dbhandler.execute("""INSERT INTO `total_data`(`player_id`, `postsid`, `pageid`) VALUES ('""" + str(fbid) + """','""" + str(postsinformationid) + """',""" + evedayfancount + """)""")
                connection.commit()
                # result = list(dbhandler.fetchall())
                connection.close()
                writetocsv.writelines(plteam+"\t")
                writetocsv.writelines(str(profile['id'])+"\t")
                writetocsv.writelines(plname+"\t")
                writetocsv.writelines(str(profile['fan_count'])+"\t")
                # writetocsv.writelines(str(fanfollower)+"\t")
                writetocsv.writelines(str(profile['talking_about_count'])+"\t")
                writetocsv.writelines(str(profile['posts']['data'][index]["id"])+"\t")
                writetocsv.writelines(str(profile['posts']['data'][index]["message"])+"\t")
                writetocsv.writelines(str(profile['posts']['data'][index]["updated_time"])+"\t")
                writetocsv.writelines(str(profile['posts']['data'][index]["shares"]['count'])+"\t")
                writetocsv.writelines(str(profile['posts']['data'][index]["likes"]["summary"]["total_count"])+"\n")
            except:
                evedayfancount = str(fbid) + str(gettoday.year) + str(gettoday.month) + str(gettoday.day)
                postsinformationid = str(profile['posts']['data'][index]["id"]) + str(gettoday.year) + str(gettoday.month) + str(gettoday.day)
                connection = db.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)
                dbhandler = connection.cursor()
                dbhandler.execute("""INSERT INTO `posts_message`(`postsid`, `postmessage`) VALUES ('""" + str(postid) + """','""" + '' + """')""")
                connection.commit()
                dbhandler.execute("""INSERT INTO `post_information`(`postsinformationid`, `postid`, `postupdated_time`, `postshare`, `postlikes`) VALUES ('""" + str(postsinformationid) + """','""" + str(profile['posts']['data'][index]["id"]) + """','""" + str(profile['posts']['data'][index]["updated_time"]) + """',""" + '' + """,""" + str(profile['posts']['data'][index]["likes"]["summary"]["total_count"]) + """)""")
                connection.commit()
                dbhandler.execute("""INSERT INTO `player_data_pagedat`(`every_day_fan_count`, `fan_count`, `fan_follower`, `fan_talking_about_count`) VALUES (""" + evedayfancount + """,""" + str(profile['fan_count']) + """,""" + '' + """,""" + str(profile['talking_about_count']) + """)""")
                connection.commit()
                dbhandler.execute("""INSERT INTO `total_data`(`player_id`, `postsid`, `pageid`) VALUES ('""" + str(fbid) + """','""" + str(postsinformationid) + """',""" + evedayfancount + """)""")
                connection.commit()
                # result = list(dbhandler.fetchall())
                connection.close()
                writetocsv.writelines(plteam+"\t")
                writetocsv.writelines(str(profile['id'])+"\t")
                writetocsv.writelines(plname+"\t")
                writetocsv.writelines(str(profile['fan_count'])+"\t")
                # writetocsv.writelines(str(fanfollower)+"\t")
                writetocsv.writelines(str(profile['talking_about_count'])+"\t")
                writetocsv.writelines(str(profile['posts']['data'][index]["id"])+"\t")
                writetocsv.writelines(' '+"\t")
                writetocsv.writelines(str(profile['posts']['data'][index]["updated_time"])+"\t")
                writetocsv.writelines(' '+"\t")
                writetocsv.writelines(str(profile['posts']['data'][index]["likes"]["summary"]["total_count"])+"\n")
                
        writetocsv.close()
    
    def writealldata2(token, fbid, plteam, plname):
            HOST = "localhost"
            PORT = 3306
            USER = "scott"
            PASSWORD = "scott919086"
            DB = "entertainment_brokers_web_crawler"
            gettoday = datetime.datetime.now()
            graph = facebook.GraphAPI(access_token=token, version="2.12")
            profile = graph.get_object(id=str(fbid), fields='fan_count,name,talking_about_count,posts.limit(100){id,message,shares,updated_time,likes.summary(true)}')
            # friends = graph.get_connections(id=findid,  connection_name='friends')are
            # fanfollower = getfbdata.gethtml(fbid)
            # while fanfollower == ",":
            #     fanfollower = gethtml(fbid)

            writetocsv = open('D:\\python\\ArtistIDcoldata\\'+str(gettoday.year)+'-' + str(gettoday.month) + '-' + str(gettoday.day)+'_'+str(fbid)+'_'+'FBfan_count.csv', 'w', encoding="utf-8")
            csv_file = csv.writer(writetocsv)
            # writetocsv.writelines('team :'+"\t"+'id :'+"\t"+'name :'+"\t"+'fan_count :'+"\t"+'fan_follower :'+"\t"+'fan_talking_about_count :'+"\t"+'postid :'+"\t"+'postmessage :'+"\t"+'postupdated_time :'+"\t"+'postshare :'+"\t"+'postlikes :'+"\n")
            writetocsv.writelines('team :'+"\t"+'id :'+"\t"+'name :'+"\t"+'fan_count :'+"\t"+"\t"+'fan_talking_about_count :'+"\t"+'postid :'+"\t"+'postmessage :'+"\t"+'postupdated_time :'+"\t"+'postshare :'+"\t"+'postlikes :'+"\n")
            for index in range(len(profile['posts']['data'])):
                try:
                    evedayfancount = str(fbid) + str(gettoday.year) + str(gettoday.month) + str(gettoday.day)
                    postsinformationid = str(profile['posts']['data'][index]["id"]) + str(gettoday.year) + str(gettoday.month) + str(gettoday.day)
                    connection = db.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)
                    dbhandler = connection.cursor()
                    dbhandler.execute("""INSERT INTO `posts_message`(`postsid`, `postmessage`) VALUES ('""" + str(postid) + """','""" + str(profile['posts']['data'][index]["message"]) + """')""")
                    connection.commit()
                    dbhandler.execute("""INSERT INTO `post_information`(`postsinformationid`, `postid`, `postupdated_time`, `postshare`, `postlikes`) VALUES ('""" + str(postsinformationid) + """','""" + str(profile['posts']['data'][index]["id"]) + """','""" + str(profile['posts']['data'][index]["updated_time"]) + """',""" + str(profile['posts']['data'][index]["shares"]['count']) + """,""" + str(profile['posts']['data'][index]["likes"]["summary"]["total_count"]) + """)""")
                    connection.commit()
                    dbhandler.execute("""INSERT INTO `player_data_pagedat`(`every_day_fan_count`, `fan_count`, `fan_follower`, `fan_talking_about_count`) VALUES (""" + evedayfancount + """,""" + str(profile['fan_count']) + """,""" + '' + """,""" + str(profile['talking_about_count']) + """)""")
                    connection.commit()
                    dbhandler.execute("""INSERT INTO `total_data`(`player_id`, `postsid`, `pageid`) VALUES ('""" + str(fbid) + """','""" + str(postsinformationid) + """',""" + evedayfancount + """)""")
                    connection.commit()
                    # result = list(dbhandler.fetchall())
                    connection.close()
                    writetocsv.writelines(plteam+"\t")
                    writetocsv.writelines(str(profile['id'])+"\t")
                    writetocsv.writelines(plname+"\t")
                    writetocsv.writelines(str(profile['fan_count'])+"\t")
                    # writetocsv.writelines(str(fanfollower)+"\t")
                    writetocsv.writelines(str(profile['talking_about_count'])+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["id"])+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["message"])+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["updated_time"])+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["shares"]['count'])+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["likes"]["summary"]["total_count"])+"\n")
                except:
                    evedayfancount = str(fbid) + str(gettoday.year) + str(gettoday.month) + str(gettoday.day)
                    postsinformationid = str(profile['posts']['data'][index]["id"]) + str(gettoday.year) + str(gettoday.month) + str(gettoday.day)
                    connection = db.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)
                    dbhandler = connection.cursor()
                    dbhandler.execute("""INSERT INTO `posts_message`(`postsid`, `postmessage`) VALUES ('""" + str(postid) + """','""" + '' + """')""")
                    connection.commit()
                    dbhandler.execute("""INSERT INTO `post_information`(`postsinformationid`, `postid`, `postupdated_time`, `postshare`, `postlikes`) VALUES ('""" + str(postsinformationid) + """','""" + str(profile['posts']['data'][index]["id"]) + """','""" + str(profile['posts']['data'][index]["updated_time"]) + """',""" + '' + """,""" + str(profile['posts']['data'][index]["likes"]["summary"]["total_count"]) + """)""")
                    connection.commit()
                    dbhandler.execute("""INSERT INTO `player_data_pagedat`(`every_day_fan_count`, `fan_count`, `fan_follower`, `fan_talking_about_count`) VALUES (""" + evedayfancount + """,""" + str(profile['fan_count']) + """,""" + '' + """,""" + str(profile['talking_about_count']) + """)""")
                    connection.commit()
                    dbhandler.execute("""INSERT INTO `total_data`(`player_id`, `postsid`, `pageid`) VALUES ('""" + str(fbid) + """','""" + str(postsinformationid) + """',""" + evedayfancount + """)""")
                    connection.commit()
                    # result = list(dbhandler.fetchall())
                    connection.close()
                    writetocsv.writelines(plteam+"\t")
                    writetocsv.writelines(str(profile['id'])+"\t")
                    writetocsv.writelines(plname+"\t")
                    writetocsv.writelines(str(profile['fan_count'])+"\t")
                    # writetocsv.writelines(str(fanfollower)+"\t")
                    writetocsv.writelines(str(profile['talking_about_count'])+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["id"])+"\t")
                    writetocsv.writelines(' '+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["updated_time"])+"\t")
                    writetocsv.writelines(' '+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["likes"]["summary"]["total_count"])+"\n")

            writetocsv.close()

    def writealldata3(token, fbid, plteam, plname):
            HOST = "localhost"
            PORT = 3306
            USER = "scott"
            PASSWORD = "scott919086"
            DB = "mlb_web_crawler_1"
            gettoday = datetime.datetime.now()
            graph = facebook.GraphAPI(access_token=token, version="2.12")
            profile = graph.get_object(id=str(fbid), fields='fan_count,name,talking_about_count,posts.limit(100){id,message,shares,updated_time,likes.summary(true)}')
            # friends = graph.get_connections(id=findid,  connection_name='friends')are
            # fanfollower = getfbdata.gethtml(fbid)
            # while fanfollower == ",":
            #     fanfollower = gethtml(fbid)

            writetocsv = open('D:\\python\\mlbcoldata\\'+str(gettoday.year)+'-' + str(gettoday.month) + '-' + str(gettoday.day)+'_'+str(fbid)+'_'+'FBfan_count.csv', 'w', encoding="utf-8")
            csv_file = csv.writer(writetocsv)
            # writetocsv.writelines('team :'+"\t"+'id :'+"\t"+'name :'+"\t"+'fan_count :'+"\t"+'fan_follower :'+"\t"+'fan_talking_about_count :'+"\t"+'postid :'+"\t"+'postmessage :'+"\t"+'postupdated_time :'+"\t"+'postshare :'+"\t"+'postlikes :'+"\n")
            writetocsv.writelines('team :'+"\t"+'id :'+"\t"+'name :'+"\t"+'fan_count :'+"\t"+"\t"+'fan_talking_about_count :'+"\t"+'postid :'+"\t"+'postmessage :'+"\t"+'postupdated_time :'+"\t"+'postshare :'+"\t"+'postlikes :'+"\n")
            for index in range(len(profile['posts']['data'])):
                try:
                    evedayfancount = str(fbid) + str(gettoday.year) + str(gettoday.month) + str(gettoday.day)
                    postsinformationid = str(profile['posts']['data'][index]["id"]) + str(gettoday.year) + str(gettoday.month) + str(gettoday.day)
                    connection = db.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)
                    dbhandler = connection.cursor()
                    dbhandler.execute("""INSERT INTO `posts_message`(`postsid`, `postmessage`) VALUES ('""" + str(postid) + """','""" + str(profile['posts']['data'][index]["message"]) + """')""")
                    connection.commit()
                    dbhandler.execute("""INSERT INTO `post_information`(`postsinformationid`, `postid`, `postupdated_time`, `postshare`, `postlikes`) VALUES ('""" + str(postsinformationid) + """','""" + str(profile['posts']['data'][index]["id"]) + """','""" + str(profile['posts']['data'][index]["updated_time"]) + """',""" + str(profile['posts']['data'][index]["shares"]['count']) + """,""" + str(profile['posts']['data'][index]["likes"]["summary"]["total_count"]) + """)""")
                    connection.commit()
                    dbhandler.execute("""INSERT INTO `player_data_pagedat`(`every_day_fan_count`, `fan_count`, `fan_follower`, `fan_talking_about_count`) VALUES (""" + evedayfancount + """,""" + str(profile['fan_count']) + """,""" + '' + """,""" + str(profile['talking_about_count']) + """)""")
                    connection.commit()
                    dbhandler.execute("""INSERT INTO `total_data`(`player_id`, `postsid`, `pageid`) VALUES ('""" + str(fbid) + """','""" + str(postsinformationid) + """',""" + evedayfancount + """)""")
                    connection.commit()
                    writetocsv.writelines(plteam+"\t")
                    writetocsv.writelines(str(profile['id'])+"\t")
                    writetocsv.writelines(plname+"\t")
                    writetocsv.writelines(str(profile['fan_count'])+"\t")
                    # writetocsv.writelines(str(fanfollower)+"\t")
                    writetocsv.writelines(str(profile['talking_about_count'])+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["id"])+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["message"])+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["updated_time"])+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["shares"]['count'])+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["likes"]["summary"]["total_count"])+"\n")
                except:
                    evedayfancount = str(fbid) + str(gettoday.year) + str(gettoday.month) + str(gettoday.day)
                    postsinformationid = str(profile['posts']['data'][index]["id"]) + str(gettoday.year) + str(gettoday.month) + str(gettoday.day)
                    connection = db.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)
                    dbhandler = connection.cursor()
                    dbhandler.execute("""INSERT INTO `posts_message`(`postsid`, `postmessage`) VALUES ('""" + str(postid) + """','""" + '' + """')""")
                    connection.commit()
                    dbhandler.execute("""INSERT INTO `post_information`(`postsinformationid`, `postid`, `postupdated_time`, `postshare`, `postlikes`) VALUES ('""" + str(postsinformationid) + """','""" + str(profile['posts']['data'][index]["id"]) + """','""" + str(profile['posts']['data'][index]["updated_time"]) + """',""" + '' + """,""" + str(profile['posts']['data'][index]["likes"]["summary"]["total_count"]) + """)""")
                    connection.commit()
                    dbhandler.execute("""INSERT INTO `player_data_pagedat`(`every_day_fan_count`, `fan_count`, `fan_follower`, `fan_talking_about_count`) VALUES (""" + evedayfancount + """,""" + str(profile['fan_count']) + """,""" + '' + """,""" + str(profile['talking_about_count']) + """)""")
                    connection.commit()
                    dbhandler.execute("""INSERT INTO `total_data`(`player_id`, `postsid`, `pageid`) VALUES ('""" + str(fbid) + """','""" + str(postsinformationid) + """',""" + evedayfancount + """)""")
                    connection.commit()
                    # result = list(dbhandler.fetchall())
                    connection.close()
                    writetocsv.writelines(plteam+"\t")
                    writetocsv.writelines(str(profile['id'])+"\t")
                    writetocsv.writelines(plname+"\t")
                    writetocsv.writelines(str(profile['fan_count'])+"\t")
                    # writetocsv.writelines(str(fanfollower)+"\t")
                    writetocsv.writelines(str(profile['talking_about_count'])+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["id"])+"\t")
                    writetocsv.writelines(' '+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["updated_time"])+"\t")
                    writetocsv.writelines(' '+"\t")
                    writetocsv.writelines(str(profile['posts']['data'][index]["likes"]["summary"]["total_count"])+"\n")

            writetocsv.close()


    def gethtml(pid):

        htmlcode = requests.get("https://www.facebook.com/"+str(pid))
        soup = BeautifulSoup(htmlcode.text, 'html.parser')
        cut_1 = str(soup.find_all("div", class_="clearfix _ikh"))
        cut_2 = cut_1.split('_4bl9')
        cut_3 = cut_2[2].split(' 個人正在追蹤')
        cut_4 = cut_3[0].split('<div>')
        return cut_4[1]