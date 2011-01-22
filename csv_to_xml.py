import string

csv_file = "FCCS_loadings_2.2_12-7-2010.csv"
xml_file = "FCCS_loadings_2.2_12-7-2010.xml"
node2 = "FCCS"

def clean_line(line):
    line = line.split(',')
    print line
    for i in range(0, len(line)):
        if "\n" in line[i]:
            line[i] = line[i].replace('\n','')
        if line[i] == "\n":
            line.remove(line[i])

    return line

t = open(csv_file,'r')
lines = t.readlines(); t.close()

col_heads = clean_line(lines[0])

print col_heads
xml = open(xml_file,'w')
#xml.write("""<?xml version="1.0" standalone="yes"?>""")

for line in lines:
    if col_heads[1] not in line:
        data = clean_line(line)
        if len(col_heads) <> len(data):
            print "ERROR: amount of headers and data differ\n\nHEADERS: "
            print col_heads
            print data
        else:
            a = "\n<" + node2 + ">"
            for i in range(0,len(data)):
                a += "\n\t<" + col_heads[i] + ">" + data[i] + "</" + col_heads[i] + ">"
            a += "\n</" + node2 + ">"
            
            xml.write(a)

xml.close()

print "DONE"

xml = open(xml_file,'r')
print xml.read()
