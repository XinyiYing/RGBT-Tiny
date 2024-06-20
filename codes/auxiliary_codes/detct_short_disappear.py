import os
import xml.dom.minidom
import cv2 as cv
import numpy as np

def detect(AnnoPath, check_dir, f):
    Annolist = []
    Annolist1 = os.listdir(AnnoPath)
    for Anno in Annolist1:
        if Anno.split('.')[-1] == 'xml':
            Annolist.append(Anno)    
            
    if not os.path.exists(check_dir):
        os.makedirs(check_dir)
    
    storage_curr = dict()
    loc_curr = dict()
    for Anno in Annolist:
        Anno_pre, ext = os.path.splitext(Anno)
        xmlfile = AnnoPath + Anno
        imgfile = AnnoPath + Anno_pre + '.jpg'
        
        
        try:
            DOMTree = xml.dom.minidom.parse(xmlfile)
        except:
            f111 = open(xmlfile, "r")
            r = f111.read()
            text = str(r.encode('utf-8'), encoding = "utf-8")
            DOMTree = xml.dom.minidom.parseString(text)
        
        collection = DOMTree.documentElement
        
        filenamelist = collection.getElementsByTagName("filename")
        filename = filenamelist[0].childNodes[0].data
        
        objectlist = collection.getElementsByTagName("object")

        for index in range(len(objectlist)):
            objects = objectlist[index]
            namelist = objects.getElementsByTagName('name')
            idlist = objects.getElementsByTagName('id')
            objectname = namelist[0].childNodes[0].data
            idname = idlist[0].childNodes[0].data
            
            bndbox = objects.getElementsByTagName('bndbox')
            box = bndbox[0]
            x1_list = box.getElementsByTagName('xmin')
            x1 = int(x1_list[0].childNodes[0].data)
            y1_list = box.getElementsByTagName('ymin')
            y1 = int(y1_list[0].childNodes[0].data)
            x2_list = box.getElementsByTagName('xmax')
            x2 = int(x2_list[0].childNodes[0].data)
            y2_list = box.getElementsByTagName('ymax')
            y2 = int(y2_list[0].childNodes[0].data)
            
            cur_name = objectname + idname
            try:
                storage_curr[cur_name].append(int(Anno_pre))
                loc_curr[Anno_pre]=[x1, y1, x2, y2]
            except:
                storage_curr[cur_name] = []
                storage_curr[cur_name].append(int(Anno_pre))
                loc_curr[Anno_pre] = []
                loc_curr[Anno_pre]=[x1, y1, x2, y2]
                
    
    for key, values in storage_curr.items():
        for i in range(len(values)-1):
            if values[i+1] - values[i] != 1 and values[i+1] - values[i] < 10:
                print(AnnoPath + '\t' + key + '\t' + str(values[i]) + '\t' + str(values[i+1]))  
                f.write(AnnoPath + '\t' + key + '\t' + str(values[i]) + '\t' + str(values[i+1]) + '\n')
                for iii in range(values[i], values[i+1]+1):
                    imgfile = AnnoPath + str(iii).zfill(5) + '.jpg'
                    xmlfile = AnnoPath + str(iii).zfill(5) + '.xml'
                    img = cv.imread(imgfile)
                    try:
                        DOMTree = xml.dom.minidom.parse(xmlfile)
                    except:
                        f111 = open(xmlfile, "r")
                        r = f111.read()
                        text = str(r.encode('utf-8'), encoding = "utf-8")
                        DOMTree = xml.dom.minidom.parseString(text)
                    
                    collection = DOMTree.documentElement
                    
                    filenamelist = collection.getElementsByTagName("filename")
                    filename = filenamelist[0].childNodes[0].data

                    objectlist = collection.getElementsByTagName("object")

                    for index in range(len(objectlist)):
                        objects = objectlist[index]

                        namelist = objects.getElementsByTagName('name')
                        idlist = objects.getElementsByTagName('id')
                        objectname = namelist[0].childNodes[0].data
                        idname = idlist[0].childNodes[0].data
                        if objectname + idname == key:
                            bndbox = objects.getElementsByTagName('bndbox')
                            box = bndbox[0]
                            x1_list = box.getElementsByTagName('xmin')
                            x1 = int(x1_list[0].childNodes[0].data)
                            y1_list = box.getElementsByTagName('ymin')
                            y1 = int(y1_list[0].childNodes[0].data)
                            x2_list = box.getElementsByTagName('xmax')
                            x2 = int(x2_list[0].childNodes[0].data)
                            y2_list = box.getElementsByTagName('ymax')
                            y2 = int(y2_list[0].childNodes[0].data)
                            cv.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), thickness=2)
                            cv.putText(img, objectname + idname, (x1, y1), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),
                            thickness=2)
                    filename = check_dir + AnnoPath.split('/')[-3] + '_' + AnnoPath.split('/')[-2] + '_' + str(iii).zfill(5) + '.jpg'
                    cv.imwrite(filename, img)
                

if __name__ == '__main__':
    ### This code is developed for detecting short dispear annotations
    data_xml_dir = './data/'
    check_dir = './short_disappear/' 

    f = open('./short_disappear_targets.txt',"w")
    xml_list = os.listdir(data_xml_dir)
    for xml_dir in xml_list:
        AnnoPath = data_xml_dir + xml_dir + '/00/'
        detect(AnnoPath, check_dir, f)
        AnnoPath = data_xml_dir + xml_dir + '/01/'
        detect(AnnoPath, check_dir, f)
    f.close()