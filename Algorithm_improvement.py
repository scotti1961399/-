import os
import sys
import csv
import re
import numpy as np
import pandas as pd
import networkx as nx
import operator
import time
from sklearn import cluster
from collections import Counter


class personandjaccard:
    
    def compute_jaccard_index(set_1, set_2):
        n = len(set_1.intersection(set_2))
        return n / float(len(set_1) + len(set_2) - n)

    def personmath(topmallid, alldatadict, allid):
        allscore = 0
        for index in topmallid:
            perscore = 0
            for index2 in allid:  # b
                a1 = list(map(float, alldatadict[index]))
                a2 = list(map(float, alldatadict[index2]))
                # if a2.count(0) == 1319:
                # if a2.count(0) == 186:
                if a2.count(0) == 28:
                # if a2.count(0) == 47:
                    score = 0
                    perscore = float(perscore) + float(score)
                else:
                    score = np.corrcoef([a1, a2])
                    score = np.corrcoef([a1, a2])
                    perscore = float(perscore) + float(score[0][1])
            allscore = allscore + (perscore/int(len(allid)))  # b
        anser = allscore/float(len(topmallid))
        return anser

path = r'J:\python\enword'  # 文件夹目录
# path = r'J:\python\NBAfn\fn100'  # 文件夹目录
os.chdir(path)
os.getcwd()

os.listdir(path)
fileadderss = []
writetocsv = open(r'J:\jornalUSE\othercluster\ENWORDNEWAgglomerativeClustering ward 812-1.csv', 'w', encoding="utf-8")
# writetocsv = open(r'J:\jornalUSE\othercluster\NBAFNAgglomerativeClustering ward 812-1.csv', 'w', encoding="utf-8")
csv_file = csv.writer(writetocsv)
for i in os.listdir(path):  # 全部的檔案名稱
    fileadderss.append(str(i))

ifile = open(r'J:\jornalUSE\alldayscore\enalliserscore.csv', "r")
# ifile = open(r'J:\jornalUSE\alldayscore\NBAalluserscore.csv', "r")
reader = csv.reader(ifile, delimiter=",")
aa = list(reader)
allid = aa[0]
allid.remove('')
# print(allid)
# print(len(allid))
ifile.close()
ifile = open(r'J:\jornalUSE\alldayscore\enalliserscore.csv', "r")
# ifile = open(r'J:\jornalUSE\alldayscore\NBAalluserscore.csv', "r")
reader = csv.reader(ifile, delimiter=",")
next(reader)

dictallsec = dict({})
gggg = list(reader)
# print(len(gggg[0]),len(allid))
# os.system("pause")
for row in range(len(gggg[0])-1):
    onerow = []
    for row1 in range(len(gggg)):
        onerow.append(float(gggg[row1][row]))
    dictallsec.update({str(allid[row]): np.float_(onerow)})
    # print(dictallsec[allid[row]])
    # os.system("pause")

ifile.close()


