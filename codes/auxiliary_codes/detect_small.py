import os
import xml.dom.minidom
import cv2 as cv

def detect_small(AnnoPath, f):
    Annolist = []
    Annolist1 = os.listdir(AnnoPath)
    for Anno in Annolist1:
        if Anno.split('.')[-1] == 'xml':
            Annolist.append(Anno)    
            
    for Anno in Annolist:
        Anno_pre, ext = os.path.splitext(Anno)
        xmlfile = AnnoPath + Anno
        imgfile = AnnoPath + Anno_pre + '.jpg'
        
        try:
            DOMTree = xml.dom.minidom.parse(xmlfile)
        except:
            f = open(xmlfile, "r")
            r = f.read()
            text = str(r.encode('utf-8'), encoding = "utf-8")
            DOMTree = xml.dom.minidom.parseString(text)

        collection = DOMTree.documentElement

        objectlist = collection.getElementsByTagName("object")

        img = cv.imread(imgfile)
            
        for index in range(len(objectlist)):
            objects = objectlist[index]

            namelist = objects.getElementsByTagName('name')
            idlist = objects.getElementsByTagName('id')
            objectname = namelist[0].childNodes[0].data
            idname = idlist[0].childNodes[0].data
    
            bndbox = objects.getElementsByTagName('bndbox')
            for box in bndbox:
                x1_list = box.getElementsByTagName('xmin')
                x1 = int(x1_list[0].childNodes[0].data)
                y1_list = box.getElementsByTagName('ymin')
                y1 = int(y1_list[0].childNodes[0].data)
                x2_list = box.getElementsByTagName('xmax')
                x2 = int(x2_list[0].childNodes[0].data)
                y2_list = box.getElementsByTagName('ymax')
                y2 = int(y2_list[0].childNodes[0].data)
                if (x2-x1)<3 or (y2-y1)<3:
                    print(xmlfile + ':\t' + objectname + idname)
                    f.write(xmlfile + ':\t' + objectname + idname + '\t' + str(x1) + '\t' + str(x2)+ '\t' + str(y1)+ '\t' + str(y2) +'\n')
                    cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), thickness=2)
        
if __name__ == '__main__':
    ### This code is developed for detecting too small annotations
    data_xml_dir = './data/'
    f = open('./small_targets.txt',"w")
    xml_list = os.listdir(data_xml_dir)
    for xml_dir in xml_list:
        AnnoPath = data_xml_dir + xml_dir + '/00/'
        detect_small(AnnoPath, f)
        AnnoPath = data_xml_dir + xml_dir + '/01/'
        detect_small(AnnoPath, f)
    f.close()