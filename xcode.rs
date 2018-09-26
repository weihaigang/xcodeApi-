require 'xcodeproj'

#打开项目工程A.xcodeproj
project_path =  'test1.xcodeproj'
project = Xcodeproj::Project.open(project_path)
#修改某个target在debug模式下的证书配置

targetIndex = 0

project.targets.each_with_index do |target, index|
  if target.name  == "test1"
    targetIndex = index
  end
end

target = project.targets[targetIndex]



#找到要插入的group (参数中true表示如果找不到group，就创建一个group)
group = project.main_group.find_subpath(File.join('data'),true)

#set一下sorce_tree
group.set_source_tree('SOURCE_ROOT')

#向group中增加文件引用（.h文件只需引用一下，.m引用后还需add一下）
ret = target.add_file_references([group.new_reference('data/ApiManager.h'),group.new_reference('data/ApiManager.m'),group.new_reference('ApiHeader.h'),group.new_reference('data/api/user/userInfo/Api_user_userinfo.h'),group.new_reference('data/api/user/userInfo/Api_user_userinfo_data.h'),group.new_reference('data/api/user/userInfo/Api_user_userinfo.m'),group.new_reference('data/api/user/userInfo/Api_user_userinfo_data.m'),group.new_reference('data/api/user/registered/Api_user_registered.h'),group.new_reference('data/api/user/registered/Api_user_registered.m'),group.new_reference('data/api/user/obtain/Api_user_obtain.h'),group.new_reference('data/api/user/obtain/Api_user_obtain.m'),])

project.save