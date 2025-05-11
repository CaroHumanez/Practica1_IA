# === SISTEMA INTEGRADO: Ontología + Lógica Difusa + Sistema Experto ===

from experta import *
import streamlit as st
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

from experta import *
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS
from experta import *
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
from rdflib.plugins.sparql import prepareQuery

# === Ontología ===
g = Graph()
SPACE = Namespace("http://SPACEample.org/space/")
g.parse("ontologia.ttl", format="turtle")

q = prepareQuery("""
    SELECT ?genero ?idioma ?formato WHERE {
        ?contenido a space:Contenido .
        ?contenido space:tieneGenero ?genero .
        ?contenido space:tieneIdioma ?idioma .
        ?contenido space:tieneFormato ?formato .
    }
""", initNs={"space": SPACE})

# === Definición de los hechos ===

class Usuario(Fact):
    pass

class Genero_favorito(Fact):
    pass

class Idioma_preferido(Fact):
    pass

class Formato_preferido(Fact):
    pass

class Recomendacion(Fact):
    pass


# === Motor Sistema experto ===
# === Sistema experto ===
class MotorRecomendador(KnowledgeEngine):

    #1
    @Rule(Genero_favorito(valor="ciencia ficción"), Idioma_preferido(valor="Español"), Formato_preferido(valor="serie"), NOT(Fact(valor="evaluado")), salience=12)
    def recomendar_dark(self):
        print("🎯 Recomendación: Te recomendamos la serie *Dark*.")
        self.declare(Recomendacion(valor="Te recomendamos la serie Dark."))
        self.declare(Fact(valor="evaluado"))
        self.halt()

    #2
    @Rule(Genero_favorito(valor="drama"), Idioma_preferido(valor="Inglés"), Formato_preferido(valor="serie"), NOT(Fact(valor="evaluado")), salience=12)
    def recomendar_the_crown(self):
        print("🎯 Recomendación: Te recomendamos la serie *The Crown*.")
        self.declare(Recomendacion(valor="Te recomendamos la serie The Crown."))
        self.declare(Fact(valor="evaluado"))

    #3
    @Rule(Genero_favorito(valor="comedia"), Idioma_preferido(valor="italiano"), Formato_preferido(valor="película"), NOT(Fact(valor="evaluado")), salience=12)
    def recomendar_la_vida_es_bella(self):
        print("🎯 Recomendación: Te recomendamos la película *La vida es bella*.")
        self.declare(Recomendacion(valor="Te recomendamos la película La vida es bella."))
        self.declare(Fact(valor="evaluado"))

    #4
    @Rule(Genero_favorito(valor="ciencia ficción"), Idioma_preferido(valor="Inglés"), Formato_preferido(valor="película"), NOT(Fact(valor="evaluado")), salience=12)
    def recomendar_dune(self):
        print("🎯 Recomendación: Te recomendamos la película *Dune*.")
        self.declare(Recomendacion(valor="Te recomendamos la película Dune."))
        self.declare(Fact(valor="evaluado"))

    #5
    @Rule(Genero_favorito(valor="comedia"), Idioma_preferido(valor="Español"), Formato_preferido(valor="película"), NOT(Fact(valor="evaluado")), salience=12)
    def recomendar_el_paseo(self):
        print("🎯 Recomendación: Te recomendamos la película *El paseo*.")
        self.declare(Recomendacion(valor="Te recomendamos la película El paseo."))
        self.declare(Fact(valor="evaluado"))

    #6
    @Rule(Genero_favorito(valor="ciencia ficción"), Formato_preferido(valor="película"), NOT(Fact(valor="evaluado")), salience=9)
    def recomendar_interstellar(self):
        print("🎯 Recomendación: Te recomendamos la película *Interstellar*.")
        self.declare(Recomendacion(valor="Te recomendamos la película Interstellar."))
        self.declare(Fact(valor="evaluado"))

    #7
    @Rule(Genero_favorito(valor="drama"), Formato_preferido(valor="película"), NOT(Fact(valor="evaluado")), salience=9)
    def recomendar_Pianista(self):
        print("🎯 Recomendación: Te recomendamos la película *Pianista*.")
        self.declare(Recomendacion(valor="Te recomendamos la película Pianista."))
        self.declare(Fact(valor="evaluado"))

    #8
    @Rule(Genero_favorito(valor="policial"), Formato_preferido(valor="serie"), NOT(Fact(valor="evaluado")), salience=9)
    def recomendar_mentes_criminales(self):
        print("🎯 Recomendación: Te recomendamos la serie *Mentes criminales*.")
        self.declare(Recomendacion(valor="Te recomendamos la serie Mentes criminales."))
        self.declare(Fact(valor="evaluado"))

    #9
    @Rule(Genero_favorito(valor="documental"), Formato_preferido(valor="película"), NOT(Fact(valor="evaluado")), salience=9)
    def recomendar_camino_serpiente(self):
        print("🎯 Recomendación: Te recomendamos la película *El camino de la serpiente*.")
        self.declare(Recomendacion(valor="Te recomendamos la película El camino de la serpiente."))
        self.declare(Fact(valor="evaluado"))

    #10
    @Rule(Genero_favorito(valor="terror"), Formato_preferido(valor="película"), NOT(Fact(valor="evaluado")), salience=9)
    def recomendar_hannibal(self):
        print("🎯 Recomendación: Te recomendamos la película *Hannibal*.")
        self.declare(Recomendacion(valor="Te recomendamos la película Hannibal."))
        self.declare(Fact(valor="evaluado"))

    #11
    @Rule(Genero_favorito(valor="romance"), NOT(Fact(valor="evaluado")), salience=6)
    def recomendar_orgullo_prejuicio(self):
        print("🎯 Recomendación: Te recomendamos la película *Orgullo y Prejuicio*.")
        self.declare(Recomendacion(valor="Te recomendamos la película Orgullo y Prejuicio."))
        self.declare(Fact(valor="evaluado"))

    #12
    @Rule(Idioma_preferido(valor="francés"), NOT(Fact(valor="evaluado")), salience=5)
    def recomendar_amelie(self):
        print("🎯 Recomendación: Te recomendamos la película francesa *Amélie*.")
        self.declare(Recomendacion(valor="Te recomendamos la película francesa Amélie."))
        self.declare(Fact(valor="evaluado"))

    #13
    @Rule(Formato_preferido(valor="serie"), NOT(Fact(valor="evaluado")), salience=4)
    def recomendar_friends(self):
        print("🎯 Recomendación: Te recomendamos la serie clásica *Friends*.")
        self.declare(Recomendacion(valor="Te recomendamos la serie clásica Friends."))
        self.declare(Fact(valor="evaluado"))

    #14
    @Rule(Genero_favorito(valor="animación"), NOT(Fact(valor="evaluado")), salience=3)
    def recomendar_shrek(self):
        print("🎯 Recomendación: Te recomendamos la película animada *Shrek*.")
        self.declare(Recomendacion(valor="Te recomendamos la película animada Shrek."))
        self.declare(Fact(valor="evaluado"))

    #15
    @Rule(Idioma_preferido(valor="Inglés"), NOT(Fact(valor="evaluado")), salience=3)
    def recomendar_stranger_things(self):
        print("🎯 Recomendación: Te recomendamos la serie *Stranger Things*.")
        self.declare(Recomendacion(valor="Te recomendamos la serie Stranger Things."))
        self.declare(Fact(valor="evaluado"))

