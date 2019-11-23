#Creates the "emails" file from the input using the following format:
#from-"from_address":"row_id"
#to-"to_address":"row_id"
from xml.dom import minidom
import xml.etree.ElementTree as ET
tree = ET.parse('10.xml')
root = tree.getroot()

recs_file = open("recs.txt", "w+")
for x in root.findall('mail'):
    recs_file.write(minidom.parseString(ET.tostring(root)).toxml())
recs_file.close()
