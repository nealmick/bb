### this is just a bit of code to collect datasets and make one big train data set then split that into train/test
###filter games with bad stats
import random
paths=['2019.csv','2018.csv','2018.csv','2017.csv','2016.csv','2015.csv','2014.csv','2013.csv','2012.csv','2011.csv','2010.csv','2009.csv','2008.csv','2007.csv','2006.csv', '2005.csv','2004.csv','2003.csv','2002.csv','2001.csv','2000.csv']
lines = []
#paths = ['2019.csv']
uni = []
labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']#added min

def uniCsv(path):
    csv = open(path,'r')#appending
    asdf = []
    for line in csv.readlines():
        if line.count('winner')==0:
            #print('-----------')
            #print(line)
            asdf.append(line)
    return asdf

for path in paths:
    for line in uniCsv(path):
        lines.append(line)


myset = set(lines)
mynewlist = list(myset)
stat = ''
oof = 0
asdf = []
for line in mynewlist:
    c=0
    cc=0
    for char in line:
        c+=1
        if char != ',':
            stat+=char
        else:
            cc+=1
            if cc ==2:
                print(stat)
            if cc==19 or cc==36 or cc==53 or cc==70 or cc==87 or cc==103:
                if cc ==103:
                    stat = stat[:2]
                    stat = line[-3:]
                    if stat.count(',')>=1:
                        stat = line[-2:]
                if float(stat) < 23:#minshere#------------------------------------------
                    print(float(stat),':',c,':',cc,'not so good')
                    #print(asdf[oof])
                    oof+=1
                    stat = ''
                    break
                else:
                    print(float(stat),':',c,':',cc,'good')
                    if cc ==103:
                        asdf.append(line)
                #
            stat = ''


mynewlist=asdf
def writecsv(labels, mynewlist):
    header = 'winner,gameid'
    derp = ['home_', 'visitor_']
    for foo in derp:
        for i in range(1,4):
            for label in labels:
                header+=','+foo+str(i)+'_'+label
    csv = open('ffall.csv','w')
    #csv.write(header+'\n')
    for line in asdf:
        csv.write(line)
        #print(line,'---')

writecsv(labels, mynewlist)



csv = open('ffall.csv','r')
lines = []
labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']#added min
path ='csv4/ffasdf'
for line in csv.readlines():
    lines.append(line)
lines = list(set(lines))
new = []
n = 300 ##holdout data set
for i in range(n):
    r = random.randint(1,len(lines))
    new.append(lines[r])
    del lines[r]

def writecsv(labels):
    header = 'winner,gameid'
    derp = ['home_', 'visitor_']
    for foo in derp:
        for i in range(1,4):
            for label in labels:
                header+=','+foo+str(i)+'_'+label
    return header




#----derp
header = writecsv(labels)
for i in range(n):
    asdf = path+str(i)+'.csv'
    #print(asdf)
    csv = open(asdf,'w')
    csv.write(header+'\n')
    csv.write(new[i])

#holdout data set
csv = open('ffasdf.csv','w')
csv.write(header+'\n')
for line in new:
    csv.write(line)

#all the rest of the data
csv = open('ffall.csv','w')
csv.write(header+'\n')
for line in lines:
    csv.write(line)





'''
gameids = []
for line in lines:
    gameid = ''
    for char in line[1:]:
        if char!=',':
            gameid = gameid+char
        else:
            break

'''