# === Sistema difuso ===
# Variables difusas
interes = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'interes')
apertura = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'apertura')
edad = ctrl.Antecedent(np.arange(0, 12.1, 0.1), 'edad')
recomendabilidad = ctrl.Consequent(np.arange(0, 101, 1), 'recomendabilidad')

# Función Modificadora
def modificacion(conjunto, potencia):
    return conjunto ** potencia

# Funciones de pertenencia: Interés del usuario
interes['bajo'] = fuzz.trimf(interes.universe, [0, 0, 4])
interes['medio'] = fuzz.trapmf(interes.universe, [3.5, 4.5, 5.5, 6.5])
interes['alto'] = fuzz.gaussmf(interes.universe, 8, 1.2)
interes['muy_interesado'] = modificacion(fuzz.gaussmf(interes.universe, 8, 1.2), 2)

# Funciones de pertenencia: Apertura a nuevos géneros
apertura['cerrado'] = fuzz.trapmf(apertura.universe, [0, 0, 2.5, 4])
apertura['neutral'] = fuzz.gaussmf(apertura.universe, 5, 1.5)
apertura['abierto'] = fuzz.trimf(apertura.universe, [6, 8, 10])
apertura['mas_menos_abierto'] = modificacion(fuzz.trimf(apertura.universe, [6, 8, 10]), 1/2)

