import os
import xml.dom.minidom

def add_label(data_dir1, data_dir2, label_name_list):
    AnnoPath = data_dir1
    Annolist = []
    Annolist1 = os.listdir(AnnoPath)
    for Anno in Annolist1:
        if Anno.split('.')[-1] == 'xml':
            Annolist.append(Anno)    
    
    for Anno in Annolist:
        label_name_list1 = label_name_list.copy()
        xmlfile = AnnoPath + Anno
        xmlfile_write = data_dir2 + Anno
        
        try:
            DOMTree = xml.dom.minidom.parse(xmlfile)
        except:
            f = open(xmlfile, "r")
            r = f.read()
            text = str(r.encode('utf-8'), encoding = "utf-8")
            DOMTree = xml.dom.minidom.parseString(text)
            
        try:
            DOMTree_write = xml.dom.minidom.parse(xmlfile_write)
        except:
            f_write = open(xmlfile_write, "r")
            r_write = f_write.read()
            text_write = str(r_write.encode('utf-8'), encoding = "utf-8")
            DOMTree_write = xml.dom.minidom.parseString(text_write)

        
        collection = DOMTree.documentElement
        objectlist = collection.getElementsByTagName("object")
        
        collection_write = DOMTree_write.documentElement
        objectlist_write = collection_write.getElementsByTagName("object")
        for index in range(len(objectlist_write)):
            objects = objectlist_write[index]
            namelist = objects.getElementsByTagName('name')
            idlist = objects.getElementsByTagName('id')
            objectname = namelist[0].childNodes[0].data
            idname = idlist[0].childNodes[0].data
            if objectname + idname in label_name_list1:
                label_name_list1.remove(objectname + idname)
            tab_text = DOMTree.createTextNode('\t')
            collection_write.appendChild(tab_text)
            collection_write.appendChild(objects)
            tab_text = DOMTree.createTextNode('\n')
            collection_write.appendChild(tab_text)
        
        for index in range(len(objectlist)):
            objects = objectlist[index]

            namelist = objects.getElementsByTagName('name')
            idlist = objects.getElementsByTagName('id')
            objectname = namelist[0].childNodes[0].data
            idname = idlist[0].childNodes[0].data
            if objectname + idname in label_name_list1:
                tab_text = DOMTree.createTextNode('\t')
                collection_write.appendChild(tab_text)    
                collection_write.appendChild(objects)
                tab_text = DOMTree.createTextNode('\n')
                collection_write.appendChild(tab_text)
                
        with open(xmlfile_write, 'w', encoding='utf-8') as f_write:    
            DOMTree_write.writexml(f_write, encoding='utf-8')     

if __name__ == '__main__':
    ### This code is developed for dense annotaion in DarkLabel.
    ### You can first annotate one instance in a seperate dir, and then use the code to add the annotate in another dir.
    data_dir1 = './DJI_0323_2_11/00/' ## dir for annotation
    data_dir2 = './DJI_0323_2/00/' ## dir for annotation add (dense annotations)
    label_name_list = ['pedestrian0','plane1'] ## name list of added annotations
    add_label(data_dir1, data_dir2, label_name_list) ### add anntations 'pedestrian0' and 'plane1' in ".xml" of data_dir1 to ".xml" of data_dir2.
    
    
    
    