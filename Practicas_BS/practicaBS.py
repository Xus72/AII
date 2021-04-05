from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3

def initUI():
    
    def cerrar_ventana():
        root.destroy()
    
    root = Tk()

    root.title("APP LIBROS")

    menubar = Menu(root)
    root.config(menu=menubar)

    menu_datos = Menu(menubar)
        
    menubar.add_cascade(label="Datos", menu=menu_datos)
        
    menu_datos.add_command(label="Cargar", command=almacenar_bd)
    menu_datos.add_command(label="Salir", command=cerrar_ventana)
    
    menu_listar = Menu(menubar)
        
    menubar.add_cascade(label="Listar", menu=menu_listar)
        
    menu_listar.add_command(label="Libros", command=listar_libros)
    menu_listar.add_command(label="Ebooks", command=listar_ebooks)
    
    menu_buscar = Menu(menubar)
        
    menubar.add_cascade(label="Buscar", menu=menu_buscar)
        
    menu_buscar.add_command(label="Libros por género", command=buscar_genero)
    menu_buscar.add_command(label="Libros agotados", command=buscar_agotados)
        
    root.mainloop()
    
url_principal = "https://editorialamarante.es"
 
def extraer_urls_libros():
    f = urllib.request.urlopen(url_principal+"/libros/narrativa")
    s = BeautifulSoup(f,"lxml")
    l = s.find("div", class_= "book-list")
    h4 =l.findAll("h4")
    urls = []
    for a in h4:
        urls.append(a.find("a")["href"])
    return urls
 
def recorrer_urls(urls):

    conn = sqlite3.connect('libros.db')
    conn.text_factory = str

    for url in urls:
        f = urllib.request.urlopen(url_principal + url)
        s = BeautifulSoup(f,"lxml")
        partes =s.findAll("p", class_="indent")
 
        titulo,autor,genero,anno="","","",""
 
        titulo = s.find(itemprop="name").contents[0]
        autor = partes[0].find(itemprop="author").contents[0]
        genero = partes[0].find(itemprop="genre").contents[0]
        anno = partes[0].contents[-1].strip()
 
        ISBNS =  s.findAll(itemprop="isbn")
 
        lista = s.findAll("h4")
        
        if (len(partes)==3):
            isbn_f = ISBNS[1].contents[0]
            isbn_d = ISBNS[0].contents[0]
            precio_d = partes[1].contents[-1].strip()[:-2]
            formato = partes[1].contents[13]
            precio_f = partes[2].contents[-1].strip()[:-2]
            paginas = partes[2].contents[7].strip()
        
        elif(lista[1].contents[0]=="Libro impreso") :
            precio_f = partes[1].contents[-1].strip()[:-2]
            paginas = partes[1].contents[7].strip()
            isbn_f = ISBNS[0].contents[0]
 
        else:
            precio_d = partes[1].contents[-1].strip()[:-2]
            formato = partes[1].contents[13]
            isbn_d = ISBNS[0].contents[0]
 
 
        if (len(partes)==3):
            conn.execute(
            """INSERT INTO LIBROS (TITULO, AUTOR, GENEROS, ANIO, ISBN, PAGINAS, FORMATO, PRECIO) VALUES (?,?,?,?,?,?,?,?)""",
            (titulo, autor, genero, anno, isbn_f, paginas, None, precio_f))
            
            conn.execute(
            """INSERT INTO LIBROS (TITULO, AUTOR, GENEROS, ANIO, ISBN, PAGINAS, FORMATO, PRECIO) VALUES (?,?,?,?,?,?,?,?)""",
            (titulo, autor, genero, anno, isbn_d, None, formato, precio_d))
        
        elif(lista[1].contents[0]=="Libro impreso") :
            conn.execute(
            """INSERT INTO LIBROS (TITULO, AUTOR, GENEROS, ANIO, ISBN, PAGINAS, FORMATO, PRECIO) VALUES (?,?,?,?,?,?,?,?)""",
            (titulo, autor, genero, anno, isbn_f, paginas, None, precio_f))
            
        else: 
            conn.execute(
            """INSERT INTO LIBROS (TITULO, AUTOR, GENEROS, ANIO, ISBN, PAGINAS, FORMATO, PRECIO) VALUES (?,?,?,?,?,?,?,?)""",
            (titulo, autor, genero, anno, isbn_d, None, formato, precio_d))
        
        conn.commit()
        
    cursor = conn.execute("SELECT COUNT(*) FROM LIBROS")

    messagebox.showinfo("Base Datos",

                "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")

    conn.close()
    
