import pygame
import time
import math
import random

circles = []
rects = []
lines = []
Cr = 0.95
d = (math.pi)/2
g = 1
gx = g/100
display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (50,250,30)
blue = (90,80,250)
yellow = (240,250,200)

pygame.init()
playing =True
#sound = pygame.mixer.Sound("bois.wav")
sound2 = pygame.mixer.Sound("music.wav")
#sound2.play(loops = -1)

game_display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('')
clock = pygame.time.Clock()

def hex():
	while True:
		colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
		if (colour == green or colour == blue):
			pass
		else:
			break
	return colour

class Circle():
	def __init__(self):
		self.pos = {"x": 0,"y": 0}
		self.vel = {"x": 0,"y": 0}
		self.mass = {"m": 0}
		self.rad = {"r": 0}
		self.look = {"c": (0,0,0), "f": 0,"rot": 0,"s": 0}

class Rect:
	def __init__(self):
		self.p0 = {"xy": (0,0)}
		self.p1 = {"xy": (0,0)}
		self.p2 = {"xy": (0,0)}
		self.p3 = {"xy": (0,0)}
		self.look = {"c": black}

class Line:
	def __init__(self):
		self.pos = {"b": (0,0),"e": (0,0)}

ball = pygame.image.load("ball.png")
shadow = pygame.image.load("shadow.png")
def circlef():
	for circle in circles:
		circle.vel["y"] += gx*math.sin(d)
		circle.vel["x"] += gx*math.cos(d)
		circle.pos["x"] += circle.vel["x"]
		circle.pos["y"] += circle.vel["y"]

		s = (circle.rad["r"]*2)*(round(((circle.pos["y"]+circle.rad["r"])-((display_height/2)-50))/(((display_height/2))/100))/100)
		if (s>0):
			circle.look["s"] = s
		else:
			circle.look["s"] = 0
		nshadow = pygame.transform.scale(shadow, (round(circle.look["s"]),round(circle.look["s"])))
		game_display.blit(nshadow, (circle.pos["x"]-(circle.look["s"]/2), (display_height-50)-circle.look["s"]/2))

		pygame.draw.circle(game_display, circle.look["c"], (round(circle.pos["x"]), round(circle.pos["y"])), circle.rad["r"], circle.look["f"])
		nball = pygame.transform.scale(ball, (circle.rad["r"]*2,circle.rad["r"]*2))
		circle.look["rot"] -= circle.vel["x"]*2
		nnball = pygame.transform.rotate(nball, circle.look["rot"])
		nnrect = nnball.get_rect()
		nnrect.center = (round(circle.pos["x"]), round(circle.pos["y"]))
		game_display.blit(nnball, nnrect)
"""
grass = pygame.image.load("grass.png")
def rectf():
	for rect in rects:
		pygame.draw.rect(game_display, rect.look["c"], (rect.pos["x"]-(rect.size["w"]/2), rect.pos["y"]-(rect.size["h"]/2), rect.size["w"], rect.size["h"]), 0)
		ngrass = pygame.transform.scale(grass, (round(rect.size["w"]/rect.look["a"]),round(rect.size["h"]/rect.look["u"])))
		for i in range(rect.look["u"]):
			for j in range(rect.look["a"]):
				x = (rect.pos["x"]-(rect.size["w"]/2))+(rect.size["w"]/rect.look["a"])*j
				y = (rect.pos["y"]-(rect.size["h"]/2))+(rect.size["h"]/rect.look["u"])*i
				game_display.blit(ngrass, (x,y))
"""

pointlist = []
def rectf():
	for rect in rects:
		pointlist = [rect.p0["xy"],rect.p1["xy"],rect.p2["xy"],rect.p3["xy"]]
		pygame.draw.polygon(game_display, rect.look["c"], pointlist, 0)

