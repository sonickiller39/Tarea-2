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
        self.cabeza = nodo
        if self.cola is None:
            self.cola = nodo
        self.size += 1

    def insertar_al_final(self, vuelo):
        nodo = Nodo(vuelo)
        nodo.anterior = self.cola
        if self.cola:
            self.cola.siguiente = nodo
        self.cola = nodo
        if self.cabeza is None:
            self.cabeza = nodo
        self.size += 1

    def obtener_primero(self):
        return self.cabeza.vuelo if self.cabeza else None

    def obtener_ultimo(self):
        return self.cola.vuelo if self.cola else None

    def longitud(self):
        return self.size

    def insertar_en_posicion(self, vuelo, posicion):
        if posicion <= 0:
            self.insertar_al_frente(vuelo)
        elif posicion >= self.size:
            self.insertar_al_final(vuelo)
        else:
            nodo = Nodo(vuelo)
            actual = self.cabeza
            for _ in range(posicion):
                actual = actual.siguiente
            nodo.anterior = actual.anterior
            nodo.siguiente = actual
            if actual.anterior:
                actual.anterior.siguiente = nodo
            actual.anterior = nodo
            self.size += 1

    def extraer_de_posicion(self, posicion):
        if self.size == 0 or posicion < 0 or posicion >= self.size:
            return None
        actual = self.cabeza
        for _ in range(posicion):
            actual = actual.siguiente
        if actual.anterior:
            actual.anterior.siguiente = actual.siguiente
        else:
            self.cabeza = actual.siguiente
        if actual.siguiente:
            actual.siguiente.anterior = actual.anterior
        else:
            self.cola = actual.anterior
        self.size -= 1
        return actual.vuelo

    def recorrer(self):
        actual = self.cabeza
        lista = []
        while actual:
            lista.append(actual.vuelo)
            actual = actual.siguiente
        return lista
