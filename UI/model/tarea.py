import uuid

class Proyecto:
    def __init__(self, nombre):
        self.nombre = str(nombre)
        self.uuid = str(uuid.uuid4())
       

class Tarea:
    def __init__(self, nombre, descripcion, proyecto_uuid):
        self.uuid = str(uuid.uuid4())
        self.nombre = nombre
        self.descripcion = descripcion
        self.completada = False
        self.proyecto_uuid = proyecto_uuid
        