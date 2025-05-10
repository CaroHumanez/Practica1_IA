from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS

# Reutilizamos el grafo y namespace
SPACE = Namespace("http://SPACEample.org/space/")
g = Graph()

# Clases e individuos representativos
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

# Serializamos la parte nueva
print(g.serialize(format="turtle"))