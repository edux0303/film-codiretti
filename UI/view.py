import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Sim11 - Registi in co-direzione"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (inizializzato nel main, dopo la creazione del controller)
        self._controller = None
        # graphical elements
        self._title = None
        self._ddanno1 = None
        self._ddanno2 = None
        self._btnCreaGrafo = None
        self._btnCammino = None
        self.txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP - Grafo dei registi (co-direzione)",
                              color="blue", size=24)
        self._page.controls.append(self._title)

        # --- Riga 1: dropdown anno min/max + bottone Crea Grafo ---
        self._ddanno1 = ft.Dropdown(label="Anno min", hint_text="Anno minimo")
        self._ddanno2 = ft.Dropdown(label="Anno max", hint_text="Anno massimo")

        # il controller esiste gia': il main chiama set_controller
        # PRIMA di load_interface
        self._controller.fillDDsAnni()

        self._btnCreaGrafo = ft.ElevatedButton(
            text="Crea Grafo",
            on_click=self._controller.handleCreaGrafo)

        row1 = ft.Row([self._ddanno1, self._ddanno2, self._btnCreaGrafo],
                      alignment=ft.MainAxisAlignment.CENTER,
                      vertical_alignment=ft.CrossAxisAlignment.END)
        self._page.controls.append(row1)

        # --- Riga 2: bottone del punto 2 ---
        self._btnCammino = ft.ElevatedButton(
            text="Cerca percorso",
            on_click=self._controller.handleCammino)
        row2 = ft.Row([self._btnCammino],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # List View dove viene stampato l'output
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20,
                                      auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
