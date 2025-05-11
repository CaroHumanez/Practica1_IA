from rdflib import Graph, Namespace
from owlrl import DeductiveClosure, RDFS_Semantics
from experta import Fact

# Definición del hecho
class Contenido(Fact):
    nombre = ""
    genero = ""
    clasificacion = ""

# Namespace usado en tu ontología
SPACE = Namespace("http://example.org/space#")

# Cargar y razonar el grafo
g = Graph()
g.parse("contenido.ttl", format="turtle")  # Ajusta el nombre si es distinto
DeductiveClosure(RDFS_Semantics).expand(g)

# Extraer contenidos (películas y series)
contenidos = []
for tipo in [SPACE.Pelicula, SPACE.Serie]:
    for s in g.subjects(predicate=None, object=tipo):
        nombre = s.split("#")[-1]
        genero = g.value(s, SPACE.tieneGenero)
        clasif = g.value(s, SPACE.tieneClasificacion)

        if genero and clasif:
            contenidos.append({
                "nombre": nombre,
                "genero": genero.split("#")[-1],
                "clasificacion": clasif.split("#")[-1]
            })

# Declarar hechos en Experta
from experta import KnowledgeEngine

class MotorContenido(KnowledgeEngine):
    def cargar_contenidos(self, contenidos):
        for c in contenidos:
            self.declare(Contenido(
                nombre=c["nombre"],
                genero=c["genero"],
                clasificacion=c["clasificacion"]
            ))

# Ejemplo de uso
if __name__ == "__main__":
    motor = MotorContenido()
    motor.reset()
    motor.cargar_contenidos(contenidos)
    motor.run()
