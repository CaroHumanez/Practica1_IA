# Para compatibilidad con versiones anteriores, siempre utilizarlo.
import collections.abc
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping
    
import streamlit as st
from experta import *
from motorExperta import MotorRecomendacion, peliculas, series, Usuario
from skfuzzy import control as ctrl
from logicaDifusa import evaluar_recomendabilidad


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
            tipo_usuario = st.selectbox("tipo", ["pelicula", "serie"])
            plataforma_usuario = st.selectbox("Plataforma", ["Netflix", "DisneyPlus", "HBO_Max"])
            interes_usuario = st.slider("Nivel de interés (0-10)", 0.0, 10.0, 7.5)
            apertura_usuario = st.slider("Apertura a géneros (0-10)", 0.0, 10.0, 6.0)

        if st.form_submit_button("Generar Recomendación"):
            puntuacion_difusa = evaluar_recomendabilidad(interes_usuario, apertura_usuario, edad_usuario) 
            
            # Determinar nivel de recomendación
            if puntuacion_difusa <= 40:
                nivel_usuario = "baja"
            elif puntuacion_difusa <= 70:
                nivel_usuario = "media"
            else:
                nivel_usuario = "alta"

            if edad_usuario <= 13:  
                edad_usuario = "nino"
            elif 13 > edad_usuario <= 20:
                edad_usuario = "adolescente"
            else:
                edad_usuario = "adulto"  

            # Motor Experto
            motor.reset()
            motor.cargar_hechos_iniciales()
            motor.declare(Usuario(
                genero_usuario=str(genero_usuario),
                idioma_usuario=str(idioma_usuario),
                formato_usuario=str(tipo_usuario),
                clasificacion_edad=str(edad_usuario),
                plataforma_usuario=str(plataforma_usuario),
                nivel_recomendacion=str(nivel_usuario)
            ))
            motor.run()
            for fact in motor.facts.values():
                st.write(fact)

            # Mostrar resultados
            st.subheader(f"Resultados para {nombre_usuario}")
            st.write(f"Nivel de recomendación: {nivel_usuario.capitalize()} (puntuación difusa: {puntuacion_difusa:.1f}/100)")
            
            # Recuperar recomendación
            recomendacion = next((fact for fact in motor.facts if 'recomendacion' in str(fact)), None)

            for fact in motor.facts.values():
                if isinstance(fact, Fact):
                    if 'pelicula_recomendada' in fact:
                        recomendacion = fact['pelicula_recomendada']
                        tipo = "Película"
                        break
                    elif 'serie_recomendada' in fact:
                        recomendacion = fact['serie_recomendada']
                        tipo = "Serie"
                        break

            if recomendacion:
                st.success(f"🎬 {tipo} recomendada: {recomendacion}")
            else:
                st.warning("No se encontró una recomendación.")

if __name__ == "__main__":
    main()                