import xml.etree.ElementTree as ET

def main():
    print(" Hello World ^_^ ")

    tree = ET.parse('10.xml')
    root = tree.getroot()
    count = len(tree.findall('mail'))

    date_file = open("dates.txt","w+")
                
    for x in root.findall('mail'):
        date = x.find('date').text
        row_id = x.find('row').text
        body = x.find('body').text
        date_file.write("%s: %s\n" %(date,row_id))
                           
date_file.close()

if __name__ == "__main__":
    main()
