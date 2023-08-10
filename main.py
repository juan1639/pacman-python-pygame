import pygame
import random
import sys
from pac1 import *
from pac2 import *
from pac3 import *
from pac4 import *

# ====================================================================================
#	Codigo Principal (main.py) ... class Game
#
#	Funciones Principales:
#		
#		new_game()
#		crear_pantallaNivel()
#		obtenerGrafico()
#		(funciones de instanciar sprites y textos)
#		(funciones de checkeos)	
#
#		bucle_principal()
#				checkEvent()
#				update()
#				draw()
# ------------------------------------------------------------------------------------
class Game:
	def __init__(self):
		pygame.init()
		pygame.mixer.init()
		self.AMARILLO = (220, 190, 0)
		self.BLANCO = (240, 240, 240)
		self.GRIS_FONDO = (73, 73, 73)
		self.ROJO = (230, 30, 20)
		self.VERDE_FONDO = (20, 240, 30)
		self.AZUL_C = (144, 205, 205)

		self.laberinto = [
		9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
		9,5,1,1,1,1,1,1,1,9,1,1,1,1,1,1,1,5,9,
		9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,

		9,1,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,1,9,
		9,1,1,1,2,1,1,1,1,0,1,1,1,1,2,1,1,1,9,
		9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,

		9,1,1,1,1,9,1,1,1,9,1,1,1,1,1,1,1,1,9,
		9,9,9,9,1,9,9,9,1,9,1,9,9,9,1,9,9,9,9,
		9,1,1,1,2,1,1,1,1,1,1,1,1,1,2,1,1,1,9,

		9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
		9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
		0,1,1,1,1,9,1,1,1,0,1,1,1,9,1,1,1,1,0,

		9,1,9,9,1,9,1,9,9,9,9,9,1,9,1,9,9,1,9,
		9,5,1,1,2,1,1,1,1,0,1,1,1,1,2,1,1,5,9,
		9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,
		]

		self.programaEjecutandose = True
		self.menuPresentacion = True
		self.preparado = False
		self.enJuego = False
		self.gameOver = False
		self.nivelSuperado = False
		self.invulnerabilidad = False

		self.reinstanciar_pacmanFantasmas = True

		self.TX = 50	# Tamaño Tiles
		self.TY = 50
		self.FILAS = 15
		self.COLUMNAS = 19

		# (x, y, nroFantasma, direccionInicial)
		self.lista_argumentosFantasmas = [
			(5, 8, 0, 'le'), (8, 8, 1, 'le'),
			(10, 8, 2, 'ri'), (13, 8, 3, 'ri')
		]

		self.sumaPtosComeFantasmas = 100	# 200 -> 400 -> 800 -> 1600
		self.temporizadorAzules = False 
		self.duracion_azules = 8000
		self.ultimoUpdate_azules = pygame.time.get_ticks()

		self.RESOLUCION = (self.TX * self.COLUMNAS + 200, self.TY * self.FILAS)
		self.FPS = 100

		self.sonido_wakawaka = pygame.mixer.Sound("sonido/pacmanwakawaka.ogg")
		self.sonido_wakawaka.set_volume(0.9)
		self.sonido_sirena = pygame.mixer.Sound("sonido/pacmansirena.ogg")
		self.sonido_sirena.set_volume(0.2)
		self.sonido_eatingCherry = pygame.mixer.Sound("sonido/pacmaneatingcherry.ogg")
		self.sonido_pacmanDies = pygame.mixer.Sound("sonido/pacmandies.ogg")
		self.sonido_gameover_retro = pygame.mixer.Sound("sonido/gameoveretro.ogg")
		self.sonido_fantasmas_azules = pygame.mixer.Sound("sonido/pacmanazules.ogg")
		self.sonido_eatingGhost = pygame.mixer.Sound("sonido/pacmaneatinghost.ogg")
		self.sonido_inicioNivel = pygame.mixer.Sound("sonido/pacmaninicionivel.ogg")

		pygame.mixer.music.load("sonido/pacmanintermision.ogg")
		pygame.mixer.music.set_volume(0.3)
		pygame.mixer.music.play(loops=2)

		self.pantalla = pygame.display.set_mode(self.RESOLUCION)
		self.reloj = pygame.time.Clock()

		self.imagen_vidasMarcador = self.obtenerGrafico('pacman1.png', 1)

		self.lista_sprites_adibujar = pygame.sprite.Group()
		self.lista_pacman = pygame.sprite.Group()
		self.lista_laberinto = pygame.sprite.Group()
		self.lista_puntitos = pygame.sprite.Group()
		self.lista_puntosGordos = pygame.sprite.Group()
		self.lista_items = pygame.sprite.Group()
		self.lista_textos = pygame.sprite.Group()
		self.lista_bonus_comeFantasmas = pygame.sprite.Group()
		self.lista_los4fantasmas = pygame.sprite.Group()

		self.instanciarTextosPresentacion()


	def new_game(self):
		if self.nivelSuperado:
			self.nivelSuperado = False 
			self.sumaPtosComeFantasmas = 100
			self.lista_bonus_comeFantasmas.empty()
			self.temporizadorAzules = False
			self.reinstanciar_pacmanFantasmas = True
			self.preparado = True 
			self.lista_los4fantasmas.empty()
			self.ultimo_update_preparado = pygame.time.get_ticks()
			self.sonido_inicioNivel.play()
		else:
			self.puntos = 0
			self.nivel = 1
			self.vidas = 3

		self.lista_sprites_adibujar.empty()
		self.lista_textos.empty()

		if len(self.lista_laberinto) > 0:
			self.lista_laberinto.empty()

		if len(self.lista_puntitos) > 0:
			self.lista_puntitos.empty()

		if len(self.lista_puntosGordos) > 0:
			self.lista_puntosGordos.empty()

		if len(self.lista_pacman) > 0:
			self.lista_pacman.empty()

		self.crear_pantallaNivel()
		self.instanciarObjetos()
		self.instanciarTextosMarcadores()
		self.instanciaTextoPreparado()


	def crear_pantallaNivel(self):
		contador = -1

		for i in range(self.FILAS):
			for ii in range(self.COLUMNAS):
				contador += 1
				valorArray = self.laberinto[contador]

				if valorArray == 9:
					self.laberintoTile = LaberintoTile(self, ii, i, self.TX, self.TY, valorArray)
					self.lista_sprites_adibujar.add(self.laberintoTile)
					self.lista_laberinto.add(self.laberintoTile)

				elif valorArray == 1:
					self.puntitos = Puntitos(self, ii, i, self.TX, self.TY, valorArray)
					self.lista_sprites_adibujar.add(self.puntitos)
					self.lista_puntitos.add(self.puntitos)

				elif valorArray == 5:
					self.puntosgordos = PuntosGordos(self, ii, i, self.TX, self.TY, valorArray)
					self.lista_puntosGordos.add(self.puntosgordos)
					self.lista_sprites_adibujar.add(self.puntosgordos)


	def obtenerIndice(self, x, y):
		if x < 0 or x > self.COLUMNAS - 1 or y < 0 or y > self.FILAS -1:
			return None

		return y * self.COLUMNAS + x 


	def obtenerGrafico(self, nombrePng, escala):
		img = pygame.image.load('pacGraf/' + nombrePng).convert()
		escalaX = int(self.TX / escala)
		escalaY = int(self.TY / escala)
		image = pygame.transform.scale(img, (escalaX, escalaY))
		image.set_colorkey((255, 255, 255))
		rect = image.get_rect()
		image_rect = (image, rect)

		return image_rect


	def renderizar_vidasMarcador(self):
		if self.menuPresentacion or self.gameOver or self.vidas <= 0:
			return 

		for i in range(self.vidas):
			self.pantalla.blit(self.imagen_vidasMarcador[0], (self.TX * self.COLUMNAS, 
				self.TY * 7 + i * self.TY))


	# INSTANCIAR (Sprites & Textos) ------------------------------------
	def instanciarObjetos(self):
		if not self.reinstanciar_pacmanFantasmas:
			return

		self.reinstanciar_pacmanFantasmas = False

		if self.vidas < 0:
		    self.gameOver = True
		    self.enJuego = False
		    self.instanciarTextosPresentacion()
		    self.ultimo_updateGameOver = pygame.time.get_ticks()
		    self.sonido_gameover_retro.play()
		    return

		self.pacman = PacMan(self, 9, 4, 'ri')	# (x, y, dirPorDefecto)
		self.lista_sprites_adibujar.add(self.pacman)
		self.lista_pacman.add(self.pacman)

		# if self.vidas >= 1:
		#     for i in range(self.vidas):
		#         mostrarvidas = MostrarVidas(self, i + 1)
		#         self.arrayMostrarVidas.append(mostrarvidas)
		#         self.lista_sprites_adibujar.add(self.arrayMostrarVidas[i])


		for i in range(4):
			datos = self.lista_argumentosFantasmas[i]
			coorX = datos[0]
			coorY = datos[1]
			self.instanciar_fantasma(coorX, coorY, i, datos[3], False, False)

		# self.instanciar_item()


	def instanciar_fantasma(self, coorX, coorY, i, direc, azul, ojos):
		fantasma = Fantasma(self, coorX, coorY, i, direc, azul, ojos)
		#self.lista_sprites_adibujar.add(fantasma)
		self.lista_los4fantasmas.add(fantasma)


	def instanciarPacmanDies(self, x, y):
		pacmanDies = PacManDies(self, x, y)
		self.lista_sprites_adibujar.add(pacmanDies)


	def instanciar_item(self):
		self.sonido_eatingCherry.play()

		self.item = Items(self, 9, 11)
		self.lista_sprites_adibujar.add(self.item)
		self.lista_items.add(self.item)

	# Instancias de Textos --------------------------------------
	def instanciarTextosPresentacion(self):
		centerx = self.RESOLUCION[0] // 2
		centery = self.RESOLUCION[1] // 2

		if self.gameOver and not self.enJuego:
			self.instanciaTextosGameOver(centerx, centery)
			return 

		textoTitulo = Textos(self, 'Pac Clon', 180, centerx, centery - 200, self.AMARILLO)
		textoPulseEnter = Textos(self, ' Pulse ENTER para jugar... ', 
			40, centerx, self.RESOLUCION[1] - 40 * 3 , self.AZUL_C)

		self.lista_textos.add(textoTitulo, textoPulseEnter)

		pacpresentacion = PacPresentacion(self, 9, 7, 'pacman', 0)
		self.lista_sprites_adibujar.add(pacpresentacion)

		pacpresentacion = PacPresentacion(self, 6, 7, 'fantasma', 0)
		self.lista_sprites_adibujar.add(pacpresentacion)
		pacpresentacion = PacPresentacion(self, 4, 7, 'fantasma', 1)
		self.lista_sprites_adibujar.add(pacpresentacion)
		pacpresentacion = PacPresentacion(self, 2, 7, 'fantasma', 2)
		self.lista_sprites_adibujar.add(pacpresentacion)
		pacpresentacion = PacPresentacion(self, 0, 7, 'fantasma', 3)
		self.lista_sprites_adibujar.add(pacpresentacion)


	def instanciaTextosGameOver(self, centerx, centery):
		centerx = (self.RESOLUCION[0] - 200) // 2

		textoGameOver = Textos(self, ' Game Over ', self.RESOLUCION[0] // 8, centerx, 
			centery, self.AMARILLO)
		
		self.lista_textos.add(textoGameOver)


	def instanciarTextosMarcadores(self):
		small = self.RESOLUCION[0] // 30
		x = self.TX * self.COLUMNAS + 90

		textoPuntos = Textos(self, 'Puntos: ', small, x, self.TY * 1, self.AMARILLO)

		textoPuntosInt = Textos(self, f'{self.puntos}', small, x, self.TY * 2, self.BLANCO)

		textoNivel = Textos(self, 'Nivel: ', small, x, self.TY * 4, self.AMARILLO)

		textoNivelInt = Textos(self, f'{self.nivel}', small, x, self.TY * 5, self.BLANCO)

		self.lista_textos.add(textoPuntos, textoPuntosInt, textoNivel, textoNivelInt)


	def instanciaTextoPreparado(self):
		centerx = int(self.RESOLUCION[0] - 200) // 2
		centery = self.RESOLUCION[1] // 2

		self.textoPreparado = Textos(self, ' Preparado ', self.RESOLUCION[0] // 12, centerx, 
			centery - self.RESOLUCION[1] // 12, self.AMARILLO)

		self.lista_textos.add(self.textoPreparado)


	def instanciaPtosComeFantasmas(self, showBonus, x, y):
		# print(str(showBonus))
		textoBonus = Textos(self, str(showBonus), self.RESOLUCION[0] // 20, 
			x * self.TX, y * self.TY, self.ROJO)

		self.lista_bonus_comeFantasmas.add(textoBonus)

	# CHECKEOS (Temporizador Azules, Nivel superado, Transicion GameOver-Newgame)
	def checkTemporizadorAzules(self):
		if self.temporizadorAzules:
			calculo = pygame.time.get_ticks()

			duracion = self.obtenerDuracionAzules()

			if calculo - self.ultimoUpdate_azules > duracion:
				self.temporizadorAzules = False 
				self.sumaPtosComeFantasmas = 100	# Reset bonus Fantasmas
				self.lista_bonus_comeFantasmas.empty()

				for fantasma in self.lista_los4fantasmas:
					x = int(fantasma.rect.x / self.TX)
					y = int(fantasma.rect.y / self.TY)
					i = fantasma.idFantasma
					direcc = fantasma.direccion

					fantasma.kill()
					self.instanciar_fantasma(x, y, i, direcc, False, False)


	def obtenerDuracionAzules(self):
		duracion = self.duracion_azules - self.nivel * 500
		if duracion < 2000:
			duracion = 2000

		return duracion


	def checkNivelSuperado(self):
		if len(self.lista_puntitos) <= 0 and not self.nivelSuperado and self.enJuego:
			self.nivelSuperado = True 
			self.nivel += 1
			print(self.nivelSuperado)
			self.new_game()


	def checkTransicion_gameOverRejugar(self):
		if self.gameOver and not self.enJuego:
			calculo = pygame.time.get_ticks()
			if calculo - self.ultimo_updateGameOver > 7000:
				self.gameOver = False 
				self.enJuego = True
				self.reinstanciar_pacmanFantasmas = True

				self.preparado = True 
				self.ultimo_update_preparado = pygame.time.get_ticks()
				self.sonido_inicioNivel.play()
				self.new_game()

	# FUNCIONES PRINCIPALES del juego (update, draw y check_event) --------
	def update(self):
		pygame.display.set_caption(str(int(self.reloj.get_fps())))

		self.checkTemporizadorAzules()
		self.checkNivelSuperado()

		if not self.preparado:
			self.lista_sprites_adibujar.update()
			self.lista_los4fantasmas.update()
			self.lista_textos.update()

		else:
			calculo = pygame.time.get_ticks()
			if calculo - self.ultimo_update_preparado > 4200:
				self.ultimo_update_preparado = calculo
				self.preparado = False 
				self.lista_textos.remove(self.textoPreparado)

		self.checkTransicion_gameOverRejugar()

		pygame.display.flip()
		self.reloj.tick(self.FPS) 


	def draw(self):
		self.pantalla.fill(self.GRIS_FONDO)

		self.lista_sprites_adibujar.draw(self.pantalla)
		self.lista_los4fantasmas.draw(self.pantalla)

		pygame.draw.rect(self.pantalla, self.GRIS_FONDO, 
			(self.COLUMNAS * self.TX, 11 * self.TY, self.TX, self.TY))

		self.renderizar_vidasMarcador()

		self.lista_bonus_comeFantasmas.draw(self.pantalla)
		self.lista_textos.draw(self.pantalla)


	def check_event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.programaEjecutandose = False
				pygame.quit()
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.programaEjecutandose = False
					pygame.quit()
					sys.exit()

				if event.key == pygame.K_RETURN and self.menuPresentacion:
					pygame.mixer.music.stop()
					self.menuPresentacion = False
					self.enJuego = True

					self.preparado = True 
					self.ultimo_update_preparado = pygame.time.get_ticks()
					self.sonido_inicioNivel.play()

					self.new_game()


	def bucle_principal(self):
		while self.programaEjecutandose:
			self.check_event()
			self.update()
			self.draw()


if __name__ == '__main__':
    game = Game()
    game.bucle_principal()

