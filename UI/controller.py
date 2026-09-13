import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._minAnno = None
        self._maxAnno = None

    def fillDDsAnni(self):
        anni = self._model.getYears()
        if anni is None:
            self._view.create_alert("Errore di connessione al database")
            return
        for a in anni:
            self._view._ddanno1.options.append(
                ft.dropdown.Option(text=str(a), on_click=self.readDDMin))
            self._view._ddanno2.options.append(
                ft.dropdown.Option(text=str(a), on_click=self.readDDMax))

    def readDDMin(self, e):
        self._minAnno = int(e.control.text)

    def readDDMax(self, e):
        self._maxAnno = int(e.control.text)

    # ---------------- PUNTO 1 ----------------

    def handleCreaGrafo(self, e):
        if self._minAnno is None or self._maxAnno is None:
            self._view.create_alert("Selezionare entrambi gli anni (min e max)")
            return
        if self._minAnno > self._maxAnno:
            self._view.create_alert("L'anno minimo deve essere <= del massimo")
            return

        self._model.buildGraph(self._minAnno, self._maxAnno)

        out = self._view.txt_result.controls
        out.clear()
        out.append(ft.Text(f"Grafo creato: {self._model.getNumNodi()} vertici, "
                           f"{self._model.getNumArchi()} archi"))

        if self._model.getNumArchi() == 0:
            out.append(ft.Text("Nessuna co-direzione nel range selezionato."))
        else:
            out.append(ft.Text("I 5 archi di peso maggiore "
                               "(più film co-diretti):"))
            for reg1, reg2, peso in self._model.getTop5Archi():
                out.append(ft.Text(f"  {reg1.name} <-> {reg2.name}  |  "
                                   f"{peso} film insieme"))

        # --- punto 1c arricchito ---
        top = self._model.getRegistaGradoMax()
        if top is not None:
            regista, grado = top
            out.append(ft.Text(f"Regista di grado massimo: {regista.name} "
                               f"({grado} co-registi diversi)"))

        out.append(ft.Text(f"Nodi isolati (nessuna co-direzione): "
                           f"{self._model.getNumNodiIsolati()}"))
        out.append(ft.Text(f"Numero di componenti connesse: "
                           f"{self._model.getNumComponenti()}"))
        out.append(ft.Text(f"La componente connessa maggiore ha "
                           f"{len(self._model.getMaxComponente())} vertici"))
        self._view.update_page()

    # ------- PUNTO 2: cammino a pesi non decrescenti -------

    def handleCammino(self, e):
        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo")
            return

        cammino = self._model.getCamminoMax()
        out = self._view.txt_result.controls
        out.clear()

        if len(cammino) <= 1:
            out.append(ft.Text("Nessun cammino trovato (nessun arco)."))
            self._view.update_page()
            return

        out.append(ft.Text(f"Cammino trovato: {len(cammino) - 1} archi, "
                           f"{len(cammino)} registi (pesi non decrescenti):"))
        pesi = self._model.getPesoCammino(cammino)
        for i, regista in enumerate(cammino):
            out.append(ft.Text(f"  {regista}"))
            if i < len(pesi):
                out.append(ft.Text(f"     | peso arco = {pesi[i]}"))
        self._view.update_page()