import os
import xml.dom.minidom

def detect(AnnoPath, f):
    Annolist = []
    Annolist1 = os.listdir(AnnoPath)
    for Anno in Annolist1:
        if Anno.split('.')[-1] == 'xml':
            Annolist.append(Anno)    

    for Anno in Annolist:
        xmlfile = AnnoPath + Anno
        
        try:
            DOMTree = xml.dom.minidom.parse(xmlfile)
        except:
            f = open(xmlfile, "r")
            r = f.read()
            text = str(r.encode('utf-8'), encoding = "utf-8")
            DOMTree = xml.dom.minidom.parseString(text)
        
        collection = DOMTree.documentElement
        
        objectlist = collection.getElementsByTagName("object")
        
        storage_curr = dict()
        for index in range(len(objectlist)):
            objects = objectlist[index]

            namelist = objects.getElementsByTagName('name')
            idlist = objects.getElementsByTagName('id')
            objectname = namelist[0].childNodes[0].data
            idname = idlist[0].childNodes[0].data
            
            cur_name = objectname + idname
            try: 
                storage_curr[cur_name] == 1
                print(xmlfile + ':\t' + objectname + idname)
                f.write(xmlfile + ':\t' + objectname + idname + '\n')
            except:
                storage_curr[cur_name] = 1

if __name__ == '__main__':
    ### This code is developed for detecting repeat annotations              
    data_xml_dir = './data/'
    f = open('./repeat_targets.txt',"w")
    xml_list = os.listdir(data_xml_dir)
    for xml_dir in xml_list:
        AnnoPath = data_xml_dir + xml_dir + '/00/'
        detect(AnnoPath,f)
        AnnoPath = data_xml_dir + xml_dir + '/01/'
        detect(AnnoPath,f)
    f.close()