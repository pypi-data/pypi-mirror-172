import os
from Step import Step
import json
import pandas as pd




class Ml(Step):
    def __init__(self):
        self.setStartTime()
        self.step = "Ml"
        self.paramsFile = 'ML.properties'
        self.logger = 'logMl'
        self.logFile = self.getRelativeFile(os.getcwd() +'\../logs/Ml.log')

    def startup(self):
        super(Ml, self).startup()
        self.taskExecutionID = None
        self.startMLSubscriber()
        
    def startMLSubscriber(self):
        self.subscriber = self.rC.pubsub()
        self.subscriber.subscribe(self.taskID + "_" + "Tr")

    def processML(self):
        for message in self.subscriber.listen():
            self.taskExecutionID = None
            print("##### process ML ####")
            if  (message.get('type') == 'message'):
                df = pd.DataFrame(eval(message.get('data')))
                # nodeID = 'abcd1234'
                nodeID = self.getNodeId()
                dataframeTojsonString = json.dumps(eval(df.iloc[0,0]))
                json_object = json.loads(dataframeTojsonString)
                self.taskExecutionID = json_object["taskExecutionID"]
                self.computeML(df)
                finalresult = { "taskExecutionID" : self.taskExecutionID , "nodeID" : nodeID, "result" : self.mlResult }
                jsonforhandoff = json.dumps(finalresult)
                print('Final result', finalresult)
                self.logInfo(self.step, json.dumps(finalresult))
                self.handOff(self.step, jsonforhandoff)
            
            self.taskExecutionID = None
            

    
    def computeML(self,msg):
        pass   
                
    def setpicklename(self,name):
        pass

    def getpicklename(self):
        pass

 


