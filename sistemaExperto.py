#pip install experta
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
from experta import KnowledgeEngine, Fact, Rule, NOT

# Definición de los hechos
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



# Motor del sistema experto
class MotorRecomendador(KnowledgeEngine):

#1
    @Rule(
    Genero_favorito(valor="ciencia ficción"),
    Idioma_preferido(valor="Español"),
    Formato_preferido(valor="serie"),
    NOT(Fact(valor="evaluado")),
    salience=12
)
    def recomendar_dark(self):
      print("🎯 Recomendación: Te recomendamos la serie *Dark*.")
      self.declare(Recomendacion(valor="Te recomendamos la serie Dark."))
      self.declare(Fact(valor="evaluado"))
      self.halt()  # Detiene el motor luego de recomendar


#2
    @Rule(
      Genero_favorito(valor="drama"),
      Idioma_preferido(valor="Inglés"),
      Formato_preferido(valor="serie"),
      NOT(Fact(valor="evaluado")),
      salience=12
)
    def recomendar_the_crown(self):
      print("🎯 Recomendación: Te recomendamos la serie *The Crown*.")
      self.declare(Recomendacion(valor="Te recomendamos la serie The Crown."))
      self.declare(Fact(valor="evaluado"))

#3
    @Rule(
    Genero_favorito(valor="comedia"),
    Idioma_preferido(valor="italiano"),
    Formato_preferido(valor="película"),
    NOT(Fact(valor="evaluado")),
    salience=12
)
    def recomendar_la_vida_es_bella(self):
      print("🎯 Recomendación: Te recomendamos la película *La vida es bella*.")
      self.declare(Recomendacion(valor="Te recomendamos la película La vida es bella."))
      self.declare(Fact(valor="evaluado"))

#4

    @Rule(
    Genero_favorito(valor="ciencia ficción"),
    Idioma_preferido(valor="Inglés"),
    Formato_preferido(valor="pelicula"),
    NOT(Fact(valor="evaluado")),
    salience=12
)
    def recomendar_juego_de_tronos(self):
      print("🎯 Recomendación: Te recomendamos la pelicula *Dune*.")
      self.declare(Recomendacion(valor="Dune"))
      self.declare(Fact(valor="evaluado"))

#5

    @Rule(
    Genero_favorito(valor="comedia"),
    Idioma_preferido(valor="Español"),
    Formato_preferido(valor="pelicula"),
    NOT(Fact(valor="evaluado")),
    salience=12
)
    def recomendar_el_paseo(self):
      print("🎯 Recomendación: Te recomendamos la pelicula *El paseo*.")
      self.declare(Recomendacion(valor="Te recomendamos la pelicula El paseo."))
      self.declare(Fact(valor="evaluado"))

#6
    @Rule(
      Genero_favorito(valor="ciencia ficción"),
      Formato_preferido(valor="película"),
      NOT(Fact(valor="evaluado")),
      salience=9
)
    def recomendar_interstellar(self):
      print("🎯 Recomendación: Te recomendamos la película *Interstellar*.")
      self.declare(Recomendacion(valor="Te recomendamos la película Interstellar."))
      self.declare(Fact(valor="evaluado"))
#7

    @Rule(
    Genero_favorito(valor="drama"),
    Formato_preferido(valor="película"),
    NOT(Fact(valor="evaluado")),
    salience=9
)
    def recomendar_Pianista(self):
      print("🎯 Recomendación: Te recomendamos la película *Pianista*.")
      self.declare(Recomendacion(valor="Te recomendamos la película Pianista."))
      self.declare(Fact(valor="evaluado"))

#8

    @Rule(
    Genero_favorito(valor="policial"),
    Formato_preferido(valor="serie"),
    NOT(Fact(valor="evaluado")),
    salience=9
)
    def recomendar_mentes_criminales(self):
      print("🎯 Recomendación: Te recomendamos la serie *Mentes criminales*.")
      self.declare(Recomendacion(valor="Te recomendamos la serie Mentes criminales."))
      self.declare(Fact(valor="evaluado"))

#9

    @Rule(
    Genero_favorito(valor="documental"),
    Formato_preferido(valor="película"),
    NOT(Fact(valor="evaluado")),
    salience=9
)
    def recomendar_camino_serpiente(self):
      print("🎯 Recomendación: Te recomendamos la película *El camino de la serpiente*.")
      self.declare(Recomendacion(valor="Te recomendamos la película El camino de la serpiente."))
      self.declare(Fact(valor="evaluado"))


#10

    @Rule(
    Genero_favorito(valor="terror"),
    Formato_preferido(valor="película"),
    NOT(Fact(valor="evaluado")),
    salience=9
)
    def recomendar_hannibal(self):
      print("🎯 Recomendación: Te recomendamos la película *Hannibal*.")
      self.declare(Recomendacion(valor="Te recomendamos la película Hannibal."))
      self.declare(Fact(valor="evaluado"))

#11
    @Rule(
    Genero_favorito(valor="romance"),
    NOT(Fact(valor="evaluado")),
    salience=6
)
    def recomendar_orgullo_prejuicio(self):
      print("🎯 Recomendación: Te recomendamos la película *Orgullo y Prejuicio*.")
      self.declare(Recomendacion(valor="Te recomendamos la película Orgullo y Prejuicio."))
      self.declare(Fact(valor="evaluado"))

