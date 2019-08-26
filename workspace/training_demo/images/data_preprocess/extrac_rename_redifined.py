import tarfile
import os
import shutil
import os, glob
from xml.etree.ElementTree import ElementTree,Element  

def extract(tarfile_path, target_path):
    for tarfile_name in os.listdir(tarfile_path):
        per_file_name = tarfile_name
        tar = tarfile.open(tarfile_path + "/" + per_file_name)
        tar.extractall(target_path)
        tar.close()

def rename_and_copy(target_path, result_path):
    for label_name in os.listdir(target_path):
        old_name_1 = ''
        new_name_1 = old_name_1 + label_name
        path_1 = os.path.join(target_path, label_name)
        for camera_name in  os.listdir(path_1):
            old_name_2 = new_name_1
            new_name_2 = old_name_2 + "_" + camera_name
            path_2 = os.path.join(path_1, camera_name)
            for position_name in  os.listdir(path_2):
                old_name_3 = new_name_2
                new_name_3 = old_name_3 + "_" + position_name
                path_3 = os.path.join(path_2, position_name)
                for file_name in  os.listdir(path_3):
                    old_name_4 = new_name_3
                    new_name_4 = old_name_4 + "_" + file_name
                    shutil.copy( os.path.join(path_3, file_name), os.path.join(result_path, new_name_4))
def read_xml(in_path):  
    '''''读取并解析xml文件 
       in_path: xml路径 
       return: ElementTree'''  
    tree = ElementTree()  
    tree.parse(in_path)  
    return tree  

def write_xml(tree, out_path):  
    '''''将xml文件写出 
       tree: xml树 
       out_path: 写出路径'''  
    tree.write(out_path, encoding="utf-8",xml_declaration=True)  

def change_node_text(nodelist, text, is_add=False, is_delete=False):  
    '''''改变/增加/删除一个节点的文本 
       nodelist:节点列表 
       text : 更新后的文本'''  
    for node in nodelist:  
        if is_add:  
            node.text += text  
        elif is_delete:  
            node.text = ""  
        else:  
            node.text = text  

def rename_xml(result_path, folder_name):
    for xml_file in os.listdir(result_path):
        if xml_file.endswith('.xml'):
            print('Prossese file :',  xml_file)
            xml_path = os.path.join(result_path, xml_file)
            tree = read_xml(xml_path)  
            path_nodes = get_node_by_keyvalue(find_nodes(tree, "path"), {})
            image_path = os.path.join(result_path, xml_file.split('.')[0] + '.png')
            change_node_text(path_nodes, image_path)
            print(image_path)

            filename_nodes = get_node_by_keyvalue(find_nodes(tree, "filename"), {})
            filename = xml_file.split('.')[0] + '.png'
            change_node_text(filename_nodes, filename)
            print(filename)

            folder_nodes = get_node_by_keyvalue(find_nodes(tree, "folder"), {})
            folder = folder_name
            change_node_text(folder_nodes, folder)
            print(folder)

            write_xml(tree, os.path.join(result_path, xml_file))

def get_node_by_keyvalue(nodelist, kv_map):  
    '''''根据属性及属性值定位符合的节点，返回节点 
       nodelist: 节点列表 
       kv_map: 匹配属性及属性值map'''  
    result_nodes = []  
    for node in nodelist:  
        if if_match(node, kv_map):  
            result_nodes.append(node)  
    return result_nodes  

def find_nodes(tree, path):  
    '''''查找某个路径匹配的所有节点 
       tree: xml树 
       path: 节点路径'''  
    return tree.findall(path)  

def if_match(node, kv_map):  
    '''''判断某个节点是否包含所有传入参数属性 
       node: 节点 
       kv_map: 属性及属性值组成的map'''  
    for key in kv_map:  
        if node.get(key) != kv_map.get(key):  
            return False  
    return True  

if __name__ == "__main__":
    tarfile_path = '...' # 壓縮檔位置
    target_path = '...'        # 解壓縮資料夾存放位置
    result_path = '...'    # 重命名後存放位置
    extract(tarfile_path, target_path)
    rename_and_copy(target_path, result_path)
    rename_xml(result_path, 'train-data')
