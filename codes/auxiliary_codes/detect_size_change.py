import os
import xml.dom.minidom
import cv2 as cv
import numpy as np

def show_img(xmlfile, key, video_check_dir):
    index_img = int(os.path.splitext(xmlfile.split('/')[-1])[0])
    for iii in range(index_img-3, index_img+3):
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
        filename = video_check_dir + AnnoPath.split('/')[-3] + '_' + AnnoPath.split('/')[-2] + '_' + str(iii).zfill(5) + '.jpg'
        cv.imwrite(filename, img)

def detect(AnnoPath, f, video_check_dir):
    
    if not os.path.exists(video_check_dir):
        os.makedirs(video_check_dir)
    Annolist = []
    Annolist1 = os.listdir(AnnoPath)
    for Anno in Annolist1:
        if Anno.split('.')[-1] == 'xml':
            Annolist.append(Anno)    

    storage_curr = None
    storage_before = None
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
            
            cur_name = objectname + idname
            storage_curr[cur_name] = np.array((x2-x1)*(y2-y1))

            if storage_before != None:
                for key, value in storage_curr.items():
                    try:
                        if objectname == 'pedestrain' and (storage_before[key] - value)/value > 1:
                            print(xmlfile + ':\t' + objectname + idname)
                            f.write(xmlfile + ':\t' + objectname + idname + '\n') 
                            show_img(xmlfile, key, video_check_dir)  
                        if objectname != 'pedestrain' and (storage_before[key] - value)/value > 1:
                            print(xmlfile + ':\t' + objectname + idname)
                            f.write(xmlfile + ':\t' + objectname + idname + '\n')
                            show_img(xmlfile, key, video_check_dir)  
                    except:
                        continue
            
        storage_before = storage_curr

if __name__ == '__main__':
    ### This code is developed for detecting annotations with large size varitions
    data_xml_dir = './data/'
    video_check_dir = './size_change/' 
    f = open('./size_change_targets.txt',"w")
    xml_list = os.listdir(data_xml_dir)
    for xml_dir in xml_list:
        AnnoPath = data_xml_dir + xml_dir + '/00/'
        detect(AnnoPath, f, video_check_dir)
        AnnoPath = data_xml_dir + xml_dir + '/01/'
        detect(AnnoPath, f, video_check_dir)
    f.close()