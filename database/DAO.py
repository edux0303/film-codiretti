from database.DB_connect import DBConnect
from model.regista import Regista


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        """Anni distinti dei film, per i due menù a tendina."""
        cnx = DBConnect.get_connection()
        if cnx is None:
            return None
        result = []
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT m.year AS anno
                   FROM movie m
                   WHERE m.year IS NOT NULL
                   ORDER BY anno ASC"""
        try:
            cursor.execute(query)
            for row in cursor:
                result.append(row["anno"])
        except Exception as e:
            print(f"Errore in getAllYears: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodi(minA, maxA):
        """Nodi = registi che hanno diretto almeno un film nel range."""
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            return result
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT n.id, n.name
                   FROM names n, director_mapping dm, movie m
                   WHERE n.id = dm.name_id
                     AND dm.movie_id = m.id
                     AND m.year BETWEEN %s AND %s"""
        try:
            cursor.execute(query, (minA, maxA))
            for row in cursor:
                result.append(Regista(**row))
        except Exception as e:
            print(f"Errore in getNodi: {e}")
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(minA, maxA):
        """Archi = coppie di registi che hanno CO-DIRETTO almeno uno
        STESSO film del range. Peso = numero di film co-diretti.
        NB la differenza strutturale rispetto alle varianti 'anche in
        film diversi': qui il perno e' dm1.movie_id = dm2.movie_id
        (STESSO FILM), quindi basta UNA copia di movie per il filtro
        anni — il film e' uno solo, non due catene indipendenti.
        Niente DISTINCT nel COUNT necessario in teoria (la PK di
        director_mapping impedisce duplicati), ma lo tengo per
        esplicitare 'film distinti'."""
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            return result
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT dm1.name_id AS r1, dm2.name_id AS r2,
                          COUNT(DISTINCT dm1.movie_id) AS peso  -- film co-diretti
                   FROM director_mapping dm1, director_mapping dm2,
                        movie m
                   WHERE dm1.movie_id = dm2.movie_id   -- PERNO: STESSO film
                     AND dm1.movie_id = m.id           -- aggancio al film (unico)
                     AND m.year BETWEEN %s AND %s      -- filtro anni (una volta sola)
                     AND dm1.name_id < dm2.name_id     -- anti-self-loop/duplicati
                   GROUP BY dm1.name_id, dm2.name_id"""
        try:
            cursor.execute(query, (minA, maxA))
            for row in cursor:
                result.append(row)
        except Exception as e:
            print(f"Errore in getEdges: {e}")
        finally:
            cursor.close()
            cnx.close()
        return result