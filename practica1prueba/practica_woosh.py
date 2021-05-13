from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import re, os, shutil
import datetime
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID, KEYWORD
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh.qparser.dateparse import DateParserPlugin
 
url_principal = "https://www.elseptimoarte.net/"
 
def extraer_urls_peliculas():
    f = urllib.request.urlopen(url_principal+"estrenos/")
    s = BeautifulSoup(f,"lxml")
    l = s.find("ul", class_= "elements")
    a =l.findAll("a")
    return a
 
def recorrer_urls(urls):
 
    lista = list()
 
    for url in urls:
        href=url.attrs['href']
        f = urllib.request.urlopen(url_principal + href)
        s = BeautifulSoup(f,"lxml")
        p_generos = s.find("p",class_="categorias")
        sin = s.find("div",class_="info").findAll("p")
        generos = p_generos.findAll('a')
        sinopsis,titulo,tit_or,pais,fecha_estr,director,genero="","","","","","",""
 
        for info in sin:
            sinopsis+=info.get_text()
        for i in generos:
            genero+=i.attrs["href"][19:-1]+","
        genero=genero[:-1]
        datos = s.findAll(["dt","dd"])
        for dato,contenido in zip(datos[0::2],datos[1::2]):
            if(dato.get_text()=="Título"):
                titulo = contenido.get_text()
            elif(dato.get_text()=="Título original"):
                tit_or=contenido.get_text()
            elif(dato.get_text()=="País"):
                pais = contenido.get_text()
            elif(dato.get_text()=="Estreno en España"):
                fecha_estr = contenido.get_text()
            elif(dato.get_text()=="Director"):
                director=contenido.get_text()
 
        pais = [p for p in pais.split(" ") if len(p)>=2]
 
        pais = ' '.join(pais)
 
        director = [d for d in director.split(" ") if len(d)>=2]
 
        director = ' '.join(director)
    
        lista.append((titulo,tit_or, fecha_estr,pais,genero,director,sinopsis))
    
    return lista
 
def almacenar_datos():
    
    #define el esquema de la información
    schem = Schema(titulo=TEXT(stored=True), titulo_original=TEXT(stored=True), fecha=DATETIME(stored=True), pais=KEYWORD(stored=True), genero=KEYWORD(stored=True), director=TEXT(stored=True), sinopsis=TEXT(stored=True))
    
    #eliminamos el directorio del índice, si existe
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    #creamos el índice
    ix = create_in("Index", schema=schem)
    #creamos un writer para poder añadir documentos al indice
    writer = ix.writer()
    i=0
    lista=recorrer_urls(extraer_urls_peliculas())
    for pelicula in lista:
        #añade cada pelicula de la lista al índice
        writer.add_document(titulo=pelicula[0], titulo_original=pelicula[1], fecha=datetime.datetime.strptime(pelicula[2], '%d/%m/%Y'), pais=pelicula[3], genero=pelicula[4], director=pelicula[5], sinopsis=pelicula[6])    
        i+=1
    writer.commit()
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " películas") 
 
