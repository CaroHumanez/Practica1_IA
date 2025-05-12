import streamlit as st
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
from experta import *

# === SISTEMA DIFUSO ===
interes = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'interes')
apertura = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'apertura')
edad = ctrl.Antecedent(np.arange(0, 12.1, 0.1), 'edad')
recomendabilidad = ctrl.Consequent(np.arange(0, 101, 1), 'recomendabilidad')

def modificacion(conjunto, potencia):
    return conjunto ** potencia

interes['bajo'] = fuzz.trimf(interes.universe, [0, 0, 4])
interes['medio'] = fuzz.trapmf(interes.universe, [3.5, 4.5, 5.5, 6.5])
interes['alto'] = fuzz.gaussmf(interes.universe, 8, 1.2)
interes['muy_interesado'] = modificacion(fuzz.gaussmf(interes.universe, 8, 1.2), 2)

apertura['cerrado'] = fuzz.trapmf(apertura.universe, [0, 0, 2.5, 4])
apertura['neutral'] = fuzz.gaussmf(apertura.universe, 5, 1.5)
apertura['abierto'] = fuzz.trimf(apertura.universe, [6, 8, 10])
apertura['mas_menos_abierto'] = modificacion(fuzz.trimf(apertura.universe, [6, 8, 10]), 1/2)

edad['nino'] = fuzz.trimf(edad.universe, [0, 0, 3])
edad['adolescente'] = fuzz.trapmf(edad.universe, [2, 4, 6, 8])
edad['adulto'] = fuzz.gaussmf(edad.universe, 9, 1)

recomendabilidad['baja'] = fuzz.trapmf(recomendabilidad.universe, [0, 0, 20, 35])
recomendabilidad['media'] = fuzz.gaussmf(recomendabilidad.universe, 50, 10)
recomendabilidad['alta'] = fuzz.trapmf(recomendabilidad.universe, [65, 80, 100, 100])

reglas = [
    ctrl.Rule(interes['alto'] & apertura['abierto'], recomendabilidad['alta']),
    ctrl.Rule(interes['medio'] & apertura['neutral'], recomendabilidad['media']),
    ctrl.Rule(interes['bajo'] | apertura['cerrado'], recomendabilidad['baja']),
    ctrl.Rule(interes['muy_interesado'] & apertura['mas_menos_abierto'], recomendabilidad['alta']),
    ctrl.Rule(apertura['neutral'] & ~edad['nino'], recomendabilidad['media']),
    ctrl.Rule(interes['medio'] & edad['adulto'], recomendabilidad['media']),
    ctrl.Rule(edad['nino'] & ~apertura['abierto'], recomendabilidad['baja']),
    ctrl.Rule(interes['alto'] | edad['adolescente'], recomendabilidad['media']),
    ctrl.Rule(interes['muy_interesado'] & apertura['cerrado'] & edad['adulto'], recomendabilidad['media'])
]

sistema_ctrl = ctrl.ControlSystem(reglas)

# === SISTEMA EXPERTO ===
class Genero_favorito(Fact): pass
class Idioma_preferido(Fact): pass
class Formato_preferido(Fact): pass
class Recomendabilidad(Fact): pass
class Recomendacion(Fact): pass

class MotorRecomendador(KnowledgeEngine):
    @Rule(Genero_favorito(valor="ciencia ficción"),
          Formato_preferido(valor="película"),
          Recomendabilidad(valor=MATCH.v),
          TEST(lambda v: v >= 60),
          NOT(Fact(valor="evaluado")))
    def recomendar_interstellar(self, v):
        self.declare(Recomendacion(valor="🎬 Recomendamos Interstellar."))
        self.declare(Fact(valor="evaluado"))
        self.halt()

    @Rule(Genero_favorito(valor="comedia"),
          Formato_preferido(valor="película"),
          Recomendabilidad(valor=MATCH.v),
          TEST(lambda v: v >= 60),
          NOT(Fact(valor="evaluado")))
    def recomendar_paseo(self, v):
        self.declare(Recomendacion(valor="🎬 Recomendamos El Paseo."))
        self.declare(Fact(valor="evaluado"))
        self.halt()

# === INTERFAZ STREAMLIT ===
st.title("🎥 Sistema de Recomendación Inteligente")

nombre = st.text_input("Nombre del usuario")
edad_val = st.slider("Edad", 0, 12, 9)
genero = st.selectbox("Género favorito", ["ciencia ficción", "comedia", "terror", "drama", "documental"])
idioma = st.selectbox("Idioma preferido", ["Español", "Inglés", "italiano"])
formato = st.selectbox("Formato preferido", ["película", "serie"])

interes_val = st.slider("Nivel de interés (0–10)", 0.0, 10.0, 7.5)
apertura_val = st.slider("Nivel de apertura (0–10)", 0.0, 10.0, 6.5)

if st.button("🔍 Obtener recomendación"):
    sistema = ctrl.ControlSystemSimulation(sistema_ctrl)
    sistema.input['interes'] = interes_val
    sistema.input['apertura'] = apertura_val
    sistema.input['edad'] = edad_val
    sistema.compute()
    nivel_reco = round(sistema.output['recomendabilidad'], 2)

    st.markdown(f"**📊 Nivel de recomendabilidad:** {nivel_reco}/100")

    engine = MotorRecomendador()
    engine.reset()
    engine.declare(Genero_favorito(valor=genero))
    engine.declare(Formato_preferido(valor=formato))
    engine.declare(Idioma_preferido(valor=idioma))
    engine.declare(Recomendabilidad(valor=nivel_reco))
    engine.run()

    recomendacion = None
    for _, fact in engine.facts.items():
        if isinstance(fact, Recomendacion):
            recomendacion = fact['valor']
            st.success(recomendacion)

    if not recomendacion:
        st.warning("⚠️ No encontramos una recomendación adecuada para este perfil. Intenta ajustar tus preferencias.")


