from datetime import datetime
def repr(classname,self,args):
    ret=f"{classname}("
    for v in args.split(","):
        try:
            ret += f'{v}={eval(f"self.{v}")},'
        except:
            pass
    ret += "\b)"
    return ret
def getUnix(lst:list): return datetime(*lst).timestamp()
class load:
    class date:
        def __init__(self,y=None,M=None,d=None,day=None):
            if y!=None:
                self.day=day
                self.y=int(y)
                self.M=int(M)
                self.d=int(d)
        def fromStr(self,txt):
            self.day=txt[11:] 
            txt=txt[0:10].split(".")
            self.y=int(txt[0])
            self.M=int(txt[1])
            self.d=int(txt[2])
        def __repr__(self):
            return f"date(y={self.y},M={self.M},d={self.d},day='{self.day}')"
        def __str__(self):
            return f"{self.y}.{self.M}.{self.d} {self.day}"
    class speech:
        def __init__(self,date=None,line=None,y=None,M=None,d=None,day=None,h=None,m=None,user=None,seq=None,stamp=None):
            if date:
                self.day=date[11:] 
                date=date[0:10].split(".")
                self.y=int(date[0])
                self.M=int(date[1])
                self.d=int(date[2])
                del(date)
                self.h=int(line[0:2])
                self.m=int(line[3:5])
                line=line[6:]
                self.user=line.split(" ")[0]
                self.seq=" ".join(line.split(" ")[1:])
            else:
                self.y=y
                self.M=M
                self.d=d
                self.day=day
                self.h=h
                self.m=m
                self.user=user
                self.seq=seq
        def __str__(self):
            return f"{self.y}.{self.M}.{self.d} {self.h}:{self.m} {self.user} {self.seq}"
        def __repr__(self):
            #return f"{self.y}.{self.M}.{self.d} {self.h}:{self.m} {self.user} {self.seq}"
            return repr("speech",self,"y,M,d,day,h,m,user,seq")
    def __init__(self,text):
        todayTalk=[]
        talkList=[s for s in text.split("\n") if s != '']+["0000.00.00"]
        dates=[]
        talks=[]
        for line in talkList:
            if line[4]==".":
                Date=self.date()
                Date.fromStr(line)
                dates.append(Date)
                talks.append(todayTalk)
                todayTalk=[]
            else:
                todayTalk.append(self.speech(str(Date),line))
        dates.pop(-1)
        talks.pop(0)
        self.dates=dates
        self.talks=talks
        self.talkFr=sum(talks, [])
    def search(self,getDate:tuple=None,user:str=""):
        answer=[]
        if getDate:
            if len(getDate)!=2:
                raise TypeError("getDate argument length must be 2")
            fromUnix=getUnix(getDate[0])
            toUnix=getUnix(getDate[1])
        else:
            fromUnix=0
            toUnix=99999999999999999999999999999999999999
        for talk in self.talkFr:
            unixtime=getUnix([talk.y,talk.M,talk.d,talk.h,talk.m])
            if bool(user) and talk.user==user:
                if fromUnix<=unixtime and unixtime<=toUnix:
                    answer.append(talk)
        return answer