import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()   # NON orientato, pesato
        self._idMap = {}           # id regista -> oggetto Regista
        self._camminoBest = []

    def getYears(self):
        return DAO.getAllYears()

    # -------------------- PUNTO 1 --------------------

    def buildGraph(self, minA, maxA):
        self._grafo.clear()
        self._idMap = {}

        nodi = DAO.getNodi(minA, maxA)
        self._idMap = {reg.id: reg for reg in nodi}
        self._grafo.add_nodes_from(nodi)

        for e in DAO.getEdges(minA, maxA):
            # qui nodi e archi hanno gli stessi filtri (nessuna
            # validazione extra sui nodi), quindi il check e' pura
            # cintura di sicurezza — ma il pattern resta
            if e["r1"] in self._idMap and e["r2"] in self._idMap:
                self._grafo.add_edge(self._idMap[e["r1"]],
                                     self._idMap[e["r2"]],
                                     weight=e["peso"])

    # ---------------- punto 1c (arricchito) ----------------

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getTop5Archi(self):
        """5 archi di peso MAGGIORE (coppie con piu' film co-diretti)."""
        archi = sorted(self._grafo.edges(data=True),
                       key=lambda e: e[2]["weight"], reverse=True)
        return [(u, v, d["weight"]) for u, v, d in archi[:5]]

    def getRegistaGradoMax(self):
        """(regista, grado) del nodo con grado massimo: il regista che
        ha co-diretto con piu' colleghi DIVERSI (il grado conta i vicini,
        non i film). None se il grafo e' vuoto."""
        if self.getNumNodi() == 0:
            return None
        nodo, grado = max(self._grafo.degree(), key=lambda x: x[1])
        return nodo, grado

    def getNumNodiIsolati(self):
        """Registi senza alcuna co-direzione (grado 0): con questo tipo
        di arco saranno la stragrande maggioranza — la maggior parte
        dei film ha un solo regista."""
        return len([n for n, g in self._grafo.degree() if g == 0])

    def getNumComponenti(self):
        return nx.number_connected_components(self._grafo)

    def getMaxComponente(self):
        if self.getNumNodi() == 0:
            return []
        return list(max(nx.connected_components(self._grafo), key=len))

    # ------- PUNTO 2: cammino massimo a pesi NON DECRESCENTI -------

    def getCamminoMax(self):
        """Vincolo sui PESI degli archi (>= del precedente), come la
        Sim2 originale: la ricorsione porta con se' il peso dell'ultimo
        arco attraversato. Peso iniziale 0: i pesi reali sono >= 1,
        quindi il primo arco e' sempre ammesso."""
        self._camminoBest = []
        for nodo in self._grafo.nodes:
            self._ricorsione([nodo], 0)
        return self._camminoBest

    def _ricorsione(self, parziale, pesoPrecedente):
        if len(parziale) > len(self._camminoBest):
            self._camminoBest = list(parziale)   # copia, non riferimento

        ultimo = parziale[-1]
        for vicino in self._grafo.neighbors(ultimo):
            peso = self._grafo[ultimo][vicino]["weight"]
            # cammino semplice + peso non decrescente (>=, non >)
            if vicino not in parziale and peso >= pesoPrecedente:
                parziale.append(vicino)
                self._ricorsione(parziale, peso)
                parziale.pop()

    def getPesoCammino(self, cammino):
        """Pesi degli archi del cammino, per mostrare in stampa che
        sono non decrescenti."""
        pesi = []
        for i in range(len(cammino) - 1):
            pesi.append(self._grafo[cammino[i]][cammino[i + 1]]["weight"])
        return pesi