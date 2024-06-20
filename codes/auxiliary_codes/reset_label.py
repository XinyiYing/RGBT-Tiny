import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree

tree=ElementTree()

def reset_label(AnnoPath):
    Annolist = []
    Annolist1 = os.listdir(AnnoPath)
    for Anno in Annolist1:
        if Anno.split('.')[-1] == 'xml':
            Annolist.append(Anno)    
    
    for Anno in Annolist:
        Anno_pre, ext = os.path.splitext(Anno)
        xmlfile = AnnoPath + Anno

        tree.parse(xmlfile)
        root = tree.getroot()
        objectlist = root.findall("object")
        for index in range(len(objectlist)):
            objects = objectlist[index]
            try:
                objects.findall("id")[0]
            except:
                SubElement = ET.SubElement(objects,'id')
                SubElement.text = str(index+100)
                
        tree.write(xmlfile)          

if __name__ == '__main__':
    ### This code is developed for reset label id
    AnnoPath = './data/'
    reset_label(AnnoPath)