def almacenar_bd():
    conn = sqlite3.connect('libros.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS LIBROS")
    conn.execute('''CREATE TABLE LIBROS
       (TITULO            TEXT NOT NULL,
        AUTOR    TEXT ,
        GENEROS        TEXT,
        ANIO TEXT,
        ISBN TEXT,
        PAGINAS INTEGER,
        FORMATO TEXT,
        PRECIO TEXT);''')
    
    conn.close()
    urls = extraer_urls_libros()
    recorrer_urls(urls)

def listar_libros():
    
    def imprimir_libros(cursor):
        
        v = Toplevel()
        v.title("Libros impresos")
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width = 150, yscrollcommand=sc.set)

        for row in cursor:

            titulo = row[0]
            autor = row[1]
            generos = row[2]
            anio = row[3]
            
            lb.insert(END,"-----------------------------------------------------")

            s = "Título: " + titulo + " || Autor: " + autor + " || Género: " + generos + " || Año: " + anio
            lb.insert(END,s)

        lb.pack(side=LEFT,fill=BOTH)
        sc.config(command = lb.yview)
    
    conn = sql.connect('libros.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT * FROM LIBROS WHERE FORMATO IS NULL ORDER BY TITULO")
    imprimir_libros(cursor)
    conn.close()

def listar_ebooks():
    
    def imprimir_consulta(cursor):
        
        v = Toplevel()
        v.title("Ebooks")
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width = 150, yscrollcommand=sc.set)

        for row in cursor:
            
            titulo = row[0]
            autor = row[1]
            generos = row[2]
            isbn = row[4]
            formato = row[6]
            precio = row[7]
            
            lb.insert(END,"-----------------------------------------------------")

            s = "Título: " + titulo + " || Autor: " + autor + " || Género: " + generos + " || ISBN: " + isbn + " || Formato: " + formato + " || Precio: " + precio
            lb.insert(END,s)

        lb.pack(side=LEFT,fill=BOTH)
        sc.config(command = lb.yview)
    
    conn = sqlite3.connect('libros.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT * FROM LIBROS WHERE PAGINAS IS NULL ORDER BY TITULO")
    imprimir_consulta(cursor)
    conn.close()

def buscar_genero():
    
    def listar_busqueda(event):
        
        conn = sqlite3.connect('libros.db')
        conn.text_factory = str
        s =  str(w.get())
        cursor = conn.execute("""SELECT * FROM LIBROS WHERE GENEROS LIKE ?""",('%'+ s +'%',))
        listar_libros_genero(cursor)       
        conn.close()
        
    def listar_libros_genero(cursor):
    
        v = Toplevel()
        v.title("Resultados búsqueda")
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width = 150, yscrollcommand=sc.set)

        for row in cursor:

            titulo = row[0]
            autor = row[1]
            generos = row[2]
            anio = row[3]
            
            lb.insert(END,"-----------------------------------------------------")

            s = "Título: " + titulo + " || Autor: " + autor + " || Género: " + generos + " || Año: " + anio
            lb.insert(END,s)
        
        lb.pack(side=LEFT,fill=BOTH)
        sc.config(command = lb.yview)
                
    v = Toplevel()
    v.title("Búsqueda por género")
    conn = sql.connect('libros.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT GENEROS FROM LIBROS")
    lista_generos = [genero for genero in cursor]
    lista_generos_final = set()
    for tupla in lista_generos:
        for elem in tupla:
            elems = elem.split(".")
            for i in elems:
                lista_generos_final.add(i)
                
    lista_generos_final = list(lista_generos_final)
    conn.close()
    
    w = Spinbox(v, values=lista_generos_final)

    w.bind("<Return>", listar_busqueda)
    w.pack(side = LEFT)

# No esta terminado
def buscar_agotados():
    
    def listar_libros_agotados(cursor):
    
        v = Toplevel()
        v.title("Resultados búsqueda")
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width = 150, yscrollcommand=sc.set)

        for row in cursor:

            titulo = row[0]
            autor = row[1]
            generos = row[2]
            anio = row[3]
            
            lb.insert(END,"-----------------------------------------------------")

            s = "Título: " + titulo + " || Autor: " + autor + " || Género: " + generos + " || Año: " + anio
            lb.insert(END,s)
        
        lb.pack(side=LEFT,fill=BOTH)
        sc.config(command = lb.yview)
    
    v = Toplevel()
    v.title("Búsqueda agotados")
    
    f = urllib.request.urlopen(url_principal+"/libros/narrativa")
    s = BeautifulSoup(f,"lxml")
    agotados = s.findAll("a", class_=["disabled"])
    titulos_libros = list()
    for agotado in agotados:
        x = agotado.parent.parent.parent.parent.parent.parent.find("a").contents[0]
        titulos_libros.append(x)
        
    
        
    libro_impreso = IntVar()      # 1 si, 0 no
    ebook = IntVar()    # 1 si, 0 no
    
    c1 = Checkbutton(v, text="Libro impreso", variable=libro_impreso, 
            onvalue=1, offvalue=0).pack()
    c2 = Checkbutton(v, text="Ebook",variable=ebook, 
            onvalue=1, offvalue=0).pack()
    
    if libro_impreso and ebook:
        for titulo in titulos_libros:
            cursor = (conn.execute("""SELECT * FROM LIBROS WHERE TITULO LIKE ?""",('%'+ titulo +'%',)))
        listar_libros_agotados(cursor)