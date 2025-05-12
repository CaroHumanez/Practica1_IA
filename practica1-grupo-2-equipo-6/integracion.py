import streamlit as st
from experta import *
from logicaDifusa import cargar_recomendabilidad
from motorExperta import MotorRecomendacion, peliculas, series, Preferencia, Usuario, NivelRecomendacion, PlataformaPreferida
from skfuzzy import control as ctrl

motor = MotorRecomendacion(peliculas, series)

def main():
    st.title("🎬 Sistema de Recomendación Inteligente")

    with st.form("form_recomendacion"):
        col1, col2 = st.columns(2)

        with col1:
            nombre_usuario = st.text_input("Nombre del usuario")
            edad_usuario = st.slider("Edad del usuario", 0, 60, 18)
            genero_usuario = st.selectbox("Género", ["CienciaFiccion", "Comedia", "Terror", "Drama", "Documental"])
            idioma_usuario = st.selectbox("Idioma", ["espanol", "ingles", "frances"])

        with col2:
            formato_usuario = st.selectbox("Formato", ["pelicula", "serie"])
            plataforma_usuario = st.selectbox("Plataforma", ["Netflix", "DisneyPlus", "HBO_Max"])
            interes_usuario = st.slider("Nivel de interés (0-10)", 0.0, 10.0, 7.5)
            apertura_usuario = st.slider("Apertura a géneros (0-10)", 0.0, 10.0, 6.0)

        if st.form_submit_button("Generar Recomendación"):
            # Sistema Difuso
            sistema_difuso = ctrl.ControlSystem(cargar_recomendabilidad())
            simulador = ctrl.ControlSystemSimulation(sistema_difuso)
            
            simulador.input["interes"] = interes_usuario
            simulador.input["apertura"] = apertura_usuario
            simulador.input["edad"] = edad_usuario
            simulador.compute()
            
            puntuacion_difusa = simulador.output["recomendabilidad"]
            
            # Determinar nivel de recomendación
            if puntuacion_difusa <= 40:
                nivel = "baja"
            elif puntuacion_difusa <= 70:
                nivel = "media"
            else:
                nivel = "alta"

            # Motor Experto
            motor.reset()
            motor.cargar_hechos_iniciales()
            motor.declare(Preferencia(tipo=formato_usuario))
            motor.declare(Usuario(
                genero=genero_usuario,
                idioma=idioma_usuario,
                clasificacion_edad=str(edad_usuario)
            ))
            motor.declare(NivelRecomendacion(nivel=nivel))
            motor.declare(PlataformaPreferida(plataforma=plataforma_usuario))
            motor.run()

            # Mostrar resultados
            st.subheader(f"Resultados para {nombre_usuario}")
            st.write(f"Nivel de recomendación: {nivel.capitalize()} (puntuación difusa: {puntuacion_difusa:.1f}/100)")
            
            # Recuperar recomendación
            recomendacion = next((fact for fact in motor.facts if 'recomendacion' in str(fact)), None)
            if recomendacion:
                st.success(f"🎬 Recomendación: {recomendacion['recomendacion']} (Puntuación: {recomendacion['puntuacion']}/10)")

if __name__ == "__main__":
    main()