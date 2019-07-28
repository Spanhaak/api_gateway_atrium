from flask import Flask, request
import os
import json
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import cx_Oracle
import keyring

## adding other stuff

import time
import datetime as dt 
import pandas as pd 
import numpy as np 
import keyring
from pandas import DataFrame

DSN = keyring.get_password("dog", "paw")

app = Flask(__name__)
api = Api(app)

class countComputerSystems(Resource):
    def get(self):
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select count(*) from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID='BMC.ASSET'")
        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))
        w = str1.replace("'" , "")
        x = w.replace(",", "")
        y = x.replace("(" , "")
        z = y.replace(")" , "")
        return (z)       
        
class listDuplicates(Resource):
    def get(self):
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select NAME from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID = 'BMC.ASSET' AND CLASSID='BMC_COMPUTERSYSTEM' and MARKASDELETED <>1 and CATEGORY <> 'Network' and ITEM <> 'Load balancer' GROUP BY NAME HAVING count(NAME) > 1")
        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))
        a = str1.replace("'" , "")
        b = a.replace("," , "\n")
        c = b.replace("(" , "")
        d = c.replace(")" , "")
        return (d)

class countComputerSystemsNSG(Resource):
    def get(self):
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select count(NAME) from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID='BMC.ASSET' AND MARKASDELETED <>1 and CATEGORY <> 'Network' and ITEM <> 'Load balancer' AND MonitoredSupportGroup is null")
        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))
        w = str1.replace("'" , "")
        x = w.replace(",", "")
        y = x.replace("(" , "")
        z = y.replace(")" , "")
        return (z)       
        
class listComputerSystemsNSG(Resource):
    def get(self):
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select NAME from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID='BMC.ASSET' AND MARKASDELETED <>1 and CATEGORY <> 'Network' and ITEM <> 'Load balancer' AND MonitoredSupportGroup is null")
        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))
        a = str1.replace("'" , "")
        b = a.replace("," , "\n")
        c = b.replace("(" , "")
        d = c.replace(")" , "")
        return (d)        

class countApplicationNSG(Resource):
    def get(self):
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select count(NAME) from ARADMIN.BMC_CORE_BMC_APPLICATION where DATASETID='BMC.ASSET' AND MARKASDELETED <>1 AND MonitoredSupportGroup is null")
        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))
        w = str1.replace("'" , "")
        x = w.replace(",", "")
        y = x.replace("(" , "")
        z = y.replace(")" , "")
        return (z)


class updateRatio(Resource):
    def get(self):
        connection = cx_Oracle.connect(DSN)
        query = """select name, modifieddate from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID='BMC.ASSET' AND MARKASDELETED <>1 and CATEGORY <> 'Network' and ITEM <> 'Load balancer'"""
        dforg = pd.read_sql_query(query, con=connection)
        df = pd.read_sql_query(query, con=connection)
        df['MODIFIEDDATE'] = pd.to_datetime(df['MODIFIEDDATE'], unit='s')
        dfnew = df[df['MODIFIEDDATE']>=(dt.datetime.now()-dt.timedelta(hours=24))]['NAME'] #hours = 6,12, 24
        count_row_modified = dfnew.shape[0]
        count_row_all = dforg.shape[0]
        percentage = count_row_modified / count_row_all *100
        percentage = round(percentage,2)
        percentage = percentage," %"
        return (percentage)   

class listApplicationCIS(Resource):
    def get(self):
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select NAME from ARADMIN.BMC_CORE_BMC_APPLICATION where DATASETID='BMC.ASSET' AND MARKASDELETED <>1")
        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))
        w = str1.replace("'" , "")
        x = w.replace("," , "\n")
        y = x.replace("(" , "")
        z = y.replace(")" , "")
        return (z)             

class countPCIDSS(Resource):
    def get(self):
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select count(*) from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID='BMC.ASSET' AND IKEA_CDE = 1 AND MARKASDELETED <>1")
        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))
        w = str1.replace("'" , "")
        x = w.replace(",", "")
        y = x.replace("(" , "")
        z = y.replace(")" , "")
        return (z)

class listPCIDSS(Resource):
    def get(self):
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select NAME from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID='BMC.ASSET' AND IKEA_CDE = 1 AND MARKASDELETED <>1")
        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))
        w = str1.replace("'" , "")
        x = w.replace("," , "\n")
        y = x.replace("(" , "")
        z = y.replace(")" , "")
        return (z)        

class countComputerSystemsMAD(Resource):
    def get(self):
        DSN = keyring.get_password("dog", "paw")
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select count(*) from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID='BMC.ASSET' AND MARKASDELETED = 1")
        mad = cur.fetchall()
        cur.execute("select count(*) from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID='BMC.ASSET'")
        ci = cur.fetchall()
        #format the output
        str1 = ''.join(map(str, mad))
        w = str1.replace("'" , "")
        x = w.replace(",", "")
        y = x.replace("(" , "")
        z = y.replace(")" , "")
        #format the output
        str2 = ''.join(map(str, ci))
        a = str2.replace("'" , "")
        b = a.replace(",", "")
        c = b.replace("(" , "")
        d = c.replace(")" , "")
        d = int(d)
        z = int(z)  
        result = z/d *100
        countComputerSystemsMAD = "Percentage ", "%.2f" % result, " Absolute ", z, " Total ", d
        return (countComputerSystemsMAD)


