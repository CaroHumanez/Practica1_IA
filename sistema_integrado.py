# === SISTEMA INTEGRADO: Ontología + Lógica Difusa + Sistema Experto ===
# FIX para compatibilidad con experta y frozendict en Python 3.10+
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

# Luego puedes importar experta
from experta import *

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, DCTERMS
#from owlrl import DeductiveClosure, RDFS_Semantics
from experta import *
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
from rdflib.plugins.sparql import prepareQuery

# === Paso 1: Ontología ===
g = Graph()
SPACE = Namespace("http://SPACEample.org/space/")
g.parse("ontologia.ttl", format="turtle")
#DeductiveClosure(RDFS_Semantics).expand(g)

q = prepareQuery("""
    SELECT ?genero ?idioma ?formato WHERE {
        ?contenido a space:Contenido .
        ?contenido space:tieneGenero ?genero .
        ?contenido space:tieneIdioma ?idioma .
        ?contenido space:tieneFormato ?formato .
    }
""", initNs={"space": SPACE})

# === Paso 2: Sistema difuso ===
interes = ctrl.Antecedent(np.arange(0, 11, 1), 'interes')
apertura = ctrl.Antecedent(np.arange(0, 11, 1), 'apertura')
edad = ctrl.Antecedent(np.arange(0, 13, 1), 'edad')
recomendabilidad = ctrl.Consequent(np.arange(0, 101, 1), 'recomendabilidad')

interes['bajo'] = fuzz.trimf(interes.universe, [0, 0, 4])
interes['alto'] = fuzz.gaussmf(interes.universe, 8, 1.5)

apertura['cerrado'] = fuzz.trapmf(apertura.universe, [0, 0, 2, 4])
apertura['abierto'] = fuzz.trimf(apertura.universe, [6, 8, 10])

edad['nino'] = fuzz.trimf(edad.universe, [0, 0, 6])
edad['adulto'] = fuzz.gaussmf(edad.universe, 10, 1.5)

recomendabilidad['baja'] = fuzz.trapmf(recomendabilidad.universe, [0, 0, 20, 40])
recomendabilidad['alta'] = fuzz.trapmf(recomendabilidad.universe, [60, 80, 100, 100])

reglas = [
    ctrl.Rule(interes['alto'] & apertura['abierto'], recomendabilidad['alta']),
    ctrl.Rule(interes['bajo'] | apertura['cerrado'] | edad['nino'], recomendabilidad['baja'])
]

sistema_ctrl = ctrl.ControlSystem(reglas)
simulador = ctrl.ControlSystemSimulation(sistema_ctrl)
simulador.input['interes'] = 8
simulador.input['apertura'] = 7
simulador.input['edad'] = 9
simulador.compute()
valor_reco = round(simulador.output['recomendabilidad'], 2)
print(f"[Difuso] Recomendabilidad calculada: {valor_reco}")

# === Paso 3: Sistema experto ===
class Genero_favorito(Fact): pass
class Idioma_preferido(Fact): pass
class Formato_preferido(Fact): pass
class Recomendabilidad(Fact): pass
class Recomendacion(Fact): pass

class MotorRecomendador(KnowledgeEngine):
    @Rule(Genero_favorito(valor="ciencia ficcion"),
          Recomendabilidad(valor=MATCH.v),
          TEST(lambda v: v >= 60),
          NOT(Fact(valor="evaluado")), salience=10)
    def recomendar_exp(self, v):
        print(f"🎯 Recomendación con recomendabilidad {v}: Te recomendamos *The Expanse*.")
        self.declare(Recomendacion(valor="Te recomendamos la serie The Expanse."))
        self.declare(Fact(valor="evaluado"))
        self.halt()

# === Ejecutar el sistema ===
engine = MotorRecomendador()
engine.reset()

# Declarar hechos desde ontología
for row in g.query(q):
    genero = str(row.genero).split("/")[-1].replace("_", " ").lower()
    idioma = str(row.idioma).lower()
    formato = str(row.formato).lower()
    engine.declare(Genero_favorito(valor=genero))
    engine.declare(Idioma_preferido(valor=idioma))
    engine.declare(Formato_preferido(valor=formato))

# Declarar hecho difuso
engine.declare(Recomendabilidad(valor=valor_reco))
engine.run()
