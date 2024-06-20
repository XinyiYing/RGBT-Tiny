import os
import xml.dom.minidom
import cv2 as cv
import cv2
import matplotlib.pyplot as plt
import numpy as np

def edgeSegmentation(img0, location, xmlfile, show=False):
    [x1,y1,x2,y2] = location
    d = 5
    if y1-d < 0:
        y10 = 0
    else:
        y10 = y1-d
    if x1-d < 0:
        x10 = 0
    else:
        x10 = x1-d
    if y2+d > 511:
        y20 = 511
    else:
        y20 = y2+d
    if x2+d >639:
        x20 = 639
    else:
        x20 = x2+d
        
    img = img0[y10:y20,x10:x20]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1)
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    blured = cv2.GaussianBlur(gradient, (9, 9), 0)
    _, dst = cv2.threshold(blured, blured.max()*0.4, 255, cv2.THRESH_BINARY)

    cnts, _ = cv2.findContours(
        dst.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    x, y, w, h = cv2.boundingRect(c)
    
    if show == True:
        draw_img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
        images = [img, blured, dst, draw_img]
        imgaesTitle = ['img', 'blured', 'dst', 'draw_img']
        plt.figure()
        for i in range(4):
            plt.subplot(2, 2, i+1)
            plt.imshow(images[i], 'gray')
            plt.title(imgaesTitle[i])
        xmlfile_list = xmlfile.split('/')
        save_pth = './refine_temp/' + xmlfile_list[-3] + '/' + xmlfile_list[-2] + '/' 
        if not os.path.exists(save_pth):
            os.makedirs(save_pth)
        plt.savefig(save_pth + xmlfile_list[-1].replace('.xml','.jpg'))
        plt.close()
        plt.figure()
        draw_img1 = cv2.rectangle(img0, (x10+x, y10+y), (x10+x+w, y10+y+h), (0, 255, 0), 1)
        plt.imshow(draw_img1, 'gray')
        plt.savefig(save_pth + 'img_' + xmlfile_list[-1].replace('.xml','.jpg'))
        plt.close()
    
    return x10+x, x10+x+w, y10+y, y10+y+h

def refine_label(AnnoPath):
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
        img = cv.imread(imgfile)
        objectlist = collection.getElementsByTagName("object")
    
        for index in range(len(objectlist)):
            objects = objectlist[index]
    
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
                # refine and rejust label
                x11, x21, y11, y21  = edgeSegmentation(img.copy(), [x1,y1,x2,y2], xmlfile, show=False)
                box.getElementsByTagName('xmin')[0].childNodes[0].data = x11
                box.getElementsByTagName('xmax')[0].childNodes[0].data = x21
                box.getElementsByTagName('ymin')[0].childNodes[0].data = y11
                box.getElementsByTagName('ymax')[0].childNodes[0].data = y21
        with open(xmlfile, 'w', encoding='utf-8') as f:
            DOMTree.writexml(f, encoding='utf-8')         

if __name__ == '__main__':
    ### This code is developed for refining corase label
    data_xml_dir = './data/' # data dir
    xml_list = os.listdir(data_xml_dir)
    for xml_dir in xml_list:
        AnnoPath = data_xml_dir + xml_dir + '/00/'
        refine_label(AnnoPath)
        AnnoPath = data_xml_dir + xml_dir + '/01/'
        refine_label(AnnoPath)