import pygame
import math
import random
pygame.init()

win_width=1000
win_height=697
win = pygame.display.set_mode((win_width,win_height))
bg = pygame.image.load('src/bg5.png').convert()
lazer_image=pygame.image.load('src/lazer.png')
disperse_image=pygame.image.load('src/disperse.png')
line_image=pygame.image.load('src/line.png')
track_image=pygame.image.load('src/track.png')
enemy_img = pygame.image.load('src/enemy2.png')
player_image= pygame.image.load('src/Player.png').convert()
bullet_image=pygame.image.load('src/bullet.png').convert()
ebullet_image=pygame.image.load('src/ebullet.png').convert()
trackbullet_image=pygame.image.load('src/ebullet2.png').convert()
music=pygame.mixer.music.load('src/bgm.mp3')
death_image=pygame.image.load('src/death.png').convert()
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()
sansmusic,bgm,sansdeath=True,True,True
kshsmusic=True
boss1music=True

RED = (237, 28, 36)
RED_FOR_LAZER = (221,50,20,255)
GREEN = (78, 255, 87)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)

FPS=60

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,vel):
        super().__init__()
        self.image = pygame.transform.scale(player_image, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.vel=vel
        self.x=x
        self.y=y
        self.invincible=-1000
        self.hp=200
        self.cooldown=500
        self.lastshoot=pygame.time.get_ticks()
        self.mask = pygame.mask.from_surface(self.image)
        self.alpha_minus=True
    def shoot(self):
        now= pygame.time.get_ticks()
        if now-self.lastshoot>self.cooldown:
             bullet=PlayerBullet((self.rect.center[0],self.rect.top),400)
             all_sprites.add(bullet)
             bullets.add(bullet)
             self.lastshoot=now
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x >self.vel*dt:
            self.x-= self.vel*dt   
        if keys[pygame.K_RIGHT] and  self.rect.right < win_width- self.vel*dt:
            self.x+=self.vel*dt
        if keys[pygame.K_UP] and self.rect.y > self.vel*dt:
            self.y -= self.vel*dt
        if keys[pygame.K_DOWN] and self.rect.bottom< win_height - self.vel*dt:
            self.y+=self.vel*dt
        #if keys[pygame.K_SPACE]:
        #    self.shoot()
        if keys[pygame.K_z]:
            if interval.speedup<=0:
                interval.speedup=100
                interval.speeduptime=7
                self.vel=char_vel*5
        if interval.speeduptime < 0:
            self.vel=char_vel
        self.rect.x=self.x
        self.rect.y=self.y
    def hit(self):
        self.hp-=10
        self.invincible=pygame.time.get_ticks()
    def invincible_animation(self):
        alpha=self.image.get_alpha()
        if self.alpha_minus and alpha>8:
            self.image.set_alpha(alpha-16)
        elif self.alpha_minus and  alpha<=8:
            self.alpha_minus = False
        if not self.alpha_minus:
            if alpha<248:
                self.image.set_alpha(alpha+16)
            else:
                self.alpha_minus=True
    def draw(self):
        pygame.draw.rect(win,GREEN,[self.x-15,self.y+45,self.hp*0.4,10])
        pygame.draw.rect(win,RED,[self.x-15,self.y+45,80,10],2)

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self,center,vel):
        super().__init__()
        self.image=bullet_image
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.center = center
        self.vel=vel
    def update(self):
        if self.rect.y > 0 :
            self.rect.y -= self.vel*dt
        else:
            self.kill()