def conc_circles(c1, c2):
	m1 = c1.mass["m"]
	m2 = c2.mass["m"]
	v1 = (c1.vel["x"]**2 + c1.vel["y"]**2)**0.5
	v2 = (c2.vel["x"]**2 + c2.vel["y"]**2)**0.5
	o1 = math.atan2(c1.vel["y"],c1.vel["x"])
	o2 = math.atan2(c2.vel["y"],c2.vel["x"])
	p = math.atan2((c2.pos["y"]-c1.pos["y"]),(c1.pos["x"]-c2.pos["x"]))
	c1_vxe = ((v1*math.cos(o1-p)*(m1-m2)+2*m2*v2*math.cos(o2-p))/(m1+m2))*math.cos(p)+v1*math.sin(o1-p)*math.cos(p+(math.pi/2))
	c1_vye = ((v1*math.cos(o1-p)*(m1-m2)+2*m2*v2*math.cos(o2-p))/(m1+m2))*math.sin(p)+v1*math.sin(o1-p)*math.sin(p+(math.pi/2))
	c2_vxe = ((v2*math.cos(o2-p)*(m2-m1)+2*m1*v1*math.cos(o1-p))/(m2+m1))*math.cos(p)+v2*math.sin(o2-p)*math.cos(p+(math.pi/2))
	c2_vye = ((v2*math.cos(o2-p)*(m2-m1)+2*m1*v1*math.cos(o1-p))/(m2+m1))*math.sin(p)+v2*math.sin(o2-p)*math.sin(p+(math.pi/2))
	c1_vx = (Cr*m2*(c2_vxe-c1_vxe)+m1*c1_vxe+m2*c2_vxe)/(m1+m2)
	c1_vy = (-Cr*m2*(c2_vye-c1_vye)+m1*c1_vye+m2*c2_vye)/(m1+m2)
	c2_vx = (Cr*m1*(c1_vxe-c2_vxe)+m1*c1_vxe+m2*c2_vxe)/(m1+m2)
	c2_vy = (-Cr*m1*(c1_vye-c2_vye)+m1*c1_vye+m2*c2_vye)/(m1+m2)
	c1.vel["x"] = c1_vx
	c1.vel["y"] = c1_vy
	c2.vel["x"] = c2_vx
	c2.vel["y"] = c2_vy

def check_circles():
	for i in range (0,len(circles)):
		for j in range (i+1, len(circles)):
			dx = circles[i].pos["x"] - circles[j].pos["x"]
			dy = circles[i].pos["y"] - circles[j].pos["y"]
			distance = math.sqrt(dx * dx + dy * dy)
			if(distance<=circles[i].rad["r"]+circles[j].rad["r"]):
				a = math.atan2(dy,dx)
				h = (circles[i].rad["r"]+circles[j].rad["r"])-distance
				mpx = circles[i].pos["x"]-((circles[i].rad["r"]*math.cos(a))-(h*math.cos(a))/2)
				mpy = circles[i].pos["y"]-((circles[i].rad["r"]*math.sin(a))-(h*math.sin(a))/2)
				o1 = math.atan2((circles[i].pos["y"]-mpy),(mpx-circles[i].pos["x"]))
				o2 = math.atan2((circles[j].pos["y"]-mpy),(mpx-circles[j].pos["x"]))
				x1 = math.sqrt(((mpx-circles[i].pos["x"])**2)+((circles[i].pos["y"]-mpy)**2))
				x2 = math.sqrt(((mpx-circles[j].pos["x"])**2)+((circles[j].pos["y"]-mpy)**2))
				circles[i].pos["x"] -= (circles[i].rad["r"]-x1)*math.cos(o1)
				circles[i].pos["y"] += (circles[i].rad["r"]-x1)*math.sin(o1)
				circles[j].pos["x"] -= (circles[j].rad["r"]-x2)*math.cos(o2)
				circles[j].pos["y"] += (circles[j].rad["r"]-x2)*math.sin(o2)
				conc_circles(circles[i], circles[j])


