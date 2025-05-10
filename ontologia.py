from re import S
from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, RDFS, FOAF, XSD, DC, DCTERMS
from rdflib.collection import Collection

g = Graph()
SPACE = Namespace("http://SPACEample.org/space/")

g.bind("space", SPACE)
g.bind("foaf", FOAF)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)
g.bind("dc", DC)
g.bind("dcterms", DCTERMS)


# === Clases ===
# Declaración de clases una por una
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

# Serialización en Turtle
print(g.serialize(format="turtle"))