#12

    @Rule(
    Idioma_preferido(valor="francés"),
    NOT(Fact(valor="evaluado")),
    salience=5
)
    def recomendar_amelie(self):
      print("🎯 Recomendación: Te recomendamos la película francesa *Amélie*.")
      self.declare(Recomendacion(valor="Te recomendamos la película francesa Amélie."))
      self.declare(Fact(valor="evaluado"))

#13

    @Rule(
    Formato_preferido(valor="serie"),
    NOT(Fact(valor="evaluado")),
    salience=4
)
    def recomendar_friends(self):
      print("🎯 Recomendación: Te recomendamos la serie clásica *Friends*.")
      self.declare(Recomendacion(valor="Te recomendamos la serie clásica Friends."))
      self.declare(Fact(valor="evaluado"))

#14

    @Rule(
    Genero_favorito(valor="animación"),
    NOT(Fact(valor="evaluado")),
    salience=3
)
    def recomendar_shrek(self):
      print("🎯 Recomendación: Te recomendamos la película animada *Shrek*.")
      self.declare(Recomendacion(valor="Te recomendamos la película animada Shrek."))
      self.declare(Fact(valor="evaluado"))

#15
    @Rule(
    Idioma_preferido(valor="Inglés"),
    NOT(Fact(valor="evaluado")),
    salience=3
)
    def recomendar_stranger_things(self):
      print("🎯 Recomendación: Te recomendamos la serie *Stranger Things*.")
      self.declare(Recomendacion(valor="Te recomendamos la serie Stranger Things."))
      self.declare(Fact(valor="evaluado"))

engine = MotorRecomendador()
engine.reset()

# Usuario 1
engine.declare(Usuario(nombre="Ana", edad=25))
engine.declare(Genero_favorito(valor="ciencia ficción"))
engine.declare(Idioma_preferido(valor="Español"))
engine.declare(Formato_preferido(valor="serie"))

# Usuario 2
engine.declare(Usuario(nombre="Carlos", edad=30))
engine.declare(Genero_favorito(valor="drama"))
engine.declare(Idioma_preferido(valor="Inglés"))
engine.declare(Formato_preferido(valor="serie"))

# Usuario 3
engine.declare(Usuario(nombre="Lucía", edad=22))
engine.declare(Genero_favorito(valor="comedia"))
engine.declare(Idioma_preferido(valor="italiano"))
engine.declare(Formato_preferido(valor="película"))

# Usuario 4
engine.declare(Usuario(nombre="Mateo", edad=28))
engine.declare(Genero_favorito(valor="ciencia ficción"))
engine.declare(Idioma_preferido(valor="Inglés"))
engine.declare(Formato_preferido(valor="película"))

# Usuario 5
engine.declare(Usuario(nombre="Laura", edad=26))
engine.declare(Genero_favorito(valor="comedia"))
engine.declare(Idioma_preferido(valor="Español"))
engine.declare(Formato_preferido(valor="película"))

# Usuario 6
engine.declare(Usuario(nombre="Julián", edad=32))
engine.declare(Genero_favorito(valor="policial"))
engine.declare(Idioma_preferido(valor="Español"))
engine.declare(Formato_preferido(valor="serie"))

# Usuario 7
engine.declare(Usuario(nombre="Sofía", edad=19))
engine.declare(Genero_favorito(valor="documental"))
engine.declare(Idioma_preferido(valor="Español"))
engine.declare(Formato_preferido(valor="película"))

# Usuario 8
engine.declare(Usuario(nombre="Camila", edad=27))
engine.declare(Genero_favorito(valor="terror"))
engine.declare(Idioma_preferido(valor="Inglés"))
engine.declare(Formato_preferido(valor="película"))

# Usuario 9
engine.declare(Usuario(nombre="Esteban", edad=35))
engine.declare(Genero_favorito(valor="romance"))
engine.declare(Idioma_preferido(valor="Español"))
engine.declare(Formato_preferido(valor="película"))

# Usuario 10
engine.declare(Usuario(nombre="Valentina", edad=29))
engine.declare(Genero_favorito(valor="animación"))
engine.declare(Idioma_preferido(valor="Español"))
engine.declare(Formato_preferido(valor="película"))

engine.run()







engine = MotorRecomendador()
engine.reset()

engine.declare(Usuario(nombre="Sebastián", edad=31))
engine.declare(Genero_favorito(valor="ciencia ficción"))
engine.declare(Formato_preferido(valor="película"))
engine.declare(Idioma_preferido(valor="Español"))  # ✅ ¡Esto faltaba!

print("\n== Hechos declarados antes del motor (Sebastián) ==")
for fact in engine.facts.values():
    print(fact)

engine.run()




# === Prueba adicional: Juan ===
engine = MotorRecomendador()
engine.reset()

engine.declare(Usuario(nombre="Juan", edad=20))
engine.declare(Genero_favorito(valor="terror"))
engine.declare(Idioma_preferido(valor="Inglés"))
engine.declare(Formato_preferido(valor="película"))

engine.run()








engine.run()