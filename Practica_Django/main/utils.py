from .models import Bodega, Pais, Maridaje, Vino


path = "data"

def populate_bd():
    return (populateBodega(),populatePais(), populateMaridaje(), populateVinos())

def populateVinos():
    print("Loading ...")
    Vino.objects.all().delete()
    maridaje = dict()
    lista=[]
    fileobj=open(path+"/vinos", "r", encoding="ISO-8859-15")
    for line in fileobj.readlines():
        line_list = line.split('|')
        idVino = line_list[0]
        pais = Pais.objects.get(idPais=line_list[3].strip())
        bodega = Bodega.objects.get(idBodega=line_list[4].strip())
        listM = list()
        for i in line_list[5:]:
             listM.append((Maridaje.objects.get(idMaridaje=str(i).strip())))
        maridaje[idVino] = listM
        lista.append(Vino(idVino = idVino
                        , nombre = line_list[1]
                        , anyo = line_list[2]
                        , pais = pais
                        , bodega = bodega))
    fileobj.close()
    Vino.objects.bulk_create(lista)

    for vino in Vino.objects.all():
        vino.maridaje.set(maridaje[vino.idVino])

    print("Vino inserted: " + str(Vino.objects.count()))
    print("---------------------------------------------------------")

    return Vino.objects.count()

def populateBodega():
    print("Loading ...")
    Bodega.objects.all().delete()

    lista=[]
    fileobj=open(path+"/bodegas", "r", encoding="ISO-8859-15")
    for line in fileobj.readlines():
        line_list = line.split('|')
        lista.append(Bodega(idBodega=line_list[0], nombre=line_list[1]))
    fileobj.close()
    Bodega.objects.bulk_create(lista)

    print("Bodega inserted: " + str(Bodega.objects.count()))
    print("---------------------------------------------------------")
    
    return Bodega.objects.count()

def populatePais():
    print("Loading ...")
    Pais.objects.all().delete()

    lista=[]
    fileobj=open(path+"/paises", "r", encoding="ISO-8859-15")
    for line in fileobj.readlines():
        line_list = line.split('|')
        lista.append(Pais(idPais=line_list[0], nombre=line_list[1]))
    fileobj.close()
    Pais.objects.bulk_create(lista)

    print("Pais inserted: " + str(Pais.objects.count()))
    print("---------------------------------------------------------")

    return Pais.objects.count()

def populateMaridaje():
    print("Loading ...")
    Maridaje.objects.all().delete()

    lista=[]
    fileobj=open(path+"/maridajes", "r", encoding="ISO-8859-15")
    for line in fileobj.readlines():
        line_list = line.split('|')
        lista.append(Maridaje(idMaridaje=line_list[0], nombre=line_list[1]))
    fileobj.close()
    Maridaje.objects.bulk_create(lista)

    print("Maridaje inserted: " + str(Maridaje.objects.count()))
    print("---------------------------------------------------------")

    return Maridaje.objects.count()

