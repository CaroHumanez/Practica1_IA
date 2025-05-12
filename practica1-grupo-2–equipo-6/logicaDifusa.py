import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# === Definición de variables difusas ===
interes = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'interes')
apertura = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'apertura')
edad = ctrl.Antecedent(np.arange(0, 12.1, 0.1), 'edad')
recomendabilidad = ctrl.Consequent(np.arange(0, 101, 1), 'recomendabilidad')

# === Funcion Modificador===
def modificacion(conjunto, potencia):
    return conjunto ** potencia

# === Funciones de pertenencia: Interés del usuario ===
interes['bajo'] = fuzz.trimf(interes.universe, [0, 0, 4])
interes['medio'] = fuzz.trapmf(interes.universe, [3.5, 4.5, 5.5, 6.5])
interes['alto'] = fuzz.gaussmf(interes.universe, 8, 1.2)
# Muy interesado: Concentración de 'alto' (potencia = 2)
interes['muy_interesado'] = modificacion(fuzz.gaussmf(interes.universe, 8, 1.2),2)

# === Funciones de pertenencia: Apertura a nuevos géneros ===
apertura['cerrado'] = fuzz.trapmf(apertura.universe, [0, 0, 2.5, 4])
apertura['neutral'] = fuzz.gaussmf(apertura.universe, 5, 1.5)
apertura['abierto'] = fuzz.trimf(apertura.universe, [6, 8, 10])
# Ligeramente abierto: Dilatación de 'abierto' (potencia = 1.3)
apertura['mas_menos_abierto'] = modificacion(fuzz.trimf(apertura.universe, [6, 8, 10]),1/2)

# === Funciones de pertenencia: Adecuación por edad ===
edad['nino'] = fuzz.trimf(edad.universe, [0, 0, 3])
edad['adolescente'] = fuzz.trapmf(edad.universe, [2, 4, 6, 8])
edad['adulto'] = fuzz.gaussmf(edad.universe, 9, 1)

# === Funciones de pertenencia: Nivel de recomendabilidad ===
recomendabilidad['baja'] = fuzz.trapmf(recomendabilidad.universe, [0, 0, 20, 35])
recomendabilidad['media'] = fuzz.gaussmf(recomendabilidad.universe, 50, 10)
recomendabilidad['alta'] = fuzz.trapmf(recomendabilidad.universe, [65, 80, 100, 100])

# === Grafica de funciones de pertenencia ===
interes.view()

# === Reglas del sistema ===
reglas = [
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

# === Sistema de control ===
sistema_ctrl = ctrl.ControlSystem(reglas)
sistema = ctrl.ControlSystemSimulation(sistema_ctrl)


def cargar_recomendabilidad (interes, apertura, edad):
    sistema.input['interes'] = interes
    sistema.input['apertura'] = apertura
    sistema.input['edad'] = edad

    sistema.compute()
    print(f"Nivel de recomendabilidad: {sistema.output['recomendabilidad']:.2f}")
    return sistema.output['recomendabilidad']

