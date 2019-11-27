import sys


def removeDuplicate(array,iner=False):
    newlist = []
    if iner:
        for x in array:
            if x not in newlist:
                newlist.append(x)
    else:
        newlist = list(set(array))
    return newlist
    
class RobinsonResolve:

    def __init__(self):
        self.logicList = []
        
    def getNegative(self,logicstring):
        logic = self.getLogic(logicstring)
        newlogic = []
        for x in logic:
            if x.count('~') == 1:
                newlogic.append([x[1]])
            else:
                newlogic.append(['~' + x])
        return newlogic
        
    def getLogic(self,logicstring):
        logicstring = logicstring.replace(' ','').replace('\n','')
        logic = filter(None,logicstring.split('|'))
        return list(logic)
        
    def addLogic(self,logicstring):
        logic = self.getLogic(logicstring)
        logic = removeDuplicate(logic)
        self.logicList.append(logic)
        self.logicList = removeDuplicate(self.logicList,True)
        
    def checkNegative(self,a,b):
        #if len(a) > 1 and len(b) > 1:
        for x in a:
            if x.count('~') == 1:
                if x[1] in b:
                    return True
            else :
                if ('~' + x) in b:
                    return True
        return False
        
    def getRobinsonIndex(self,logicList):
        for i in range(0,len(logicList)-1):        
            for j in range(i+1,len(logicList)):
                if self.checkNegative(logicList[i],logicList[j]):
                    return (i,j)
                    
        return (-1,-1)
        
    def joinLogic(self,a,b):
        a=a.copy()
        b=b.copy()
        c = []
        for x in a:
            f = False
            if x.count('~') == 1:
                if x[1] in b:
                    f = True 
                    b.remove(x[1])
            else :
                if ('~' + x) in b:
                    f = True
                    b.remove('~' + x)
            if f:
                a.remove(x)
                c = a+b
                return c
                
    def testResult(self,logicList):
        for i in range(0,len(logicList)-1):
            if len(logicList[i]) == 1:
                a = logicList[i]
                for j in range(i+1,len(logicList)):
                    if len(logicList[j]) == 1:
                        b = logicList[j]
                        if a[0].count('~') == 1:
                            if a[0][1] in b:
                                return True
                        else :
                            if ('~' + a[0]) in b:
                                return True
        return False
        
    def process(self,testLogic):
        negativeTestLogic = self.getNegative(testLogic)
    
        robinlist = self.logicList.copy()
        robinlist = robinlist+ negativeTestLogic
        robinlist = removeDuplicate(robinlist,True)
        
        robinlist = sorted(robinlist,key=lambda x: len(x),reverse=True)
        
        print('PhuDinhKetQua: ',negativeTestLogic)
        print('KB: ',robinlist)
        
        if self.testResult(robinlist):
            return True


        x,y = self.getRobinsonIndex(robinlist);
        while True:
            
            if x < 0 or y < 0:
                break
                            
            logica = robinlist[x]
            logicb = robinlist[y]
            
            logicc = self.joinLogic(logica,logicb)
            
            logicc = removeDuplicate(logicc)
                        
            
            robinlist.remove(logica)
            robinlist.remove(logicb)
            robinlist.append(logicc)
            
            
            
            robinlist = removeDuplicate(robinlist,True)
            
            robinlist = sorted(robinlist,key=lambda x: len(x),reverse=True)
                        
            print ('KB: ',robinlist)
            if self.testResult(robinlist):
                return True
            
            x,y = self.getRobinsonIndex(robinlist);

        return False


if (len(sys.argv) < 3):
    print('python 1760357.py <tenfiledauvao> <tenfiledaura>')
    sys.exit(1)
    
inputfile = sys.argv[1]
outputfile = sys.argv[2]

f = open(inputfile,'r')
num = int(f.readline())

robinsonResolve = RobinsonResolve()

for i in range(num - 1):
    robinsonResolve.addLogic(f.readline())
    
result = f.readline()    
f.close()

f = open(outputfile,'w')
kq = robinsonResolve.process(result)
print(kq)
f.write(str(kq))
f.close()
