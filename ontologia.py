from re import S
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, FOAF, XSD, DC, DCTERMS
from rdflib.collection import Collection
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD
from owlrl import DeductiveClosure, RDFS_Semantics

g = Graph()
SPACE = Namespace("http://SPACEample.org/space/")

# === Prefijos ===
g.bind("space", SPACE)
g.bind("foaf", FOAF)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)
g.bind("dc", DC)
g.bind("dcterms", DCTERMS)

# === Clases ===
g.add((SPACE.Serie, RDF.type, RDFS.Class))
g.add((SPACE.Pelicula, RDF.type, RDFS.Class))
g.add((SPACE.Contenido, RDF.type, RDFS.Class))
g.add((SPACE.Genero, RDF.type, RDFS.Class))
g.add((SPACE.Usuario, RDF.type, RDFS.Class))
g.add((SPACE.Director, RDF.type, RDFS.Class))
g.add((SPACE.Idioma, RDF.type, RDFS.Class))
g.add((SPACE.Actor, RDF.type, RDFS.Class))
g.add((SPACE.Formato, RDF.type, RDFS.Class))
g.add((SPACE.ClasificacionEdad, RDF.type, RDFS.Class))

# === Jerarquis(SubClases) ===
g.add((SPACE.Serie, RDFS.subClassOf, SPACE.Contenido))
g.add((SPACE.Pelicula, RDFS.subClassOf, SPACE.Contenido))

g.add((SPACE.Comedia, RDFS.subClassOf, SPACE.Genero))
g.add((SPACE.Drama, RDFS.subClassOf, SPACE.Genero))
g.add((SPACE.Accion, RDFS.subClassOf, SPACE.Genero))


# === Declaración de Propiedades ===

# Propiedad 1: tieneGenero (Genero de la Serie/Pelicula)
g.add((SPACE.tieneGenero, RDF.type, RDF.Property))
g.add((SPACE.tieneGenero, RDFS.domain, SPACE.Contenido))
g.add((SPACE.tieneGenero, RDFS.range, SPACE.Genero))

# Propiedad 2: tieneDirector (Director de la Serie/Pelicula)
g.add((SPACE.tieneDirector, RDF.type, RDF.Property))
g.add((SPACE.tieneDirector, RDFS.domain, SPACE.Contenido))
g.add((SPACE.tieneDirector, RDFS.range, SPACE.Director))

# Propiedad 3: tieneActor(Principal) (Actor en la Serie/Pelicula)
g.add((SPACE.tieneActor, RDF.type, RDF.Property))
g.add((SPACE.tieneActor, RDFS.domain, SPACE.Contenido))
g.add((SPACE.tieneActor, RDFS.range, SPACE.Actor))

# Propiedad 4: tieneIdioma (Idioma de la Serie/Pelicula) + USO DUBLINCORE
g.add((SPACE.tieneIdioma, RDF.type, RDF.Property))
g.add((SPACE.tieneIdioma, RDFS.domain, SPACE.Contenido))
g.add((SPACE.tieneIdioma, RDFS.range, SPACE.Idioma))
g.add((SPACE.tieneIdioma, RDFS.subPropertyOf, DCTERMS.language)) 

# Propiedad 5: tieneFormato (Formato de la Serie/Pelicula)
g.add((SPACE.tieneFormato, RDF.type, RDF.Property))
g.add((SPACE.tieneFormato, RDFS.domain, SPACE.Contenido))
g.add((SPACE.tieneFormato, RDFS.range, SPACE.Formato))

# Propiedad 6: tieneDuracion (Duración de la Serie/Pelicula)
g.add((SPACE.tieneDuracion, RDF.type, RDF.Property))
g.add((SPACE.tieneDuracion, RDFS.domain, SPACE.Contenido))
g.add((SPACE.tieneDuracion, RDFS.range, XSD.int))

# Propiedad 7: tienePuntuacion (Calificación de la Serie/Pelicula)
g.add((SPACE.tienePuntuacion, RDF.type, RDF.Property))
g.add((SPACE.tienePuntuacion, RDFS.domain, SPACE.Contenido))
g.add((SPACE.tienePuntuacion, RDFS.range, XSD.float))

# Propiedad 8: tieneEpisodios (Número de episodios en una Serie)
g.add((SPACE.tieneEpisodios, RDF.type, RDF.Property))
g.add((SPACE.tieneEpisodios, RDFS.domain, SPACE.Serie))
g.add((SPACE.tieneEpisodios, RDFS.range, XSD.int))

