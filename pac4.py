import pygame

# ======================================================================
# 	Módulo (pac4.py) ... class PacPresentacion 
#
#-----------------------------------------------------------------------
class PacPresentacion(pygame.sprite.Sprite):
	def __init__(self, game, x, y, imgPng, idF):
		super().__init__()
		self.game = game 

		self.imgPng = imgPng
		self.idF = idF

		self.nextAnima = 0
		self.lista_imagenes = []

		if self.imgPng == 'pacman':
			for i in range(4):
				file = imgPng + '{}.png'.format(i + 1)
				image_rect = self.game.obtenerGrafico(file, 0.7)
				self.lista_imagenes.append(image_rect[0])

		else:
			for i in range(38):
				if i != 8 and i !=9 and i != 18 and i != 19 and i != 28 and i != 29:
					file = imgPng + '{}.png'.format(i + 1)
					image_rect = self.game.obtenerGrafico(file, 0.7)
					self.lista_imagenes.append(image_rect[0])


		self.image = self.lista_imagenes[0 + self.nextAnima]	# Img (por defecto)
		self.rect = self.image.get_rect()

		self.rect.x = x * self.game.TX
		self.rect.y = y * self.game.TY

		self.velXY = (1, 0) 
		self.vel = 2 		# velocidad (en Pixels)

		self.ultimo_update = pygame.time.get_ticks()
		self.fotograma_vel = 100		# Velocidad de la animacion


	def update(self):
		ld = self.game.RESOLUCION[0] + self.game.RESOLUCION[0] // 4
		li = -self.game.RESOLUCION[0] // 3

		self.cambiarAnimacion()

		self.rect.x += self.velXY[0] * self.vel

		if (self.rect.x >= ld and self.velXY[0] > 0) or (self.rect.x < li and self.velXY[0] < 0):
			direccion = self.velXY[0]
			direccion = -direccion
			self.velXY = (direccion, 0)

	
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

			anima = self.idF * 2

			if self.imgPng == 'fantasma':
				if self.velXY[0] > 0:
					anima = self.idF * 2
				else:
					anima += 8

			elif self.imgPng == 'pacman':
				if self.velXY[0] > 0:
					anima = 0 
				else:
					anima = 2

			self.image = self.lista_imagenes[anima + self.nextAnima]
			self.rect.x = x 
			self.rect.y = y 


