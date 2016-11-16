'''
Created on Nov 15, 2016

@author: vvaradarajan
'''
import  pymysql
import pymysql.cursors
import json
import sys

####### Decorator named dbReconnect ########
#Retry decorator
#Retries a database function twice and the 1st failure  results in a reconnect
def dbReconnect():
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except  Exception as inst:
                print ("DB error({0}):".format(inst))
                print ("Reconnecting")
                job.conn=None
                job.setConn()
            return function(*args, **kwargs)
        return wrapper
    return real_decorator

###### Decorator Test code below #####
class job:
    #(jobId:String,jobClass:String,jobPrams:String)
    conn=None
    @staticmethod
    def setConn():
        if job.conn != None:
            #check for dead connection
            testCursor=job.conn.cursor()
            testCursor.execute("select 1")
            rows = testCursor.fetchall()
            if len(rows) <=0:
                job.conn = None
            testCursor.close()
        if job.conn==None :
            job.conn = pymysql.connect(host='xx.xx.xx.xxx',
                                           database='jobdb',
                                           user='xxxxxxxx',
                                           password='xxxxxxxx')
        if job.conn==None:
            print('Connect to database not made - aborting!' )
            sys.exit(1)
    @staticmethod
    def getJob(jobId,jobClass,jobParams):
        job=[]
        job.append(jobId)
        job.append(jobClass)
        job.append(jobParams)
        return job
    @staticmethod 
    @dbReconnect()
    def getJobList(categ):
        #job.setConn()
        sql= "select j.jobId,j.jobClass,j.jobParams from jobs j inner join jobCategory jc " \
        + " on j.jobid=jc.jobid and jc.category='"+categ+"'"
        print(sql)
        try:
            jobList=[] #return array of jobs - each job an array of Strings
            testCursor=job.conn.cursor()
            testCursor.execute(sql)
            hdr=testCursor.description #returns an array of nm, type,etc for each column
            jobList.append(job.getJob(hdr[0][0],hdr[1][0],hdr[2][0]))
            for row in testCursor:
                print("Success")
                jobList.append(job.getJob(row[0],row[1],row[2]))
            testCursor.close()
            print("jobList length=" + str(len(jobList)))
            return jobList 
        except Exception as e:
            print(e)
            raise #reraise the exception

# getting crazy down here
jobList=job.getJobList("ProjectG")
print("jobList length=" + str(len(jobList)))
if __name__ == '__main__':
    pass