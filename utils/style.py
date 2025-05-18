from tkinter import ttk

def aplicar_estilos_generales():
    style = ttk.Style()
    style.theme_use("default")

    # Tabla (Treeview)
    style.configure("Treeview",
                    font=("Arial", 10),
                    background="#f9f9f9",
                    foreground="#000000",
                    rowheight=25,
                    fieldbackground="#f9f9f9")

    style.configure("Treeview.Heading",
                    font=("Arial", 11, "bold"),
                    background="#007ACC",
                    foreground="white")

    # Opcional: más estilos para botones, labels, etc. podrían definirse aquí si se usan estilos personalizados