# Propiedad 9: tieneClasificacion( por edades)
g.add((SPACE.tieneClasificacion, RDF.type, RDF.Property))
g.add((SPACE.tieneClasificacion, RDFS.domain, SPACE.Contenido))  # Serie o Película
g.add((SPACE.tieneClasificacion, RDFS.range, SPACE.ClasificacionEdad))

# Propiedad 10  relacionContenido
g.add((SPACE.relacionContenido, RDF.type, RDF.Property))
g.add((SPACE.relacionContenido, RDFS.domain, SPACE.Contenido))
g.add((SPACE.relacionContenido, RDFS.range, SPACE.Contenido))

# Subpropiedad: basadaEnPelicula (cuando una serie se basa en una película)
g.add((SPACE.basadaEnPelicula, RDF.type, RDF.Property))
g.add((SPACE.basadaEnPelicula, RDFS.domain, SPACE.Serie))
g.add((SPACE.basadaEnPelicula, RDFS.range, SPACE.Pelicula))
g.add((SPACE.basadaEnPelicula, RDFS.subPropertyOf, SPACE.relacionContenido))


# === Instancias ===

# === Idiomas ===
idiomas = {
    "espanol": "Espa\u00f1ol",
    "ingles": "Ingl\u00e9s",
    "frances": "Franc\u00e9s",
    "aleman": "Alem\u00e1n",
    "japones": "Japon\u00e9s"
}
for k, v in idiomas.items():
    g.add((SPACE[k], RDF.type, SPACE.Idioma))
    g.add((SPACE[k], RDFS.label, Literal(v)))

# === Formatos ===
formatos = ["HD", "SD", "4K", "BluRay", "Streaming"]
for fmt in formatos:
    fmt_uri = SPACE[fmt.replace(" ", "")]
    g.add((fmt_uri, RDF.type, SPACE.Formato))

# === Clasificaciones por Edad ===
edades = ["TP", "+7", "+13", "+16", "+18"]
for ed in edades:
    clas_uri = SPACE["Edad" + ed.replace("+", "Plus")]
    g.add((clas_uri, RDF.type, SPACE.ClasificacionEdad))

# === Generos ===
generos = ["Comedia", "Drama", "Accion"]
for gen in generos:
    g.add((SPACE[gen], RDF.type, SPACE.Genero))

# === Directores ===
directores = [
    ("nolan", "Christopher Nolan"),
    ("spielberg", "Steven Spielberg"),
    ("tarantino", "Quentin Tarantino"),
    ("wachowski", "Lana Wachowski"),
    ("bigelow", "Kathryn Bigelow")
]
for uri, name in directores:
    g.add((SPACE[uri], RDF.type, SPACE.Director))
    g.add((SPACE[uri], RDFS.label, Literal(name)))

# === Actores ===
actores = [
    ("dicaprio", "Leonardo DiCaprio"),
    ("winslet", "Kate Winslet"),
    ("reeves", "Keanu Reeves"),
    ("washington", "Denzel Washington"),
    ("watson", "Emma Watson")
]
for uri, name in actores:
    g.add((SPACE[uri], RDF.type, SPACE.Actor))
    g.add((SPACE[uri], RDFS.label, Literal(name)))

# === Peliculas ===
peliculas = [
    ("inception", "Inception", "nolan", "dicaprio", "ingles", "4K", 148, 8.8, "Accion", "EdadPlus13"),
    ("matrix", "The Matrix", "wachowski", "reeves", "ingles", "BluRay", 136, 8.7, "Accion", "EdadPlus16"),
    ("titanic", "Titanic", "cameron", "winslet", "espanol", "HD", 195, 7.8, "Drama", "EdadPlus13"),
    ("django", "Django Unchained", "tarantino", "washington", "ingles", "4K", 165, 8.4, "Accion", "EdadPlus18"),
    ("harrypotter", "Harry Potter", "columbus", "watson", "ingles", "Streaming", 152, 7.6, "Comedia", "EdadPlus7")
]

# Algunos directores no definidos aún
extra_directores = {
    "cameron": "James Cameron",
    "columbus": "Chris Columbus"
}
for uri, name in extra_directores.items():
    g.add((SPACE[uri], RDF.type, SPACE.Director))
    g.add((SPACE[uri], RDFS.label, Literal(name)))

for uri, title, director, actor, idioma, formato, dur, punt, genero, clasif in peliculas:
    g.add((SPACE[uri], RDF.type, SPACE.Pelicula))
    g.add((SPACE[uri], SPACE.tieneDirector, SPACE[director]))
    g.add((SPACE[uri], SPACE.tieneActor, SPACE[actor]))
    g.add((SPACE[uri], SPACE.tieneIdioma, SPACE[idioma]))
    g.add((SPACE[uri], SPACE.tieneFormato, SPACE[formato]))
    g.add((SPACE[uri], SPACE.tieneDuracion, Literal(dur, datatype=XSD.int)))
    g.add((SPACE[uri], SPACE.tienePuntuacion, Literal(punt, datatype=XSD.float)))
    g.add((SPACE[uri], SPACE.tieneGenero, SPACE[genero]))
    g.add((SPACE[uri], SPACE.tieneClasificacion, SPACE[clasif]))

