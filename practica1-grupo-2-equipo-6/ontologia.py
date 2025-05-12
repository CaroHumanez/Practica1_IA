from re import S
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, FOAF, XSD, DC, DCTERMS
from rdflib.collection import Collection
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD
from owlrl import DeductiveClosure, RDFS_Semantics

g = Graph()
SPACE = Namespace("ht+7://SPACEample.org/space/")

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
g.add((SPACE.Plataforma, RDF.type, RDFS.Class))
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

# Propiedad 11  disponibleEn
g.add((SPACE.disponibleEn, RDF.type, RDF.Property))
g.add((SPACE.disponibleEn, RDFS.domain, SPACE.Contenido))
g.add((SPACE.disponibleEn, RDFS.range, SPACE.Plataforma))

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
edades = ["+7", "+16", "+18"]
for ed in edades:
    if ed == "+7":
        clas_uri = SPACE["nino"]
        g.add((clas_uri, RDF.type, SPACE.ClasificacionEdad))
    elif ed == "+16":
        clas_uri = SPACE["adolescente"]
        g.add((clas_uri, RDF.type, SPACE.ClasificacionEdad))
    elif ed == "+18":
        clas_uri = SPACE["adulto"]
        g.add((clas_uri, RDF.type, SPACE.ClasificacionEdad))


# === Géneros ===
generos = ["CienciaFiccion", "Comedia", "Terror", "Drama", "Documental"]
for gen in generos:
    g.add((SPACE[gen], RDF.type, SPACE.Genero))

# === Plataforma ===
plataformas = ["Netflix", "DisneyPlus", "HBO_Max"]

for plat in plataformas:
    plat_uri = SPACE[plat.replace("+", "Plus").replace(" ", "_")]
    g.add((plat_uri, RDF.type, SPACE.Plataforma))

# === Directores ===
directores = [
    ("nolan", "Christopher Nolan"),
    ("spielberg", "Steven Spielberg"),
    ("tarantino", "Quentin Tarantino"),
    ("wachowski", "Lana Wachowski"),
    ("bigelow", "Kathryn Bigelow"),
    ("peele", "Jordan Peele"),
    ("scott", "Ridley Scott"),
    ("greta", "Greta Gerwig"),
    ("zhao", "Chloé Zhao"),
    ("morris", "Errol Morris")
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
    ("watson", "Emma Watson"),
    ("theron", "Charlize Theron"),
    ("isaac", "Oscar Isaac"),
    ("jovovich", "Milla Jovovich"),
    ("nyong", "Lupita Nyong'o"),
    ("murray", "Bill Murray"),
    ("bale", "Christian Bale"),
    ("gyllenhaal", "Maggie Gyllenhaal"),
    ("burns", "Ken Burns")
]
for uri, name in actores:
    g.add((SPACE[uri], RDF.type, SPACE.Actor))
    g.add((SPACE[uri], RDFS.label, Literal(name)))

# === Películas ===
plataformas = ["Netflix", "DisneyPlus", "HBO_Max"]

