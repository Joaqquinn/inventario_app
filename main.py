from db import init_db
from gui import InventoryApp

if __name__ == '__main__':
    init_db()
    app = InventoryApp()
    app.mainloop()
