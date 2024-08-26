import os, sys
import glob
theme = ["Arcana",
        "Gruvbox",
        "Kicad Classic",
        "Kicad Default",
        "Monokai High Contrast",
        "Nord",
        "Nuova Elettronica",
        "Skyline",
        #"Solarized Dark",
        #"Solarized Light",
        "Vampire",
        "Witch Hazel"]

command = sys.argv[1:]



#Find all .sch files
path = os.getcwd()
#print(path)
direct = glob.glob(path+"/*/")
#print(direct)

schematic_file = ['']

for i in range(len(direct)):
    tempstring = glob.glob(direct[i]+"*.kicad_sch")
    #print(tempstring)
    if tempstring:
        #print(tempstring[0])
        schematic_file.append(tempstring[0])

schematic_file.pop(0)
print(schematic_file)


#Plot PDF
for i in range(len(schematic_file)):
    #print(schematic_file[3])
    #string = schematic_file[i]
    string_splice_begin = schematic_file[i].rfind("/")
    pdf_file_name = schematic_file[i][string_splice_begin+1:len(schematic_file[i])-10]
    os.system("kicad-cli sch export pdf -o 'outputs/"+pdf_file_name+".pdf' -t '" + theme[6] +"' -e -n "+schematic_file[i]) 
