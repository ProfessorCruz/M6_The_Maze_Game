from pygame import *

# Classe pai para outros sprites
class GameSprite(sprite.Sprite):
  # Construtor da classe
  def __init__(self, player_image, player_x, player_y, size_x, size_y):
      # Chamando o construtor da classe Sprite
      sprite.Sprite.__init__(self)
 
      # Cada sprite deve armazenar uma imagem como propriedade
      self.image = transform.scale(image.load(player_image), (size_x, size_y))

      # Cada sprite deve armazenar uma propriedade 'rect' (retângulo em que está inscrito)
      self.rect = self.image.get_rect()
      self.rect.x = player_x
      self.rect.y = player_y
 
  # Método que desenha o sprite na janela
  def reset(self):
      window.blit(self.image, (self.rect.x, self.rect.y))

# Classe principal para o jogador
class Player(GameSprite):
  # Método que implementa o controle do sprite pelas setas do teclado
  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
      # Chamando o construtor da classe GameSprite
      GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

      # Velocidade do jogador em X e Y
      self.x_speed = player_x_speed
      self.y_speed = player_y_speed

  # Método que atualiza a posição do jogador com base na velocidade
  def update(self):
       # Movimenta o personagem horizontalmente
       if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
         self.rect.x += self.x_speed
       # Checa colisão com barreiras após movimento horizontal
       platforms_touched = sprite.spritecollide(self, barriers, False)
       if self.x_speed > 0:  # Indo para a direita
           for p in platforms_touched:
               self.rect.right = min(self.rect.right, p.rect.left) 
       elif self.x_speed < 0:  # Indo para a esquerda
           for p in platforms_touched:
               self.rect.left = max(self.rect.left, p.rect.right)
       
       # Movimenta o personagem verticalmente
       if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
         self.rect.y += self.y_speed
       # Checa colisão com barreiras após movimento vertical
       platforms_touched = sprite.spritecollide(self, barriers, False)
       if self.y_speed > 0:  # Indo para baixo
           for p in platforms_touched:
               self.y_speed = 0
               if p.rect.top < self.rect.bottom:
                   self.rect.bottom = p.rect.top
       elif self.y_speed < 0:  # Indo para cima
           for p in platforms_touched:
               self.y_speed = 0
               self.rect.top = max(self.rect.top, p.rect.bottom)

  # Método de disparo do jogador (cria uma bala na posição atual do jogador)
  def fire(self):
      bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
      bullets.add(bullet)

# Classe de inimigo
class Enemy(GameSprite):
  side = "left"  # Direção inicial do inimigo
  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
      # Chamando o construtor da classe GameSprite
      GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
      self.speed = player_speed

  # Movimento do inimigo (zig-zag horizontal)
  def update(self):
      if self.rect.x <= 420:  # Limite esquerdo
          self.side = "right"
      if self.rect.x >= win_width - 85:  # Limite direito
          self.side = "left"
      if self.side == "left":
          self.rect.x -= self.speed
      else:
          self.rect.x += self.speed

# Classe para o sprite da bala
class Bullet(GameSprite):
  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
      # Chamando o construtor da classe GameSprite
      GameSprite.__init__(self, player_image, player_x, player_y+25, size_x, size_y)
      self.speed = player_speed

  # Movimento da bala
  def update(self):
      self.rect.x += self.speed
      # A bala desaparece ao atingir a borda da tela
      if self.rect.x > win_width+10:
          self.kill()

# Criando a janela do jogo
win_width = 700
win_height = 500
display.set_caption("Maze Game")  # Título da janela
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)  # Define a cor de fundo no esquema RGB

# Criando um grupo para as barreiras
barriers = sprite.Group()

# Criando um grupo para as balas
bullets = sprite.Group()

# Criando um grupo para os monstros
monsters = sprite.Group()

# Criando as barreiras (paredes do labirinto)
w1 = GameSprite('platform2.png', win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)

# Adiciona as barreiras ao grupo
barriers.add(w1)
barriers.add(w2)

# Criando os sprites principais
packman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
monster = Enemy('cyborg.png', win_width - 80, 180, 80, 80, 5)
final_sprite = GameSprite('prize.png', win_width - 85, win_height - 100, 80, 80)

# Adiciona o monstro ao grupo
monsters.add(monster)

# Variável que indica se o jogo terminou
finish = False
# Loop principal do jogo
run = True
while run:
  # Loop executa a cada 0.05 segundos
  time.delay(50)
   # Itera pelos eventos que podem ter ocorrido
  for e in event.get():
       if e.type == QUIT:
           run = False
       elif e.type == KEYDOWN:  # Pressionar tecla
           if e.key == K_LEFT:
               packman.x_speed = -5
           elif e.key == K_RIGHT:
               packman.x_speed = 5
           elif e.key == K_UP:
               packman.y_speed = -5
           elif e.key == K_DOWN:
               packman.y_speed = 5
           elif e.key == K_SPACE:
              packman.fire()
       elif e.type == KEYUP:  # Soltar tecla
           if e.key == K_LEFT:
               packman.x_speed = 0
           elif e.key == K_RIGHT:
               packman.x_speed = 0 
           elif e.key == K_UP:
               packman.y_speed = 0
           elif e.key == K_DOWN:
               packman.y_speed = 0

  # Verifica se o jogo ainda não terminou
  if not finish:
      # Atualiza o fundo em cada iteração
      window.fill(back)
      
      # Atualiza os movimentos e desenha os sprites
      packman.update()
      bullets.update()

      packman.reset()
      bullets.draw(window)
      barriers.draw(window)
      final_sprite.reset()

      # Colisão entre monstros e balas
      sprite.groupcollide(monsters, bullets, True, True)
      monsters.update()
      monsters.draw(window)
      sprite.groupcollide(bullets, barriers, True, False)

      # Verifica colisões do jogador com inimigos ou barreiras
      if sprite.spritecollide(packman, monsters, False):
          finish = True
          # Exibe tela de derrota
          img = image.load('game-over_1.png')
          d = img.get_width() // img.get_height()
          window.fill((255, 255, 255))
          window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

      if sprite.collide_rect(packman, final_sprite):
          finish = True
          # Exibe tela de vitória
          img = image.load('thumb.jpg')
          window.fill((255, 255, 255))
          window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
 
  display.update()