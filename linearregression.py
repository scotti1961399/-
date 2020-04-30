import os
import sys
import MySQLdb as db
import re
import csv
import itertools
from pandas import DataFrame
from sklearn import linear_model
import statsmodels.api as sm


class regression:
    def connectscoredb():
        HOST = "localhost"
        PORT = 3306
        USER = "scott"
        PASSWORD = "scott919086"
        DB = "text_score"
        connection = db.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)
        connection.set_character_set('utf8')
        dbhandler = connection.cursor()
        return connection, dbhandler

    def connectiddb(seldb):
        HOST = "localhost"
        PORT = 3306
        USER = "scott"
        PASSWORD = "scott919086"
        if seldb == 0:
            DB = "nba_web_crawler"
        elif seldb == 1:
            DB = "entertainment_brokers_web_crawler"
        connection = db.Connection(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB)
        connection.set_character_set('utf8')
        dbhandler = connection.cursor()
        return connection, dbhandler
    
    def getallid(dbhandler):
        dbhandler.execute("""SELECT `id` FROM `player_data`""")
        result = dbhandler.fetchall()
        playerid = []
        for index in range(len(result)):
            playerid.append(result[index][0])
        return playerid
    
    def gettenid(dbhandler):
        dbhandler.execute("""SELECT `id` FROM `player_data`  LIMIT 10 """)
        result = dbhandler.fetchall()
        playerid = []
        for index in range(len(result)):
            playerid.append(result[index][0])
        return playerid

    def getselplayerscore(dbhandler, id, selta):
        if selta == 0:
            dbhandler.execute(""" SELECT * FROM `nbausereverydaywordscore` 
            WHERE `user` LIKE '{0}_%' 
            and `writeday` >= '2018-5-17' ORDER BY `writeday` DESC """.format(str(id)))
        elif selta == 1:
            dbhandler.execute(""" SELECT * FROM `usereverydaywordscore` 
            WHERE `user` LIKE '{0}_%' 
            and `writeday` >= '2018-6-4' ORDER BY `writeday` DESC """.format(str(id)))
        result = dbhandler.fetchall()
        # print(len(result))
        playerscore = [[], [], []]
        if len(result) != 0:
            for index in range(len(result)):
                playerscore[0].append(id)
                playerscore[1].append(result[index][1].strftime("%Y-%m-%d"))
                playerscore[2].append(result[index][2])
            return playerscore
        else:
            playerscore = None
            return playerscore
    
    def makeuserlist(sel, havedata, id):
        year = 2018
        month = 7
        day = 2
        returnlist1 = [[], [], []]  # is not hava first data(7/2)
        returnlist2 = [[], [], []]  # is not hava last data(5/14,6/4)
        if sel == 0 and havedata != None:  # NBA
            reindex = 0
            while True:
                if month == 5 and day == 16:
                    break
                if day < 1 and month == 7:
                    day = 30
                    month = month-1
                elif day < 1 and month == 6:
                    day = 31
                    month = month-1
                if day < 10:
                    daystr = str(year) + '-0' + str(month) + '-0' + str(day)
                else:
                    daystr = str(year) + '-0' + str(month) + '-' + str(day)
                if daystr not in havedata[1]:
                    if daystr == '2018-07-02':
                        returnlist1[0].append(id)
                        returnlist1[1].append(daystr)
                        returnlist1[2].append(0)
                    elif daystr == '2018-05-17':
                        returnlist2[0].append(id)
                        returnlist2[1].append(daystr)
                        returnlist2[2].append(0)
                    else:
                        returnlist1[0].append(id)
                        returnlist1[1].append(daystr)
                        returnlist1[2].append(0)
                        returnlist2[0].append(id)
                        returnlist2[1].append(daystr)
                        returnlist2[2].append(0)
                else:
                    if daystr == '2018-07-02':
                        returnlist1[0].append(havedata[0][reindex])
                        returnlist1[1].append(havedata[1][reindex])
                        returnlist1[2].append(havedata[2][reindex])
                        reindex = reindex + 1
                    elif daystr == '2018-05-17':
                        returnlist2[0].append(havedata[0][reindex])
                        returnlist2[1].append(havedata[1][reindex])
                        returnlist2[2].append(havedata[2][reindex])
                        reindex = reindex + 1
                    else:
                        returnlist1[0].append(havedata[0][reindex])
                        returnlist1[1].append(havedata[1][reindex])
                        returnlist1[2].append(havedata[2][reindex])
                        returnlist2[0].append(havedata[0][reindex])
                        returnlist2[1].append(havedata[1][reindex])
                        returnlist2[2].append(havedata[2][reindex])
                        reindex = reindex + 1
                day = day-1
        elif sel == 1 and havedata != None:
            reindex = 0
            while True:
                if month == 6 and day == 3:
                    break
                if day < 1 and month == 7:
                    day = 30
                    month = int(month) - 1
                if day < 10:
                    daystr = str(year) + '-0' + str(month) + '-0' + str(day)
                else:
                    daystr = str(year) + '-0' + str(month) + '-' + str(day)
                dodool = False
                # os.system("pause")
                for index in havedata[1]:
                    if str(index) ==  str(daystr):
                        dodool = True
                        break
                    else:
                        pass
                if dodool != True:
                    if daystr == '2018-07-02':
                        returnlist1[0].append(id)
                        returnlist1[1].append(daystr)
                        returnlist1[2].append(0)
                    elif daystr == '2018-06-04':
                        returnlist2[0].append(id)
                        returnlist2[1].append(daystr)
                        returnlist2[2].append(0)
                    else:
                        returnlist1[0].append(id)
                        returnlist1[1].append(daystr)
                        returnlist1[2].append(0)
                        returnlist2[0].append(id)
                        returnlist2[1].append(daystr)
                        returnlist2[2].append(0)
                elif dodool == True:
                    if daystr == '2018-07-02':
                        returnlist1[0].append(havedata[0][reindex])
                        returnlist1[1].append(havedata[1][reindex])
                        returnlist1[2].append(havedata[2][reindex])
                        reindex = reindex + 1
                    elif daystr == '2018-06-04':
                        returnlist2[0].append(havedata[0][reindex])
                        returnlist2[1].append(havedata[1][reindex])
                        returnlist2[2].append(havedata[2][reindex])
                        reindex = reindex + 1
                    else:
                        returnlist1[0].append(havedata[0][reindex])
                        returnlist1[1].append(havedata[1][reindex])
                        returnlist1[2].append(havedata[2][reindex])
                        returnlist2[0].append(havedata[0][reindex])
                        returnlist2[1].append(havedata[1][reindex])
                        returnlist2[2].append(havedata[2][reindex])
                        reindex = reindex + 1
                day = day-1
        else:
            if sel == 0:
                for index in range(47):
                    returnlist1[0].append(0)
                    returnlist2[0].append(0)
                    returnlist1[1].append(0)
                    returnlist2[1].append(0)
                    returnlist1[2].append(0)
                    returnlist2[2].append(0)
            else:
                for index in range(28):
                    returnlist1[0].append(0)
                    returnlist2[0].append(0)
                    returnlist1[1].append(0)
                    returnlist2[1].append(0)
                    returnlist1[2].append(0)
                    returnlist2[2].append(0)
        # print(returnlist1)

        return returnlist1, returnlist2
    
    def makeXY(nofirst, nolast, id, allid):
        y = dict({})
        x = dict({})
        creatneedidlist = []
        y.update({id: nolast[id]})
        for ids in allid:
            if ids == id:
                x.update({id: nofirst[id]})
                creatneedidlist.append(ids)
            else:
                x.update({ids: nolast[ids]})
                creatneedidlist.append(ids)
        return y, x, creatneedidlist

    def selpostshareandlike(id, dbhandler):
        year = 2018
        month = 6
        day = 4
        playershare = []
        playerlike = []
        while 1:
            if month == 6 and day == 30:
                daystr = str(year) + str(month) + str(day)
                dbhandler.execute("""SELECT
                SUM(`postshare`),SUM(`postlikes`)
                FROM
                `post_information`
                WHERE
                `postupdated_time` >= '2018-6-4' 
                AND `postsinformationid` LIKE '{0}_%{1}'""".format(str(id), str(daystr)))
                result = dbhandler.fetchall()
                if result[0][0] != None:
                    for index in range(len(result)):
                        playershare.append(int(result[index][0]))
                        playerlike.append(int(result[index][1]))
                else:
                    playershare.append(0)
                    playerlike.append(0)
                month = month + 1
                day = 1
            else:
                daystr = str(year) + str(month) + str(day)
                dbhandler.execute("""SELECT
                SUM(`postshare`),SUM(`postlikes`)
                FROM
                `post_information`
                WHERE
                `postupdated_time` >= '2018-6-4' 
                AND `postsinformationid` LIKE '{0}_%{1}'""".format(str(id), str(daystr)))
                result = dbhandler.fetchall()
                if result[0][0] != None:
                    for index in range(len(result)):
                        playershare.append(int(result[index][0]))
                        playerlike.append(int(result[index][1]))
                else:
                    playershare.append(0)
                    playerlike.append(0)
                day = day + 1
            if month == 7 and day == 3:
                break
        for index in range(1, len(playershare)):
            if playershare[index-1] != 0 and playershare[index] == 0:
                playershare[index] = playershare[index-1]
            else:
                pass
        for index in range(1, len(playerlike)):
            if playerlike[index-1] != 0 and playerlike[index] == 0:
                playerlike[index] = playerlike[index-1]
            else:
                pass
        # playershare = playershare.reverse()
        # playerlike = playerlike.reverse()
        return playershare[::-1], playerlike[::-1]

    def NBAselpostshareandlike(id, dbhandler):
        year = 2018
        month = 5
        day = 17
        playershare = []
        playerlike = []
        while 1:
            if month == 6 and day == 30:
                daystr = str(year) + str(month) + str(day)
                dbhandler.execute("""SELECT
                SUM(`postshare`),SUM(`postlikes`)
                FROM
                `post_information`
                WHERE
                `postupdated_time` >= '2018-5-17' 
                AND `postsinformationid` LIKE '{0}_%{1}'""".format(str(id), str(daystr)))
                result = dbhandler.fetchall()
                if result[0][0] != None:
                    for index in range(len(result)):
                        playershare.append(int(result[index][0]))
                        playerlike.append(int(result[index][1]))
                else:
                    playershare.append(0)
                    playerlike.append(0)
                month = month + 1
                day = 1
            elif month == 5 and day == 31:
                daystr = str(year) + str(month) + str(day)
                dbhandler.execute("""SELECT
                SUM(`postshare`),SUM(`postlikes`)
                FROM
                `post_information`
                WHERE
                `postupdated_time` >= '2018-5-17' 
                AND `postsinformationid` LIKE '{0}_%{1}'""".format(str(id), str(daystr)))
                result = dbhandler.fetchall()
                if result[0][0] != None:
                    for index in range(len(result)):
                        playershare.append(int(result[index][0]))
                        playerlike.append(int(result[index][1]))
                else:
                    playershare.append(0)
                    playerlike.append(0)
                month = month + 1
                day = 1
            else:
                daystr = str(year) + str(month) + str(day)
                dbhandler.execute("""SELECT
                SUM(`postshare`),SUM(`postlikes`)
                FROM
                `post_information`
                WHERE
                `postupdated_time` >= '2018-5-17' 
                AND `postsinformationid` LIKE '{0}_%{1}'""".format(str(id), str(daystr)))
                result = dbhandler.fetchall()
                if result[0][0] != None:
                    for index in range(len(result)):
                        playershare.append(int(result[index][0]))
                        playerlike.append(int(result[index][1]))
                else:
                    playershare.append(0)
                    playerlike.append(0)
                day = day + 1
            if month == 7 and day == 3:
                break
        for index in range(1, len(playershare)):
            if playershare[index-1] != 0 and playershare[index] == 0:
                playershare[index] = playershare[index-1]
            else:
                pass
        for index in range(1, len(playerlike)):
            if playerlike[index-1] != 0 and playerlike[index] == 0:
                playerlike[index] = playerlike[index-1]
            else:
                pass
        # playershare = playershare.reverse()
        # playerlike = playerlike.reverse()
        return playershare[::-1], playerlike[::-1]
    
    def selpagelikeandtalk(id, dbhandler):
        dbhandler.execute("""
        SELECT `fan_count`,`fan_talking_about_count`
        FROM `player_data_pagedat`
        WHERE `every_day_fan_count`
        LIKE '{0}%' ORDER BY `coldatatime` DESC""".format(id))
        result = dbhandler.fetchall()
        pagefancount = []
        pagefantalk = []
        if len(result) != 0:
            for index in range(len(result)):
                pagefancount.append(int(result[index][0]))
                pagefantalk.append(int(result[index][1]))
        else:
            pagefancount.append(0)
            pagefantalk.append(0)
        if len(pagefancount) < 29:
            while len(pagefancount) < 29:
                pagefancount.append(pagefancount[len(pagefancount)-1])
            while len(pagefantalk) < 29:
                pagefantalk.append(pagefantalk[len(pagefantalk)-1])
        return pagefancount, pagefantalk

    def NBAselpagelikeandtalk(id, dbhandler):
        dbhandler.execute("""
        SELECT `fan_count`,`fan_talking_about_count`
        FROM `player_data_pagedat`
        WHERE `every_day_fan_count`
        LIKE '{0}%' ORDER BY `coldatatime` DESC""".format(id))
        result = dbhandler.fetchall()
        pagefancount = []
        pagefantalk = []
        if len(result) != 0:
            for index in range(len(result)):
                pagefancount.append(int(result[index][0]))
                pagefantalk.append(int(result[index][1]))
        else:
            pagefancount.append(0)
            pagefantalk.append(0)
        if len(pagefancount) < 47:
            while len(pagefancount) < 47:
                pagefancount.append(pagefancount[len(pagefancount)-1])
            while len(pagefantalk) < 47:
                pagefantalk.append(pagefantalk[len(pagefantalk)-1])
        return pagefancount, pagefantalk
