import sys, pygame
import os
import random as r
import threading
global points 
import wx
app=wx.App(False)
frame=wx.Frame(None, wx.ID_ANY, "название!")
panel = wx.Panel(frame, wx.ID_ANY)
global points
points=0

questions = [
	["Ваш друг пригласил вас на вечеринку. \nЧто вы сделаете?", 
		["Убедить друга отменить вечеринку.", "Друг успешно отменяет его \nвечеринку и не заражается короновирусом", "+очко"],
		["Пойти на вечеринку.", "К несчастью к другу приходят \nзараженные знакомые. Вы ложитесь в \nбольницу на обследование.", "-очко"],
	],
	["В больнице закончились места, новая в постройке. \nЧто делать?", 
		["Направить больных в другой город.", "Вы успешно направляете больных \nв Нова-проспект, где они проходят \nлечение.", "+очко"],
		["Оставить все как есть.", "Больные остаются в переполненных \nбольницах, из-за чего вас \nнедолюбливают.", "-очко"]
	],
	["У вас закончились маски. \nКакие меры вы предпримите?",
		["Сделать самому.", "Вы сделали маски и тем самым \nзащитили большое количество больных!", "+очко"],
		["Оставить все как есть.", "Из-за нехватки масок \nнесколько человек заразились!", "-очко"]
	],
	["У вашего пожилого соседа закончились продукты \nи он решил сходить в магазин. \nЧто вы сделаете?",
		["Сходить самому.", "Вы успешно идете в магазин и \nприносите соседу продуктов.", "+очко"],
		["Вызвать службу доставки.", "Вы вызвали службу доставки, \nкоторая привезла вашему соседу еды.", "+очко"],
		["Не обращать на него внимание.", "Вы не обратили внимание на соседа, \nиз-за чего тот направился в магазин в одиночку \nи заразился.", "-очко"]
	],
	["Вам скучно сидеть дома. \nЧто вы сделаете, чтобы развлечь себя?", 
		["Посмотреть сериал.", "Вы посмотрели сериал.", "+очко"],
		["Пойти гулять.", "Вы отправились в парк, где вас \nуспешно заразили.", "-очко"]
	]
]

os.environ['SDL_VIDEO_CENTERED'] = '1'
global x, y, w, h
global g_events, current_problem, matchscreen
g_events = []
ingame_buttons = []
matchscreen = []

all_pos = [[475, 374], [665, 322], [385, 207], [250, 282], [508, 310]]

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('BEBASNEUE_BOLD', 48)
notification = pygame.image.load('notification.png')
pygame.mixer.music.load('ost1.mp3')
pygame.mixer.music.play()

sz = width, height = 1024, 768
scrn = pygame.display.set_mode(sz)

def is_inbox(px1, py1, x2, y2, x3, y3):
	return px1 >= x2 and px1 <= x3 and py1 >= y2 and py1 <= y3







global __mous_press
__mous_press = False
def is_mousepressed():
	global __mous_press
	br = pygame.mouse.get_pressed()
	if __mous_press != br:
		__mous_press = br
		return br
	return False

def updscores():
	scrn.blit(pygame.image.load('topbar.png'), [0, 0])
	scrn.blit(pygame.image.load('menu.png'), [960, -12])
	textsurface = myfont.render("Очки: " + str(points), False, (255, 255, 255))
	scrn.blit(textsurface,(1,1))
		
#Action surface		
sr = pygame.Surface((sz[0] - 120, sz[1] - 120))
sr.set_alpha(230)
sr.fill((0, 0, 5))

#Button Template
br = pygame.Surface((sz[0] - 124, 35))
br.set_alpha(255)
br.fill((0, 0, 0))

#Exit Template
Ebr = pygame.Surface((sz[0] - 124, 35))
Ebr.set_alpha(255)
Ebr.fill((128, 0, 0))

def ui():
	global g_events, matchscreen
	scrn.blit(pygame.image.load("map.png"), [0, 0])
	scrn.blit(pygame.image.load('events.png'), [0, 80])
	#scrn.blit(pygame.image.load('event_standart.png'), [5, 125])
	updscores()
	
	for i in g_events:
		scrn.blit(notification, (i[0], i[1]))
	if len(matchscreen) > 0:
		scrn.blit(sr, (60, 60))
		h = -1
		h1 = 0
		for i in matchscreen:
			if i[0] == "text":
				h += 1
				ts = myfont.render(i[1], False, (255, 255, 255))
				scrn.blit(ts,(67, 65 + 33 * h))
			elif i[0] == "answer":
				h1 += 1
				PosY = sz[1] - 60 - 38 * (h1)
				scrn.blit(br, (62, PosY))
				ts = myfont.render(i[1], False, (255, 255, 255))
				scrn.blit(ts, (sz[0] / 2 - myfont.size(i[1])[0] / 2, PosY + 2))
			elif i[0] == "exit":
				h1 += 1
				PosY = sz[1] - 60 - 38 * (h1)
				scrn.blit(Ebr, (62, PosY))
				ts = myfont.render(i[1], False, (255, 255, 255))
				scrn.blit(ts, (sz[0] / 2 - myfont.size(i[1])[0] / 2, PosY + 2))
		

def question():
	global current_problem, matchscreen
	a = questions[r.randint(0, len(questions) - 1)]
	current_problem = a
	matchscreen = []
	for i in a[0].split("\n"):
		matchscreen.append(["text", i])
	for i in range(1, len(a)):
		matchscreen.append(["answer", a[i][0], i])
	

def answer(a):
	global current_problem, points, matchscreen
	b = current_problem[a]

	matchscreen = []
	for i in b[1].split("\n"):
		matchscreen.append(["text", i])
	matchscreen.append(["exit", "Выход"])	
	
	if b[2] == "+очко":
		points += 1
	elif b[2] == "-очко":
		points -= 1
	ui()
	
	print(a)	
	
def gameplay():
	global g_events, matchscreen
	timer = threading.Timer(30.0, gameplay) 
	timer.start() 
	random_location = r.randint(0, len(all_pos) - 1)
	#random_location = 0
	print(random_location + 1)
	pos = all_pos[random_location]
	
	g_events.append(pos)

gameplay()
while True:
	ui()
	#for event in pygame.event.get():
	#	if event.type == pygame.MOUSEBUTTONDOWN:
	if is_mousepressed():
		x, y = pygame.mouse.get_pos()
		s = notification.get_rect().size
		if len(matchscreen) == 0:
			for i in g_events:
				if is_inbox(x, y, i[0], i[1], i[0] + s[0], i[1] + s[1]):
					question()
					g_events.remove(i)
					break
		else:
			h = 0
			for i in matchscreen:
				if i[0] == "answer" or i[0] == "exit":
					h += 1
					pos = (sz[0] / 2 - myfont.size(i[1])[0] / 2, sz[1] - 60 - 38 * (h) + 2)
					if is_inbox(x, y, pos[0], pos[1], pos[0] + sz[0] - 124, pos[1] + 35):
						if i[0] == "answer":
							answer(i[2])
						else:
							matchscreen = []
	pygame.event.wait()
	pygame.display.update()
	