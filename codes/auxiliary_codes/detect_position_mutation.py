import os
import xml.dom.minidom
import cv2 as cv
import numpy as np

def detect(AnnoPath, f, video_check_dir):
    Annolist = []
    Annolist1 = os.listdir(AnnoPath)
    for Anno in Annolist1:
        if Anno.split('.')[-1] == 'xml':
            Annolist.append(Anno)    

    if not os.path.exists(video_check_dir):
        os.makedirs(video_check_dir)
        
    storage_curr = None
    storage_before = None
    for i in range(len(Annolist)):
        Anno = Annolist[i]
        Anno_pre, ext = os.path.splitext(Anno)
        xmlfile = AnnoPath + Anno
        imgfile = AnnoPath + Anno_pre + '.jpg'
        
        try:
            Anno1 = Annolist[i-1]
        except:
            Anno1 = Annolist[i]
        Anno_pre1, ext = os.path.splitext(Anno1)
        imgfile1 = AnnoPath + Anno_pre1 + '.jpg'
        xmlfile1 = AnnoPath + Anno_pre1 + '.xml'  
        
        try:
            DOMTree = xml.dom.minidom.parse(xmlfile)
            DOMTree1 = xml.dom.minidom.parse(xmlfile1)
        except:
            f = open(xmlfile, "r")
            r = f.read()
            text = str(r.encode('utf-8'), encoding = "utf-8")
            DOMTree = xml.dom.minidom.parseString(text)
            f1 = open(xmlfile1, "r")
            r1 = f1.read()
            text1 = str(r1.encode('utf-8'), encoding = "utf-8")
            DOMTree1 = xml.dom.minidom.parseString(text1)
        
        collection = DOMTree.documentElement
        collection1 = DOMTree1.documentElement
        
        filenamelist = collection.getElementsByTagName("filename")
        filename = filenamelist[0].childNodes[0].data
        
        objectlist = collection.getElementsByTagName("object")
        objectlist1 = collection1.getElementsByTagName("object")

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
            storage_curr[cur_name] = np.array([(x1+x2)/2, (y1+y2)/2])

            if storage_before != None:
                for key, value in storage_curr.items():
                    try:
                        storage_before[key]
                        if np.sum(np.square(storage_before[key] - value)) >100:
                            print(xmlfile + ':\t' + objectname + idname)
                            f.write(xmlfile + ':\t' + str(i) + '\t' + objectname + idname + '\n')
                            img = cv.imread(imgfile)
                            img1 = cv.imread(imgfile1)
                            for index in range(len(objectlist)):
                                objects = objectlist[index]

                                namelist = objects.getElementsByTagName('name')
                                idlist = objects.getElementsByTagName('id')
                                objectname = namelist[0].childNodes[0].data
                                idname = idlist[0].childNodes[0].data
                                if objectname + idname != key or AnnoPath.split('/')[-3] + '_' + AnnoPath.split('/')[-2] + '_' + key + '_' + Anno_pre + '.jpg' in video_check_dir:
                                    continue
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
                                    cv.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), thickness=1)
                                    cv.putText(img, objectname + idname, (x1, y1), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),
                                            thickness=1)

                            filename = video_check_dir + AnnoPath.split('/')[-3] + '_' + AnnoPath.split('/')[-2] + '_' + key + '_' + Anno_pre + '.jpg'
                            cv.imwrite(filename, img)
                            
                            for index in range(len(objectlist1)):
                                objects = objectlist1[index]

                                namelist = objects.getElementsByTagName('name')
                                idlist = objects.getElementsByTagName('id')
                                objectname = namelist[0].childNodes[0].data
                                idname = idlist[0].childNodes[0].data
                                if objectname + idname != key or AnnoPath.split('/')[-3] + '_' + AnnoPath.split('/')[-2] + '_' + key + '_' + Anno_pre + '.jpg' in video_check_dir:
                                    continue
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
                                    cv.rectangle(img1, (x1, y1), (x2, y2), (255, 255, 255), thickness=1)
                                    cv.putText(img1, objectname + idname, (x1, y1), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),
                                            thickness=1)
                                    
                            filename1 = video_check_dir + AnnoPath.split('/')[-3] + '_' + AnnoPath.split('/')[-2] + '_' + key + '_' + Anno_pre1 + '.jpg'
                            cv.imwrite(filename1, img1)
                    except:
                        continue
        storage_before = storage_curr
   
if __name__ == '__main__':
    ### This code is developed for detecting annotations with position mutation
    data_xml_dir = './data/'
    video_check_dir = './position_mutation_targets/'
    f = open('./position_mutation_targets.txt',"w")
    xml_list = os.listdir(data_xml_dir)
    for xml_dir in xml_list:
        AnnoPath = data_xml_dir + xml_dir + '/00/'
        detect(AnnoPath, f)
        AnnoPath = data_xml_dir + xml_dir + '/01/'
        detect(AnnoPath, f)
    f.close()