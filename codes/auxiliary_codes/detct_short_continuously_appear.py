import os
import xml.dom.minidom

def detect(AnnoPath, f):
    Annolist = []
    Annolist1 = os.listdir(AnnoPath)
    for Anno in Annolist1:
        if Anno.split('.')[-1] == 'xml':
            Annolist.append(Anno)    
    
    storage_curr = dict()
    for Anno in Annolist:
        Anno_pre, ext = os.path.splitext(Anno)
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
            try:
                storage_curr[cur_name].append(int(Anno_pre))
            except:
                storage_curr[cur_name] = []
                storage_curr[cur_name].append(int(Anno_pre))
    
    for key, values in storage_curr.items():
        cot = 0
        for i in range(len(values)-1):
            if values[i+1] - values[i] == 1:
                cot = cot + 1
            else:
                if cot < 10:
                  print(AnnoPath + '\t' + key + '\t' + str(values[i]))  
                  f.write(AnnoPath + '\t' + key + '\t' + str(values[i]) + '\n')
                cot = 0

if __name__ == '__main__':
    ### This code is developed for detecting short continuously appear annotations
    data_xml_dir = './data/'
    f = open('./shrort_continuously_appear_targets.txt',"w")
    xml_list = os.listdir(data_xml_dir)
    for xml_dir in xml_list:
        AnnoPath = data_xml_dir + xml_dir + '/00/'
        detect(AnnoPath, f)
        AnnoPath = data_xml_dir + xml_dir + '/01/'
        detect(AnnoPath, f)
    f.close()