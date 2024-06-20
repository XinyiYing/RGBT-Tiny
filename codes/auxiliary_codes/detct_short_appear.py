import os
import xml.dom.minidom

def detect(AnnoPath, f, real_shor_appear):
    Annolist = []
    Annolist1 = os.listdir(AnnoPath)
    for Anno in Annolist1:
        if Anno.split('.')[-1] == 'xml':
            Annolist.append(Anno)    
    
    storage_curr = dict()
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
            try:
                storage_curr[cur_name] > 0
                storage_curr[cur_name] = storage_curr[cur_name] + 1
            except:
                storage_curr[cur_name] = 1
                
    for key, values in storage_curr.items():
        if values<20:
            if AnnoPath.split('/')[-3] + '/' + AnnoPath.split('/')[-2] + '/' + key in real_shor_appear:
                print('Checked:' + '\t' + xmlfile.split('/')[-3] + '/' + xmlfile.split('/')[-2] + '\t' + key + '\t times:\t' + str(values))
                continue
            print(xmlfile.split('/')[-3] + '/' + xmlfile.split('/')[-2] + '\t' + key + '\t times:\t' + str(values))
            f.write(xmlfile.split('/')[-3] + '/' + xmlfile.split('/')[-2] + '\t' + key + '\t times:\t' + str(values) + '\n')

if __name__ == '__main__':
    ### This code is developed for detecting short appear annotations
    data_xml_dir = './data/'
    real_shor_appear = []
    f = open('./short_appear_targets.txt',"w")
    xml_list = os.listdir(data_xml_dir)
    for xml_dir in xml_list:
        AnnoPath = data_xml_dir + xml_dir + '/00/'
        detect(AnnoPath, f, real_shor_appear)
        AnnoPath = data_xml_dir + xml_dir + '/01/'
        detect(AnnoPath, f, real_shor_appear)
    f.close()