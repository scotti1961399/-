import os
import sys
import csv
import re
import numpy as np
import pandas as pd
import networkx as nx
import operator
import time

class allcen:

    def greedy(file, selflo, M):
        gapminder = pd.read_csv(file)
        df = pd.DataFrame(gapminder)
        id = list(df.columns.values)
        test = dict({})
        check = []
        # print(df)
        for index in id:
            df.isin([])
            a = df[df[str(index)].isin(['NaN', 'inf', 0])]
            b = df[str(index)].isin(['NaN', 'inf', 0])
            s = 0
            ss = []
            for i in range(len(b)):
                s = s+1
                if b[i] == True:
                    ss.append(0)
                else:
                    if abs(df[str(index)][i]) > selflo:
                        ss.append(1)
                    else:
                        ss.append(0)
            test.update({index: ss})
        df1 = pd.DataFrame(test, index=id[:1319])
        # df1 = pd.DataFrame(test, index=id[:186])
        df1.drop(df1.columns[[1319]], 1, inplace=True)
        # df1.drop(df1.columns[[186]], 1, inplace=True)
        saveperson = []
        # print(list(df1.index.values))
        countM = list(df1.index.values)
        for indexaa in range(int(M)):
            countedge = []
            idaa = list(df1.columns.values)
            iden = list(df1.index.values)
            for index in idaa:  # 取得邊際數量
                aaa = pd.value_counts(df1[str(index)].values, sort=False)
                bbb = list(pd.value_counts(df1[str(index)].values, sort=False).iteritems())
                if len(aaa) == 2:
                    countedge.append(aaa[1])
                # elif bbb[0] == 1:
                #     countedge.append(aaa[1])
                else:
                    countedge.append(0)
            inlistmax = max(countedge)
            if inlistmax == 0:
                break

            firstmix = 0
            for maxm in range(len(countedge)):  # 找尋符合最大數量的人將人存起來並將位置取出
                if countedge[maxm] == inlistmax:
                    saveperson.append(idaa[maxm])
                    firstmix = maxm
                    break
                else:
                    pass
            aaaa = (df1[str(idaa[firstmix])] == 1)
            for findneedre in range(len(aaaa)):  # 刪除找到符合資格列的人
                if aaaa[findneedre] == True:
                    dropid = str(iden[findneedre])
                    df1 = df1.drop([dropid])
                else:
                    pass
            df1 = df1.drop(str(idaa[firstmix]), axis=1)
        return saveperson

    def main(filename, selpersen, M):
        tistgre = time.time()
        gretop = allcen.greedy(filename, selpersen, M)
        tiengre = time.time()
        ifile = open(filename, "r")
        reader = csv.reader(ifile, delimiter=",")
        aa = list(reader)
        allid = aa[0]
        allid.remove('')
        # print(allid)
        ifile.close()
        ifile = open(filename, "r")
        reader = csv.reader(ifile, delimiter=",")
        next(reader)
        a = []
        for row in reader:
            row.remove('')
            a.append(row)
        ifile.close()
        tist = time.time()
        G = nx.DiGraph()
        G.add_nodes_from(allid)
        for index in range(len(a)):
            for index2 in range(len(a[index])):
                if abs(float(a[index][index2])) > selpersen:
                    G.add_edge(allid[index], allid[index2])
                else:
                    pass
        tien = time.time()
        sametime = tien - tist
        tistclo = time.time()
        a = nx.closeness_centrality(G)
        tienclo = time.time()
        clospendtime = sametime + tienclo - tistclo

        tistdeg = time.time()
        a1 = nx.degree_centrality(G)
        tiendeg = time.time()
        degspendtime = sametime + tiendeg - tistdeg

        tistbet = time.time()
        a2 = nx.betweenness_centrality(G)
        tienbet = time.time()
        betspendtime = sametime + tienbet - tistbet

        tistpr = time.time()
        a3 = nx.pagerank(G)
        tienpr = time.time()
        prspendtime = sametime + tienpr - tistpr

        TopM = []
        TopM1 = []
        TopM2 = []
        TopM3 = []
        for index in range(M):
            tistclo = time.time()
            b = max(a.items(), key=operator.itemgetter(1))
            TopM.append(b[0])
            del a[b[0]]
            tienclo = time.time()
            clospendtime = clospendtime + tienclo - tistclo
            tistdeg = time.time()
            b1 = max(a1.items(), key=operator.itemgetter(1))
            TopM1.append(b[0])
            del a1[b1[0]]
            tiendeg = time.time()
            degspendtime = degspendtime + tiendeg - tistdeg
            tistbet = time.time()
            b2 = max(a2.items(), key=operator.itemgetter(1))
            TopM2.append(b[0])
            del a2[b2[0]]
            tienbet = time.time()
            betspendtime = betspendtime + tienbet - tistbet
            tistpr = time.time()
            b3 = max(a3.items(), key=operator.itemgetter(1))
            TopM3.append(b[0])
            del a3[b3[0]]
            tienpr = time.time()
            prspendtime = prspendtime + tienpr - tistpr
        print(gretop)
        print(TopM)
        print(TopM1)
        print(TopM2)
        print(TopM3)
        grespendtime = tiengre - tistgre
        return gretop, TopM, TopM1, TopM2, TopM3, grespendtime, clospendtime, degspendtime, betspendtime, prspendtime