def check_walls():
	for circle in circles:
		if((circle.pos["y"]+circle.rad["r"])>display_height):
			circle.pos["y"] = display_height-circle.rad["r"]
		if((circle.pos["y"]-circle.rad["r"])<0):
			circle.pos["y"] = circle.rad["r"]
		if((circle.pos["y"]+circle.rad["r"])==display_height or (circle.pos["y"]-circle.rad["r"])==0):
			circle.vel["y"] *= -Cr
		if((circle.pos["x"]+circle.rad["r"])>display_width):
			circle.pos["x"] = display_width-circle.rad["r"]
		if((circle.pos["x"]-circle.rad["r"])<0):
			circle.pos["x"] = circle.rad["r"]
		if((circle.pos["x"]+circle.rad["r"])==display_width or (circle.pos["x"]-circle.rad["r"])==0):
			circle.vel["x"] *= -Cr
"""
def check_rects():
		for rect in rects:
				rx = rect.pos["x"]+(rect.size["w"]/2)
				lx = rect.pos["x"]-(rect.size["w"]/2)
				ty = rect.pos["y"]-(rect.size["h"]/2)
				by = rect.pos["y"]+(rect.size["h"]/2)
				for circle in circles:
						cx = circle.pos["x"]
						cy = circle.pos["y"]
						if (cx<rx and cx>lx and (cy-circle.rad["r"])<by and (cy-circle.rad["r"])>ty):
							circle.pos["y"] = by+circle.rad["r"]
						if (cx<rx and cx>lx and (cy+circle.rad["r"])<by and (cy+circle.rad["r"])>ty):
							circle.pos["y"] = ty-circle.rad["r"]
						if (cy<by and cy>ty and (cx-circle.rad["r"])<rx and (cx-circle.rad["r"])>lx):
							circle.pos["x"] = rx+circle.rad["r"]
						if (cy<by and cy>ty and (cx+circle.rad["r"])<rx and (cx+circle.rad["r"])>lx):
							circle.pos["x"] = lx-circle.rad["r"]
						cx = circle.pos["x"]
						cy = circle.pos["y"]
						if (((cx-circle.rad["r"])==rx and cy>=ty and cy<=by) or ((cx+circle.rad["r"])==lx and cy>=ty and cy<=by)):
							circle.vel["x"] *= -Cr
						if (((cy-circle.rad["r"])==by and cx>=lx and cx<=rx) or ((cy+circle.rad["r"])==ty and cx>=lx and cx<=rx)):
							circle.vel["y"] *= -Cr
"""

def check_lines():
	for circle in circles:
		for line in lines:
			chx = line.pos["e"][0]-line.pos["b"][0]
			chy = line.pos["e"][1]-line.pos["b"][1]
			ah = math.atan2(abs(chy),abs(chx))
			av = math.atan2(abs(chx),abs(chy))
			bx = line.pos["b"][0]
			by = line.pos["b"][1]
			cx = circle.pos["x"]
			cy = circle.pos["y"]
			if chx!=0 and chy!=0:
				m = (chy/chx)
				nm = -(1/m)
				x = (m*bx - by - nm*cx + cy)/(m-nm)
				y = (m*(x-bx))+by
				leng = ((x-cx)**2+(y-cy)**2)**0.5
			elif chx==0:
				leng = bx-cx
			else:
				leng = by-cy
			if circle.pos["x"]-circle.rad["r"] < line.pos["e"][0] and circle.pos["x"]+circle.rad["r"] > line.pos["b"][0]:
				if (leng < circle.rad["r"]):
					try:
						if y>circle.pos["y"]:
							circle.pos["x"] -= ((circle.rad["r"]-leng)*math.cos((math.pi/2)-ah))
							circle.pos["y"] -= ((circle.rad["r"]-leng)*math.sin((math.pi/2)-ah))
							o = math.atan2(circle.vel["x"],circle.vel["y"])+ah
							no = math.atan2(Cr*math.sin(o),math.cos(o))
							v1 = (circle.vel["x"]**2+circle.vel["y"]**2)**0.5
							v2 = ((v1*math.cos(o))**2 + (v1*math.sin(o))**2)**0.5
							circle.vel["x"] = -(v2*math.cos((math.pi/2)-(no+av)))
							circle.vel["y"] = v2*math.sin((math.pi/2)-(no+av))
						else:
							circle.pos["x"] += ((circle.rad["r"]-leng)*math.cos((math.pi/2)-ah))
							circle.pos["y"] += ((circle.rad["r"]-leng)*math.sin((math.pi/2)-ah))
							o = math.atan2(circle.vel["x"],circle.vel["y"])+ah
							no = math.atan2(Cr*math.sin(o),math.cos(o))
							v1 = (circle.vel["x"]**2+circle.vel["y"]**2)**0.5
							v2 = ((v1*math.cos(o))**2 + (v1*math.sin(o))**2)**0.5
							circle.vel["x"] = -(v2*math.cos((math.pi/2)-(no+av)))
							circle.vel["y"] = v2*math.sin((math.pi/2)-(no+av))
					except:
						circle.pos["x"] += ((circle.rad["r"]-leng)*math.cos((math.pi/2)-ah))
						circle.pos["y"] += ((circle.rad["r"]-leng)*math.sin((math.pi/2)-ah))
						o = math.atan2(circle.vel["x"],circle.vel["y"])+ah
						no = math.atan2(Cr*math.sin(o),math.cos(o))
						v1 = (circle.vel["x"]**2+circle.vel["y"]**2)**0.5
						v2 = ((v1*math.cos(o))**2 + (v1*math.sin(o))**2)**0.5
						circle.vel["x"] = -(v2*math.cos((math.pi/2)-(no+av)))
						circle.vel["y"] = v2*math.sin((math.pi/2)-(no+av))