peliculas = [
    ("inception", "Inception", "nolan", "dicaprio", "ingles", "4K", 148, 8.8, "CienciaFiccion", "+16", "Netflix"),
    ("matrix", "The Matrix", "wachowski", "reeves", "ingles", "BluRay", 136, 8.7, "CienciaFiccion", "+16", "DisneyPlus"),
    ("prometheus", "Prometheus", "scott", "theron", "espanol", "HD", 124, 7.0, "CienciaFiccion", "+16", "HBO_Max"),
    ("dune", "Dune", "scott", "isaac", "frances", "Streaming", 155, 8.1, "CienciaFiccion", "+16", "Netflix"),
    
    ("ghostbusters", "Ghostbusters", "reitman", "murray", "ingles", "SD", 105, 7.8, "Comedia", "+7", "DisneyPlus"),
    ("barbie", "Barbie", "greta", "watson", "espanol", "4K", 114, 7.2, "Comedia", "EdadPlus7", "HBO_Max"),
    ("frenchdispatch", "The French Dispatch", "anderson", "bale", "frances", "BluRay", 108, 7.4, "Comedia", "+16", "Netflix"),
    ("meanGirls", "Mean Girls", "waters", "gyllenhaal", "ingles", "HD", 97, 7.0, "Comedia", "+16", "DisneyPlus"),
    
    ("getout", "Get Out", "peele", "washington", "ingles", "4K", 104, 7.7, "Terror", "+16", "HBO_Max"),
    ("us", "Us", "peele", "nyong", "espanol", "Streaming", 116, 6.8, "Terror", "+16", "Netflix"),
    ("residentEvil", "Resident Evil", "anderson", "jovovich", "frances", "HD", 100, 6.7, "Terror", "+16", "DisneyPlus"),
    ("babadook", "The Babadook", "kent", "winslet", "ingles", "BluRay", 93, 6.8, "Terror", "+16", "HBO_Max"),

    ("titanic", "Titanic", "cameron", "winslet", "espanol", "HD", 195, 7.8, "Drama", "+16", "Netflix"),
    ("interstellar", "Interstellar", "nolan", "dicaprio", "ingles", "4K", 169, 8.6, "Drama", "+16", "DisneyPlus"),
    ("nomadland", "Nomadland", "zhao", "watson", "frances", "Streaming", 108, 7.3, "Drama", "+16", "HBO_Max"),
    ("littleWomen", "Little Women", "greta", "watson", "ingles", "BluRay", 135, 7.8, "Drama", "+16", "Netflix"),

    ("fogofwar", "The Fog of War", "morris", "washington", "ingles", "SD", 95, 8.2, "Documental", "+16", "DisneyPlus"),
    ("13th", "13th", "duvernay", "washington", "espanol", "Streaming", 100, 8.3, "Documental", "+16", "HBO_Max"),
    ("citizenfour", "Citizenfour", "poitras", "watson", "frances", "HD", 114, 8.0, "Documental", "+16", "Netflix"),
    ("civilwar", "The Civil War", "burns", "burns", "ingles", "BluRay", 70, 8.9, "Documental", "+7", "DisneyPlus")
]


# Directores extra
extra_directores = {
    "cameron": "James Cameron",
    "anderson": "Wes Anderson",
    "reitman": "Ivan Reitman",
    "greta": "Greta Gerwig",
    "scott": "Ridley Scott",
    "peele": "Jordan Peele",
    "duvernay": "Ava DuVernay",
    "poitras": "Laura Poitras",
    "kent": "Jennifer Kent",
    "zhao": "Chloé Zhao",
    "burns": "Ken Burns",
    "waters": "Mark Waters"
}
for uri, name in extra_directores.items():
    g.add((SPACE[uri], RDF.type, SPACE.Director))
    g.add((SPACE[uri], RDFS.label, Literal(name)))

for uri, title, director, actor, idioma, formato, dur, punt, genero, clasif, plataforma in peliculas:
    g.add((SPACE[uri], RDF.type, SPACE.Pelicula))
    g.add((SPACE[uri], SPACE.tieneDirector, SPACE[director]))
    g.add((SPACE[uri], SPACE.tieneActor, SPACE[actor]))
    g.add((SPACE[uri], SPACE.tieneIdioma, SPACE[idioma]))
    g.add((SPACE[uri], SPACE.tieneFormato, SPACE[formato]))
    g.add((SPACE[uri], SPACE.tieneDuracion, Literal(dur, datatype=XSD.int)))
    g.add((SPACE[uri], SPACE.tienePuntuacion, Literal(punt, datatype=XSD.float)))
    g.add((SPACE[uri], SPACE.tieneGenero, SPACE[genero]))
    g.add((SPACE[uri], SPACE.tieneClasificacion, SPACE[clasif]))
    g.add((SPACE[uri], SPACE.disponibleEn, SPACE[plataforma]))

# === Series ===
series = [
    ("strangerthings", "Stranger Things", "duffer", "brown", "ingles", "4K", 34, 8.7, "CienciaFiccion", "+16", "contact", "Netflix"),
    ("chernobyl", "Chernobyl", "mazin", "harris", "ingles", "BluRay", 5, 9.4, "Drama", "+16", None, "DisneyPlus"),
    ("dark", "Dark", "bood", "weise", "aleman", "Streaming", 26, 8.8, "CienciaFiccion", "+16", None, "HBO_Max"),
    ("blackmirror", "Black Mirror", "brooker", "mara", "ingles", "Streaming", 27, 8.8, "CienciaFiccion", "+16", None, "Netflix"),
    ("theoffice", "The Office", "daniels", "carell", "ingles", "HD", 201, 8.9, "Comedia", "+7", None, "DisneyPlus"),
    ("lupin", "Lupin", "sy", "omay", "frances", "Streaming", 15, 7.8, "Drama", "+16", "gravity", "HBO_Max"),
    ("hillhouse", "The Haunting of Hill House", "flanagan", "pedretti", "ingles", "HD", 10, 8.6, "Terror", "+16", "psycho", "Netflix"),
    ("cosmos", "Cosmos: A Spacetime Odyssey", "tyson", "tyson", "ingles", "Streaming", 13, 9.3, "Documental", "+7", None, "DisneyPlus"),
    ("loveDeathRobots", "Love, Death & Robots", "miller", "bernal", "espanol", "4K", 35, 8.4, "CienciaFiccion", "+18", None, "HBO_Max"),
    ("modernfamily", "Modern Family", "levitan", "vergara", "ingles", "HD", 250, 8.5, "Comedia", "+7", None, "Netflix"),
    ("makingamurderer", "Making a Murderer", "demos", "avery", "ingles", "Streaming", 20, 8.6, "Documental", "+16", None, "DisneyPlus"),
    ("marianne", "Marianne", "siri", "bela", "frances", "Streaming", 8, 7.5, "Terror", "+18", None, "HBO_Max")
]

