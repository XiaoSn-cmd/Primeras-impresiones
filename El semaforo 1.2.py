import tkinter as tk

class SemaforoControlable:
    def __init__(self, root):
        self.root = root
        self.root.title("Semáforo Controlable")
        self.root.geometry("300x580")
        self.root.configure(bg="#222222")

        # Variables de estado
        self.estado_actual = "rojo"  # "rojo", "amarillo", "verde"
        self.es_automatico = False
        self.timer_id = None

        # Canvas para el semáforo
        self.canvas = tk.Canvas(root, width=160, height=360, bg="#333333", highlightthickness=0)
        self.canvas.pack(pady=15)

        # Dibujo de las luces
        self.rojo = self.canvas.create_oval(30, 20, 130, 120, fill="#440000")
        self.amarillo = self.canvas.create_oval(30, 130, 130, 230, fill="#444400")
        self.verde = self.canvas.create_oval(30, 240, 130, 340, fill="#004400")

        # Indicador de estado
        self.lbl_estado = tk.Label(
            root, text="Modo: Manual | Luz: ROJO", 
            fg="#FFFFFF", bg="#222222", font=("Helvetica", 10, "bold")
        )
        self.lbl_estado.pack(pady=5)

        # Panel 1: Botones para cambiar color directo
        lbl_seleccion = tk.Label(root, text="Selección Manual:", fg="#AAAAAA", bg="#222222", font=("Helvetica", 9))
        lbl_seleccion.pack(pady=(5, 2))

        frame_luces = tk.Frame(root, bg="#222222")
        frame_luces.pack(pady=5)

        btn_rojo = tk.Button(
            frame_luces, text="Rojo", bg="#CC2222", fg="white", font=("Helvetica", 9, "bold"),
            width=7, command=lambda: self.cambiar_luz_directa("rojo")
        )
        btn_rojo.grid(row=0, column=0, padx=3)

        btn_amarillo = tk.Button(
            frame_luces, text="Amarillo", bg="#CCCC22", fg="black", font=("Helvetica", 9, "bold"),
            width=7, command=lambda: self.cambiar_luz_directa("amarillo")
        )
        btn_amarillo.grid(row=0, column=1, padx=3)

        btn_verde = tk.Button(
            frame_luces, text="Verde", bg="#22CC22", fg="white", font=("Helvetica", 9, "bold"),
            width=7, command=lambda: self.cambiar_luz_directa("verde")
        )
        btn_verde.grid(row=0, column=2, padx=3)

        # Panel 2: Controles del ciclo
        frame_ciclo = tk.Frame(root, bg="#222222")
        frame_ciclo.pack(pady=10)

        btn_siguiente = tk.Button(
            frame_ciclo, text="⏭ Siguiente Luz", bg="#444444", fg="white",
            width=20, command=self.siguiente_manual
        )
        btn_siguiente.pack(pady=3)

        self.btn_auto = tk.Button(
            frame_ciclo, text="▶ Iniciar Automático", bg="#1E5AA8", fg="white",
            width=20, font=("Helvetica", 9, "bold"), command=self.conmutar_modo_automatico
        )
        self.btn_auto.pack(pady=3)

        # Render inicial
        self.actualizar_interfaz()

    def apagar_luces(self):
        self.canvas.itemconfig(self.rojo, fill="#440000")
        self.canvas.itemconfig(self.amarillo, fill="#444400")
        self.canvas.itemconfig(self.verde, fill="#004400")

    def actualizar_interfaz(self):
        self.apagar_luces()

        if self.estado_actual == "rojo":
            self.canvas.itemconfig(self.rojo, fill="#FF0000")
        elif self.estado_actual == "amarillo":
            self.canvas.itemconfig(self.amarillo, fill="#FFFF00")
        elif self.estado_actual == "verde":
            self.canvas.itemconfig(self.verde, fill="#00FF00")

        modo_str = "Automático" if self.es_automatico else "Manual"
        self.lbl_estado.config(text=f"Modo: {modo_str} | Luz: {self.estado_actual.upper()}")

    def cambiar_luz_directa(self, nueva_luz):
        self.detener_automatico()
        self.estado_actual = nueva_luz
        self.actualizar_interfaz()

    def avanzar_secuencia(self):
        secuencia = {"rojo": "verde", "verde": "amarillo", "amarillo": "rojo"}
        self.estado_actual = secuencia[self.estado_actual]

    def siguiente_manual(self):
        self.detener_automatico()
        self.avanzar_secuencia()
        self.actualizar_interfaz()

    def ciclo_automatico(self):
        if not self.es_automatico:
            return

        self.avanzar_secuencia()
        self.actualizar_interfaz()

        # Tiempos de encendido (milisegundos)
        duraciones = {"rojo": 6000, "verde": 2000, "amarillo": 1500}
        tiempo = duraciones[self.estado_actual]

        self.timer_id = self.root.after(tiempo, self.ciclo_automatico)

    def conmutar_modo_automatico(self):
        if self.es_automatico:
            self.detener_automatico()
        else:
            self.es_automatico = True
            self.btn_auto.config(text="⏸ Pausar Automático", bg="#A83232")
            self.ciclo_automatico()

    def detener_automatico(self):
        self.es_automatico = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.btn_auto.config(text="▶ Iniciar Automático", bg="#1E5AA8")
        self.actualizar_interfaz()

if __name__ == "__main__":
    ventana = tk.Tk()
    app = SemaforoControlable(ventana)
    ventana.mainloop()