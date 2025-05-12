from experta import Fact, KnowledgeEngine, Rule, Field, MATCH
from rdflib import Graph, Namespace
from owlrl import DeductiveClosure, RDFS_Semantics
from ontologia import cargar_grafo

# Cargar grafo y namespace
g, SPACE = cargar_grafo()

# --------------------------
# DEFINICIÓN DE HECHOS (5 clases de hechos)
# --------------------------

class Pelicula(Fact):
    """
    Representa una película con sus atributos.
    """
    nombre = ""
    genero = ""
    clasificacion = ""
    idioma = ""
    formato = ""
    

class Serie(Fact):
    """
    Representa una serie con sus atributos.
    """
    nombre = ""
    genero = ""
    clasificacion = ""
    idioma = ""
    formato = ""

class Usuario(Fact):
    """
    Representa a un usuario con sus preferencias.
    """
    genero = Field(str, default="")
    idioma = Field(str, default="")
    formato = Field(str, default="")
    clasificacion_edad = Field(str, default="")

class Preferencia(Fact):
    """
    Representa el tipo de preferencia del usuario (Película o Serie).
    """
    tipo = ""

class NivelRecomendacion(Fact):
    """
    Representa el nivel de recomendación deseado.
    """
    nivel = ""

class PlataformaPreferida(Fact):
    """Representa la plataforma preferida del usuario."""
    plataforma = Field(str)

# --------------------------
# EXTRAER PELÍCULAS Y SERIES
# --------------------------

# Renombrar las listas para evitar conflictos de nombres
peliculas_lista = []
series_lista = []

for tipo, lista in [(SPACE.Pelicula, peliculas_lista), (SPACE.Serie, series_lista)]:
    print(f"Extrayendo {tipo.split('#')[-1]}...")
    for s in g.subjects(predicate=None, object=tipo):
        nombre = s.split("#")[-1]

        genero_uri = g.value(s, SPACE.tieneGenero)
        clasif_uri = g.value(s, SPACE.tieneClasificacion)
        idioma_uri = g.value(s, SPACE.tieneIdioma)
        formato_uri = g.value(s, SPACE.tieneFormato)

        if genero_uri and clasif_uri and idioma_uri and formato_uri:
            genero = genero_uri.split("#")[-1]
            idioma = idioma_uri.split("#")[-1]
            formato = formato_uri.split("#")[-1]
            print(f"  Nombre: {nombre}, Género: {genero}, Idioma: {idioma}, Formato: {formato}")
            lista.append({
                "nombre": nombre,
                "genero": genero,
                "clasificacion": clasif_uri.split("#")[-1],
                "idioma": idioma,
                "formato": formato
            })

# Asegurar que las listas sean accesibles con nombres únicos
peliculas = list(peliculas_lista)
series = list(series_lista)

# --------------------------
# SISTEMA EXPERTO
# --------------------------

