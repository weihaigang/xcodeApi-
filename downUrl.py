import json
import os
class JsonTooc:
    def __init__(self,path):
        self.dirpath =path
    def deleOldFile(self,filename):
        if os.path.exists(filename):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(filename)  # 则删除
    def addHeaderTop(self,obj,filename):
        for k,v in obj.items():
            if isinstance(v,dict) or isinstance(v,list):
                self.savetext(filename + '.h',
                              '#import "{}.h"\r\n'.format(filename.capitalize()+'_'+k))
        self.savetext(filename + '.h',
                      '#import <Foundation/Foundation.h>\r\n@interface {} : NSObject\r\n'.format(filename.capitalize()))

    def addHeaderBottom(self, filename):
        self.savetext(filename + '.h', '+ (instancetype)modelObjectWithDictionary:(NSDictionary *)dict;\r\n')
        self.savetext(filename + '.h', '- (instancetype)initWithDictionary:(NSDictionary *)dict;\r\n')
        self.savetext(filename + '.h', '- (NSDictionary *)dictionaryRepresentation;\r\n')
        self.savetext(filename + '.h', '@end\r\n')

    def start(self,obj,filename):
        self.deleOldFile(filename+'.h')
        self.addHeaderTop(obj,filename)
        self.parejsondic(obj, filename)
        self.addHeaderBottom(filename)

        self.deleOldFile(filename + '.m')
        self.addMTop(obj,filename)
        self.addMContent(obj,filename)
        self.addMBottom(obj,filename)


    def parejsondic(self,obj,fileName):
        if isinstance(obj,dict):
            for k,v in obj.items():
                self.parDicitem(k,v,fileName)


    def parDicitem(self,k,v,fileName):
        contentstr = ''
        if k=='id':
            k='identification__id'
        if isinstance(v,str):
            contentstr = '@property (nonatomic, strong) NSString *'+k+';'
        elif isinstance(v,int):
            contentstr = '@property (nonatomic, assign) NSInteger ' + k+';'
        elif isinstance(v,bool):
            contentstr = '@property (nonatomic, assign) BOOL ' + k+';'
        elif isinstance(v,float):
            contentstr = '@property (nonatomic, assign) float ' + k+';'
        elif isinstance(v,list):
            contentstr = '@property (nonatomic, strong) NSArray *' + k+';'
            fileNamearr = fileName+'_'+k

            self.deleOldFile(fileNamearr + '.h')

            self.parArray(v, fileNamearr)

        elif isinstance(v,dict):
            fileNamedic1 = fileName + '_' + k
            contentstr = '@property (nonatomic, strong){} *'.format(fileNamedic1.capitalize()) + k + ';'

            self.deleOldFile(fileNamedic1 + '.h')
            self.addHeaderTop(v,fileNamedic1)
            for k,v1 in v.items():
                self.parDicitem(k,v1,fileNamedic1)
            self.addHeaderBottom(fileNamedic1)

        self.savetext(fileName+'.h',contentstr+'\r\n')
    def parArray(self,v,fileName):
        firstobj = None
        if len(v)>0:
            firstobj = v[0]
        contentstr = ''
        if isinstance(firstobj, dict):
            self.addHeaderTop(firstobj, fileName)
            self.parejsondic(firstobj,fileName)
            self.addHeaderBottom(fileName)


    #-----------------.m
    def addMTop(self, obj,filename):
        self.savetext(filename + '.m',
                      '#import "{}.h"'.format(filename.capitalize()))
        for key in obj.keys():
            if key == 'id':
                keydub = 'identification__id'
                self.savetext(filename + '.m', '\r\nNSString *const {}_{} = @"{}";\r\n'.format(filename, keydub, key))
            else:
                self.savetext(filename + '.m','\r\nNSString *const {}_{} = @"{}";\r\n'.format(filename,key,key))
        self.savetext(filename + '.m', '@interface {} ()\r\n'.format(filename.capitalize()))
        self.savetext(filename + '.m', '- (id)objectOrNilForKey:(id)aKey fromDictionary:(NSDictionary *)dict;\r\n')
        self.savetext(filename + '.m', '@end\r\n@implementation {}'.format(filename.capitalize()))
        for key in obj.keys():
            if key == 'id':
                key = 'identification__id'
            self.savetext(filename + '.m','\r\n@synthesize {} = _{};\r\n'.format(key,key))
        self.savetext(filename + '.m', '+ (instancetype)modelObjectWithDictionary:(NSDictionary *)dict\r\n{\r\nreturn [[self alloc] initWithDictionary:dict];\r\n}\r\n')
        self.savetext(filename + '.m', '- (instancetype)initWithDictionary:(NSDictionary *)dict\r\n{')
        self.savetext(filename + '.m', '\r\n    self = [super init];\r\n')
        self.savetext(filename + '.m', '    if(self && [dict isKindOfClass:[NSDictionary class]]) {\r\n        ')
    def addMBottom(self, obj,filename):
        self.savetext(filename + '.m', '    }\r\n    return self;\r\n}\r\n')
        self.savetext(filename + '.m', '- (NSDictionary *)dictionaryRepresentation\r\n{\r\n')
        self.savetext(filename + '.m', 'NSMutableDictionary *mutableDict = [NSMutableDictionary dictionary];\r\n')
        for k,v in obj.items():
            if k == 'id':
                k = 'identification__id'
            if isinstance(v,int):
                self.savetext(filename + '.m',
                              '[mutableDict setValue:[NSNumber numberWithInteger:self.{}] forKey:{}];\r\n'.format(k,filename+'_'+k))
            elif isinstance(v,float):
                self.savetext(filename + '.m',
                              '[mutableDict setValue:[NSNumber numberWithFloat:self.{}] forKey:{}];\r\n'.
                                  format(k, filename + '_' + k))
            elif isinstance(v,bool):
                self.savetext(filename + '.m',
                              '[mutableDict setValue:[NSNumber numberWithBool:self.{}] forKey:{}];\r\n'.
                                  format(k, filename + '_' + k))
            elif isinstance(v,str):
                self.savetext(filename + '.m',
                              '[mutableDict setValue:self.{} forKey:{}];\r\n'.format
                                (k, filename + '_' + k))
            elif isinstance(v,dict):
                self.savetext(filename + '.m',
                              '[mutableDict setValue:[self.{} dictionaryRepresentation] forKey:{}];\r\n'.format
                                  (k, filename + '_' + k))
            elif isinstance(v,list):
                self.savetext(filename + '.m',
                              'NSMutableArray *mutablearray = [NSMutableArray new];\r\n')
                self.savetext(filename + '.m',
                              'for (Test_arr *obj in self.{})'.format(k))
                self.savetext(filename+'.m',' {\r\n[mutablearray addObject:[obj dictionaryRepresentation]];\r\n}')
                self.savetext(filename + '.m',
                              '[mutableDict setObject:mutablearray forKey:{}];\r\n'.format(filename + '_' + k))
        self.savetext(filename + '.m', 'return [NSDictionary dictionaryWithDictionary:mutableDict];\r\n}\r\n')
        self.savetext(filename + '.m', '- (id)objectOrNilForKey:(id)aKey fromDictionary:(NSDictionary *)dict\r\n{\r\nid object =[dict objectForKey:aKey];\r\nreturn [object isEqual:[NSNull null]] ? nil : object;\r\n}\r\n@end')
    def addMContent(self,obj,filename):
        if isinstance(obj,dict):
            for k,v in obj.items():
                key=''
                if k == 'id':
                    key = 'identification__id'
                else:
                    key=k
                if isinstance(v,int):
                    self.savetext(filename + '.m', 'self.{} = [[self objectOrNilForKey:{} fromDictionary:dict] integerValue];\r\n'.format(key,filename+'_'+key))
                elif isinstance(v,float):
                    self.savetext(filename + '.m','self.{} = [[self objectOrNilForKey:{} fromDictionary:dict] floatValue];\r\n'.format(key, filename + '_' + key))
                elif isinstance(v,bool):
                    self.savetext(filename + '.m','self.{} = [[self objectOrNilForKey:{} fromDictionary:dict] boolValue];\r\n'.format(key, filename + '_' + key))
                elif isinstance(v,str):
                    self.savetext(filename + '.m',
                                  'self.{} = [self objectOrNilForKey:{} fromDictionary:dict];\r\n'.format(
                                      key, filename + '_' + key))
                elif isinstance(v,list):
                    self.savetext(filename + '.m', '        NSObject *receivedarray = [dict objectForKey:{}];\r\n'.format(filename+'_'+key))
                    self.savetext(filename + '.m',
                                  '        NSMutableArray *parsedarray = [NSMutableArray array];\r\n')
                    self.savetext(filename + '.m',
                                  '        if ([receivedarray isKindOfClass:[NSArray class]]) {\r\n')
                    self.savetext(filename + '.m',
                                  '            for (NSDictionary *item in (NSArray *)receivedarray) {\r\n')
                    self.savetext(filename + '.m',
                                  '                if ([item isKindOfClass:[NSDictionary class]]) {\r\n')
                    self.savetext(filename + '.m',
                                  '                    [parsedarray addObject:[{} modelObjectWithDictionary:item]];'.format(filename.capitalize()+'_'+key))


                    self.savetext(filename+'.m','\r\n                }\r\n            }\r\n')
                    self.savetext(filename+'.m','            self.{} = [NSArray arrayWithArray:parsedarray];'.format(key))
                    self.savetext(filename+'.m','        }')

                    filenamearray = filename+"_"+k

                    self.parMArray(v, filenamearray)


                elif isinstance(v,dict):
                    fileNamedic1 = filename + '_' + k
                    self.savetext(filename + '.m',
                                  'self.{} =[{} modelObjectWithDictionary:[self objectOrNilForKey:{} fromDictionary:dict]];\r\n'.format(
                                      key, fileNamedic1.capitalize(), fileNamedic1))
                    self.deleOldFile(fileNamedic1 + '.m')
                    self.addMTop(v,fileNamedic1)
                    self.addMContent(v, fileNamedic1)
                    self.addMBottom(v,fileNamedic1)


    def parMArray(self,v,fileName):
        firstobj = None
        if len(v)>0:
            firstobj = v[0]
        contentstr = ''
        if isinstance(firstobj, dict):
            self.deleOldFile(fileName + '.m')
            self.addMTop(firstobj, fileName)
            self.addMContent(firstobj,fileName)
            self.addMBottom(firstobj, fileName)
    def savetext(self,filename,text):
        with open(self.dirpath+filename.capitalize(),'a') as file:
            file.write(text)



j = '{"id":7, "arr":[{"aa":1}],"dic":{"zz":222}}'
dic = json.loads(j)
code = JsonTooc('./')

filename = 'test'
code.start(dic,filename)