# Funciones de pertenencia: Adecuación por edad
edad['nino'] = fuzz.trimf(edad.universe, [0, 0, 3])
edad['adolescente'] = fuzz.trapmf(edad.universe, [2, 4, 6, 8])
edad['adulto'] = fuzz.gaussmf(edad.universe, 9, 1)

# Funciones de pertenencia: Nivel de recomendabilidad
recomendabilidad['baja'] = fuzz.trapmf(recomendabilidad.universe, [0, 0, 20, 35])
recomendabilidad['media'] = fuzz.gaussmf(recomendabilidad.universe, 50, 10)
recomendabilidad['alta'] = fuzz.trapmf(recomendabilidad.universe, [65, 80, 100, 100])

# Reglas del sistema de recomendabilidad
reglas_recomendabilidad = [
    ctrl.Rule(interes['alto'] & apertura['abierto'], recomendabilidad['alta']),
    ctrl.Rule(interes['medio'] & apertura['neutral'], recomendabilidad['media']),
    ctrl.Rule(interes['bajo'] | apertura['cerrado'], recomendabilidad['baja']),
    ctrl.Rule(interes['muy_interesado'] & apertura['mas_menos_abierto'], recomendabilidad['alta']),
    ctrl.Rule(apertura['neutral'] & ~edad['nino'], recomendabilidad['media']),
    ctrl.Rule(interes['medio'] & edad['adulto'], recomendabilidad['media']),
    ctrl.Rule(edad['nino'] & ~apertura['abierto'], recomendabilidad['baja']),
    ctrl.Rule(interes['alto'] | edad['adolescente'], recomendabilidad['media']),
    ctrl.Rule(interes['muy_interesado'] & apertura['cerrado'] & edad['adulto'], recomendabilidad['media']),
]

# Sistema de control para recomendabilidad
sistema_recomendabilidad_ctrl = ctrl.ControlSystem(reglas_recomendabilidad)
sistema_recomendabilidad = ctrl.ControlSystemSimulation(sistema_recomendabilidad_ctrl)

# === Función para consultar la ontología RDF ===
def consultar_ontologia():
    g = Graph()
    g.parse("ontologia_recomendaciones.owl", format="xml")

    print("\n📚 Consultando ontología...")
    for s, p, o in g:
        print(f"{s} -- {p} --> {o}")

# === INTERFAZ STREAMLIT ===
st.title("🎥 Sistema de Recomendación Inteligente ")

nombre = st.text_input("Nombre del usuario")
edad_val = st.slider("Edad", 0, 12, 9)
genero = st.selectbox("Género favorito", ["ciencia ficción", "comedia", "terror", "drama", "documental"])
idioma = st.selectbox("Idioma preferido", ["Español", "Inglés", "italiano"])
formato = st.selectbox("Formato preferido", ["película", "serie"])

interes_val = st.slider("Nivel de interés (0–10)", 0.0, 10.0, 7.5)
apertura_val = st.slider("Nivel de apertura (0–10)", 0.0, 10.0, 6.5)

if st.button("🔍 Obtener recomendación"):
    sistema = ctrl.ControlSystemSimulation(sistema_recomendabilidad_ctrl)
    sistema.input['interes'] = interes_val
    sistema.input['apertura'] = apertura_val
    sistema.input['edad'] = edad_val
    sistema.compute()
    nivel_reco = round(sistema.output['recomendabilidad'], 2)

    st.markdown(f"**📊 Nivel de recomendación:** {nivel_reco}/100")

    engine = MotorRecomendador()
    engine.reset()
    engine.declare(Genero_favorito(valor=genero))
    engine.declare(Formato_preferido(valor=formato))
    engine.declare(Idioma_preferido(valor=idioma))
    engine.declare(Recomendacion(valor=nivel_reco))

    engine.run()

    for fact in engine.facts.values():
        if isinstance(fact, Recomendacion):
            st.success(fact['valor'])