import tkinter as tk
from tkinter import ttk, messagebox

from service.tarea_service import TareaService


class AppWindow:
    def __init__(self, proyecto_service, tarea_service):

        self.proyecto_service = proyecto_service
        self.tarea_service = tarea_service

        self.proyecto_actual = None

        self.root = tk.Tk()
        self.root.title("Gestor de Tareas")
        self.root.geometry("850x500")
        self.root.configure(bg="#0d1b2a")  # Azul oscuro

        self.crear_interfaz()

    def crear_interfaz(self):

        # ===== FRAME PRINCIPAL =====

        frame_principal = tk.Frame(self.root, bg="#0d1b2a")
        frame_principal.grid(row=0, column=0, padx=10, pady=10)

        # ==========================
        # PROYECTOS
        # ==========================

        frame_proyectos = tk.LabelFrame(
            frame_principal,
            text="Proyectos",
            bg="#a8dadc",   # Verde claro
            fg="black",
            padx=10,
            pady=10
        )

        frame_proyectos.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        tk.Label(
            frame_proyectos,
            text="Lista de Proyectos",
            bg="#a8dadc",
            fg="black"
        ).grid(row=0, column=0, pady=5)

        self.listbox = tk.Listbox(
            frame_proyectos,
            width=30,
            bg="white"
        )

        self.listbox.grid(row=1, column=0, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.seleccionar_proyecto)

        self.entry_proyecto = tk.Entry(frame_proyectos)
        self.entry_proyecto.grid(row=2, column=0, pady=5)

        tk.Button(
            frame_proyectos,
            text="Crear Proyecto",
            bg="#1d3557",
            fg="white",
            command=self.crear_proyecto
        ).grid(row=3, column=0, pady=3, sticky="ew")

        tk.Button(
            frame_proyectos,
            text="Eliminar Proyecto",
            bg="#457b9d",
            fg="white",
            command=self.eliminar_proyecto
        ).grid(row=4, column=0, pady=3, sticky="ew")

        tk.Button(
            frame_proyectos,
            text="Editar Proyecto",
            bg="#1d3557",
            fg="white",
            command=self.editar_proyecto
        ).grid(row=5, column=0, pady=3, sticky="ew")

        # ==========================
        # TAREAS
        # ==========================

        frame_tareas = tk.LabelFrame(
            frame_principal,
            text="Tareas",
            bg="#1b263b",
            fg="white",
            padx=10,
            pady=10
        )

        frame_tareas.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(
            frame_tareas,
            text="Lista de Tareas",
            bg="#1b263b",
            fg="white"
        ).grid(row=0, column=0, pady=5)

        self.tree = ttk.Treeview(
            frame_tareas,
            columns=("Nombre", "Descripcion", "Estado"),
            show="headings",
            height=10
        )

        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripcion", text="Descripcion")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("Nombre", width=150)
        self.tree.column("Descripcion", width=250)
        self.tree.column("Estado", width=80)

        self.tree.grid(row=1, column=0, pady=5)

        self.entry_tarea = tk.Entry(frame_tareas)
        self.entry_tarea.grid(row=2, column=0, pady=5, sticky="ew")

        self.entry_desc = tk.Entry(frame_tareas)
        self.entry_desc.grid(row=3, column=0, pady=5, sticky="ew")

        tk.Button(
            frame_tareas,
            text="Crear Tarea",
            bg="#1d3557",
            fg="white",
            command=self.crear_tarea
        ).grid(row=4, column=0, pady=3, sticky="ew")

        tk.Button(
            frame_tareas,
            text="Eliminar Tarea",
            bg="#457b9d",
            fg="white",
            command=self.eliminar_tarea
        ).grid(row=5, column=0, pady=3, sticky="ew")

        tk.Button(
            frame_tareas,
            text="Completar",
            bg="#1d3557",
            fg="white",
            command=self.completar_tarea
        ).grid(row=6, column=0, pady=3, sticky="ew")

        tk.Button(
            frame_tareas,
            text="Editar Tarea",
            bg="#457b9d",
            fg="white",
            command=self.editar_tarea
        ).grid(row=7, column=0, pady=3, sticky="ew")

        self.cargar_proyectos()

    # ======================
    # PROYECTOS
    # ======================

    def cargar_proyectos(self):

        self.listbox.delete(0, tk.END)

        proyectos = self.proyecto_service.obtener_proyectos()

        for p in proyectos:
            self.listbox.insert(tk.END, p.nombre)

    def seleccionar_proyecto(self, event):

        seleccion = self.listbox.curselection()

        if seleccion:
            index = seleccion[0]
            proyectos = self.proyecto_service.obtener_proyectos()

            self.proyecto_actual = proyectos[index]
            self.cargar_tareas()

    def crear_proyecto(self):

        nombre = self.entry_proyecto.get()

        try:
            self.proyecto_service.crear_proyecto(nombre)
            self.cargar_proyectos()
            self.entry_proyecto.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_proyecto(self):

        seleccion = self.listbox.curselection()

        if seleccion:
            index = seleccion[0]
            proyectos = self.proyecto_service.obtener_proyectos()

            proyecto = proyectos[index]

            self.proyecto_service.eliminar_proyecto(proyecto.uuid)
            self.cargar_proyectos()

    def editar_proyecto(self):

        seleccion = self.listbox.curselection()

        if not seleccion:
            return

        index = seleccion[0]
        proyectos = self.proyecto_service.obtener_proyectos()

        proyecto = proyectos[index]

        nuevo_nombre = self.entry_proyecto.get()

        self.proyecto_service.actualizar_proyecto(
            proyecto.uuid,
            nuevo_nombre
        )

        self.cargar_proyectos()

    # ======================
    # TAREAS
    # ======================

    def cargar_tareas(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        tareas = self.tarea_service.obtener_tareas()

        for tarea in tareas:

            if tarea.proyecto_uuid == self.proyecto_actual.uuid:

                estado = "✔" if tarea.completada else "✘"

                self.tree.insert(
                    "",
                    "end",
                    iid=tarea.uuid,
                    values=(
                        tarea.nombre,
                        tarea.descripcion,
                        estado
                    )
                )

    def crear_tarea(self):

        if not self.proyecto_actual:
            messagebox.showwarning("Aviso", "Seleccione un proyecto")
            return

        nombre = self.entry_tarea.get()
        descripcion = self.entry_desc.get()

        self.tarea_service.crear_tarea(
            nombre,
            descripcion,
            self.proyecto_actual.uuid
        )

        self.cargar_tareas()

        self.entry_tarea.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)

    def eliminar_tarea(self):

        seleccion = self.tree.selection()

        if seleccion:
            uuid = seleccion[0]
            self.tarea_service.eliminar_tarea(uuid)
            self.cargar_tareas()

    def completar_tarea(self):

        seleccion = self.tree.selection()

        if seleccion:
            uuid = seleccion[0]
            self.tarea_service.completar_tarea(uuid)
            self.cargar_tareas()

    def editar_tarea(self):

        seleccion = self.tree.selection()

        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione una tarea")
            return

        uuid = seleccion[0]

        nuevo_nombre = self.entry_tarea.get()
        nueva_desc = self.entry_desc.get()

        try:
            self.tarea_service.repo.actualizar_tarea(
                uuid,
                nuevo_nombre,
                nueva_desc,
                False
            )

            self.cargar_tareas()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()