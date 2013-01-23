from music21 import *
from music21.qrs import basic, algo
import numpy.random as np



a = []

for i in ['c','d','e','f']:
    a.append(i)#basic.CreateNote(Type=0,Pitch=i,Volume=127,QuarterLength=1))

b = []

for i in ['g','g','g','g']:
    b.append(i)#basic.CreateNote(Type=0,Pitch=i,Volume=127,QuarterLength=1))


L1 = {}
L1['A'] = a
L1['b'] = b

seq = []
seq = ['A','A','A','A','A']

Rep = []
Rep = [1,1,4,1,1,]




def CreateSong(Input,Sequence,Repeat):

    OutPut = [[]]
    s = []
    s2 = []
    s3 = []

    for index, (part, num) in enumerate(zip(Sequence,Repeat),start=1):
        s = Input[part]*num
        s2.append(s)
        s3.append(index)

    OutPut = [Sequence,s3,s2]

    return OutPut

Song = CreateSong(Input=L1,Sequence=seq,Repeat=Rep)

#print Song

##test = Song

#Extend array
##for x,y in enumerate(Song):
##    Song[x].extend(y)

#add to array
##Song = zip(Song,test)

##for x in test:
##    for y in x:
##        for z in y:
##            print z

##print Song

##for x, y in zip(Song[0], Song[1]):
##    print x,y



##def AddSongLayer(Base,Section,Bar,Input,Sequence):
##
##    OutPut = [[]]
##    T = []
##    T2 = []
##    s = []
##    s2 = []
##    s3 = []
##
##    for part, part2, num in [(x,y,z) for x in Sequence for y in Section for z in Bar]:
##        print part,part2,num
##        for x, y in zip(Song[0], Song[1]):
##            print x,y
##            if x == part2 and y == num:
##                s = Input[part]
##                s2.append(s)
##                T.append(y)
##                T2.append(part)
####            else:
####                s = 'R'
##
####        s2.append(s)
####        print s2
##
##    OutPut = [T2,T,s2]
##    return OutPut
##
##
##woop = AddSongLayer(Base=Song,Section=['b'],Bar=[2],Input=L1,Sequence=['b'])
##
##print woop





def AddSongLayer2(Base,Section,Bar,Input,Sequence):

    BaseCopy = Base
    t1=[]
    t2=[]
    t3=[]
    for aa in BaseCopy[0]:
        t1.append(aa)
    for aa in BaseCopy[1]:
        t2.append(aa)
    for aa in BaseCopy[2]:
        t3.append(aa)


    if len(Bar) == 0:

        for part, part2 in [(x,y) for x in Sequence for y in Section]:
            #print part,part2
            for a, (b,c,d) in enumerate(zip(BaseCopy[0], BaseCopy[1], BaseCopy[2])):
                #print a,b,c,d
                if b == part2:
                    #print 'modify'
                    t1[a] = part
                    t3[a] = Input[part]*(len(t3[a])/len(Input[part]))
                    #print t1,t2,t3
                    BaseCopy = [t1,t2,t3]
                else:
                    t1[a] = 'R'
                    t3[a] = ['R' for ii in range(len(t3[a]))]
                    #print t1,t2,t3
                    BaseCopy = [t1,t2,t3]

    else:

        for part, part2, num in [(x,y,z) for x in Sequence for y in Section for z in Bar]:
            #print part,part2,num
            for a, (b,c,d) in enumerate(zip(BaseCopy[0], BaseCopy[1], BaseCopy[2])):
                #print a,b,c,d
                if b == part2 and c == num:
                    #print 'modify'
                    t1[a] = part
                    t2[a] = num
                    t3[a] = Input[part]*(len(t3[a])/len(Input[part]))
                    #print t1,t2,t3
                    BaseCopy = [t1,t2,t3]
                else:
                    t1[a] = 'R'
                    t3[a] = ['R' for ii in range(len(t3[a]))]
                    #print t1,t2,t3
                    BaseCopy = [t1,t2,t3]

    return BaseCopy


woop2 = AddSongLayer2(Base=Song,Section=['A'],Bar=[5],Input=L1,Sequence=['b'])

print Song
print woop2

final=[]
for aa in Song[2]:
    for bb in aa:
        final.append(basic.CreateNote(Type=0,Pitch=bb,Volume=127,QuarterLength=1))


final2=[]
for aa in woop2[2]:
    for bb in aa:
        if bb == 'R':
            final2.append(basic.CreateNote(Type=4,QuarterLength=1))
        else:
            final2.append(basic.CreateNote(Type=0,Pitch=bb,Volume=127,QuarterLength=1))

m1 = basic.CreateMeasure(4,4,120)
m2 = basic.CreateMeasure(4,4,120)
m1.append(final)
m2.append(final2)

p1 = basic.CreatePart(0,0)
p2 = basic.CreatePart(0,10)
p1.append(m1)
p2.append(m2)

Cancion = basic.CreateScore()
Cancion.insert(p1)
Cancion.insert(p2)

#Cancion.show('text')
Cancion.show('midi')





