
### step class   
step class consist common  functions which can be inherited by other classes  -- setTaskID, setUUID,setTaskExecutionID,startRedisConn,setLogger,loadParams,connectToAPIForKey,createAndGetResponseFromURL,getLogger,exceptionTraceback,getRelativeFile

### extract class
extract class consist of init method which sets all loadParams and log files .. also contains super class startup which can be defined from client extract ..  it also consist of startWs- starting websocket connection functions .