def buscar_titulo_sinopsis():
    def mostrar_lista(event):
        #abrimos el índice
        ix=open_dir("Index")
        #creamos un searcher en el índice    
        with ix.searcher() as searcher:
            #se crea la consulta: buscamos en el campo "titulo" y "sinopsis" la palabra que hay en el Entry "en"
            query = MultifieldParser(["titulo", "sinopsis"], ix.schema).parse(str(en.get()))
            #llamamos a la función search del searcher, pasándole como parámetro la consulta creada
            results = searcher.search(query)
            #recorremos los resultados obtenidos(es una lista de diccionarios) y mostramos lo solicitado
            v = Toplevel()
            v.title("Listado de Películas")
            v.geometry('800x150')
            sc = Scrollbar(v)
            sc.pack(side=RIGHT, fill=Y)
            lb = Listbox(v, yscrollcommand=sc.set)
            lb.pack(side=BOTTOM, fill = BOTH)
            sc.config(command = lb.yview)
            #Importante: el diccionario solo contiene los campos que han sido almacenados(stored=True) en el Schema
            for r in results: 
                lb.insert(END,"Título: " + r['titulo'])
                lb.insert(END,"Título original: " + r['titulo_original'])
                lb.insert(END,"Director: " + r['director'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Busqueda por Título o Sinopsis")
    l = Label(v, text="Introduzca palabra a buscar:")
    l.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
 
def buscar_genero():
    def mostrar_lista(event):
        #abrimos el índice
        ix=open_dir("Index")
        #creamos un searcher en el índice    
        with ix.searcher() as searcher:
            #se crea la consulta: buscamos en el campo "titulo" y "sinopsis" la palabra que hay en el Entry "en"
            query = QueryParser("genero", ix.schema).parse(str(en.get()))
            #llamamos a la función search del searcher, pasándole como parámetro la consulta creada
            results = searcher.search(query)
            #recorremos los resultados obtenidos(es una lista de diccionarios) y mostramos lo solicitado
            v = Toplevel()
            v.title("Listado de Películas")
            v.geometry('800x150')
            sc = Scrollbar(v)
            sc.pack(side=RIGHT, fill=Y)
            lb = Listbox(v, yscrollcommand=sc.set)
            lb.pack(side=BOTTOM, fill = BOTH)
            sc.config(command = lb.yview)
            #Importante: el diccionario solo contiene los campos que han sido almacenados(stored=True) en el Schema
            for r in results: 
                lb.insert(END,"Título: " + r['titulo'])
                lb.insert(END,"Título original: " + r['titulo_original'])
                lb.insert(END,"País: " + r['pais'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Busqueda por Título o Sinopsis")
    l = Label(v, text="Introduzca palabra a buscar:")
    l.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
 
def buscar_fecha():
    def mostrar_lista(event):
        #abrimos el índice
        ix=open_dir("Index")
        #creamos un searcher en el índice    
        with ix.searcher() as searcher:
            #se crea la consulta: buscamos en el campo "titulo" y "sinopsis" la palabra que hay en el Entry "en"
            query = QueryParser("fecha", ix.schema)
            #query.add_plugin(DateParserPlugin())
            fecha_inicio, fecha_fin = en.get().split(" ")
            query = query.parse(u"[{} to {}]".format(fecha_inicio, fecha_fin))
            #llamamos a la función search del searcher, pasándole como parámetro la consulta creada
            results = searcher.search(query)
            #recorremos los resultados obtenidos(es una lista de diccionarios) y mostramos lo solicitado
            v = Toplevel()
            v.title("Listado de Películas")
            v.geometry('800x150')
            sc = Scrollbar(v)
            sc.pack(side=RIGHT, fill=Y)
            lb = Listbox(v, yscrollcommand=sc.set)
            lb.pack(side=BOTTOM, fill = BOTH)
            sc.config(command = lb.yview)
            #Importante: el diccionario solo contiene los campos que han sido almacenados(stored=True) en el Schema
            for r in results: 
                lb.insert(END,"Título: " + r['titulo'])
                lb.insert(END,"Título original: " + r['titulo_original'])
                lb.insert(END,"País: " + r['pais'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Busqueda por Título o Sinopsis")
    l = Label(v, text="Introduzca fecha a buscar:")
    l.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
 
def ventana_principal():
        
    root = Tk()
    menubar = Menu(root)
    
    datosmenu = Menu(menubar, tearoff=0)
    datosmenu.add_command(label="Cargar", command=almacenar_datos)
    datosmenu.add_separator()   
    datosmenu.add_command(label="Salir", command=root.quit)
    
    menubar.add_cascade(label="Datos", menu=datosmenu)
    
    buscarmenu = Menu(menubar, tearoff=0)
    buscarmenu.add_command(label="Título o sinopsis", command=buscar_titulo_sinopsis)
    buscarmenu.add_command(label="Géneros", command=buscar_genero)
    buscarmenu.add_command(label="Fecha", command=buscar_fecha)
    
    menubar.add_cascade(label="Buscar", menu=buscarmenu)
        
    root.config(menu=menubar)
    root.mainloop()
 
if __name__ == "__main__":
    ventana_principal()