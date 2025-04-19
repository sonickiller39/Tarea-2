class Nodo:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.anterior = None
        self.siguiente = None

class ListaVuelos:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.size = 0

    def insertar_al_frente(self, vuelo):
        nodo = Nodo(vuelo)
        nodo.siguiente = self.cabeza
        if self.cabeza:
            self.cabeza.anterior = nodo
        else:
            self.cola = nodo
        self.cabeza = nodo
        self.size += 1

    def insertar_al_final(self, vuelo):
        nodo = Nodo(vuelo)
        nodo.anterior = self.cola
        if self.cola:
            self.cola.siguiente = nodo
        else:
            self.cabeza = nodo
        self.cola = nodo
        self.size += 1

    def obtener_primero(self):
        return self.cabeza.vuelo if self.cabeza else None

    def obtener_ultimo(self):
        return self.cola.vuelo if self.cola else None

    def longitud(self):
        return self.size

    def recorrer(self):
        actual = self.cabeza
        lista = []
        while actual:
            lista.append(actual.vuelo)
            actual = actual.siguiente
        return lista