class Intervals():
    def __init__(self,pl_bullet,speedup,speeduptime):
        self.pl_bullet=pl_bullet
        self.speedup=speedup
        self.speeduptime=speeduptime
    def add(self,name_time):
        self.name_time[0]=self.name_time[1]
    def minus(self):
        self.pl_bullet -= 1
        self.speedup -= 1
        self.speeduptime -= 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,vel,heading,start,interval,type,hp,rage=False):
        super().__init__()
        self.type=type
        if self.type=='line':
            self.image=pygame.transform.scale(line_image, (100, 100))
        elif self.type=='disperse':
            self.image=pygame.transform.scale(disperse_image, (100, 100))
        elif self.type=='track':
            self.image=pygame.transform.scale(track_image, (100, 100))
        elif self.type=='lazer':
            self.image=pygame.transform.scale(lazer_image, (100, 100))
        self.rect=self.image.get_rect()
        self.x=x
        self.y=y
        self.rect.x = x
        self.rect.y = y
        self.vel=vel
        self.heading=heading
        self.start=start
        self.interval=interval
        self.initial=interval
        self.last=pygame.time.get_ticks()
        self.hp=hp
        self.rage=rage
        self.stronger=False
        if self.type=='random':
            self.angle=math.pi*random.randrange(5,175)/180
    def shoot(self):
        if self.type=='line': 
            ebullet=EnemyBullet(self.rect.midbottom,400,'line')             
        elif self.type=='track':
            ebullet=EnemyBullet(self.rect.midbottom,200,'track')
        elif self.type=='disperse':
            ebullet=[EnemyBullet(self.rect.midbottom,300,'line'),EnemyBullet(self.rect.midbottom,300,'45degree'),
                    EnemyBullet(self.rect.midbottom,300,'135degree')]
        elif self.type=='lazer':
            ebullet=EnemyBullet(self.rect.midbottom,400,'line')
        elif self.type=='random':
            ebullet=EnemyBullet(self.rect.midbottom,200,'random')
        ebullets.add(ebullet)
        all_sprites.add(ebullet)
    def hit(self):
        if self.ready:
            self.hp-=1
        if self.hp==0:
            self.kill()
        if self.hp<4:
            self.stronger=True
    def update(self):
        if self.y<50:
            self.ready = False
            self.y += 100*dt
            self.rect.y=self.y
        else:
            self.ready=True
            if self.rect.x<15 :
                self.heading= 1
            elif self.rect.right > win_width:
                self.heading = -1
            self.x += 2*self.vel*dt*self.heading if self.rage and self.stronger else self.vel*dt*self.heading 
            self.rect.x=self.x
            self.start-=1
            now=pygame.time.get_ticks()
            if self.rage and self.stronger:
                self.interval=self.initial/2
            if self.type=='lazer' or self.type=='random':
                if self.start==0:
                    self.shoot()
                    self.last=now
                elif self.start<0:
                    if self.stronger:
                        if now-self.last<self.interval/2:
                            self.shoot()
                    else:
                        if now-self.last<self.interval/3:
                            self.shoot()
                    if now-self.last>self.interval:
                        self.last=now
            else:
                if self.start==0:
                    self.shoot()
                    self.last=now
                elif self.start<0:
                    if now-self.last>self.interval:
                        self.shoot()
                        self.last=now
    def draw(self):
        pygame.draw.rect(win,YELLOW,[self.x+25,self.y-20,self.hp*10,10])
        pygame.draw.rect(win,RED,[self.x+25,self.y-20,50,10],2)

