import pygame
import random

# ======================================================================
# 	Módulo (pac2.py) ... class Fantasma 
#
# ----------------------------------------------------------------------
class Fantasma(pygame.sprite.Sprite):
	def __init__(self, game, x, y, idFantasma, dirPorDefecto, fantasmaAzul, ojos):
		super().__init__()
		self.game = game 

		self.ojos = ojos
		self.fantasmaAzul = fantasmaAzul
		self.idFantasma = idFantasma
		self.direccion = dirPorDefecto		# Tecla Pulsada Dcha (por defecto)

		if self.fantasmaAzul or self.ojos:
			an = [0, 2, 4, 6]
		else:
			an = [0, 8, 16, 24]

		# 'direccion': [velX, velY, imagen, 'las otras 3 direcciones']
		self.dic_direccion = {
			'ri': [1, 0, an[0], 'updole'], 'le': [-1, 0, an[1], 'updori'],
			'up': [0, -1, an[2], 'riledo'], 'do': [0, 1, an[3], 'rileup']
		}

		ptosClaveImport = [
			(75, 425), (225, 225), (225, 425), (225, 675), (225, 575),
			(325, 575), (225, 75), (425, 425), (325, 225),
			(875, 425), (725, 225), (725, 425), (725, 675), (725, 575),
			(625, 575), (725, 75), (525, 425), (625, 225)
		]

		# Puntos Especificos en los que los Fantasmas deciden perseguir
		self.ptosClave = []
		
		for i in range(len(ptosClaveImport)):
			pcx = ptosClaveImport[i][0]
			pcy = ptosClaveImport[i][1]
			pcx = (pcx - 25) // 50
			pcy = (pcy - 25) // 50
			self.ptosClave.append((pcx, pcy))

		self.nextAnima = 0
		self.lista_imagenes = []

		if self.ojos:
			for i in range(8):
				file = 'fantasma{}.png'.format(i + 51)
				image_rect = self.game.obtenerGrafico(file, 1)
				self.lista_imagenes.append(image_rect[0])

		else:
			if self.fantasmaAzul:
				for i in range(8):
					file = 'fantasmaAzul{}.png'.format(i + 1)
					image_rect = self.game.obtenerGrafico(file, 1)
					self.lista_imagenes.append(image_rect[0])

			else:
				for i in range(38):
					if i != 8 and i !=9 and i != 18 and i != 19 and i != 28 and i != 29:
						file = 'fantasma{}.png'.format(i + 1)
						image_rect = self.game.obtenerGrafico(file, 1)
						self.lista_imagenes.append(image_rect[0])

		if self.ojos:
			animaPorDefecto = self.dic_direccion[self.direccion][2]

		else:
			if self.fantasmaAzul:
				animaPorDefecto = 0
			else:
				animaPorDefecto = self.dic_direccion[self.direccion][2] + self.idFantasma * 2


		self.image = self.lista_imagenes[animaPorDefecto + self.nextAnima]	# Img (por defecto)
		self.rect = self.image.get_rect()

		self.radius = self.game.TX // 2 // 1.5 	# 1.5 colis. mas permisivas

		self.rect.x = x * self.game.TX
		self.rect.y = y * self.game.TY

		self.i_d = self.game.lista_los4fantasmas	# Id (para colisiones Group)

		self.velXY = (self.dic_direccion[self.direccion][0], self.dic_direccion[self.direccion][1]) 
		self.vel = 2 		# velocidad (en Pixels)
		self.avanzar = True

		self.ultimo_update = pygame.time.get_ticks()
		self.fotograma_vel = 100		# Velocidad de la animacion

		self.ultimo_updateSirena = pygame.time.get_ticks()
		self.cadenciaSirena = 500	# Cada cuanto suena (para NO acumular el Buffer)


	def update(self):
		self.cambiarAnimacion()
		self.checkColisionesAvanzar()
		self.checkColisionesVsPacman()


	def checkColisionesAvanzar(self):
		if self.rect.x % self.game.TX == 0 and self.rect.y % self.game.TY == 0:

			x = self.rect.x // self.game.TX
			y = self.rect.y // self.game.TY

			posXY = (x, y)
			if posXY in self.ptosClave:
				self.fantasmaPersigue()

			colisionVelXY = self.check_colisionLaberintoVelXY(x, y)

			if not colisionVelXY:
				self.avanzar = True
				velX = self.dic_direccion[self.direccion][0]
				velY = self.dic_direccion[self.direccion][1]
				self.velXY = (velX, velY)

			else:
				self.avanzar = False


		if self.avanzar:
			self.rect.x += self.velXY[0] * self.vel
			self.rect.y += self.velXY[1] * self.vel
		else:
			self.elegirOtraDireccion()
			velX = self.dic_direccion[self.direccion][0]
			velY = self.dic_direccion[self.direccion][1]
			self.velXY = (velX, velY)


	def elegirOtraDireccion(self):
		opciones = self.dic_direccion[self.direccion][3]
		num_rnd = random.randrange(3) * 2
		self.direccion = opciones[num_rnd] + opciones[num_rnd + 1]
		# print(self.direccion)


	def fantasmaPersigue(self):
		noPerseguir = random.randrange(100)
		if noPerseguir > self.game.nivel * 30:
			return
		
		horiz_vert = random.randrange(10)

		if horiz_vert < 5:
			if self.game.pacman.rect.y < self.rect.y:
				self.direccion = 'up'

			elif self.game.pacman.rect.y > self.rect.y:
				self.direccion = 'do'

		else:
			if self.game.pacman.rect.x < self.rect.x:
				self.direccion = 'le'

			elif self.game.pacman.rect.x > self.rect.x:
				self.direccion = 'ri'

		velX = self.dic_direccion[self.direccion][0]
		velY = self.dic_direccion[self.direccion][1]
		self.velXY = (velX, velY)


	def check_colisionLaberintoVelXY(self, x, y):
		if self.checkEscapatorias(x, y):
			return

		indice = self.game.obtenerIndice(x + self.velXY[0], y + self.velXY[1])

		if self.game.laberinto[indice] == 9:
			return True
		else:
			return False


	def checkEscapatorias(self, x, y):
		if x + self.velXY[0] > self.game.COLUMNAS and y == 11:
			self.rect.x = -self.game.TX
			return True

		if x + self.velXY[0] < -1 and y == 11:
			self.rect.x = self.game.COLUMNAS * self.game.TX
			return True

		if x + self.velXY[0] >= self.game.COLUMNAS and y == 11:
			return True

		if x + self.velXY[0] < 0 and y == 11:
			return True

		return False


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

			if self.fantasmaAzul or self.ojos:
				anima = self.dic_direccion[self.direccion][2]
			else:
				anima = self.dic_direccion[self.direccion][2] + self.idFantasma * 2

			# SET IMAGE del fantasma ----------------------------------
			self.image = self.lista_imagenes[anima + self.nextAnima]
			# ---------------------------------------------------------

			intermitente = pygame.time.get_ticks()
			duracion = self.game.obtenerDuracionAzules()

			if self.nextAnima == 1 and self.fantasmaAzul and intermitente - self.game.ultimoUpdate_azules > int(duracion / 1.5):
				self.image.set_alpha(100) #30
			else:
				self.image.set_alpha(255)

			self.rect.x = x 
			self.rect.y = y 


	def checkColisionesVsPacman(self):
		if self.ojos or self.game.invulnerabilidad:
			return


		if self.fantasmaAzul:
			impactos = pygame.sprite.spritecollide(self, self.game.lista_pacman, False, 
			pygame.sprite.collide_circle)
		else:
			impactos = pygame.sprite.spritecollide(self, self.game.lista_pacman, True, 
				pygame.sprite.collide_circle)

		for impacto in impactos:
			if impacto:
				if self.fantasmaAzul:
					self.game.sonido_eatingGhost.play()
					self.kill()

					coorX = int(self.rect.x / self.game.TX)
					coorY = int(self.rect.y / self.game.TY)
					self.game.sumaPtosComeFantasmas *= 2
					self.game.puntos += self.game.sumaPtosComeFantasmas

					self.game.instanciaPtosComeFantasmas(self.game.sumaPtosComeFantasmas, coorX, coorY)
					self.game.instanciar_fantasma(coorX, coorY, self.idFantasma, self.direccion, False, True)

				else:
					self.game.instanciarPacmanDies(impacto.rect.x, impacto.rect.y)
					self.game.sonido_pacmanDies.play()

