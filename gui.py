import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db import init_db, ejecutar, consultar, get_movements, delete_item, backup_db
from datetime import datetime
import csv

# Usuarios estáticos (en futura versión se podrían almacenar en BD)
USERS = {
    "admin":   {"password": "admin",   "role": "admin"},
    "manager": {"password": "manager", "role": "manager"},
    "viewer":  {"password": "viewer",  "role": "viewer"}
}

class LoginWindow(tk.Tk):
    """
    Pantalla de login que solicita usuario y contraseña.
    Al autenticarse, inicia la aplicación principal con el rol correspondiente.
    """
    def __init__(self):
        super().__init__()
        self.title("Login - Inventarios")
        self.geometry("300x160")
        self.resizable(False, False)
        
        ttk.Label(self, text="Usuario:").pack(pady=(15,0))
        self.user_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.user_var).pack()

        ttk.Label(self, text="Contraseña:").pack(pady=(10,0))
        self.pw_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.pw_var, show="*").pack()

        ttk.Button(self, text="Entrar", command=self._login).pack(pady=15)

    def _login(self):
        user = self.user_var.get().strip()
        pw   = self.pw_var.get().strip()
        info = USERS.get(user)
        if info and pw == info['password']:
            self.destroy()
            init_db()
            app = InventoryApp(user, info['role'])
            app.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrecta.")

