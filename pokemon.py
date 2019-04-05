import pygame
from typing import List, Optional


class Move:
    """Represents a move a pokemon would use.

    === Attributes ===
    name: This move's name
    type_: The type of this move
    accuracy: The chance of this move successfully executing on the
              enemy pokemon
    power: The power/damage of this move

    === Representation Invarants ===
    - type_ should be an actual type from pokemon
    - 0 <= acccuracy <= 100
    - power >= 0
    """
    name: str
    type_: str
    accuracy: int
    power: int

    def __init__(self, name: str, type_: str, accuracy: int, power: int)\
            -> None:
        """Initialize this move"""

        self.name = name
        self.accuracy = accuracy
        self.power = power
        self.type_ = type_


class Pokemon:
    """Represents a pokemon.

    === Public Attributes ===
    name: This pokemon's name
    type_: This pokemon's type
    moves: The list of moves this pokemon has
    image: The pygame image of this pokemon

    === Private Attributes ===
    _level: Should prob be public
    _on: Status telling if pokemon is in battle

    === Representation Invariants ===
    - len(moves) < n
    - type_ should be one of the actual types
    - _level >= 1
    """
    name: str
    type_: str
    moves: List[Move]
    image: pygame.Surface
    _level: int
    _on: bool

    def __init__(self, name, type_: str, image: pygame.Surface,
                 move1: Optional[Move] = None,
                 move2: Optional[Move] = None, move3: Optional[Move] = None,
                 move4: Optional[Move] = None) -> None:
        """Initialize a pokemon with name, type, and moves."""
        self.name = name

        self.moves = [move1, move2, move3, move4]
        self.type_ = type_

        self._level = 1
        self._on = False

        self.image = image

    def evolve(self, name: str) -> None:
        """Evolve this pokemon."""
        self.name = name

    def learn_move(self, learning: Move, replacing: Optional[Move] = None):
        """Learn a move.
        Precondition: If <replacing> is not None, it is in this pokemon's
        moves.
        """
        if replacing is not None:
            self.moves.remove(replacing)

        self.moves.append(learning)

    def sent(self) -> None:
        """This pokemon is sent out to battle.
        Precondition: self._on is False."""
        self._on = True

    def returned(self) -> None:
        """This pokemon is returned from battle.
        Precondition: self._on is True."""
        self._on = False

    def is_in_battle(self) -> bool:
        """Return True if this pokemon is in battle.
        Otherwise, return False."""
        return self._on


class Trainer:
    """Represents a pokemon trainer.

    === Attributes ===
    name: This trainer's name.
    pokemons: List of this trainer's pokemons.
    curr_sent: This trainer's pokemon that is currently sent out to battle.

    === Representation Invariants ===
    - 0 <= len(self.pokemons) <= 6
    - If curr_sent is not None, then it is in self.pokemons.
    - Within self.pokemons, at most one pokemon's _on attribute is True and
      rest False.
    """

    name: str
    pokemons: List[Pokemon]
    curr_sent: Optional[Pokemon]

    def __init__(self, name: str, pokemons: List[Pokemon]) -> None:
        """Initialize a trainer."""

        self.name = name
        self.pokemons = pokemons
        self.curr_sent = None

    def send(self, pokemon: Pokemon) -> None:
        """Send the given <pokemon> out if it is in
        self.pokemons. Update its' status of sent.
        Otherwise do nothing."""
        if pokemon in self.pokemons:
            pokemon.sent()
            self.curr_sent = pokemon

    def is_in_battle(self) -> bool:
        """Return True if a pokemon in self.pokemons
        is sent to battle. Otherwise return False."""
        for pokemon in self.pokemons:
            if pokemon.is_in_battle():
                return True

        return False

    def __str__(self) -> None:
        """String representation of this trainer."""
        string_rep = "Name: " + self.name
        pokemons = ""
        for pokemon in self.pokemons:
            pokemons += "\n" + pokemon.name

        return string_rep + pokemons
