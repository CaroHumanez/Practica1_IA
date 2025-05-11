import streamlit as st
import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl
from experta import *

# 1. Base de datos de películas
peliculas = {
    "ciencia ficción": {
        "alta": [
            {"titulo": "Interstellar", "idioma": "Inglés", "formato": "película", "valoracion": 92},
            {"titulo": "Blade Runner 2049", "idioma": "Inglés", "formato": "película", "valoracion": 85},
            {"titulo": "The Expanse", "idioma": "Inglés", "formato": "serie", "valoracion": 88}
        ],
        "media": [
            {"titulo": "Ready Player One", "idioma": "Español", "formato": "película", "valoracion": 68},
            {"titulo": "Altered Carbon", "idioma": "Español", "formato": "serie", "valoracion": 72},
            {"titulo": "The Martian", "idioma": "Inglés", "formato": "película", "valoracion": 75}
        ],
        "baja": [
            {"titulo": "Pixels", "idioma": "Español", "formato": "película", "valoracion": 32},
            {"titulo": "The Rain", "idioma": "Inglés", "formato": "serie", "valoracion": 28},
            {"titulo": "Moonfall", "idioma": "Español", "formato": "película", "valoracion": 35}
        ]
    },
    "drama": {
        "alta": [
            {"titulo": "El Padrino", "idioma": "Español", "formato": "película", "valoracion": 95},
            {"titulo": "Forrest Gump", "idioma": "Español", "formato": "película", "valoracion": 90},
            {"titulo": "Breaking Bad", "idioma": "Inglés", "formato": "serie", "valoracion": 97}
        ],
        "media": [
            {"titulo": "La La Land", "idioma": "Español", "formato": "película", "valoracion": 70},
            {"titulo": "The Crown", "idioma": "Inglés", "formato": "serie", "valoracion": 68},
            {"titulo": "Birdman", "idioma": "Español", "formato": "película", "valoracion": 65}
        ],
        "baja": [
            {"titulo": "After", "idioma": "Español", "formato": "película", "valoracion": 25},
            {"titulo": "365 Días", "idioma": "Español", "formato": "película", "valoracion": 18},
            {"titulo": "Riverdale", "idioma": "Inglés", "formato": "serie", "valoracion": 30}
        ]
    }
}

# 2. Sistema Difuso
def crear_sistema_difuso():
    # Variables de entrada
    interes = ctrl.Antecedent(np.arange(0, 11, 0.1), 'interes')
    apertura = ctrl.Antecedent(np.arange(0, 11, 0.1), 'apertura')
    edad = ctrl.Antecedent(np.arange(11, 60, 0.1), 'edad')
    
    # Variable de salida
    recomendacion = ctrl.Consequent(np.arange(0, 101, 1), 'recomendacion')
    
    # Funciones de pertenencia
    interes.automf(names=['bajo', 'medio', 'alto'])
    apertura.automf(names=['cerrado', 'neutral', 'abierto'])
    edad.automf(names=['niño', 'adolescente', 'adulto'])
    
    recomendacion['baja'] = fuzz.trimf(recomendacion.universe, [0, 0, 40])
    recomendacion['media'] = fuzz.trimf(recomendacion.universe, [30, 50, 70])
    recomendacion['alta'] = fuzz.trimf(recomendacion.universe, [60, 100, 100])
    
    # Reglas difusas
    reglas = [
        ctrl.Rule(interes['alto'] & apertura['abierto'], recomendacion['alta']),
        ctrl.Rule(interes['medio'] & apertura['neutral'], recomendacion['media']),
        ctrl.Rule(interes['bajo'] | apertura['cerrado'], recomendacion['baja']),
        ctrl.Rule(edad['adulto'] & interes['medio'], recomendacion['media']),
        ctrl.Rule(edad['niño'] & ~apertura['abierto'], recomendacion['baja'])
    ]
    
    return ctrl.ControlSystem(reglas)

# 3. Motor Experto
class MotorRecomendador(KnowledgeEngine):
    @DefFacts()
    def _initial_facts(self):
        yield Fact(accion="recomendar")
    
    @Rule(Fact(accion="recomendar"),
          Fact(genero=MATCH.genero),
          Fact(idioma=MATCH.idioma),
          Fact(formato=MATCH.formato),
          Fact(nivel=MATCH.nivel))
    def recomendar_pelicula(self, genero, idioma, formato, nivel):
        candidatas = [
            p for p in peliculas.get(genero, {}).get(nivel, [])
            if p['idioma'] == idioma and p['formato'] == formato
        ]
        
        if candidatas:
            mejor = max(candidatas, key=lambda x: x['valoracion'])
            self.declare(Fact(recomendacion=mejor['titulo'], puntuacion=mejor['valoracion']))
        else:
            self.declare(Fact(recomendacion="No encontrado", puntuacion=0))

# 4. Interfaz de Usuario
def main():
    st.title("🎬 Sistema de Recomendación Inteligente")
    
    with st.form("form_recomendacion"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre del usuario")
            edad_val = st.slider("Edad del contenido", 11, 60, 8)
            genero = st.selectbox("Género", list(peliculas.keys()))
            
        with col2:
            idioma = st.selectbox("Idioma", ["Español", "Inglés"])
            formato = st.selectbox("Formato", ["película", "serie"])
            interes_val = st.slider("Nivel de interés (0-10)", 0.0, 10.0, 7.5)
            apertura_val = st.slider("Apertura a géneros (0-10)", 0.0, 10.0, 6.0)
        
        if st.form_submit_button("Generar Recomendación"):
            # Sistema difuso
            sistema_difuso = crear_sistema_difuso()
            simulador = ctrl.ControlSystemSimulation(sistema_difuso)
            
            simulador.input['interes'] = interes_val
            simulador.input['apertura'] = apertura_val
            simulador.input['edad'] = edad_val
            
            simulador.compute()
            puntuacion = simulador.output['recomendacion']
            
            # Determinar nivel
            if puntuacion <= 40:
                nivel = "baja"
            elif 40 < puntuacion <= 70:
                nivel = "media"
            else:
                nivel = "alta"
            
            # Motor experto
            motor = MotorRecomendador()
            motor.reset()
            motor.declare(Fact(genero=genero))
            motor.declare(Fact(idioma=idioma))
            motor.declare(Fact(formato=formato))
            motor.declare(Fact(nivel=nivel))
            motor.run()
            
            # Mostrar resultados
            st.subheader("Resultado de la Recomendación")
            st.write(f"**Puntuación calculada:** {puntuacion:.1f}/100")
            st.write(f"**Nivel de recomendación:** {nivel.capitalize()}")
            
            for hecho in motor.facts.values():
                if isinstance(hecho, Fact) and 'recomendacion' in hecho:
                    if hecho['puntuacion'] > 0:
                        st.success(f"🎉 **Recomendación:** {hecho['recomendacion']}")
                        st.write(f"⭐ **Puntuación de la película/serie:** {hecho['puntuacion']}/100")
                    else:
                        st.warning("⚠️ No se encontraron recomendaciones adecuadas")

if __name__ == "__main__":
    main()