def draw():
	game_display.fill(blue)
	check_circles()
	check_walls()
	#check_rects()
	check_lines()
	rectf()
	circlef()
	pygame.display.flip()

def myDown():
	global sound
	x = (display_width/2)+random.randint(-2,2)
	y = 100
	c = Circle()
	c.pos["x"] = x
	c.pos["y"] = y
	c.mass["m"] = random.uniform(0.1,0.2)
	c.rad["r"] = round((math.sqrt(c.mass["m"]/math.pi))*100)
	c.look["c"] = white
	circles.append(c)
	#sound.play(loops = 0)

#bx,by,ex,ey,c
#u,r,b,l
line_info = [[50,300,150,200,green], [150,200,160,210], [60,310,160,210], [50,300,60,310]
			, [0,display_height-50,display_width,display_height-50,green], [display_width,display_height-50,display_width,display_height], [0,display_height,display_width,display_height], [0,display_height-50,0,display_height]
			, [display_width/2-50,display_height/2-50,display_width/2+50,display_height/2-50,green], [display_width/2+50,display_height/2-50,display_width/2+50,display_height/2+50], [display_width/2-50,display_height/2+50,display_width/2+50,display_height/2+50], [display_width/2-50,display_height/2-50,display_width/2-50,display_height/2+50]
			]

for i in range(0,len(line_info),4):
	r = Rect()
	r.p0["xy"] = (line_info[i][0],line_info[i][1])
	r.p1["xy"] = (line_info[i][2],line_info[i][3])
	r.p2["xy"] = (line_info[i+1][2],line_info[i+1][3])
	r.p3["xy"] = (line_info[i+2][0],line_info[i+2][1])
	r.look["c"] = line_info[i][4]
	rects.append(r)

for j in range(len(line_info)):
	l = Line()
	l.pos["b"] = (line_info[i][0],line_info[i][1])
	l.pos["e"] = (line_info[i][2],line_info[i][3])
	lines.append(l)

"""
#x,y,h,w,c,a,u,r
rects_info = [[display_width/2,display_height-25,50,display_width,green,16,1,0], [display_width/2,display_height/2,100,100,green,2,2,45]]

for i in range(len(rects_info)):
		r = Rect()
		r.pos["x"] = rects_info[i][0]
		r.pos["y"] = rects_info[i][1]
		r.size["w"] = rects_info[i][3]
		r.size["h"] = rects_info[i][2]
		r.look["c"] = rects_info[i][4]
		r.look["a"] = rects_info[i][5]
		r.look["u"] = rects_info[i][6]
		r.look["r"] = rects_info[i][7]
		rects.append(r)
"""

while playing:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				myDown()
	draw()
	clock.tick(100)

pygame.quit()
quit()