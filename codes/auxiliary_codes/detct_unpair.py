import os
import xml.dom.minidom

def detect(AnnoPath):
    Annolist = []
    Annolist1 = os.listdir(AnnoPath)
    for Anno in Annolist1:
        if Anno.split('.')[-1] == 'xml':
            Annolist.append(Anno)    
    
    storage_curr = []
    for Anno in Annolist:
        xmlfile = AnnoPath + Anno
        
        try:
            DOMTree = xml.dom.minidom.parse(xmlfile)
        except:
            f111 = open(xmlfile, "r")
            r = f111.read()
            text = str(r.encode('utf-8'), encoding = "utf-8")
            DOMTree = xml.dom.minidom.parseString(text)
        
        collection = DOMTree.documentElement
        
        objectlist = collection.getElementsByTagName("object")

        for index in range(len(objectlist)):
            objects = objectlist[index]

            namelist = objects.getElementsByTagName('name')
            idlist = objects.getElementsByTagName('id')
            objectname = namelist[0].childNodes[0].data
            idname = idlist[0].childNodes[0].data
            
            cur_name = objectname + idname
            storage_curr.append(cur_name)   
            
    return storage_curr

if __name__ == '__main__':
    ### This code is developed for detecting unpaired RBGT annotations
    ### data_xml_dir: data dir that is consistent with pubilc datasets
    ### --------------------------------------
    ## DJI_0022_1
        ## 00 
            ## 00000.xml
            ## 00001.xml
            ## ...
        ## 01 
            ## 00000.xml
            ## 00001.xml
            ## ...
    ## ...
    ## DJI_0024_2
    ## -----------------------------
    data_xml_dir = './data/' 
    real_Nexist = []
    f = open('./IR_RGB_Npaired.txt',"w")
    xml_list = os.listdir(data_xml_dir)
    for xml_dir in xml_list:
        AnnoPath = data_xml_dir + xml_dir + '/00/'
        target_list_00 = detect(AnnoPath)
        AnnoPath = data_xml_dir + xml_dir + '/01/'
        target_list_01 = detect(AnnoPath)
        for target_00 in target_list_00:
            if target_00 in target_list_01:
                ffffffff = 1
            else:
                if AnnoPath.split('/')[-3] + '/' + AnnoPath.split('/')[-2] + '/' + target_00 in real_Nexist:
                    print('Checked:' + '\t' + AnnoPath + '\t 01 not exsit:\t' + target_00)
                    continue
                print(AnnoPath + '\t 01 not exsit:\t' + target_00)
                f.write(AnnoPath + '\t 01 not exsit:\t' + target_00 + '\n')
        for target_01 in target_list_01:
            if target_01 in target_list_00:
                ffffffff = 1
            else:
                if AnnoPath.split('/')[-3] + '/' + AnnoPath.split('/')[-2] + '/' + target_01 in real_Nexist:
                    print('Checked:' + '\t' + AnnoPath + '\t 01 not exsit:\t' + target_01)
                    continue
                print(AnnoPath + '\t 00 not exsit:\t' + target_01)
                f.write(AnnoPath + '\t 00 not exsit:\t' + target_01 + '\n')
    f.close()
