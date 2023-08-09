import pygame
import random

# ======================================================================
# 	Módulo (pac1.py) ... class PacMan y class PacManDies 
#
# ----------------------------------------------------------------------
class PacMan(pygame.sprite.Sprite):
	def __init__(self, game, x, y, dirPorDefecto):
		super().__init__()
		self.game = game 

		self.pulsada = dirPorDefecto		# Tecla Pulsada Dcha (por defecto)
		self.pulsadaConfirmada = self.pulsada

		# 'teclaPulsada': [velX, velY, imagen]
		self.dic_Pulsada = {
			'ri': [1, 0, 0], 'le': [-1, 0, 2],
			'up': [0, -1, 4], 'do': [0, 1, 6]
		}

		self.nextAnima = 0
		self.lista_imagenes = []

		for i in range(8):
			file = 'pacman{}.png'.format(i + 1)
			image_rect = self.game.obtenerGrafico(file, 1)
			self.lista_imagenes.append(image_rect[0])

		animaPorDefecto = self.dic_Pulsada[self.pulsada][2]

		self.image = self.lista_imagenes[animaPorDefecto + self.nextAnima]	# Img (por defecto)
		self.rect = self.image.get_rect()

		self.radius = self.game.TX // 2 // 1.5 	# 1.5 colis. mas permisivas

		self.rect.x = x * self.game.TX
		self.rect.y = y * self.game.TY

		self.i_d = self.game.lista_pacman	# Id (para colisiones Group)

		self.velXY = (self.dic_Pulsada[self.pulsada][0], self.dic_Pulsada[self.pulsada][1]) 
		self.vel = 2 		# velocidad (en Pixels)
		self.avanzar = True

		self.ultimo_update = pygame.time.get_ticks()
		self.fotograma_vel = 100		# Velocidad de la animacion

		self.ultimo_updateSirena = pygame.time.get_ticks()
		self.cadenciaSirena = 500	# Cada cuanto suena (para NO acumular el Buffer)


	def update(self):
		if not self.game.enJuego:
			return

		self.leer_teclado()
		self.cambiarAnimacion()
		self.checkColisionesAvanzar()
		self.sonido_sirena()


	def checkColisionesAvanzar(self):
		if self.rect.x % self.game.TX == 0 and self.rect.y % self.game.TY == 0:

			x = self.rect.x // self.game.TX
			y = self.rect.y // self.game.TY
			colisionPulsada = self.check_colisionLaberintoPulsada(x, y)
			colisionVelXY = self.check_colisionLaberintoVelXY(x, y)

			if not colisionPulsada:
				self.avanzar = True
				self.pulsadaConfirmada = self.pulsada
				velX = self.dic_Pulsada[self.pulsada][0]
				velY = self.dic_Pulsada[self.pulsada][1]
				self.velXY = (velX, velY)

			elif not colisionVelXY:
				self.avanzar = True

			else:
				self.avanzar = False


		if self.avanzar:
			self.rect.x += self.velXY[0] * self.vel
			self.rect.y += self.velXY[1] * self.vel


	def check_colisionLaberintoPulsada(self, x, y):
		velX = self.dic_Pulsada[self.pulsada][0]
		velY = self.dic_Pulsada[self.pulsada][1]

		if self.checkEscapatorias(x, y, velX):
			return

		indice = self.game.obtenerIndice(x + velX, y + velY)

		if self.game.laberinto[indice] == 9:
			return True
		else:
			return False


	def check_colisionLaberintoVelXY(self, x, y):
		if self.checkEscapatorias(x, y, self.velXY[0]):
			return

		indice = self.game.obtenerIndice(x + self.velXY[0], y + self.velXY[1])

		if self.game.laberinto[indice] == 9:
			return True
		else:
			return False


	def checkEscapatorias(self, x, y, velX):
		if x + velX > self.game.COLUMNAS and y == 11:
			self.rect.x = -self.game.TX
			return True

		if x + velX < -1 and y == 11:
			self.rect.x = self.game.COLUMNAS * self.game.TX
			return True

		if x + velX >= self.game.COLUMNAS and y == 11:
			return True

		if x + velX < 0 and y == 11:
			return True

		return False


	def leer_teclado(self):
		tecla = pygame.key.get_pressed()

		if tecla[pygame.K_LEFT]:
			self.pulsada = 'le'

		elif tecla[pygame.K_RIGHT]:
			self.pulsada = 'ri'

		elif tecla[pygame.K_UP]:
			self.pulsada = 'up'

		elif tecla[pygame.K_DOWN]:
			self.pulsada = 'do'


	def cambiarAnimacion(self):
		calculo = pygame.time.get_ticks()

		if calculo - self.ultimo_update > self.fotograma_vel:
			self.ultimo_update = calculo

			if self.nextAnima == 0:
				self.nextAnima = 1
			else:
				self.nextAnima = 0

			x = self.rect.x
			y = self.rect.y 
			anima = self.dic_Pulsada[self.pulsadaConfirmada][2]
			self.image = self.lista_imagenes[anima + self.nextAnima]
			self.rect.x = x 
			self.rect.y = y 


	def sonido_sirena(self):
		calculo = pygame.time.get_ticks()
		if calculo - self.ultimo_updateSirena > self.cadenciaSirena:
			self.ultimo_updateSirena = calculo
			self.game.sonido_sirena.play(maxtime=500)


class PacManDies(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		super().__init__()
		self.game = game 

		self.lista_imagenes = []
		an = [1, 7, 3, 5]

		for i in range(4):
			file = 'pacman{}.png'.format(an[i])
			image_rect = self.game.obtenerGrafico(file, 1)
			self.lista_imagenes.append(image_rect[0])

		self.anima = 0

		self.image = self.lista_imagenes[self.anima]
		self.rect = self.image.get_rect()

		self.rect.x = x
		self.rect.y = y

		self.ultimo_update = pygame.time.get_ticks()
		self.fotograma_vel = 170		# Velocidad de la animacion
		self.ultimo_update_dies = pygame.time.get_ticks()
		self.duracion_dies = 2400		# Tiempo dies 'dando vueltas'


	def update(self):
		calculo = pygame.time.get_ticks()

		if calculo - self.ultimo_update > self.fotograma_vel:
			self.ultimo_update = calculo

			self.anima += 1

			if self.anima >= 4:
				self.anima = 0 


			x = self.rect.x
			y = self.rect.y 
			self.image = self.lista_imagenes[self.anima]
			self.rect.x = x 
			self.rect.y = y 

		self.checkDuracionDies()


	def checkDuracionDies(self):
		calculo = pygame.time.get_ticks()

		if calculo - self.ultimo_update_dies > self.duracion_dies:
			self.kill()
			self.game.lista_los4fantasmas.empty()

			self.game.vidas -= 1
			self.game.reinstanciar_pacmanFantasmas = True
			self.game.instanciarObjetos()