class Sans(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.which_status=1
        self.image=pygame.image.load('src/sans6.png')
        self.rect=self.image.get_rect()
        self.x=win_width/2
        self.y=10
        self.rect.center=(self.x,self.y)
        self.start=320
        self.hp=120
        self.last=pygame.time.get_ticks()
        self.last2=pygame.time.get_ticks()
        self.vel_x=0
        self.vel_y=0
        self.heading_y=1
        self.heading=1
        self.interval=0
        self.shootmode=None
        self.invincible=False
    def status(self):
        if self.hp<30:
            self.mode4()
        elif self.hp<60:
            self.mode3()
        elif self.hp<90:
            self.mode2()
        elif self.start<0:
            self.mode1()
        elif self.start>=0:
            self.modestop()
        if self.hp<=0:
            self.death_animation()
    def mode1(self):
        global sansmusic,bgm
        self.image=pygame.image.load('src/sans1.png')
        self.vel_x=150
        self.vel_y=0
        self.shootmode=1
        self.interval=3000
        self.invincible=False
        if sansmusic:
            pygame.mixer.init()
            pygame.mixer.music.load('src/Megalovania.mp3')
            bgm,sansmusic=True,False
            if pygame.mixer.get_busy != 1:
                pygame.mixer.music.play(-1)
    def mode2(self):
        self.image=pygame.image.load('src/sans5.png')
        self.vel_x=150
        self.vel_y=100
        self.shootmode=2
        self.interval=4000
    def mode3(self):
        self.image=pygame.image.load('src/sans4.png')
        self.vel_x=0
        self.vel_y=0
        self.shootmode=3
        self.interval=3000
        self.interval2=1000
    def mode4(self):
        self.image=pygame.image.load('src/sans2.png')
        self.vel_x=500
        self.vel_y=500
        self.shootmode=4
        self.interval=3000
    def modestop(self):
        pygame.mixer.music.pause()
        self.invincible=True
        if self.rect.center==(win_width/2,100):
            self.vel_y=0
            pygame.font.init() 
            myfont = pygame.font.SysFont('Comic Sans MS', 30)
            textsurface1 = myfont.render('YOU\'RE GONNA HAVE', False, (255,255,255))
            textsurface2=myfont.render('A BAD TIME', False, (255,255,255))
            win.blit(textsurface1,(self.rect.right,self.rect.centery-20))
            win.blit(textsurface2,(self.rect.right,self.rect.centery+10))
        else:
            self.vel_y=50

    def death_animation(self):
        global sansdeath
        if self.last!=0:
            self.last=0
            self.last2=pygame.time.get_ticks()
        now=pygame.time.get_ticks()
        sans_images=[pygame.image.load('src/sans1.png'),pygame.image.load('src/sans2.png'),pygame.image.load('src/sans3.png'),
                    pygame.image.load('src/sans4.png'),pygame.image.load('src/sans5.png'),pygame.image.load('src/sans6.png')]
        self.image=random.choice(sans_images)
        self.vel_x=0
        self.vel_y=0
        self.shootmode=0
        if sansdeath:
            pygame.mixer.init()
            pygame.mixer.music.load('src/sansdeath.mp3')
            sansdeath=False
            if pygame.mixer.get_busy != 1:
                pygame.mixer.music.play()
        if now-self.last2>5000:
            self.kill()

    def shoot(self):
        if self.shootmode==1:
            ebullet=EnemyBullet(self.rect.midbottom,300,'random')
            ebullets.add(ebullet)
            all_sprites.add(ebullet)
        if self.shootmode==2:
            if self.hp>70:
                for i in range(12):
                    ebullet=EnemyBullet(self.rect.center,400,'sans2',i*30)
                    ebullets.add(ebullet)
                    all_sprites.add(ebullet)
            else:
                for i in range(18):
                    ebullet=EnemyBullet(self.rect.center,400,'sans2',i*20)
                    ebullets.add(ebullet)
                    all_sprites.add(ebullet)
        if self.shootmode==3:
            ebullet=EnemyBullet(self.rect.midbottom,600,'trackline')
            ebullets.add(ebullet)
            all_sprites.add(ebullet)
        if self.shootmode==4:
            ebullet=EnemyBullet(self.rect.midbottom,150,'track',None,3000)
            ebullets.add(ebullet)
            all_sprites.add(ebullet)
        if self.shootmode==0:
            pass

    def shoot2(self):
        if self.shootmode==3:
            for i in range(8):
                ebullet=EnemyBullet((win_width/8*i,win_height-10),200,'up')
                ebullets.add(ebullet)
                all_sprites.add(ebullet)

    def draw(self):
        pygame.draw.rect(win,GREEN,[95,0,self.hp*6.65,10])
        pygame.draw.rect(win,RED,[95,0,800,10],2)
            
    def hit(self):
        if not self.invincible:
            self.hp-=1
        if self.hp<=0:
            self.invincible=True

    def update(self):
        self.start-=1
        self.status()
        if self.rect.x<15 :
            self.heading= 1
        elif self.rect.right > win_width-10:
            self.heading = -1
        if self.rect.top<10:
            self.heading_y=1
        elif self.rect.bottom>win_height:
            self.heading_y=-1
        if self.shootmode==3 :
            if not(self.x==win_width/2 and self.y==100):
                dx=win_width/2-self.x
                dy=100-self.y
                distance=(dx**2+dy**2)**0.5
                self.x+=dx/distance*dt*200
                self.y+=dy/distance*dt*200
                if distance<10:
                    self.x=win_width/2
                    self.y=100
                self.noshoot=True
            else:self.noshoot=False
        else:
            self.x +=self.vel_x*dt*self.heading 
            self.y +=self.vel_y*dt*self.heading_y
        self.rect.center=(self.x,self.y)
        now=pygame.time.get_ticks()
        now2=pygame.time.get_ticks()
        if self.shootmode==1:
            if now-self.last<self.interval/3:
                self.shoot()
            if now-self.last>self.interval:
                self.last=now
        if self.shootmode==2:
            if now-self.last<self.interval/4:
                self.shoot()
            if now-self.last>self.interval:
                self.last=now
        if self.shootmode==3:
            if not self.noshoot:
                if now-self.last<self.interval/3:
                    self.shoot()
                if now-self.last>self.interval:
                    self.last=now
                if now2-self.last2>self.interval2:
                    self.shoot2()
                    self.last2=now2
        if self.shootmode==4:
            if now-self.last>self.interval:
                self.shoot()
                self.last=now

class KSHS(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.which_status=1
        self.width=150
        self.height=150
        img=pygame.image.load('src/kshs1.png')
        self.image=pygame.transform.scale(img,(self.width,self.height))
        self.rect=self.image.get_rect()
        self.x=(win_width-self.width)/2
        self.y=-50
        self.rect.center=(self.x,self.y)
        self.start=250
        self.hp=120
        self.last=pygame.time.get_ticks()
        self.last2=pygame.time.get_ticks()
        self.vel_x=100
        self.vel_y=0
        self.heading_y=1
        self.heading=1
        self.interval=3000
        self.bulletinterval2=300
        self.bulletinterval3=500
        self.shootmode=None
        self.rage=False
        self.shoot2=0
        self.move=True
        self.healing=False
        self.preshoot=500
        self.bigger=False
    def update(self):
        now=pygame.time.get_ticks()
        if self.start>0:
            self.start-=1
            self.move=False
            self.y+=0.5
            self.rect.y=self.y
            self.rect.x=self.x
        elif self.start==0:
            self.start-=1
            self.move=True
            self.last=now
            self.shootmode=random.randint(1,4)
        if self.move:
            if self.rect.x<15:
                self.heading= 1
            elif self.rect.right > win_width-10:
                self.heading = -1
            if self.rect.top<10:
                self.heading_y=1
            elif self.rect.bottom>win_height:
                self.heading_y=-1
            self.x +=self.vel_x*dt*self.heading*1.5 if self.rage else self.vel_x*dt*self.heading
            self.y +=self.vel_y*dt*self.heading_y
            self.rect.x=self.x
            self.rect.y=self.y
        if now-self.last>self.interval and self.start==-1:
                self.last=now
                self.shootmode=random.randint(1,4)
        if self.shootmode==1:
            if now-self.last<self.interval/2:
                self.shoot()
        if self.shootmode==2:
            if now-self.last<self.interval/2:
                self.shoot()
            else:
                self.move=True
        if self.shootmode==3:
            if now-self.last<self.interval/2:
                self.shoot()
        if self.shootmode==4:
            if now-self.last<self.interval/2:
                self.move=False
                self.healing=True
                self.image=pygame.transform.scale(pygame.image.load('src/kshs2.png'),(self.width,self.height))
            else:
                self.move=True
                self.healing=False
                self.image=pygame.transform.scale(pygame.image.load('src/kshs1.png'),(self.width,self.height))
        if self.hp<=45 and self.bigger==False:
            self.rage=True 
            self.width=180
            self.height=180
            self.image=pygame.transform.scale(pygame.image.load('src/kshs1.png'),(self.width,self.height))
            self.rect=self.image.get_rect()
            self.bigger=True

    def shoot(self): 
        now=pygame.time.get_ticks()
        if self.shootmode==1:
            if self.rage:
                if now - self.last > self.preshoot:
                    lazer1=pygame.draw.line(win, RED_FOR_LAZER,(self.x+0.5*self.width,self.y+self.height), ((now-self.last-self.preshoot)/(self.interval/2-self.preshoot)*win_width,win_height) , 15)
                    lazer2=pygame.draw.line(win, RED_FOR_LAZER,(self.x+0.5*self.width,self.y+self.height), (0,win_height*(now-self.last-self.preshoot)/(self.interval/2-self.preshoot)) , 15)
                    lazer3=pygame.draw.line(win, RED_FOR_LAZER,(self.x+0.5*self.width,self.y+self.height), (win_width,win_height-win_height*(now-self.last-self.preshoot)/(self.interval/2-self.preshoot)) , 15)
                else:
                    pre1=pygame.draw.line(win, RED,(self.x+0.5*self.width,self.y+self.height), (0,win_height) , 5)
                    pre2=pygame.draw.line(win, RED,(self.x+0.5*self.width,self.y+self.height), (0,0) , 5)
                    pre3=pygame.draw.line(win, RED,(self.x+0.5*self.width,self.y+self.height), (win_width,win_height) , 5)
                    
            else:
                if now - self.last > self.preshoot:
                    lazer=pygame.draw.line(win, RED_FOR_LAZER,(self.x+0.5*self.width,self.y+self.height),(win_width-(now-self.last-self.preshoot)/(self.interval/2-self.preshoot)*win_width,win_height) , 15)
                else:
                    pre=pygame.draw.line(win, RED,(self.x+0.5*self.width,self.y+self.height),(win_width,win_height) , 5)
            mask=pygame.mask.from_threshold(win,RED_FOR_LAZER,(10,10,10,255))  
            mask_rect=pygame.Rect((0,0),(mask.get_size())) 
            if  now - char.invincible > 1000:
                char.image.set_alpha(256)
                if char.mask.overlap(mask,(mask_rect.x-char.rect[0],mask_rect.y-char.rect[1])):
                    char.hit()
            else:
                char.invincible_animation()
        if self.shootmode==2:
            self.move=True if self.rage else False 
            self.bulletinterval2 = 200 if self.rage else 300
            bullet_count = 15 if self.rage else 12
            if now-self.last2>self.bulletinterval2:
                if self.shoot2==0:
                    self.shoot2=1
                    for i in range(bullet_count):
                        ebullet=EnemyBullet(self.rect.center,400,'scatter',i*360/bullet_count)
                        ebullets.add(ebullet)
                        all_sprites.add(ebullet)
                    self.last2=now
                else:
                    self.shoot2=0
                    for i in range(bullet_count):
                        ebullet=EnemyBullet(self.rect.center,400,'scatter',i*360/bullet_count+180/bullet_count)
                        ebullets.add(ebullet)
                        all_sprites.add(ebullet)
                    self.last2=now
        if self.shootmode==3:
            self.bulletinterval3 = 375 if self.rage else 500
            if now-self.last2>self.bulletinterval3:
                ebullet=EnemyBullet(self.rect.midbottom,150,'big track',None,1000)
                ebullets.add(ebullet)
                all_sprites.add(ebullet)
                self.last2=now
    def draw(self):
        pygame.draw.rect(win,GREEN,[95,0,self.hp*6.65,10])
        pygame.draw.rect(win,RED,[95,0,800,10],2)
    def hit(self):
        if self.healing:
            self.hp+=2 if self.rage else 1
            if self.hp>120:
                self.hp=120
        else:
            self.hp+=-1
        if self.hp<=0:
            self.kill()

class Big_en_plane(pygame.sprite.Sprite):
    def __init__(self,enemy_img,hp = 100 ,width = 250,height = 275):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(enemy_img,(self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = [win_width/2,win_height/2]
        self.hp = hp
        self.mode = None
        self.shoot2 = 0
        self.last = pygame.time.get_ticks()
        self.last2 = pygame.time.get_ticks()
    def update(self):
        now = pygame.time.get_ticks()
        if  70 <= self.hp <= 90  :
            if now - self.last >= 8000 :
                self.rect.centerx = random.randint(self.width + 50,win_width - self.width - 50)
                self.rect.centery = random.randint(self.height + 50,win_height - self.height - 50)
                self.mode = 1
                self.last = now
        elif 50 <= self.hp <= 70 :
            if now - self.last >= 6000 :
                self.rect.centerx = random.randint(self.width + 50,win_width - self.width - 50)
                self.rect.centery = random.randint(self.height + 50,win_height - self.height - 50)
                self.mode = 2
                self.last = now
        elif self.hp <=50 :
            if now - self.last >= 4000 :
                self.rect.centerx = random.randint(self.width + 50,win_width - self.width - 50)
                self.rect.centery = random.randint(self.height + 50,win_height - self.height - 50)
                self.mode = 3
                self.last = now
        else :
            if now - self.last >= 3000 :
                self.rect.centerx = random.randint(self.width + 50,win_width - self.width - 50)
                self.rect.centery = random.randint(self.height + 50,win_height - self.height - 50)
                self.mode = 4
                self.last = now
        if (now - self.last2 >= 600) and (self.mode == 1  or self.mode == 4) :
            self.shoot()
            self.last2 = now
        if (now - self.last2 >= 1000) and (self.mode == 2):
            self.shoot()
            self.last2 = now
        if self.mode == 3:
            self.shoot()
        if (now - self.last2 >= 4000):
            self.last2 = now
            
    def shoot(self):
        if self.mode == 1:
            if self.rect.centery >= win_height/2:
                if self.shoot2 == 0:
                    self.shoot2 = 1
                    for i in range(15):
                        ebullet=EnemyBullet(self.rect.center,400,'scatter',i*360/15)
                        ebullets.add(ebullet)
                        all_sprites.add(ebullet)
                else:
                    self.shoot2 = 0
                    for i in range(15):
                        ebullet=EnemyBullet(self.rect.center,400,'scatter',i*360/15+180/15)
                        ebullets.add(ebullet)
                        all_sprites.add(ebullet)
            else:
                self.hp+=-1
            if self.hp<=0:
                self.kill()
            else :
                if self.shoot2 == 0:
                    self.shoot2 = 1
                    for i in range(15):
                        ebullet = EnemyBullet(self.rect.center,400,'scatter',-i*360/15)
                        ebullets.add(ebullet)
                        all_sprites.add(ebullet)
                else:
                    self.shoot2 = 0
                    for i in range(15):
                        ebullet = EnemyBullet(self.rect.center,400,'scatter',-(i*360/15+180/15))
                        ebullets.add(ebullet)
                        all_sprites.add(ebullet)
                    
        if self.mode == 2 :
            if self.rect.centery >= win_height*2/3:
                for i in range(25):
                    ebullet = EnemyBullet(self.rect.center,300,'random2',None)
                    ebullets.add(ebullet)
                    all_sprites.add(ebullet)
            else :
                for i in range(25):
                    ebullet = EnemyBullet(self.rect.center,300,'random',None)
                    ebullets.add(ebullet)
                    all_sprites.add(ebullet)
        if self.mode == 3 :
            
            if 0 <= now - self.last2 <= 800:
                lazer1 = pygame.draw.line(win,RED_FOR_LAZER,self.rect.center,(win_width-(now-self.last2)/(1200)*win_width,win_height),20)
            elif 1000 < now - self.last2 <=1800:
                lazer2 = pygame.draw.line(win,RED_FOR_LAZER,self.rect.center,((now-self.last2 -1000)/(1200)*win_width,0),20)
            elif 2000 < now - self.last2 <= 2800:
                lazer3 = pygame.draw.line(win,RED_FOR_LAZER,self.rect.center,(0,win_height-(now-self.last2 - 2000)/(1200)*win_height),20)
            elif 3000 < now- self.last2 <= 3800:
                lazer4 = pygame.draw.line(win,RED_FOR_LAZER,self.rect.center,(win_width,(now-self.last2 - 3000)/(1200)*win_height),20)
            mask=pygame.mask.from_threshold(win,RED_FOR_LAZER,(10,10,10,255))
            mask_rect=pygame.Rect((0,0),(mask.get_size()))
            if  now - char.invincible > 1000:
                char.image.set_alpha(256)
                if char.mask.overlap(mask,(mask_rect.x-char.rect[0],mask_rect.y-char.rect[1])):
                    char.hit()
            else:
                char.invincible_animation()
        if self.mode == 4:
            ebullet = EnemyBullet(self.rect.center,100,'trackline')
            ebullets.add(ebullet)
            all_sprites.add(ebullet)
            if self.rect.centery >= win_height/2:
                ebullet = EnemyBullet(self.rect.center,400,'up')
                ebullets.add(ebullet)
                all_sprites.add(ebullet)
            elif self.rect.centery <win_height/2:
                ebullet = EnemyBullet(self.rect.center,400,'line')
                ebullets.add(ebullet)
                all_sprites.add(ebullet)
    def draw(self):
        pygame.draw.rect(win,GREEN,[162,0,self.hp*6.65,10])
        pygame.draw.rect(win,RED,[162,0,665,10],2)
    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
        
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self,center,vel,type,degree=None,tracktime=6000):
        super().__init__()
        self.type=type
        if self.type=='track':
            self.image=pygame.transform.scale(trackbullet_image,(15,15))
        elif self.type=='big track':
            self.image=pygame.transform.scale(pygame.image.load('src/CKHS.png').convert(),(100,100))
        elif self.type=='sans2':
            self.image=pygame.transform.scale(pygame.image.load('src/sansb.png').convert(),(20,20))
        elif self.type=='trackline':
            self.image=pygame.transform.scale(pygame.image.load('src/sansy.png').convert(),(20,20))
        else:
            self.image=pygame.transform.scale(ebullet_image,(15,15))
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.center = center
        self.vel=vel
        self.x=self.rect.left
        self.y=self.rect.top
        self.launch=pygame.time.get_ticks()
        self.degree=degree
        self.tracktime=tracktime
        self.fire=False
        if self.type=='random':
            self.angle=random.randrange(5,175)*math.pi/180
        if self.type=='random2':
            self.angle=-random.randrange(5,175)*math.pi/180
        if self.type=='sans2' or self.type=='scatter':
            self.angle=self.degree*math.pi/180
        if self.type=='trackline':
            self.dx=char.rect.centerx-self.rect.centerx
            self.dy=char.rect.centery-self.rect.centery
    def update(self):
        if self.rect.bottom < win_height and self.rect.top>0 and self.rect.left>0 and self.rect.right<win_width:
            if self.type=='line':
                self.y += self.vel*dt
            elif self.type=='track' or self.type=='big track':
                if pygame.time.get_ticks()-self.launch<self.tracktime:
                    self.dx=char.rect.centerx-self.rect.centerx
                    self.dy=char.rect.centery-self.rect.centery
                distance=(self.dx**2+self.dy**2)**0.5
                self.x+=self.dx/distance*dt*self.vel if self.type=='track' else self.dx/distance*dt*self.vel*1.5
                self.y+=self.dy/distance*dt*self.vel
            elif self.type=='45degree':
                angle=math.pi*45/180
                self.x+=math.cos(angle)*dt*self.vel
                self.y+=math.sin(angle)*dt*self.vel
            elif self.type=='135degree':
                angle=math.pi*135/180
                self.x+=math.cos(angle)*dt*self.vel
                self.y+=math.sin(angle)*dt*self.vel
            elif self.type=='random':
                self.x+=math.cos(self.angle)*dt*self.vel
                self.y+=math.sin(self.angle)*dt*self.vel
            elif self.type=='random2':
                self.x+=math.cos(self.angle)*dt*self.vel
                self.y+=math.sin(self.angle)*dt*self.vel
            elif self.type=='sans2':
                self.x+=math.cos(self.angle)*dt*self.vel+sans.vel_x*dt*sans.heading
                self.y+=math.sin(self.angle)*dt*self.vel+sans.vel_y*dt*sans.heading_y
            elif self.type=='scatter':
                self.x+=math.cos(self.angle)*dt*self.vel
                self.y+=math.sin(self.angle)*dt*self.vel
            elif self.type=='up':
                self.y-=self.vel*dt
            elif self.type=='trackline':
                distance=(self.dx**2+self.dy**2)**0.5
                self.x+=self.dx/distance*dt*self.vel
                self.y+=self.dy/distance*dt*self.vel
        else:
            self.kill()
        self.rect.x=self.x
        self.rect.y=self.y
        self.fire_bullet()

    def fire_bullet(self):
        fire_time=1000
        if self.type=='big track':
            if  pygame.time.get_ticks()-self.launch >= fire_time and self.fire==False:
                ebullet=EnemyBullet(self.rect.midbottom,300,'line')
                ebullets.add(ebullet)
                all_sprites.add(ebullet)
                self.fire=True

def change_stage():
    return True if len(enemies) == 0 else False

class Stage():
    def __init__(self):
        self.changestage=True
        self.which=1
    def stage_1(self):
        if self.which==1:
            if self.changestage:
                self.changestage=False
                enemy=[Enemy(300,0,100,-1,50,1000,'line',5),Enemy(500,0,100,1,25,1000,'line',5)]
                enemies.add(enemy)
                all_sprites.add(enemy)
            if change_stage():
                self.changestage=True
                self.which=2
    def stage_2(self):
        if self.which==2:
            if self.changestage:
                self.changestage=False
                enemy=[Enemy(300,0,100,-1,50,4000,'disperse',5),Enemy(500,0,100,1,25,4000,'disperse',5),
                        Enemy(100,0,200,-1,50,1000,'line',5)]
                enemies.add(enemy)
                all_sprites.add(enemy)
            if change_stage():
                self.changestage=True
                self.which=3
    def stage_3(self):
        if self.which==3:
            if self.changestage:
                self.changestage=False
                enemy=[Enemy(300,0,100,-1,50,3000,'disperse',5),Enemy(300,0,100,1,25,3000,'disperse',5),
                        Enemy(100,0,200,1,50,700,'line',5),Enemy(500,0,200,1,50,700,'line',5)]
                enemies.add(enemy)
                all_sprites.add(enemy)
            if change_stage():
                self.changestage=True
                self.which=4
    def stage_4(self):
        global boss1music,bgm
        if self.which==4:
            if self.changestage:
                self.changestage=False
                if boss1music:
                    boss1music=False
                    bgm=True
                    pygame.mixer.init()
                    pygame.mixer.music.load('src/HollowKnight.mp3')
                    if pygame.mixer.get_busy != 1:
                        pygame.mixer.music.play(-1)
                bg_plane = Big_en_plane(enemy_img)
                enemies.add(bg_plane)
                all_sprites.add(bg_plane)
            if change_stage():
                if bgm:
                    bgm=False
                    pygame.mixer.init()
                    pygame.mixer.music.load('src/bgm.mp3')
                    if pygame.mixer.get_busy != 1:
                        pygame.mixer.music.play(-1)
                self.changestage = True
                self.which = 5
    def stage_5(self):
        if self.which==5:
            if self.changestage:
                self.changestage=False
                enemy=[Enemy(300,0,100,-1,50,5000,'track',5),Enemy(300,0,100,1,25,5000,'track',5)]
                enemies.add(enemy)
                all_sprites.add(enemy)
            if change_stage():
                self.changestage=True
                self.which=6
    def stage_6(self):
        if self.which==6:
            if self.changestage:
                self.changestage=False
                enemy=[Enemy(500,0,100,1,50,5000,'track',5),Enemy(300,0,100,1,25,5000,'disperse',5),
                        Enemy(600,0,100,-1,50,5000,'disperse',5,True)]
                enemies.add(enemy)
                all_sprites.add(enemy)
            if change_stage():
                self.changestage=True
                self.which=7
    def stage_7(self):
        if self.which==7:
            if self.changestage:
                self.changestage=False
                enemy=[Enemy(500,0,100,1,50,5000,'track',5),Enemy(300,0,100,1,25,5000,'disperse',5),
                        Enemy(400,0,100,-1,100,3000,'disperse',5),Enemy(100,0,100,1,50,3000,'disperse',5)
                        ,Enemy(200,0,100,1,50,3000,'line',5)]
                enemies.add(enemy)
                all_sprites.add(enemy)
            if change_stage():
                self.changestage=True
                self.which=8
    def stage_8(self):
        global kshsmusic,bgm
        if self.which==8:
            if self.changestage:
                self.changestage=False
                kshs=KSHS()
                enemies.add(kshs)
                all_sprites.add(kshs)
                if kshsmusic:
                    kshsmusic=False
                    bgm=True
                    pygame.mixer.init()
                    pygame.mixer.music.load('src/kshs1.mp3')
                    if pygame.mixer.get_busy != 1:
                        pygame.mixer.music.play(-1)
            if change_stage():
                if bgm:
                    bgm=False
                    pygame.mixer.init()
                    pygame.mixer.music.load('src/bgm.mp3')
                    if pygame.mixer.get_busy != 1:
                        pygame.mixer.music.play(-1)
                self.changestage=True
                self.which=9
    def stage_9(self):
        if self.which==9:
            if self.changestage:
                self.changestage=False
                enemy=[Enemy(500,0,100,1,50,5000,'track',5,True),Enemy(300,0,100,1,25,5000,'disperse',5,True),
                        Enemy(400,0,100,-1,100,5000,'lazer',5,True),Enemy(100,0,100,1,50,5000,'lazer',5,True)
                        ,Enemy(200,0,200,1,50,700,'line',8,True)]
                enemies.add(enemy)
                all_sprites.add(enemy)
            if change_stage():
                self.changestage=True
                self.which=10
    def stage_10(self):
        if self.which==10:
            if self.changestage:
                self.changestage=False
                enemy=[Enemy(500,0,100,1,50,5000,'track',5),Enemy(300,0,100,1,25,5000,'track',5),
                        Enemy(400,0,150,-1,100,5000,'track',5),Enemy(100,0,100,-1,50,3000,'disperse',5)
                        ,Enemy(200,0,100,1,50,5000,'lazer',5)]
                enemies.add(enemy)
                all_sprites.add(enemy)
            if change_stage():
                self.changestage=True
                self.which=11
    def stage_11(self):
        if self.which==11:
            if self.changestage:
                self.changestage=False
                enemy=[Enemy(500,0,100,1,50,5000,'track',5,True),
                    Enemy(300,0,100,1,25,5000,'disperse',5,True),
                    Enemy(400,0,100,-1,100,3000,'disperse',5,True),
                    Enemy(100,0,100,1,50,3000,'disperse',5,True),
                    Enemy(200,0,200,1,50,500,'line',5,True),
                    Enemy(600,0,200,1,50,500,'line',5,True)]
                #enemy=[Enemy(100,0,0,1,50,5000,'line',1)]
                enemies.add(enemy)
                all_sprites.add(enemy)
            if change_stage():
                self.changestage=True
                self.which=12
    def stage_12(self):
        global bgm,sansmusic
        if self.which==12:
            if self.changestage:
                self.changestage=False
                global sans
                sans=Sans()
                enemies.add(sans)
                all_sprites.add(sans)
            if change_stage():
                if bgm:
                    bgm=False
                    pygame.mixer.init()
                    pygame.mixer.music.load('src/bgm.mp3')
                    if pygame.mixer.get_busy != 1:
                        pygame.mixer.music.play(-1)                   
                self.changestage=True
                self.which=1
    def stages(self):
        self.stage_1()
        self.stage_2()
        self.stage_3()
        self.stage_4()
        self.stage_5()
        self.stage_6()
        self.stage_7()
        self.stage_8()
        self.stage_9()
        self.stage_10()
        self.stage_11()
        self.stage_12()

scroll_y=0
def draw_bg():
    global scroll_y
    rel_y = scroll_y % bg.get_rect().height
    win.blit(bg, (0,rel_y - bg.get_rect().height))
    if rel_y < win_height:
	    win.blit(bg, (0, rel_y))
    scroll_y += 2.5
def dead_screen():
    win.fill(BLACK)
    death=pygame.transform.scale(death_image, (250, 250))
    death.set_colorkey(BLACK)
    win.blit(death,(win_width/2-125,150))
    pygame.font.init() 
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface1 = myfont.render('PRESS ENTER TO CONTINUE', False, RED)
    win.blit(textsurface1,(win_width/3-40,500))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                waiting=False

char_vel=250
char=Player(win_width/2,500,char_vel)
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
ebullets=pygame.sprite.Group()
enemies=pygame.sprite.Group()
players=pygame.sprite.Group()

players.add(char)
all_sprites.add(char)

interval=Intervals(50,100,-1)
stage=Stage()
run=True
test=True
while run:
    now=pygame.time.get_ticks()
    draw_bg()
    time_passed=clock.tick(FPS)
    dt = time_passed/1000.0
    all_sprites.update()
    char.shoot()
    char.draw()
    interval.minus()
    for i in enemies:
        i.draw()
        
    get_hit=pygame.sprite.groupcollide(enemies, bullets, False, True,pygame.sprite.collide_mask)
    for enemy in get_hit.keys():
        enemy.hit()

    if  now - char.invincible > 1000:
        char.image.set_alpha(256)
        if pygame.sprite.groupcollide(players, ebullets, False, True,pygame.sprite.collide_mask):
            char.hit()
        if pygame.sprite.groupcollide(players, enemies , False,False,pygame.sprite.collide_mask):
            char.hit()
    else:
        pygame.sprite.groupcollide(players, ebullets, False, True,pygame.sprite.collide_mask)
        char.invincible_animation()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if char.hp<=0:
        for sprite in all_sprites:
            sprite.kill()
        current_stage=stage.which
        stage.which=0
        dead_screen()
        players.add(char)
        all_sprites.add(char)
        char.hp=200
        stage.which=current_stage-1

    stage.stages()
    all_sprites.draw(win)
    pygame.display.flip()

pygame.quit()
