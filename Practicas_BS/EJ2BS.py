from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def initUI():
    
    def cerrar_ventana():
        root.destroy()
    
    root = Tk()

    root.title("Estrenos APP")

    menubar = Menu(root)
    root.config(menu=menubar)

    menu_datos = Menu(menubar)
        
    menubar.add_cascade(label="Datos", menu=menu_datos)
        
    menu_datos.add_command(label="Cargar", command=almacenar_bd)
    menu_datos.add_command(label="Listar", command=listar_bd)
    menu_datos.add_command(label="Salir", command=cerrar_ventana)
        
    menu_buscar = Menu(menubar)
        
    menubar.add_cascade(label="Buscar", menu=menu_buscar)
        
    menu_buscar.add_command(label="Título", command=buscar_titulo)
    menu_buscar.add_command(label="Fecha", command=buscar_fecha)
    menu_buscar.add_command(label="Género", command=buscar_genero)
        
    root.mainloop()
        

url_principal = "https://www.elseptimoarte.net/"
 
def extraer_urls_peliculas():
    f = urllib.request.urlopen(url_principal+"estrenos/")
    s = BeautifulSoup(f,"lxml")
    l = s.find("ul", class_= "elements")
    a =l.findAll("a")
    return a
 
def recorrer_urls(urls):
 
    for url in urls:
        href=url.attrs['href']
        f = urllib.request.urlopen(url_principal + href)
        s = BeautifulSoup(f,"lxml")
        p_generos = s.find("p",class_="categorias")
        generos = p_generos.findAll('a')
        titulo,tit_or,pais,fecha_estr,director,genero="","","","","",""
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
        conn = sql.connect('estrenos.db')
        conn.text_factory = str
        conn.execute("""INSERT INTO ESTRENOS (TITULO, TIT_ORIGINAL, PAIS, FECHA_ESTR_ES, DIRECTOR, GENERO) VALUES (?,?,?,?,?,?)""",(titulo,tit_or,pais,fecha_estr,director,genero))
        conn.commit()
        conn.close()

def almacenar_bd():
    
    conn = sql.connect('estrenos.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS ESTRENOS")
    conn.execute('''CREATE TABLE ESTRENOS
    (TITULO TEXT NOT NULL,
    TIT_ORIGINAL TEXT NOT NULL,
    PAIS TEXT NOT NULL,
    FECHA_ESTR_ES TEXT NOT NULL,
    DIRECTOR TEXT NOT NULL,
    GENERO TEXT NOT NULL);''')
    conn.close()
 
    urls = extraer_urls_peliculas()
    recorrer_urls(urls)
 
    conn = sql.connect('estrenos.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT COUNT(*) FROM ESTRENOS")
    messagebox.showinfo("Base Datos", "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    conn.close()

def listar_peliculas(cursor):
    
    v = Toplevel()
    v.title("Lista de estrenos")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width = 150, yscrollcommand=sc.set)
    
    for row in cursor:
        titulo = str(row[0])
        pais = str(row[2])
        director = str(row[4])
        
        lb.insert(END,"-----------------------------------------------------")
        
        s = "Título: " + titulo + " || País: " + pais + " || Director: " + director
        lb.insert(END,s)
    
    lb.pack(side=LEFT,fill=BOTH)
    sc.config(command = lb.yview)

def listar_bd():
    
    conn = sql.connect('estrenos.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT * FROM ESTRENOS ORDER BY TITULO")
    listar_peliculas(cursor)
    conn.close()

def buscar_titulo():
    
    def listar_busqueda(event):
        
        conn = sql.connect('estrenos.db')
        conn.text_factory = str
        s =  str(en.get())
        cursor = conn.execute("""SELECT * FROM ESTRENOS WHERE TITULO = ?""",(s,)) 
        listar_peliculas(cursor)       
        conn.close()
    
    v = Toplevel()
    v.title("Búsqueda por título")
    lb = Label(v, text="Introduzca el título: ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda)
    en.pack(side = LEFT)

def buscar_fecha():
    
    def listar_busqueda(event):
        
        conn = sql.connect('estrenos.db')
        conn.text_factory = str
        s =  str(en.get())
        s = s.replace('-', '/')
        cursor = conn.execute("""SELECT * FROM ESTRENOS WHERE FECHA_ESTR_ES = ?""",(s,)) 
        listar_peliculas_fecha(cursor)       
        conn.close()
        
    def listar_peliculas_fecha(cursor):
    
        v = Toplevel()
        v.title("Resultados búsqueda")
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width = 150, yscrollcommand=sc.set)

        for row in cursor:

            titulo = str(row[0])
            fecha = str(row[3])

            lb.insert(END,"-----------------------------------------------------")
            s = "Título: " + titulo + " || Fecha de estreno: " + fecha
            lb.insert(END,s)
        
        lb.pack(side=LEFT,fill=BOTH)
        sc.config(command = lb.yview)
    
    v = Toplevel()
    v.title("Búsqueda por fecha")
    lb = Label(v, text="Introduzca la fecha (dd-mm-aaaa): ")
    lb.pack(side = LEFT)
    en = Entry(v)
    en.bind("<Return>", listar_busqueda)
    en.pack(side = LEFT)

def buscar_genero():
    
    def listar_busqueda(event):
        
        conn = sql.connect('estrenos.db')
        conn.text_factory = str
        s =  str(w.get())
        cursor = conn.execute("""SELECT * FROM ESTRENOS WHERE GENERO = ?""",(s,)) 
        listar_peliculas_genero(cursor)       
        conn.close()
        
    def listar_peliculas_genero(cursor):
    
        v = Toplevel()
        v.title("Resultados búsqueda")
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width = 150, yscrollcommand=sc.set)

        for row in cursor:

            titulo = str(row[0])
            fecha = str(row[3])

            lb.insert(END,"-----------------------------------------------------")
            s = "Título: " + titulo + " || Fecha de estreno: " + fecha
            lb.insert(END,s)
        
        lb.pack(side=LEFT,fill=BOTH)
        sc.config(command = lb.yview)
                
    v = Toplevel()
    v.title("Búsqueda por género")
    conn = sql.connect('estrenos.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT GENERO FROM ESTRENOS")
    lista_generos = [genero for genero in cursor]
    lista_generos_final = set()
    for tupla in lista_generos:
        for elem in tupla:
            elems = elem.split(",")
            for i in elems:
                lista_generos_final.add(i)
                
    lista_generos_final = list(lista_generos_final)
    conn.close()
    
    w = Spinbox(v, values=lista_generos_final)

    w.bind("<Return>", listar_busqueda)
    w.pack(side = LEFT)
    
if __name__ == "__main__":
    initUI()