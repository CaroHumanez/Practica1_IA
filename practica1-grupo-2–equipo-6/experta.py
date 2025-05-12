from experta import Fact, KnowledgeEngine, Rule, Field
from rdflib import Graph, Namespace
from owlrl import DeductiveClosure, RDFS_Semantics
from ontologia import cargar_grafo


# Cargar grafo y namespace
g, SPACE = cargar_grafo()

# --------------------------
# DEFINICIÓN DE HECHOS
# --------------------------

class Pelicula(Fact):
    nombre = Field(str, mandatory=True)
    genero = Field(str, mandatory=True)
    clasificacion = Field(str, mandatory=True)
    idioma = Field(str, mandatory=True)
    formato = Field(str, mandatory=True)

class Serie(Fact):
    nombre = Field(str, mandatory=True)
    genero = Field(str, mandatory=True)
    clasificacion = Field(str, mandatory=True)
    idioma = Field(str, mandatory=True)
    formato = Field(str, mandatory=True)


# --------------------------
# EXTRAER PELÍCULAS Y SERIES
# --------------------------

peliculas = []
series = []

for tipo, lista in [(SPACE.Pelicula, peliculas), (SPACE.Serie, series)]:
    for s in g.subjects(predicate=None, object=tipo):
        nombre = s.split("#")[-1]

        genero_uri = g.value(s, SPACE.tieneGenero)
        clasif_uri = g.value(s, SPACE.tieneClasificacion)
        idioma_uri = g.value(s, SPACE.tieneIdioma)
        formato_uri = g.value(s, SPACE.tieneFormato)

        if genero_uri and clasif_uri and idioma_uri and formato_uri:
            lista.append({
                "nombre": nombre,
                "genero": genero_uri.split("#")[-1],
                "clasificacion": clasif_uri.split("#")[-1],
                "idioma": idioma_uri.split("#")[-1],
                "formato": formato_uri.split("#")[-1]
            })

# --------------------------
# SISTEMA EXPERTO
# --------------------------

class MotorRecomendacion(KnowledgeEngine):

    def cargar_peliculas(self, peliculas):
        for p in peliculas:
            self.declare(Pelicula(
                nombre=p["nombre"],
                genero=p["genero"],
                clasificacion=p["clasificacion"],
                idioma=p["idioma"],
                formato=p["formato"]
            ))

    def cargar_series(self, series):
        for s in series:
            self.declare(Serie(
                nombre=s["nombre"],
                genero=s["genero"],
                clasificacion=s["clasificacion"],
                idioma=s["idioma"],
                formato=s["formato"]
            ))

        @Rule(
        Usuario(prefiereGenero=MATCH.g),
        Pelicula(genero=MATCH.g, titulo=MATCH.t)
        )
        def recomendar_pelicula(self, g, t):
            print(f"Recomendación: Te podría gustar '{t}' del género {g}.")

