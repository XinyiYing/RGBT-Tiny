import os
import xml.dom.minidom
import cv2 as cv

def show_img(AnnoPath, video_check_dir):
    Annolist = []
    Annolist1 = os.listdir(AnnoPath)
    for Anno in Annolist1:
        if Anno.split('.')[-1] == 'xml':
            Annolist.append(Anno)    
    Anno_dir_list = AnnoPath.split('/')
    
    if not os.path.exists(video_check_dir):
        os.makedirs(video_check_dir)
    fps = 50
    size = (640, 512)
    video = cv.VideoWriter(video_check_dir + Anno_dir_list[-3] + '_' + Anno_dir_list[-2] + '.mp4', cv.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
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

            idlist = objects.getElementsByTagName('id')
            idname = idlist[0].childNodes[0].data

            index_length = 255*255*255/200
            color_index1 = int(idname) * index_length // (255*255)
            color_index2 = int(idname) * index_length // (255) - color_index1 * 255
            color_index3 = int(idname) * index_length - color_index1 * 255 * 255 - color_index2 * 255
            
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
                cv.rectangle(img, (x1, y1), (x2, y2), (color_index1, color_index2, color_index3), thickness=1)
        video.write(img)
            
    video.release()
    cv.destroyAllWindows()      
if __name__ == '__main__':
    ### This code is developed for genenrate videos of annotaions with different colors
    data_xml_dir = './data/' ### data dir 
    video_check_dir = './videos/'  # output video dir
    xml_list = os.listdir(data_xml_dir)
    for xml_dir in xml_list:
        AnnoPath = data_xml_dir + xml_dir + '/00/'
        show_img(AnnoPath, video_check_dir)
        AnnoPath = data_xml_dir + xml_dir + '/01/'
        show_img(AnnoPath, video_check_dir)