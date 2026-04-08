from repository.Tarea_repository import proyectoRepository

class ProyectoService:
    def __init__(self, repo:proyectoRepository):
        # Instancia del repositorio de proyectos
        self.repo = repo

    def crear_proyecto(self, nombre):
        # Validar que el nombre no este vacio
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacío")

        # Crear proyecto usando el repositorio
        return self.repo.crear_proyecto(nombre)

    def obtener_proyectos(self):
        # Obtener lista de proyectos
        return self.repo.obtener_proyecto()

    def eliminar_proyecto(self, uuid):
        # Eliminar proyecto por su identificador
        self.repo.borrar_proyecto(uuid)

    def actualizar_proyecto(self, uuid, nombre):
        # Validar nombre antes de actualizar
        if not nombre:
            raise ValueError("Nombre inválido")

        return self.repo.actualizar_proyecto(uuid, nombre)
