
import hashlib


# Retorna un texto "encriptado" que se usa para almacenar el id_usuario en la cookie y que no sea visible
def hash_text(text: str) -> str:
    text: str = "entropía__" + text + "__universal"
    return hashlib.sha512(text.encode("utf-8")).hexdigest()
