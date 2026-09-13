from dataclasses import dataclass


@dataclass
class Regista:
    # i campi combaciano con le colonne della SELECT: Regista(**row)
    id: str        # id del regista, chiave primaria di names
    name: str      # nome

    def __hash__(self):
        return hash(self.id)          # nodi networkx: hashable per id

    def __eq__(self, other):
        return isinstance(other, Regista) and self.id == other.id

    def __str__(self):
        return self.name