# === Series ===
series = [
    ("breakingbad", "Breaking Bad", "gilligan", "cranston", "espanol", "HD", 62, 9.5, "Drama", "EdadPlus16", "titanic"),
    ("friends", "Friends", "bright", "aniston", "ingles", "SD", 236, 8.9, "Comedia", "TP", None),
    ("theboys", "The Boys", "goldberg", "urban", "ingles", "4K", 24, 8.7, "Accion", "EdadPlus18", "inception"),
    ("dark", "Dark", "bood", "weise", "aleman", "Streaming", 26, 8.8, "Drama", "EdadPlus13", None),
    ("lupin", "Lupin", "sy", "omay", "frances", "Streaming", 15, 7.8, "Accion", "EdadPlus13", "matrix")
]

# Directores y actores faltantes en series
series_extra = {
    "gilligan": "Vince Gilligan",
    "bright": "Kevin Bright",
    "goldberg": "Evan Goldberg",
    "bood": "Baran bo Odar",
    "sy": "Louis Leterrier",
    "cranston": "Bryan Cranston",
    "aniston": "Jennifer Aniston",
    "urban": "Karl Urban",
    "weise": "Lisa Weise",
    "omay": "Omar Sy"
}

for uri, name in series_extra.items():
    role = SPACE.Director if uri in ["gilligan", "bright", "goldberg", "bood", "sy"] else SPACE.Actor
    g.add((SPACE[uri], RDF.type, role))
    g.add((SPACE[uri], RDFS.label, Literal(name)))

for uri, title, director, actor, idioma, formato, epis, punt, genero, clasif, based in series:
    g.add((SPACE[uri], RDF.type, SPACE.Serie))
    g.add((SPACE[uri], SPACE.tieneDirector, SPACE[director]))
    g.add((SPACE[uri], SPACE.tieneActor, SPACE[actor]))
    g.add((SPACE[uri], SPACE.tieneIdioma, SPACE[idioma]))
    g.add((SPACE[uri], SPACE.tieneFormato, SPACE[formato]))
    g.add((SPACE[uri], SPACE.tieneEpisodios, Literal(epis, datatype=XSD.int)))
    g.add((SPACE[uri], SPACE.tienePuntuacion, Literal(punt, datatype=XSD.float)))
    g.add((SPACE[uri], SPACE.tieneGenero, SPACE[genero]))
    g.add((SPACE[uri], SPACE.tieneClasificacion, SPACE[clasif]))
    if based:
        g.add((SPACE[uri], SPACE.basadaEnPelicula, SPACE[based]))


# == Inferencias ==

# --- Aplicar razonamiento ---
DeductiveClosure(RDFS_Semantics).expand(g)

# --- Casos de inferencia a documentar ---

# === Caso 1. Jerarquía de Clases ===
print("\n--- Caso 1: Jerarquía de Clases ---")
for s in g.subjects(RDF.type, SPACE.Contenido):
    print(f"{s.split('/')[-1]} es inferido como Contenido")

# === Caso 2. Inferencia por dominio o rango ===
print("\n--- Caso 2: Inferencia por Dominio usando tieneEpisodios ---")
for s, o in g.subject_objects(SPACE.tieneEpisodios):
    s_type = list(g.objects(s, RDF.type))
    
    s_str = s.split('/')[-1]
    o_str = str(o)  # o puede ser un Literal
    
    s_type_str = [t.split('/')[-1] for t in s_type if t == SPACE.Serie]
    
    print(f"{s_str} tieneEpisodios {o_str}")
    print(f"  -> {s_str} tipo inferido: {s_type_str}")




# Guardamos las triples antes de la inferencia
original_triples = set(g)


# Mostrar inferencias de subpropiedades
print("\n--- Caso 3: Inferencias por subPropertyOf (basadaEnPelicula -> relacionContenido) ---")
for s, o in g.subject_objects(SPACE.basadaEnPelicula):
    if (s, SPACE.relacionContenido, o) in g:
        s_str = s.split('/')[-1]
        o_str = o.split('/')[-1]
        print(f"{s_str} relacionContenido {o_str}")




# Serialización en Turtle
#print(g.serialize(format="turtle"))
