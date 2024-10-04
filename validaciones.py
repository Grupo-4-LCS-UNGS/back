import re

class Valida:

    def patente(patente):
        return re.match(r"^[A-Z]{3}[0-9]{3}$|^[A-Z]{2}[0-9]{3}[A-Z]{2}$", patente) is not None

    def email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def nombre(nombre):
        return re.match(r"^[a-zA-Z\s]+$", nombre) is not None

    def contrasena(contrasena):
        return re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", contrasena) is not None