class listComputerSystemsMonitoredNS(Resource):
    def get(self):
        DSN = keyring.get_password("dog", "paw")
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select NAME from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID='BMC.ASSET' AND MARKASDELETED <>1 and CATEGORY <> 'Network' and ITEM <> 'Load balancer' and MONITORED =3 and NAME like 'it%'")

        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))

        w = str1.replace("'" , "")
        x = w.replace("," , "\n")
        y = x.replace("(" , "")
        k = y.replace(")" , "")
        
        return (k)  


class accadm(Resource):
    def get(self):        
        command = 'curl -X GET --header "Accept: application/json" --header "Authorization: bearer Mzo4NTY0NzgzNzQyNzAwNDFmODcyMDBhM2IzMjVjNWUyYjpBUElhY2NvdW50TWFyY286MC0zODk3YmY0MWQzNTBjOGNmNmQ3MjBmM2QyNzU3YjAzNjExOGVjODVlZjZmZDkyMTg5M2YxMjA2M2Y0ODc3YmNj" "https://itseelm-bb4252.ikea.com/api/v1.1/data/search?query=search%20BusinessApplicationInstance%20where%20name%20%3D%20%27accadm%27%20show%20name%2C%20%23AggregateSoftware%3AHostedSoftware%3AHost%3A.name%20as%20%27Hosts%27&limit=1000" -k'
        x = os.popen(command).read()
        datastore = json.loads(x)
        hosts = []
        for res in datastore: 
            list_of_results = res["results"] 
            for result in list_of_results: 
                if result[0] == "accadm": 
                    hosts = result[1]
        
        return (hosts)    

class listComputerSystemsNoRegion(Resource):
    def get(self):
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select NAME from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID = 'BMC.ASSET' AND CLASSID='BMC_COMPUTERSYSTEM' and MARKASDELETED <>1 and CATEGORY <> 'Network' and ITEM <> 'Load balancer' and REGION IS NULL")
        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))
        w = str1.replace("'" , "")
        x = w.replace(",", "\n")
        y = x.replace("(" , "")
        z = y.replace(")" , "")

        return (z)  

class countComputerSystemsNoRegion(Resource):
    def get(self):
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select count(NAME) from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID = 'BMC.ASSET' AND CLASSID='BMC_COMPUTERSYSTEM' and MARKASDELETED <>1 and CATEGORY <> 'Network' and ITEM <> 'Load balancer' and REGION IS NULL")
        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))
        w = str1.replace("'" , "")
        x = w.replace(",", "\n")
        y = x.replace("(" , "")
        z = y.replace(")" , "")

        return (z)  

class listComputerSystemsNoSite(Resource):
    def get(self):
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select NAME from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID = 'BMC.ASSET' AND CLASSID='BMC_COMPUTERSYSTEM' and MARKASDELETED <>1 and CATEGORY <> 'Network' and ITEM <> 'Load balancer' and SITE IS NULL")
        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))
        w = str1.replace("'" , "")
        x = w.replace(",", "\n")
        y = x.replace("(" , "")
        z = y.replace(")" , "")

        return (z)          

class countComputerSystemsNoSite(Resource):
    def get(self):
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select count(NAME) from ARADMIN.BMC_CORE_BMC_COMPUTERSYSTEM where DATASETID = 'BMC.ASSET' AND CLASSID='BMC_COMPUTERSYSTEM' and MARKASDELETED <>1 and CATEGORY <> 'Network' and ITEM <> 'Load balancer' and SITE IS NULL")
        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))
        w = str1.replace("'" , "")
        x = w.replace(",", "\n")
        y = x.replace("(" , "")
        z = y.replace(")" , "")

        return (z)  

class listApplicationNSG(Resource):
    def get(self):
        con = cx_Oracle.connect(DSN)
        cur = con.cursor()
        cur.execute("select NAME from ARADMIN.BMC_CORE_BMC_APPLICATION where DATASETID='BMC.ASSET' AND MARKASDELETED <>1 AND MonitoredSupportGroup is null")
        listing = cur.fetchall()
        str1 = ''.join(map(str, listing))
        w = str1.replace("'" , "")
        x = w.replace(",", "\n")
        y = x.replace("(" , "")
        z = y.replace(")" , "")

        return (z) 


api.add_resource(countComputerSystems, '/countComputerSystems') # Route_1
api.add_resource(listDuplicates, '/listDuplicates') # Route_2
api.add_resource(countComputerSystemsNSG, '/countComputerSystemsNSG') # Route_3
api.add_resource(listComputerSystemsNSG, '/listComputerSystemsNSG') # Route_4
api.add_resource(countApplicationNSG, '/countApplicationNSG') # Route_5
api.add_resource(updateRatio, '/updateRatio') # Route_6
api.add_resource(listApplicationCIS, '/listApplicationCIS') # Route_7
api.add_resource(countPCIDSS, '/countPCIDSS') # Route_8
api.add_resource(listPCIDSS, '/listPCIDSS') # Route_9
api.add_resource(countComputerSystemsMAD, '/countComputerSystemsMAD') # Route_10
api.add_resource(accadm, '/accadm') # Route_11
api.add_resource(listComputerSystemsMonitoredNS, '/listComputerSystemsMonitoredNS') # Route_12
api.add_resource(listComputerSystemsNoRegion, '/listComputerSystemsNoRegion') # Route_13
api.add_resource(countComputerSystemsNoRegion, '/countComputerSystemsNoRegion') # Route_14
api.add_resource(listComputerSystemsNoSite, '/listComputerSystemsNoSite') # Route_15
api.add_resource(countComputerSystemsNoSite, '/countComputerSystemsNoSite') # Route_16
api.add_resource(listApplicationNSG, '/listApplicationNSG') # Route_17


if __name__ == '__main__':
     app.run(port='5002')