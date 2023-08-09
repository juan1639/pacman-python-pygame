# pacman-python-pygame
Recreación en python usando la librería pygame, del juego clásico pacman (arcade del año 1980).

En el código main.py se aloja la class Game, como clase principal y ahí la función constructora
albergará las principales variables y arrays del juego. 

También estarán las funciones encargadasde iniciar el juego/superar nivel, las de instanciar
(tanto sprites como textos), las que checkean si superamos nivel, si gameover, etc. y por supuesto,
la funcion bucle principal (checkEvent, update y draw).

El módulo pac1.py contiene la class PacMan, con todo lo relativo al personaje principal del juego
y también la class PacManDies, que básicamente es la animación de cuando nuestro personaje pierde
una vida.

En pac2.py se aloja la class Fantasma, con lo relativo a los fantasmas.

En pac3.py estarán el resto de clases, como LaberintoTile, Puntitos, PtosGordos y Textos.

En pac4.py está alojada la class PacPresentación, que es lo relativo a la pequeña intro de
presentación.


