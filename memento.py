"""Memento pattern concept"""


class Memento:
    """
    A container of state
    """

    def __init__(self, blacks):
        #self.piece = piece
        #self.move = move
        self.blacks = blacks


class Originator:
    """
    The Object in the application whose state changes
    """

    def __init__(self):
        self.blacks = []

    @property
    def state(self):
        return self.blacks

    @state.setter
    def state(self, blacks):
        print(f"Originator: Setting state to `{blacks}`")
        self.blacks = blacks

    @property
    def memento(self):
        "A `getter` for the objects state but packaged as a Memento"
        print("Originator: Providing Memento of state to caretaker.")
        return Memento(self.blacks)

    @memento.setter
    def memento(self, memento):
        self.blacks = memento.blacks
        print(
            f"Originator: State after restoring from Memento: "
            f"`{self.blacks}`")


class CareTaker:
    """
    Guardian. Provides a narrow interface to the mementos
    """
    def __init__(self, originator):
        self._originator = originator
        self._mementos = []

    def save(self):
        "Store a new Memento of the Originators current state"
        print("CareTaker: Getting a copy of Originators current state")
        memento = self._originator.memento
        #print(memento.board)
        self._mementos.append(memento)

    def restore(self, index):
        """
        Replace the Originators current state with the state
        stored in the saved Memento
        """
        print("CareTaker: Restoring Originators state from Memento")
        memento = self._mementos[index]
        #print(memento.board)
        self._originator.memento = memento