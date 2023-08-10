import pygame

# ======================================================================
# 	Módulo (pac3.py)
#					class LaberintoTile
#					class Puntitos
#					class PuntosGordos
#					class Textos 
#
# ----------------------------------------------------------------------
class LaberintoTile(pygame.sprite.Sprite):
	def __init__(self, game, x, y, TX, TY, valorArray):
		super().__init__()
		self.game = game 

		if self.game.nivel > 3:
			image_rect = self.game.obtenerGrafico('bloquepac3.png', 1)
		else:
			image_rect = self.game.obtenerGrafico(f'bloquepac{self.game.nivel}.png', 1)

		self.image = image_rect[0]
		self.rect = image_rect[1]
		self.rect.x = x * TX
		self.rect.y = y * TY


	def update(self):
		pass 


class Puntitos(pygame.sprite.Sprite):
	def __init__(self, game, x, y, TX, TY, valorArray):
		super().__init__()
		self.game = game 

		image_rect = self.game.obtenerGrafico('pildopac.png', 5)
		self.image = image_rect[0]
		self.rect = image_rect[1]
		self.rect.centerx = x * TX + int(TX / 2)
		self.rect.centery = y * TY + int(TY / 2)


	def update(self):
		colision = pygame.sprite.spritecollide(self, self.game.lista_pacman, False) 
		if colision:
			self.kill()
			self.game.puntos += 10
			self.game.sonido_sirena.stop()
			self.game.sonido_wakawaka.play(maxtime=500)


class PuntosGordos(pygame.sprite.Sprite):
	def __init__(self, game, x, y, TX, TY, valorArray):
		super().__init__()
		self.game = game 

		self.escala = 1.0

		image_rect = self.game.obtenerGrafico('puntoGordo.png', self.escala)
		self.image = image_rect[0]
		self.rect = image_rect[1]
		self.rect.centerx = x * TX + int(TX / 2)
		self.rect.centery = y * TY + int(TY / 2)

		self.ultimo_update = pygame.time.get_ticks()
		self.vel_anima = 150


	def update(self):
		calculo = pygame.time.get_ticks()
		if calculo - self.ultimo_update > self.vel_anima:
			self.ultimo_update = calculo

			if self.escala == 1.0:
				self.escala = 1.5
			else:
				self.escala = 1.0

			x = self.rect.centerx
			y = self.rect.centery

			image_rect = self.game.obtenerGrafico('puntoGordo.png', self.escala)
			self.image = image_rect[0]
			self.rect = image_rect[1]

			self.rect.centerx = x 
			self.rect.centery = y 


		colision = pygame.sprite.spritecollide(self, self.game.lista_pacman, False)
		if colision and not self.game.temporizadorAzules:
			self.kill()

			for fantasma in self.game.lista_los4fantasmas:
				x = int(fantasma.rect.x / self.game.TX)
				y = int(fantasma.rect.y / self.game.TY)
				i = fantasma.idFantasma
				direcc = fantasma.direccion
				self.game.temporizadorAzules = True
				self.game.ultimoUpdate_azules = pygame.time.get_ticks()

				fantasma.kill()
				self.game.instanciar_fantasma(x, y, i, direcc, True, False)

			self.game.sonido_eatingGhost.play()


class Textos(pygame.sprite.Sprite):
	def __init__(self, game, texto, size, x, y, qcolor):
		super().__init__()
		self.game = game 
		self.qcolor = qcolor

		self.font = pygame.font.SysFont('serif', size)
		self.image = self.font.render(texto, True, self.qcolor)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		if y == self.game.TY * 2:
			self.renderPtos = True
		else:
			self.renderPtos = False

		if y == self.game.TY * 5:
			self.renderNivel = True
		else:
			self.renderNivel = False


	def update(self):
		if self.renderPtos:
			self.image = self.font.render(f'{self.game.puntos}', True, self.qcolor)

		if self.renderNivel:
			self.image = self.font.render(f'{self.game.nivel}', True, self.qcolor)


class itemFrutas(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		super().__init__()
		self.game = game 

		item = self.game.nivel 
		if item > 4:
			item = 4 

		image_rect = self.game.obtenerGrafico(f'item{item}.png', 1)
		self.image = image_rect[0]
		self.rect = image_rect[1]
		self.x = x 
		self.y = y
		self.rect.x = x * self.game.TX 	
		self.rect.y = y * self.game.TY

	def update(self):
		colision = pygame.sprite.spritecollide(self, self.game.lista_pacman, False)
		if colision:
			self.kill()
			sumaPtosFruta = (self.game.nivel * 10) * (self.game.nivel * 10)
			self.game.puntos += sumaPtosFruta
			self.game.ultimo_update_itemFruta = pygame.time.get_ticks()
			self.game.instanciaPtosComeFantasmas(sumaPtosFruta, self.x, self.y)
			self.game.sonido_eatingCherry.play()


