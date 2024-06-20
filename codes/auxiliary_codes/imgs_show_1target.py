import os
import xml.dom.minidom
import cv2 as cv

def show_img(AnnoPath, video_check_dir, annotation):
    Annolist = []
    Annolist1 = os.listdir(AnnoPath)
    for Anno in Annolist1:
        if Anno.split('.')[-1] == 'xml':
            Annolist.append(Anno)    
    Anno_dir_list = AnnoPath.split('/')
    
    if not os.path.exists(video_check_dir + Anno_dir_list[-3] + '/' + Anno_dir_list[-3]):
        os.makedirs(video_check_dir + Anno_dir_list[-3] + '/' + Anno_dir_list[-3])
    fps = 10
    size = (640, 512)

    video = cv.VideoWriter(video_check_dir + Anno_dir_list[-3] + '/' + Anno_dir_list[-3] + '_' + Anno_dir_list[-2] + '_' + annotation[0] + '.mp4', cv.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
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
        img = cv.imread(imgfile)
        
        filenamelist = collection.getElementsByTagName("filename")
        filename = filenamelist[0].childNodes[0].data
        print(filename)
        objectlist = collection.getElementsByTagName("object")
            
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
                if objectname + idname in annotation:
                    cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), thickness=1)
                    cv.putText(img, objectname + idname, (x1-10, y1-10), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),
                        thickness=2)
        video.write(img)

    video.release()
    cv.destroyAllWindows()      

def detect(AnnoPath, f):
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
            try:
                idname = idlist[0].childNodes[0].data
            except:
                idname = 'None'
            
            cur_name = objectname + idname
            try:
                storage_curr[cur_name] > 0
                storage_curr[cur_name] = storage_curr[cur_name] + 1
            except:
                storage_curr[cur_name] = 1
        
    for key, values in storage_curr.items():
        print(xmlfile.split('/')[-3] + '/' + xmlfile.split('/')[-2] + '\t' + key + '\t times:\t' + str(values))
        f.write(xmlfile.split('/')[-3] + '/' + xmlfile.split('/')[-2] + '\t' + key + '\t times:\t' + str(values) + '\n')

if __name__ == '__main__':
    ### This code is developed for genenrate a video of each annotaion
    data_xml_dir = './data/' # data dir
    video_check_dir = './videos/' # output video dir

    txt_dir = './final_target_list.txt'

    f = open(txt_dir,"w")
    xml_list = os.listdir(data_xml_dir)
    for xml_dir in xml_list:
        AnnoPath = data_xml_dir + xml_dir + '/00/'
        detect(AnnoPath, f)
        AnnoPath = data_xml_dir + xml_dir + '/01/'
        detect(AnnoPath, f)
    f.close()

    f = open(txt_dir, "r")
    show_target = 1
    cot = 0
    cot_list = []
    for line in f.readlines():
        line_split = line.split('\t')
        cot = cot + 1 
        if cot < show_target:
            cot_list.append(line_split[1])
        else:
            cot_list.append(line_split[1])
            show_img(data_xml_dir + line_split[0] + '/', video_check_dir, cot_list)
            cot = 0
            cot_list = []       
    f.close()