class InventoryApp(tk.Tk):
    """
    Aplicación principal de gestión de inventarios.
    Configura la UI según el rol del usuario.
    """
    def __init__(self, username, role):
        super().__init__()
        self.username = username
        self.role     = role
        self.title(f"Inventarios - {username} ({role})")
        self.geometry("900x600")

        self._build_ui()
        self._refresh_items()
        self._schedule_low_stock_alert()

    def _build_ui(self):
        # Barra de búsqueda siempre
        search_frm = ttk.Frame(self)
        search_frm.pack(fill='x', padx=10, pady=(10,0))
        ttk.Label(search_frm, text="Buscar:").pack(side='left')
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frm, textvariable=self.search_var)
        search_entry.pack(side='left', fill='x', expand=True, padx=5)
        search_entry.bind("<KeyRelease>", lambda e: self._refresh_items())

        # Formulario de registro solo para manager/admin
        if self.role in ("manager","admin"):
            frm = ttk.LabelFrame(self, text="Registrar ítem")
            frm.pack(fill='x', padx=10, pady=5)
            ttk.Label(frm, text="Nombre:").grid(row=0, column=0)
            self.nombre_var = tk.StringVar()
            ttk.Entry(frm, textvariable=self.nombre_var).grid(row=0, column=1)
            ttk.Label(frm, text="Descripción:").grid(row=1, column=0)
            self.desc_var = tk.StringVar()
            ttk.Entry(frm, textvariable=self.desc_var).grid(row=1, column=1)
            ttk.Label(frm, text="Stock inicial:").grid(row=2, column=0)
            self.stock_var = tk.IntVar(value=0)
            ttk.Entry(frm, textvariable=self.stock_var).grid(row=2, column=1)
            ttk.Label(frm, text="Stock mínimo:").grid(row=3, column=0)
            self.min_var = tk.IntVar(value=1)
            ttk.Entry(frm, textvariable=self.min_var).grid(row=3, column=1)
            ttk.Button(frm, text="Agregar", command=self._add_item).grid(row=4, column=0, columnspan=2, pady=5)

        # Tabla de ítems
        cols = ("ID","Nombre","Stock","Mínimo")
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)

        # Botones de acción según rol
        btn_frm = ttk.Frame(self)
        btn_frm.pack(fill='x', padx=10, pady=(0,10))
        actions = []
        # Acciones comunes
        actions.extend([
            ("Entrada +", lambda: self._movimiento('entrada')),
            ("Salida –", lambda: self._movimiento('salida')),
            ("Historial", self._view_history),
            ("Exportar CSV", self._export_csv),
            ("Dashboard", self._show_dashboard)
        ])
        # Manager/Admin agregan operaciones de modificación
        if self.role in ("manager","admin"):
            actions.insert(0, ("Editar", self._edit_item))
            actions.insert(0, ("Eliminar", self._delete_item))
            if self.role == "admin":
                actions.insert(0, ("Respaldo BD", self._backup_db))
            actions.insert(0, ("Importar CSV", self._import_csv))

        for (txt, cmd) in actions:
            ttk.Button(btn_frm, text=txt, command=cmd).pack(side='left', padx=5)

    # Resto de métodos (_add_item, _refresh_items, _movimiento, etc.) se mantienen igual que antes...
    
    def _add_item(self):
        nombre = self.nombre_var.get().strip()
        if not nombre:
            return messagebox.showwarning("Atención", "El nombre no puede estar vacío.")
        ejecutar(
            "INSERT INTO items (nombre, descripcion, stock, stock_minimo) VALUES (?,?,?,?)",
            (nombre, self.desc_var.get(), self.stock_var.get(), self.min_var.get())
        )
        self._refresh_items()

    def _refresh_items(self):
        filtro = getattr(self, 'search_var', tk.StringVar()).get().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        rows = consultar("SELECT id,nombre,stock,stock_minimo FROM items")
        for id_, nombre, stock, minimo in rows:
            if filtro and filtro not in nombre.lower():
                continue
            tag = 'bajo' if stock <= minimo else ''
            self.tree.insert('', 'end', values=(id_, nombre, stock, minimo), tags=(tag,))
        self.tree.tag_configure('bajo', background='#fdd')

    def _movimiento(self, tipo):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showinfo("Info", "Selecciona un ítem primero.")
        item_id, nombre, stock, minimo = self.tree.item(sel[0])['values']
        delta = 1 if tipo=='entrada' else -1
        nuevo = stock + delta
        ejecutar("UPDATE items SET stock=? WHERE id=?", (nuevo, item_id))
        ejecutar(
            "INSERT INTO movimientos (item_id,cantidad,tipo,fecha) VALUES (?,?,?,?)",
            (item_id, abs(delta), tipo, datetime.now().isoformat())
        )
        self._refresh_items()

    def _edit_item(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showinfo("Info", "Selecciona un ítem para editar.")
        item_id, nombre, stock, minimo = self.tree.item(sel[0])['values']
        win = tk.Toplevel(self)
        win.title("Editar ítem")
        ttk.Label(win, text="Nombre:").grid(row=0,column=0)
        name_var = tk.StringVar(value=nombre)
        ttk.Entry(win, textvariable=name_var).grid(row=0,column=1)
        ttk.Label(win, text="Stock mínimo:").grid(row=1,column=0)
        min_var = tk.IntVar(value=minimo)
        ttk.Entry(win, textvariable=min_var).grid(row=1,column=1)
        def save():
            ejecutar("UPDATE items SET nombre=?, stock_minimo=? WHERE id=?",
                    (name_var.get(), min_var.get(), item_id))
            win.destroy()
            self._refresh_items()
        ttk.Button(win, text="Guardar", command=save).grid(row=2,column=0,columnspan=2,pady=5)

    def _delete_item(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showinfo("Info", "Selecciona un ítem para eliminar.")
        item_id = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", "¿Eliminar ítem y sus movimientos?"):
            delete_item(item_id)
            self._refresh_items()

    def _view_history(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showinfo("Info", "Selecciona un ítem para ver historial.")
        item_id, nombre = self.tree.item(sel[0])['values'][:2]
        win = tk.Toplevel(self)
        win.title(f"Historial de {nombre}")
        cols = ("Fecha","Tipo","Cantidad")
        tv = ttk.Treeview(win, columns=cols, show='headings')
        for c in cols: tv.heading(c, text=c)
        tv.pack(fill='both', expand=True)
        for tipo, cantidad, fecha in get_movements(item_id):
            tv.insert('', 'end', values=(fecha, tipo, cantidad))

    def _export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not path: return
        rows = consultar("SELECT id,nombre,descripcion,stock,stock_minimo FROM items")
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID","Nombre","Descripción","Stock","Stock mínimo"])
            writer.writerows(rows)
        messagebox.showinfo("Exportar CSV", f"Lista exportada en:\n{path}")

    def _import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV","*.csv")])
        if not path: return
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ejecutar(
                    "INSERT INTO items (nombre, descripcion, stock, stock_minimo) VALUES (?,?,?,?)",
                    (row['Nombre'], row.get('Descripción',''), int(row['Stock']), int(row['Stock mínimo']))
                )
        self._refresh_items()
        messagebox.showinfo("Importar CSV", f"Datos importados desde:\n{path}")

    def _backup_db(self):
        path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite DB","*.db")])
        if not path: return
        backup_db(path)
        messagebox.showinfo("Respaldo BD", f"Base de datos respaldada en:\n{path}")

    def _show_dashboard(self):
        total = consultar("SELECT COUNT(*) FROM items")[0][0]
        low   = consultar("SELECT COUNT(*) FROM items WHERE stock <= stock_minimo")[0][0]
        win = tk.Toplevel(self)
        win.title("Dashboard")
        ttk.Label(win, text=f"Total de ítems: {total}").pack(padx=10, pady=5)
        ttk.Label(win, text=f"Ítems con stock bajo: {low}").pack(padx=10, pady=5)

    def _check_low_stock(self):
        low = consultar("SELECT nombre FROM items WHERE stock <= stock_minimo")
        if low:
            nombres = ', '.join([n[0] for n in low])
            messagebox.showwarning("Alerta Stock Bajo", f"Stock bajo para: {nombres}")
        self._schedule_low_stock_alert()

    def _schedule_low_stock_alert(self):
        self.after(60000, self._check_low_stock)

if __name__ == '__main__':
    login = LoginWindow()
    login.mainloop()
