import os
import xml.dom.minidom
import cv2 as cv

def detect_small(AnnoPath, data_dir, data_name):
    if AnnoPath.split('/')[-3] + '/' + AnnoPath.split('/')[-2] in [data_dir]:
        
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
        
            for index in range(len(objectlist)):
                objects = objectlist[index]

                namelist = objects.getElementsByTagName('name')
                idlist = objects.getElementsByTagName('id')
                objectname = namelist[0].childNodes[0].data
                idname = idlist[0].childNodes[0].data
                if AnnoPath.split('/')[-3] + '/' + AnnoPath.split('/')[-2] == data_dir and objectname + idname == data_name:
                    print(xmlfile + ':\t' + objectname + idname)
    
if __name__ == '__main__':
    ### This code is developed for detecting a specific target
    data_xml_dir = './data/' ## data dir
    data_dir = 'DJI_0061_2/00' ## scene name / modality name (00 for visible, 01 for thermal)
    data_name = 'cyclist6009' ## annotation name (category + id)
    xml_list = os.listdir(data_xml_dir)
    for xml_dir in xml_list:
        AnnoPath = data_xml_dir + xml_dir + '/00/'
        detect_small(AnnoPath, data_dir, data_name)
        AnnoPath = data_xml_dir + xml_dir + '/01/'
        detect_small(AnnoPath, data_dir, data_name)