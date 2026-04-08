from repository.Tarea_repository import proyectoRepository, tareaRepository


class TareaService:
    def __init__(self, proyecto_repo: proyectoRepository, tarea_repo: tareaRepository):
        # Repositorio de tareas (dentro de proyecto)
        self.proyecto_repo = proyecto_repo
        self.repo = tarea_repo

    def crear_tarea(self, nombre, descripcion, proyecto_uuid):
        if not nombre:
            raise ValueError("El nombre es obligatorio")

        if not descripcion:
            raise ValueError("La descripción es obligatoria")

        # validar que el proyecto exista
        proyectos = self.proyecto_repo.obtener_proyecto()
        existe = any(p.uuid == proyecto_uuid for p in proyectos)

        if not existe:
            raise ValueError("El proyecto no existe")

        # Crear tarea
        return self.repo.crear_tarea(nombre, descripcion, proyecto_uuid)

    def obtener_tareas(self):
        return self.repo.obtener_tarea()

    def eliminar_tarea(self, uuid):
        self.repo.eliminar_tarea(uuid)

    def completar_tarea(self, uuid):
        # Buscar tarea y marcarla como completada
        tareas = self.repo.obtener_tarea()

        for tarea in tareas:
            if tarea.uuid == uuid:
                return self.repo.actualizar_tarea(
                    uuid,
                    tarea.nombre,
                    tarea.descripcion,
                    True
                )

        raise ValueError("Tarea no encontrada")

    def obtener_tareas_por_proyecto(self, proyecto_uuid):
        tareas = self.repo.obtener_tarea()
        return [t for t in tareas if t.proyecto_uuid == proyecto_uuid]