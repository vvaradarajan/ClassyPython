class jsonAlgebra:
    #This class takes a masterJson object and a list of Json Objects and performs operations and returns result.
    #The json cross reference is via the dotted location.
    #The masterJsonNM is the one that is filled from jList
    #The jlist is a {jsonNM:Jobj}
    def __init__(self,masterJsonNM,jList):
        self.masterJsonNM=masterJsonNM
        self.jList=jList
        #create a map of jList => useful in mixing
        self.jMap={j.keys()[0]:j[j.keys()[0]] for j in jList}
    def processRecursiveJsonMixer(self,jMap,mJson):
        #replace templated values in masterJson from jList and return the generated masterJson
        items=mJson.items()
        NoOfItems=len(mJson.items())
        #create a list from items to be mutable
        lItems=[{'k':k,'v':v} for k,v in items]
        i=0
        while i<NoOfItems:
            k=lItems[i]['k']
            v=lItems[i]['v']
            if isinstance(v, dict):
              self.processRecursiveJsonMixer(jMap,v)
            else:
              if isinstance(v, basestring):
                temp=v.strip()  
                if v.startswith('replace with:'):
                    temp=v[len('replace with:'):].split('.')
                    try:
                        leaf = self.jMap[temp[0]]
                    except:
                        print('*** Error in jsonMixer .. reference not found:'+ temp[0])
                        raise ValueError
                    for ptr in temp[1:]:
                        leaf=leaf[ptr]
                    mJson[k] = leaf
                    #if replaced do the process again in case of nested replaces
                    lItems[i]['v']=leaf
                    i-=1
            i+=1
        return mJson
    def mix(self): 
        self.processRecursiveJsonMixer(self.jMap,self.jMap[self.masterJsonNM])
    def processJsonUnion(self):
        #makes a json Union of the list and returns
        #In case of duplicate members the unions are in the order defined in the list
        u={}
        for j in self.jList:
            k=j.keys()[0]
            #check for any overrides
            for jk in j[k]:
                if jk in u:
                    print('Warning: ', pprint.pformat(u[jk]),' is overridden by ', pprint.pformat(j[k][jk]))
            u.update(j[k])
        return u
            
    @classmethod
    def tester(cls):
        #contains various tests of this class
        title='#1. Nested substitution test'
        j=[{'l':{'abc':'replace with:j.def'}},{'j':{'def':'replace with:k.def'}},{'k':{'def':'Kalamidu'}},{'m':{'iabc':'replace with:l.abc'}}]
        tj=jsonAlgebra('m',j)
        tj.mix()
        print(title+': Result')
        pprint.pprint(tj.jMap['m'])
        title='#2. Deep substitution test'
        j=[{'l':{'baliga':{'abc':'This is abc from l','def':'replace with:j.def'}}}
           ,{'k':{'def':'Kalamidu'}}
           ,{'j':{'def':{'abc':'This is abc from l','def':'replace with:k.def'}}}
           ,{'m':{'iabc':'replace with:l.baliga'}}]
        tj=jsonAlgebra('m',j)
        tj.mix()
        print(title+': Result')
        pprint.pprint(tj.jMap['m'])
        title='#3. Union of Json'
        j=[{'l':{'baliga':{'abc':'This is abc from l','def':'replace with:j.def'}}}
           ,{'k':{'def':'Kalamidu'}}
           ,{'j':{'def':{'abc':'This is abc from l','def':'replace with:k.def'}}}
           ,{'m':{'iabc':'replace with:l.baliga'}}]
        tj=jsonAlgebra('m',j)
        print(title+': Result')
        pprint.pprint(tj.processJsonUnion())
        

if __name__ == '__main__':
    #For processing jsonMixer
    jsonAlgebra.tester() #class methods that perform tests on the class
    exit(0)
 
