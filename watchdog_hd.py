import time
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import ezdxf

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)



def opendxf(DRplik, LVplik):
    # Otwieranie pliku DrSchenk i LVersalis
    os.chdir(r"//10.52.80.61/departments/Technology/Private/KROJOWNIA SKÓRY/Makra/Dr Schenk")
    docDR = ezdxf.readfile("L:/hd/" + str(DRplik))
    docLV = ezdxf.readfile("L:/hd/" + str(LVplik))
    mspLV = docLV.modelspace()
    mspDR = docDR.modelspace()

    return docDR,mspDR, mspLV


def on_created(event):
    print(f"hey, {event.src_path} has been created!")
    srtfile = event.src_path
    file = os.path.split(event.src_path)
    rozszerzenie = file[1].split(".")
    nazwa = str(rozszerzenie[0])

    # zmiana nzawy pliku na rozszerzenie txt
    if rozszerzenie[1].lower() == "dxf":
        time.sleep(2)
        try:
            f = open("L:\\hd\\" + str(rozszerzenie[0])+".xch", "r")  # przerobić aby w przypadku braku pliku odczekał 1s
            l = f.readlines()
            l = l[2].split(":")
            Etykieta = l[6]
            Pn = l[3]
            Opis = l[4]
            Batch = l[5]    
            Versal = str(l[1])[:str(l[1]).index("_")]
            print("Etykieta: %s , PN %s , Opis: %s , Batch: %s, Versalis nr: %s" %(Etykieta, Pn, Opis, Batch, Versal))
        finally:
            f.close()
        



"""" 
    if rozszerzenie[1].lower() == "dxf":
        if nazwa[0:8] == "17DE2621":
            print(file[1])
            dstfile = file[0]+"\\"+nazwa+".txt"
            print(dstfile)
            os.rename(srtfile, dstfile)
"""
        # podmienić plik na testy
""""
        DRplik = "13I2622_2022-04-20-15-06-26_dv2.dxf"
        LVplik = file[1]
        os.chdir(r"//10.52.80.61/departments/Technology/Private/KROJOWNIA SKÓRY/Makra/Dr Schenk")
        docDR = ezdxf.readfile("wejscie/" + str(DRplik))
        #docLV = ezdxf.readfile("wejscie/" + str(LVplik))
        
        docDR.saveas(file[1])
        print("podmieniono")
"""



def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")
 
def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")
 
def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
    
my_event_handler.on_created = on_created
#my_event_handler.on_deleted = on_deleted
#my_event_handler.on_modified = on_modified
#my_event_handler.on_moved = on_moved
    
path = "L:\hd"
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    
my_observer.start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()  
    