import os
import random
import sys
from tkinter import Tk
from tkinter import messagebox
from tkinter import simpledialog

import pygame

top = Tk()
top.geometry("100x100")
top.withdraw()
fps=60
w,h=1000,750
win=pygame.display.set_mode((w,h))


particle_width,particle_helght=30,32

rw = 950
rh = 600
pygame.font.init()
playloop=True
rock=pygame.image.load('./img/rock.png')
rock=pygame.transform.rotate(pygame.transform.scale(rock,(particle_width,particle_helght)),(90))
rockrect=rock.get_rect()

paper=pygame.image.load('./img/paper.png')
paper=pygame.transform.rotate(pygame.transform.scale(paper,(particle_width,particle_helght)),(90))
paperrect=paper.get_rect()

scissor=pygame.image.load('./img/scissor.png')
scissor=pygame.transform.rotate(pygame.transform.scale(scissor,(particle_width,particle_helght)),(90))
scissorrect=scissor.get_rect()

class particle:
    def __init__(self,img):
        global rockrect,paperrect,scissorrect,rw,rh
        self.img=img
        self.x=random.choice(list(range(51,rw-30)))
        self.y=random.choice(list(range(51,rh-30)))
        self.xvel=random.choice([-1,-0.5,1,0.5])
        self.yvel=random.choice([-1,-0.5,1,0.5])
    def move(self):
        self.x+=self.xvel
        self.y+=self.yvel
        if self.x>rw-10:
            self.xvel=-1
        if self.x>rw:
            self.x=-3
        if self.x<40:
            self.xvel = 1
        if self.x<30:
            self.xvel=3
        if self.y>rh-10:
            self.yvel=-1
        if self.y>rh:
            self.yvel=-3
        if self.y<40:
            self.yvel=1
        if self.y<30:
            self.yvel=3

    def draw(self):
        # self.x+=self.xvel
        # self.y+=self.yvel
        if self.img=='r':
            self.obj=win.blit(rock,(self.x,self.y))
            self.rect=rockrect
        if self.img=='p':
            self.obj=win.blit(paper,(self.x,self.y))
            self.rect = paperrect
        if self.img=='s':
            self.obj=win.blit(scissor,(self.x,self.y))
            self.rect = scissorrect



def border():
    pygame.draw.rect(win,(255,0,0),pygame.Rect(30,30,rw,rh),5,7)
    pygame.draw.rect(win,(0,150,210),pygame.Rect(35,35,rw-10,rh-10))
    pygame.draw.rect(win,(0,255,0),pygame.Rect(35,640,rw,rh-20),border_radius=15)


def main():

    global playloop
    first_palyer = simpledialog.askstring("Input", "First player name?", parent=top)
    second_palyer = simpledialog.askstring("Input", "Second player name?", parent=top)
    third_palyer = simpledialog.askstring("Input", "Third player name?", parent=top)
    top.destroy()
    top.mainloop()


    if playloop:
        clock = pygame.time.Clock()

        rc = 0
        pc = 0
        sc = 0


        run = True
        play = False
        particles = []
        total = -1
        font = pygame.font.SysFont(name='arial', size=30)
        r, g, b = (0, 0, 0)

        while run:
            clock.tick(fps)
            pygame.display.set_caption(f'FPS:{int(clock.get_fps())}ROCK-PAPER-SCISSORS')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_UP]:
                particles.append(particle('r'))
                rc += 1
                particles.append(particle('p'))
                pc += 1
                particles.append(particle('s'))
                sc += 1

            if keys_pressed[pygame.K_DOWN]:
                try:
                    particles.pop(0)
                    rc -= 1
                    particles.pop(0)
                    pc -= 1
                    particles.pop(0)
                    sc -= 1
                except Exception:
                    pass

            win.fill((r, g, b))

            border()
            rockimg = font.render(f'TOTAL:' + str(len(particles)) + f'        ({first_palyer})ROCK:' + str(
                rc) + f'        ({second_palyer})PAPER:' + str(pc) + f'        ({third_palyer})SCISSOR:' + str(sc),
                                  True, (255, 0, 0))
            infoimg1 = font.render('Press ↑ ↓ buttons to load particles, press SPACEBAR to start the STIMULATION', True,
                                   (255, 0, 0))
            infoimg2 = font.render(
                'load particles<300 for better performance,donot toggle[↑↓] once the stimulation begins', True,
                (255, 0, 0))
            win.blit(rockimg, (40, 650))
            win.blit(infoimg1, (40, 680))
            win.blit(infoimg2, (40, 710))
            for p in particles:
                p.draw()
            if keys_pressed[pygame.K_SPACE]:
                total = len(particles)
                play = True
            if play:
                for p in particles:
                    p.move()

                colletion_tolorence = 3
                for obj1 in particles:
                    for obj2 in particles:
                        if obj1 != obj2:
                            if obj1.obj.colliderect(obj2.obj):
                                if obj1.img == 'r' and obj2.img == 'p':
                                    obj1.img = 'p'
                                    rc -= 1
                                    pc += 1
                                elif obj1.img == 'p' and obj2.img == 's':
                                    obj1.img = 's'
                                    pc -= 1
                                    sc += 1
                                elif obj1.img == 's' and obj2.img == 'r':
                                    obj1.img = 'r'
                                    sc -= 1
                                    rc += 1
                                if abs(obj1.obj.top - obj2.obj.bottom) < colletion_tolorence:
                                    obj1.yvel = random.choice([0.5, 1])
                                    obj2.yvel = random.choice([-1, -0.5])
                                if abs(obj1.obj.bottom - obj2.obj.top) < 2:
                                    obj1.yvel = random.choice([-1, -0.5])
                                    obj2.yvel = random.choice([0.5, 1])
                                if abs(obj1.obj.left - obj2.obj.right) < colletion_tolorence:
                                    obj1.xvel = random.choice([0.5, 1])
                                    obj2.xvel = random.choice([-1, -0.5])
                                if abs(obj1.obj.right - obj2.obj.left) < 2:
                                    obj1.xvel = random.choice([-1, -0.5])
                                    obj2.xvel = random.choice([0.5, 1])


                if rc == total:
                    particles.clear()
                    messagebox.showinfo(title='WINNER', message=f'{first_palyer} wins the game')

                    run = False
                    playloop = False
                    os.system('cls')
                    sys.exit()

                if pc == total:
                    particles.clear()
                    messagebox.showinfo(title='WINNER', message=f'{second_palyer} wins the game')

                    run = False
                    playloop = False
                    os.system('cls')
                    sys.exit()

            if sc == total:
                particles.clear()
                messagebox.showinfo(title='WINNER', message=f'{first_palyer} wins the game')

                run = False
                playloop = False
                os.system('cls')
                sys.exit()

            pygame.display.update()
    pygame.quit()

if __name__=='__main__':
    main()






