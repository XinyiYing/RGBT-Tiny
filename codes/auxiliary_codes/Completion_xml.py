import os
import xml.dom.minidom

def show_img(AnnoPath):
    Annolist = []
    Annolist1 = os.listdir(AnnoPath)
    for Anno in Annolist1:
        if Anno.split('.')[-1] == 'jpg':
            Annolist.append(Anno)    
    
    for Anno in Annolist:
        Anno_pre, ext = os.path.splitext(Anno)
        try:
            xmlfile = AnnoPath + Anno_pre + '.xml'
            try:
                DOMTree = xml.dom.minidom.parse(xmlfile)
            except:
                f = open(xmlfile, "r")
                r = f.read()
                text = str(r.encode('utf-8'), encoding = "utf-8")
                DOMTree = xml.dom.minidom.parseString(text)
            with open(xmlfile, 'w', encoding='utf-8') as f:   
                DOMTree.writexml(f, encoding='utf-8')   
        except:
            xmlfile_o = 'E:/data/checked_videos/00140.xml'
            DOMTree = xml.dom.minidom.parse(xmlfile_o)
            collection = DOMTree.documentElement
            
            filenamelist = collection.getElementsByTagName("filename")
            filenamelist[0].childNodes[0].data = Anno_pre + '.jpg'
            
            pathlist = collection.getElementsByTagName("path")
            pathlist[0].childNodes[0].data = AnnoPath + Anno_pre + '.jpg'
            
            objectlist = collection.getElementsByTagName("object")
            for index in objectlist:
                collection.removeChild(index) 
            with open(xmlfile, 'w', encoding='utf-8') as f:    
                DOMTree.writexml(f, encoding='utf-8')   

if __name__ == '__main__':
    ### This code is developed for compelmenting missing xml without no annotation
    AnnoPath = './xml/' ### Annotation path for ".xml"
    show_img(AnnoPath)
