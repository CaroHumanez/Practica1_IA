import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def cargar_recomendabilidad():
    # Variables difusas
    interes = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'interes')
    apertura = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'apertura')
    edad = ctrl.Antecedent(np.arange(0, 61, 0.1), 'edad')  # Rango 0-60 años
    recomendabilidad = ctrl.Consequent(np.arange(0, 101, 1), 'recomendabilidad')

    # Funciones de pertenencia: Interés
    interes['bajo'] = fuzz.trimf(interes.universe, [0, 0, 4])
    interes['medio'] = fuzz.trapmf(interes.universe, [3, 4, 6, 7])
    interes['alto'] = fuzz.gaussmf(interes.universe, 9, 1.5)
    interes['muy_interesado'] = fuzz.gaussmf(interes.universe, 9, 1.5)**2  # Modificador "muy"

    # Funciones de pertenencia: Apertura
    apertura['cerrado'] = fuzz.trapmf(apertura.universe, [0, 0, 3, 5])
    apertura['neutral'] = fuzz.gaussmf(apertura.universe, 5, 1.5)
    apertura['abierto'] = fuzz.trimf(apertura.universe, [5, 7.5, 10])
    apertura['ligeramente_abierto'] = fuzz.trimf(apertura.universe, [5, 7.5, 10])**0.5  # Modificador "ligeramente"

    # Funciones de pertenencia: Edad
    edad['nino'] = fuzz.trimf(edad.universe, [0, 0, 12])
    edad['adolescente'] = fuzz.trapmf(edad.universe, [10, 13, 17, 20])
    edad['adulto'] = fuzz.gaussmf(edad.universe, 30, 10)

    # Funciones de pertenencia: Recomendabilidad
    recomendabilidad['baja'] = fuzz.trapmf(recomendabilidad.universe, [0, 0, 30, 50])
    recomendabilidad['media'] = fuzz.gaussmf(recomendabilidad.universe, 65, 15)
    recomendabilidad['alta'] = fuzz.trapmf(recomendabilidad.universe, [70, 80, 100, 100])

    # Reglas difusas
    reglas = [
        ctrl.Rule(interes['alto'] & apertura['abierto'], recomendabilidad['alta']),
        ctrl.Rule(interes['medio'] & apertura['neutral'], recomendabilidad['media']),
        ctrl.Rule(interes['bajo'] | apertura['cerrado'], recomendabilidad['baja']),
        ctrl.Rule(edad['nino'] & ~apertura['abierto'], recomendabilidad['baja']),
        ctrl.Rule(interes['muy_interesado'] & apertura['ligeramente_abierto'], recomendabilidad['alta']),
        ctrl.Rule(interes['alto'] | edad['adolescente'], recomendabilidad['media']),
        ctrl.Rule(interes['medio'] & edad['adulto'], recomendabilidad['alta']),
        ctrl.Rule(interes['alto'] & apertura['cerrado'] & edad['adulto'], recomendabilidad['media']),
        ctrl.Rule(interes['bajo'] & apertura['neutral'], recomendabilidad['baja'])
    ]

    sistema = ctrl.ControlSystem(reglas)
    return sistema