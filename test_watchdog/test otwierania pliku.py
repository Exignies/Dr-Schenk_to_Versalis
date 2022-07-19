

with open("L:\\hd\\13J2621_2022-07-04-09-47-50test.xch", "r") as f:  # przerobić aby w przypadku braku pliku odczekał 1s
            l = f.readlines()
            l = l[2].split(":")
            Etykieta = l[6]
            print("Etykieta: %s , PN %s" %(Etykieta, "Pn"))
        