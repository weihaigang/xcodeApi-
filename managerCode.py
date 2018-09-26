import json


import loadData
from  JsonTooc import JsonTooc,JsonToOcApi


allfilename =[]
hearderfilename = []

alldata = loadData.getdata()

apimanager = JsonToOcApi(alldata,loadData._basePath)
apimanagerurl =apimanager.start(loadData._apiClassName)

allfilename.append(loadData._basePath+'/'+apimanagerurl+'.h')
allfilename.append(loadData._basePath+'/'+apimanagerurl+'.m')

allfilename.append(loadData._apiHeaderClassName)
hearderfilename.append(loadData._basePath+'/'+apimanagerurl+'.h')

for analysisur in alldata:
    try:
        responseJson =json.loads(analysisur.responsedata)
        code = JsonTooc(analysisur.getpath())
        h,m  = code.start(responseJson, analysisur.getname())
        allfilename= allfilename+h+m
        hearderfilename=hearderfilename+h
    except:
        pass


# loadData.updateXcode(allfilename)
loadData.saveHerder(hearderfilename)


