import random
from typing import Optional

from services.dao_protocols import PoemDAOProtocol

POEMAS = [
    "Podrá nublarse el sol eternamente;\nPodrá secarse en un instante el mar;\nPodrá romperse el eje de la tierra\nComo un débil cristal.\n¡Todo sucederá! Podrá la muerte\nCubrirme con su fúnebre crespón;\nPero jamás en mí podrá apagarse\nLa llama de tu amor.\n- Bécquer",
    "Te quiero no por quien eres,\nsino por quien soy cuando estoy contigo.\n- García Márquez",
    "Me gustas cuando callas porque estás como ausente,\ny me oyes desde lejos, y mi voz no te toca.\nParece que los ojos se te hubieran volado\ny parece que un beso te cerrara la boca.\n- Pablo Neruda",
    "El amor es una flor que debes dejar crecer.\n- John Lennon",
    "Si sé lo que es el amor, es gracias a ti.\n- Herman Hesse",
    "Hagamos un trato:\nyo me encargo de quererte,\ny tú de dejarte querer.",
    "Eres la casualidad más bonita que llegó a mi vida.",
    "Andábamos sin buscarnos pero sabiendo que andábamos para encontrarnos.\n- Julio Cortázar"
]

class PoemService:
    def __init__(self, poem_dao: PoemDAOProtocol) -> None:
        self._poem_dao = poem_dao

    def get_poem(self) -> str:
        if random.choice([True, False]):
            db_poem = self._poem_dao.get_random_poem()
            if db_poem:
                return db_poem
        return random.choice(POEMAS)

    def add_poem(self, content: str, author_id: int) -> None:
        self._poem_dao.add_poem(content, author_id)
