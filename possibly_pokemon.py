from pokemon import *
# from random import randint
from tkinter import *


WIDTH = 800  # 1024
HEIGHT = 600  # 768


class Game:
    """Represents the game created using pygame.

    === Attributes ===
    bg: Stores the background image for the screen
    player: The character user is controlling
    opponent: Any opponent that will appear in the game

    === Representation Invariants ===
    - if self.opponent is not None, then self.player is not None
    """

    bg: pygame.Surface
    player: Optional[Trainer]
    opponent: Optional[Trainer]

    def __init__(self, image_name: str) -> None:
        """Initialize the game."""

        self.bg = pygame.image.load(image_name)
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        self.player = None
        self.player_image = pygame.transform.scale(pygame.image.load
                                                   ("turtle_player.png"),
                                                   (225, 150))
        self.opponent = None
        self.opponent_image = pygame.transform.scale(pygame.image.load
                                                     ("fork.jpg"),
                                                     (200, 200))

        self.in_battle = False

        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.update_display(screen)
        self.event_loop(screen)

    def update_display(self, screen: pygame.Surface) -> None:
        """Update the display of the screen."""

        screen.blit(self.bg, (0, 0))
        self.display_participants(screen)

        pygame.display.flip()

    def display_participants(self, screen: pygame.Surface) -> None:
        """Display player, opponent, and pokemons if the conditions meet."""

        if self.player is not None:
            screen.blit(self.player_image, (0, HEIGHT // 1.5))
        if self.opponent is not None:
            screen.blit(self.opponent_image, (WIDTH - 200, 0))
        if self.in_battle:
            screen.blit(self.player.curr_sent.image, (250, HEIGHT // 1.3))
            screen.blit(self.opponent.curr_sent.image, (WIDTH - 338, 200))

    def choose_move(self, attacking: Pokemon, defending: Pokemon):
        """Display the tkinter window that shows the attacking
        pokemon's moves
        """
        # Still gotta get this part !!!
        window = Tk()
        Label(window, text="Hi").grid(row=2, column=2)

        def destroy(m: Tk) -> None:
            m.destroy()

        Button(window, text="Move1", command=lambda: destroy(window)).\
            grid(row=1, column=0)
        window.mainloop()

    def event_loop(self, screen: pygame.Surface) -> None:
        """This method is where the loop occurs.
        In the loop, we process the events.
        """

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_s and self.player is None:
                        self.player = self.get_trainer(1)
                        self.opponent = self.get_trainer(1)
                    elif event.key == pygame.K_b and self.player is not None:
                        self.in_battle = True
                        self.player.send(self.player.pokemons[0])
                        self.opponent.send(self.opponent.pokemons[0])
                    elif event.key == pygame.K_a and self.in_battle:
                        self.choose_move(self.player.curr_sent,
                                         self.opponent.curr_sent)

            self.update_display(screen)

    def get_trainer(self, num: int) -> Trainer:
        """Generate a trainer with <num> pokemons."""
        # Still gotta get this part !!!!
        pok1_image = pygame.transform.scale(
            pygame.image.load("pikachu.jpg"), (138, 80))
        pok1 = Pokemon("Pikachu", "Electric", pok1_image)
        trainer = Trainer("Johnny", [pok1])

        return trainer


if __name__ == "__main__":
    game = Game("Stadium.jpg")
