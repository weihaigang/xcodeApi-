import json
import os
_host = '域名'


_basePath = '../xxx/xxx/Classes'

_baseXcodeproj='test1'

_apiClassName = 'ApiManager'

_apiHeaderClassName = 'ApiHeader.h'
class Analysisurl:
    pararray=[]
    url=''
    method=''
    path=[]
    responsedata=''
    urlmark = ''


    def getpath(self):
        return _basePath+'/'+ '/'.join(self.path)+'/'
    def getname(self):
        return  '_'.join(self.path).capitalize()

    def getpar(self):
        return self.pararray



def getdata():
    allData = []
    with open("apijson.json", "rb") as f:
        print("加载入文件完成...")
        jsontxt = json.load(f)

        for dic in jsontxt['item']:
            analysisur = Analysisurl()
            analysisur.url=dic['request']['url']['raw']
            if dic['request']['method'] == 'POST':
                analysisur.pararray=dic['request']['body']['formdata']
            elif dic['request']['method'] == 'GET':
                pass
            analysisur.method=dic['request']['method']
            analysisur.path=dic['request']['url']['path']
            if len(dic['response'])>0:
                analysisur.responsedata = dic['response'][0]['body']

            analysisur.urlmark = dic['name']
            allData.append(analysisur)
    return allData




def updateXcode(patharray=[]):
    rubyvlue = '['
    for path in patharray:
        rubyvlue = rubyvlue + "group.new_reference('{}'),".format(path)
    rubyvlue = rubyvlue + ']'
    with open('xcode.txt','r') as f:
        b =f.read()##values1
        b= b.replace('##values1',rubyvlue)
        b = b.replace('##values0', _basePath)
        b = b.replace('##dirpath', _baseXcodeproj)
        if os.path.exists('xcode.rs'):
            os.remove('xcode.rs')
        with open('xcode.rs','a') as f1:
            f1.write(b)
    os.system('ruby xcode.rs')


def saveHerder(headerarray:list):
    if os.path.exists(_basePath+'/'+ _apiHeaderClassName):
        os.remove(_basePath+'/'+_apiHeaderClassName)
    writeStr = ''
    for headerstr in headerarray:
        writeStr=writeStr+'#import "{}"\r\n'.format(headerstr.split('/')[-1])
    
    with open(_basePath+'/'+_apiHeaderClassName,'a') as f:
        f.write(writeStr)