class MotorRecomendacion(KnowledgeEngine):
    def __init__(self, peliculas, series):
        super().__init__()
        self.peliculas_ontologia = peliculas
        self.series_ontologia = series

    def cargar_hechos_iniciales(self):
        """
        Carga los hechos iniciales desde la ontología. Mapea las clasificaciones.
        """
        clasificacion_map = {
            "EdadPlus13": 13,
            "EdadPlus16": 16,
            "EdadPlus18": 18,
            "General": 0
        }

        for p in self.peliculas_ontologia:
            clasificacion = clasificacion_map.get(p["clasificacion"].split("#")[-1], 0)
            self.declare(Pelicula(nombre=p["nombre"], genero=p["genero"], clasificacion=clasificacion, idioma=p["idioma"], formato=p["formato"]))

        for s in self.series_ontologia:
            clasificacion = clasificacion_map.get(s["clasificacion"].split("#")[-1], 0)
            self.declare(Serie(nombre=s["nombre"], genero=s["genero"], clasificacion=clasificacion, idioma=s["idioma"], formato=s["formato"]))

    # High-priority rules
    @Rule(Preferencia(tipo="Serie"), Usuario(genero=MATCH.genero, idioma=MATCH.idioma), NivelRecomendacion(nivel=MATCH.n), salience=30)
    def recomendar_serie_optimizada(self, genero, idioma, n):
        mejores_series = [serie for serie in self.series_ontologia if serie['genero'] == genero and serie['idioma'] == idioma]
        if mejores_series:
            mejor_serie = max(mejores_series, key=lambda s: int(s['clasificacion']))
            self.declare(Fact(serie_recomendada=mejor_serie['nombre'], nivel=n))
            self.halt()

    @Rule(Preferencia(tipo="Pelicula"), Usuario(genero=MATCH.genero, idioma=MATCH.idioma), NivelRecomendacion(nivel=MATCH.n), salience=30)
    def recomendar_pelicula_optimizada(self, genero, idioma, n):
        mejores_peliculas = [pelicula for pelicula in self.peliculas_ontologia if pelicula['genero'] == genero and pelicula['idioma'] == idioma]
        if mejores_peliculas:
            mejor_pelicula = max(mejores_peliculas, key=lambda p: int(p['clasificacion']))
            self.declare(Fact(pelicula_recomendada=mejor_pelicula['nombre'], nivel=n))
            self.halt()

    # High-priority rules based on format and score
    @Rule(Preferencia(tipo="Serie"), Usuario(formato=MATCH.formato), NivelRecomendacion(nivel=MATCH.n), salience=30)
    def recomendar_serie_por_formato_y_puntuacion(self, formato, n):
        mejores_series = [serie for serie in self.series_ontologia if serie['formato'] == formato]
        if mejores_series:
            mejor_serie = max(mejores_series, key=lambda s: int(s['clasificacion']))
            self.declare(Fact(serie_recomendada=mejor_serie['nombre'], nivel=n))
            self.halt()

    @Rule(Preferencia(tipo="Pelicula"), Usuario(formato=MATCH.formato), NivelRecomendacion(nivel=MATCH.n), salience=30)
    def recomendar_pelicula_por_formato_y_puntuacion(self, formato, n):
        mejores_peliculas = [pelicula for pelicula in self.peliculas_ontologia if pelicula['formato'] == formato]
        if mejores_peliculas:
            mejor_pelicula = max(mejores_peliculas, key=lambda p: int(p['clasificacion']))
            self.declare(Fact(pelicula_recomendada=mejor_pelicula['nombre'], nivel=n))
            self.halt()

    # Medium-priority rules
    @Rule(Preferencia(tipo="Serie"), Usuario(genero="CienciaFiccion", idioma="español"), NivelRecomendacion(nivel=MATCH.n), salience=20)
    def serie_ficcion_es(self, n):
        for serie in self.series_ontologia:
            if serie['genero'] == "CienciaFiccion" and serie['idioma'] == "español":
                self.declare(Fact(serie_recomendada=serie['nombre'], nivel=n))
                self.halt()

    @Rule(Preferencia(tipo="Pelicula"), Usuario(genero="CienciaFiccion", idioma="español"), NivelRecomendacion(nivel=MATCH.n), salience=20)
    def peli_ficcion_es(self, n):
        for pelicula in self.peliculas_ontologia:
            if pelicula['genero'] == "CienciaFiccion" and pelicula['idioma'] == "español":
                self.declare(Fact(pelicula_recomendada=pelicula['nombre'], nivel=n))
                self.halt()

    # Medium-priority rules combining genre, language, and format
    @Rule(Preferencia(tipo="Serie"), Usuario(genero=MATCH.genero, idioma=MATCH.idioma, formato=MATCH.formato), NivelRecomendacion(nivel=MATCH.n), salience=20)
    def serie_por_genero_idioma_y_formato(self, genero, idioma, formato, n):
        for serie in self.series_ontologia:
            if serie['genero'] == genero and serie['idioma'] == idioma and serie['formato'] == formato:
                self.declare(Fact(serie_recomendada=serie['nombre'], nivel=n))
                self.halt()

    @Rule(Preferencia(tipo="Pelicula"), Usuario(genero=MATCH.genero, idioma=MATCH.idioma, formato=MATCH.formato), NivelRecomendacion(nivel=MATCH.n), salience=20)
    def pelicula_por_genero_idioma_y_formato(self, genero, idioma, formato, n):
        for pelicula in self.peliculas_ontologia:
            if pelicula['genero'] == genero and pelicula['idioma'] == idioma and pelicula['formato'] == formato:
                self.declare(Fact(pelicula_recomendada=pelicula['nombre'], nivel=n))
                self.halt()

    # Low-priority rules
    @Rule(Preferencia(tipo="Serie"), Usuario(genero=MATCH.g), NivelRecomendacion(nivel=MATCH.n), salience=3)
    def serie_por_genero(self, n, g):
        for serie in self.series_ontologia:
            if serie['genero'] == g:
                self.declare(Fact(serie_recomendada=serie['nombre'], nivel=n))
                self.halt()

    @Rule(Preferencia(tipo="Pelicula"), Usuario(genero=MATCH.g), NivelRecomendacion(nivel=MATCH.n), salience=3)
    def pelicula_por_genero(self, n, g):
        for pelicula in self.peliculas_ontologia:
            if pelicula['genero'] == g:
                self.declare(Fact(pelicula_recomendada=pelicula['nombre'], nivel=n))
                self.halt()

    # Low-priority rules based on format only
    @Rule(Preferencia(tipo="Serie"), Usuario(formato=MATCH.formato), NivelRecomendacion(nivel=MATCH.n), salience=3)
    def serie_por_formato(self, formato, n):
        for serie in self.series_ontologia:
            if serie['formato'] == formato:
                self.declare(Fact(serie_recomendada=serie['nombre'], nivel=n))
                self.halt()

    @Rule(Preferencia(tipo="Pelicula"), Usuario(formato=MATCH.formato), NivelRecomendacion(nivel=MATCH.n), salience=3)
    def pelicula_por_formato(self, formato, n):
        for pelicula in self.peliculas_ontologia:
            if pelicula['formato'] == formato:
                self.declare(Fact(pelicula_recomendada=pelicula['nombre'], nivel=n))
                self.halt()

    # Wildcard rules
    @Rule(Preferencia(tipo="Serie"), NivelRecomendacion(nivel=MATCH.n), salience=1)
    def serie_comodin(self, n):
        if self.series_ontologia:
            self.declare(Fact(serie_recomendada=self.series_ontologia[0]['nombre'], nivel=n))
            self.halt()

    @Rule(Preferencia(tipo="Pelicula"), NivelRecomendacion(nivel=MATCH.n), salience=1)
    def pelicula_comodin(self, n):
        if self.peliculas_ontologia:
            self.declare(Fact(pelicula_recomendada=self.peliculas_ontologia[0]['nombre'], nivel=n))
            self.halt()

    # Wildcard rules based on minimum score
    @Rule(Preferencia(tipo="Serie"), NivelRecomendacion(nivel=MATCH.n), salience=1)
    def serie_comodin_por_puntuacion(self, n):
        if self.series_ontologia:
            mejor_serie = max(self.series_ontologia, key=lambda s: int(s['clasificacion']))
            self.declare(Fact(serie_recomendada=mejor_serie['nombre'], nivel=n))
            self.halt()

    @Rule(Preferencia(tipo="Pelicula"), NivelRecomendacion(nivel=MATCH.n), salience=1)
    def pelicula_comodin_por_puntuacion(self, n):
        if self.peliculas_ontologia:
            mejor_pelicula = max(self.peliculas_ontologia, key=lambda p: int(p['clasificacion']))
            self.declare(Fact(pelicula_recomendada=mejor_pelicula['nombre'], nivel=n))
            self.halt()