for address in fileadderss:
    filename = address
    ifile = open(filename, "r")
    reader = csv.reader(ifile, delimiter=",")
    aa = list(reader)
    allid = aa[0]
    allid.remove('')
    # print(allid)
    # print(len(allid))
    ifile.close()
    ifile = open(filename, "r")
    reader = csv.reader(ifile, delimiter=",")
    next(reader)
    a = []
    dictall = dict({})
    for row in reader:
        row.remove('')
        try:
            inf = row.index("inf")
        except ValueError:
            inf = None
        if inf != None:
            row[inf] = '0'
        a.append(row)

    ifile.close()
    # print(type(a[0][0]))
    a = list(np.float_(a))
    # matrixmax = np.matrix(a)
    # print(matrixmax.max())
    # print(a)
    # tist1 = time.time()
    # hrv = matrixmax.max()
    # tien1 = time.time()
    # os.system("pause")
    # for M in range(5, 30, 5):#研究主要程式
    #     count = 50
    #     while 1:
    #         dicmax = dict({})
    #         pers = round(count * 0.1, 1)
    #         tist = time.time()
    #         for index in range(len(allid)):
    #             # turnflo = list(map(float, a[index]))
    #             # maxv =  max(turnflo)
    #             suml = 0
    #             ii = 0
    #             # for i in turnflo:
    #             for i in a[index]:
    #                 if i > pers:
    #                     ii = ii + 1
    #                     suml = suml + i
    #             # dictall.update({str(allid[index]): turnflo})
    #             if ii == 0:
    #                 suml = 0
    #             else:
    #                 suml = suml / ii
    #             dictall.update({str(allid[index]): a[index]})
    #             dicmax.update({str(allid[index]): suml})
    #         key_max = []
    #         # print(dicmax)
    #         # os.system("pause")
    #         for index in range(M):
    #             maxm = max(dicmax, key=(lambda k: dicmax[k]))
    #             key_max.append(maxm)
    #             del dicmax[maxm]
    #         tien = time.time()
    #         print(key_max, tien-tist)

    #         # print(dictall) 
    #         getanser = personandjaccard.personmath(key_max, dictall, allid)
    #         print(address, getanser, M)
    #         writetocsv.writelines(str(address) + ',' + str(M) + ',' + str(pers) + ',' + str((tien-tist)+(tien1-tist1)) + ',')
    #         writetocsv.writelines(str(getanser))
    #         for i in key_max:
    #             writetocsv.writelines(',' + str(i))
    #         writetocsv.writelines('\n')
    #         if count == 15:
    #             break
    #         count = count - 5

    # for M in range(5, 30, 5):
    #     count = 10
    #     while 1:
    #         tist = time.time()
    #         pers = round(count * 0.1, 1)
    #         tist = time.time()
    #         for index in range(len(allid)):
    #             turnflo = list(map(float, a[index]))
    #             suml = 0
    #             for i in turnflo:
    #                 if i <= pers:
    #                     suml = suml + i
    #             dictall.update({str(allid[index]): turnflo})
    #             dicmax.update({str(allid[index]): suml})
    #         key_max = []
    #         for index in range(M):
    #             maxm = max(dicmax.keys(), key=(lambda k: dicmax[k]))
    #             key_max.append(maxm)
    #             del dicmax[maxm]

    #         tien = time.time()
    #         print(key_max, tien-tist)
    #         # print(dictall) 
    #         getanser = personandjaccard.personmath(key_max, dictall, allid)
    #         print(address, getanser, M)
    #         writetocsv.writelines(str(address) + ',' + str(M) + ',' + str(pers) + ',' + str(tien-tist) + ',')
    #         writetocsv.writelines(str(getanser))
    #         for i in key_max:
    #             writetocsv.writelines(',' + str(i))
    #         writetocsv.writelines('\n')
    #         if count == 0:
    #             break
    #         count = count - 2
    
    # for M in range(5, 30, 5):
    #     tist = time.time()
    #     for index in range(len(allid)):
    #         turnflo = list(map(float,a[index]))
    #         suml = sum(turnflo)
    #         dictall.update({str(allid[index]): turnflo})
    #         dicmax.update({str(allid[index]): suml})
    #     key_max = []
    #     for index in range(M):
    #         maxm = max(dicmax.keys(), key=(lambda k: dicmax[k]))
    #         key_max.append(maxm)
    #         del dicmax[maxm]
    #     tien = time.time()
    #     print(key_max, tien-tist)
        

    #     # print(dictall) 
    #     getanser = personandjaccard.personmath(key_max, dictall, allid)
    #     print(address, getanser, M)
    #     writetocsv.writelines(str(address) + ',' + str(M) + ',')
    #     writetocsv.writelines(str(getanser))
    #     for i in key_max:
    #         writetocsv.writelines(',' + str(i))
    #     writetocsv.writelines('\n')



        # os.system("pause")
    # for M in range(5, 41, 5): # Kmeans
    #     # for K in range(1, 26, 1):
    #     # for K in range(1, 6, 1):
    #     for K in range(1, 11, 2): # 研究用
    #         print(M, K, sep =" ")
    #         # findM = K * M 
    #         findM = K
    #         ts = time.time() # time start 1
    #         # if findM > 186:
    #         if findM > 1319:
    #         # if findM > 10: # Jotnal 10 person
    #             break
    #         for index in range(len(allid)):
    #             dictall.update({str(allid[index]): a[index]})
    #         kmeans_fit = cluster.KMeans(n_clusters=findM).fit(a)
            
    #         cluster_labels = kmeans_fit.labels_
    #         aa = list(cluster_labels)
    #         # print(aa)
    #         bb = Counter(aa)
    #         allclustername = []
    #         getalcnindex = dict({})
    #         for i in bb:
    #             allclustername.append(i)
    #             getalcnindex.update({i: []})
    #         for i in range(len(aa)):
    #             getalcnindex[aa[i]].append(i)
    #         # print(getalcnindex[allclustername[0]])
    #         topM = []
    #         count = 60
    #         te = time.time()
    #         firsttime = te - ts
    #         while 1:
    #             ts = time.time() # time start 2
    #             pers = round(count * 0.1, 1)
    #             for i in range(findM):
    #                 G = nx.DiGraph()
    #                 G.add_nodes_from(allid)
    #                 for index in range(len(getalcnindex[allclustername[0]])):
    #                     for index2 in range(len(a[index])):
    #                         if abs(float(a[getalcnindex[allclustername[0]][index]][index2])) > pers:
    #                             G.add_edge(allid[index2], allid[getalcnindex[allclustername[0]][index]])
    #                         else:
    #                             pass
    #                 # print(G)
    #                 j = nx.degree_centrality(G)
    #                 # print(j)
    #                 for index in range(M):
    #                     b = max(j.items(), key=operator.itemgetter(1))
    #                     topM.append(b[0])
    #                     del j[b[0]]
    #             G.clear()
    #             # topM = list(set(topM))

    #             COUNT = Counter(topM)
    #             # print(M)
    #             bb = dict({})
    #             allkey = list(COUNT.keys())
    #             allvalue = list(COUNT.values())
    #             for i in range(len(allkey)):
    #                 bb.update({allkey[i]: allvalue[i]})
    #             aa = sorted(bb.items(), key=operator.itemgetter(1), reverse=True)
    #             # print(bb)
    #             # print(aa[0][0])
    #             gettopM = [] # time end
    #             te = time.time() # time start 2
    #             scecondtime = te - ts
    #             for index in range(M):
    #                 gettopM.append(aa[index][0])
    #             # print(getalcnindex)
    #             getanser = personandjaccard.personmath(gettopM, dictallsec, allid)
    #             # print(getanser)
    #             writetocsv.writelines(str(address) + ',' + str(M) + ',' + str(K) + ',')
    #             writetocsv.writelines(str(findM) + ',' + str(scecondtime + firsttime)+',' +str(pers) + ',')
    #             writetocsv.writelines(str(getanser))
    #             for i in gettopM:
    #                 writetocsv.writelines(',' + str(i))
    #             writetocsv.writelines('\n')
    #             count = count - 5
    #             if count == 0:
    #                 break

    for M in range(1, 21, 1): # AgglomerativeClustering
        # for K in range(1, 26, 1):
        # for K in range(1, 6, 1):
        for K in range(1, 11): # 研究用
            print(M, K, sep =" ")
            # findM = K * M 
            findM = K
            ts = time.time() # time start 1
            # if findM > 186:
            if findM > 1319:
            # if findM > 10: # Jotnal 10 person
                break
            for index in range(len(allid)):
                dictall.update({str(allid[index]): a[index]})
            kmeans_fit = cluster.AgglomerativeClustering(n_clusters=findM).fit(a)
            cluster_labels = kmeans_fit.labels_
            aa = list(cluster_labels)
            # print(aa)
            bb = Counter(aa)
            allclustername = []
            getalcnindex = dict({})
            for i in bb:
                allclustername.append(i)
                getalcnindex.update({i: []})
            for i in range(len(aa)):
                getalcnindex[aa[i]].append(i)
            # print(getalcnindex[allclustername[0]])
            topM = []
            count = 60
            te = time.time()
            firsttime = te - ts
            while 1:
                ts = time.time() # time start 2
                pers = round(count * 0.1, 1)
                for i in range(findM):
                    G = nx.DiGraph()
                    G.add_nodes_from(allid)
                    for index in range(len(getalcnindex[allclustername[0]])):
                        for index2 in range(len(a[index])):
                            if abs(float(a[getalcnindex[allclustername[0]][index]][index2])) > pers:
                                G.add_edge(allid[index2], allid[getalcnindex[allclustername[0]][index]])
                            else:
                                pass
                    # print(G)
                    j = nx.degree_centrality(G)
                    # print(j)
                    for index in range(M):
                        b = max(j.items(), key=operator.itemgetter(1))
                        topM.append(b[0])
                        del j[b[0]]
                G.clear()
                # topM = list(set(topM))

                COUNT = Counter(topM)
                # print(M)
                bb = dict({})
                allkey = list(COUNT.keys())
                allvalue = list(COUNT.values())
                for i in range(len(allkey)):
                    bb.update({allkey[i]: allvalue[i]})
                aa = sorted(bb.items(), key=operator.itemgetter(1), reverse=True)
                # print(bb)
                # print(aa[0][0])
                gettopM = [] # time end
                te = time.time() # time start 2
                scecondtime = te - ts
                for index in range(M):
                    gettopM.append(aa[index][0])
                # print(getalcnindex)
                getanser = personandjaccard.personmath(gettopM, dictallsec, allid)
                # print(getanser)
                writetocsv.writelines(str(address) + ',' + str(M) + ',' + str(K) + ',')
                writetocsv.writelines(str(findM) + ',' + str(scecondtime + firsttime)+',' +str(pers) + ',')
                writetocsv.writelines(str(getanser))
                for i in gettopM:
                    writetocsv.writelines(',' + str(i))
                writetocsv.writelines('\n')
                count = count - 5
                if count == 0:
                    break

    # for M in range(1, 21, 1): # MeanShift
    #     # for K in range(1, 26, 1):
    #     # for K in range(1, 6, 1):
    #     for K in range(1, 2): # 研究用
    #         print(M, K, sep =" ")
    #         # findM = K * M 
    #         findM = K
    #         ts = time.time() # time start 1
    #         if findM > 186:
    #         # if findM > 1319:
    #         # if findM > 10: # Jotnal 10 person
    #             break
    #         for index in range(len(allid)):
    #             dictall.update({str(allid[index]): a[index]})
    #         kmeans_fit = cluster.AffinityPropagation().fit(a)
               
    #         cluster_labels = kmeans_fit.labels_
    #         aa = list(cluster_labels)
    #         # print(aa)
    #         bb = Counter(aa)
    #         allclustername = []
    #         getalcnindex = dict({})
    #         for i in bb:
    #             allclustername.append(i)
    #             getalcnindex.update({i: []})
    #         for i in range(len(aa)):
    #             getalcnindex[aa[i]].append(i)
    #         # print(getalcnindex[allclustername[0]])
    #         topM = []
    #         count = 60
    #         te = time.time()
    #         firsttime = te - ts
    #         while 1:
    #             ts = time.time() # time start 2
    #             pers = round(count * 0.1, 1)
    #             for i in range(len(bb)):
    #                 G = nx.DiGraph()
    #                 G.add_nodes_from(allid)
    #                 for index in range(len(getalcnindex[allclustername[0]])):
    #                     for index2 in range(len(a[index])):
    #                         if abs(float(a[getalcnindex[allclustername[0]][index]][index2])) > pers:
    #                             G.add_edge(allid[index2], allid[getalcnindex[allclustername[0]][index]])
    #                         else:
    #                             pass
    #                 # print(G)
    #                 j = nx.degree_centrality(G)
    #                 # print(j)
    #                 for index in range(M):
    #                     b = max(j.items(), key=operator.itemgetter(1))
    #                     topM.append(b[0])
    #                     del j[b[0]]
    #             G.clear()
    #             # topM = list(set(topM))

    #             COUNT = Counter(topM)
    #             # print(M)
    #             bb = dict({})
    #             allkey = list(COUNT.keys())
    #             allvalue = list(COUNT.values())
    #             for i in range(len(allkey)):
    #                 bb.update({allkey[i]: allvalue[i]})
    #             aa = sorted(bb.items(), key=operator.itemgetter(1), reverse=True)
    #             # print(bb)
    #             # print(aa[0][0])
    #             gettopM = [] # time end
    #             te = time.time() # time start 2
    #             scecondtime = te - ts
    #             for index in range(M):
    #                 gettopM.append(aa[index][0])
    #             # print(getalcnindex)
    #             getanser = personandjaccard.personmath(gettopM, dictallsec, allid)
    #             # print(getanser)
    #             writetocsv.writelines(str(address) + ',' + str(M) + ',' + str(len(bb)) + ',')
    #             writetocsv.writelines(str(findM) + ',' + str(scecondtime + firsttime)+',' +str(pers) + ',')
    #             writetocsv.writelines(str(getanser))
    #             for i in gettopM:
    #                 writetocsv.writelines(',' + str(i))
    #             writetocsv.writelines('\n')
    #             count = count - 5
    #             if count == 0:
    #                 break

writetocsv.close()
# M = 5