# Directores y actores faltantes en series
series_extra = {
    "duffer": "Duffer Brothers",
    "mazin": "Craig Mazin",
    "brooker": "Charlie Brooker",
    "daniels": "Greg Daniels",
    "sy": "Louis Leterrier",
    "flanagan": "Mike Flanagan",
    "tyson": "Neil deGrasse Tyson",
    "miller": "Tim Miller",
    "levitan": "Steven Levitan",
    "demos": "Laura Ricciardi",
    "siri": "Samuel Bodin",

    "brown": "Millie Bobby Brown",
    "harris": "Jared Harris",
    "weise": "Lisa Weise",
    "mara": "Kate Mara",
    "carell": "Steve Carell",
    "omay": "Omar Sy",
    "pedretti": "Victoria Pedretti",
    "bernal": "Gael García Bernal",
    "vergara": "Sofía Vergara",
    "avery": "Steven Avery",
    "bela": "Lucie Boujenah"
}

for uri, name in series_extra.items():
    role = SPACE.Director if uri in [
        "duffer", "mazin", "brooker", "daniels", "sy", "flanagan",
        "tyson", "miller", "levitan", "demos", "siri"
    ] else SPACE.Actor
    g.add((SPACE[uri], RDF.type, role))
    g.add((SPACE[uri], RDFS.label, Literal(name)))

for uri, title, director, actor, idioma, formato, epis, punt, genero, clasif, based, plataforma in series:
    g.add((SPACE[uri], RDF.type, SPACE.Serie))
    g.add((SPACE[uri], SPACE.tieneDirector, SPACE[director]))
    g.add((SPACE[uri], SPACE.tieneActor, SPACE[actor]))
    g.add((SPACE[uri], SPACE.tieneIdioma, SPACE[idioma]))
    g.add((SPACE[uri], SPACE.tieneFormato, SPACE[formato]))
    g.add((SPACE[uri], SPACE.tieneEpisodios, Literal(epis, datatype=XSD.int)))
    g.add((SPACE[uri], SPACE.tienePuntuacion, Literal(punt, datatype=XSD.float)))
    g.add((SPACE[uri], SPACE.tieneGenero, SPACE[genero]))
    g.add((SPACE[uri], SPACE.tieneClasificacion, SPACE[clasif]))
    g.add((SPACE[uri], SPACE.disponibleEn, SPACE[plataforma]))
    if based:
        g.add((SPACE[uri], SPACE.basadaEnPelicula, SPACE[based]))



#guardo el grafo antes de las inferencias
grafo_original = Graph()
for triple in g:
    grafo_original.add(triple)

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

# Mostrar inferencias de subpropiedades
print("\n--- Caso 3: Inferencias por subPropertyOf (basadaEnPelicula -> relacionContenido) ---")
for s, o in g.subject_objects(SPACE.basadaEnPelicula):
    if (s, SPACE.relacionContenido, o) in g:
        s_str = s.split('/')[-1]
        o_str = o.split('/')[-1]
        print(f"{s_str} relacionContenido {o_str}")

#Coparacion de grafos
# Tripletas inferidas = las que están en g pero no en original_graph
inferred_triples = set(g) - set(grafo_original)

print("\n--- Nuevos hechos inferidos automáticamente ---")
# Filtrar para mostrar solo inferencias que tengan que ver con películas/series
for triple in inferred_triples:
    # Asegurarnos de que la inferencia esté relacionada con películas o series
    if (triple[0], RDF.type, SPACE.Pelicula) in g or (triple[0], RDF.type, SPACE.Serie) in g:
        print(triple)


# Serialización en Turtle
print(g.serialize(format="turtle"))


def cargar_grafo():
    DeductiveClosure(RDFS_Semantics).expand(g)
    return g, SPACE
