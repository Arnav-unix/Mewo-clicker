import pygame as py
from pygame import mixer
from button import Button
from math import sin
import random as rd
import time
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

py.init()
mixer.init()

# Window settings


screen = py.display.set_mode((0, 0))
width, height = screen.get_size()

# title and logo
mewoBASE = py.image.load("Assets/mewo.png").convert_alpha()
mewo = mewoBASE
py.display.set_caption("Mewo Clicker")
py.display.set_icon(mewo)

# ------------work-------------
# sounds
click1 = mixer.Sound("Assets/click1.wav")
click2 = mixer.Sound("Assets/click2.wav")
click3 = mixer.Sound("Assets/click3.wav")

meow1 = mixer.Sound("Assets/meow1.mp3")
meow2 = mixer.Sound("Assets/meow2.mp3")
meow3 = mixer.Sound("Assets/meow3.mp3")

pop1 = mixer.Sound("Assets/pop1.mp3")
pop2 = mixer.Sound("Assets/pop2.mp3")
pop3 = mixer.Sound("Assets/pop3.mp3")

click1.set_volume(0.3)
click2.set_volume(0.1)
click3.set_volume(0.3)

meow1.set_volume(0.3)
meow2.set_volume(0.1)
meow3.set_volume(0.3)

pop1.set_volume(0.3)
pop2.set_volume(0.3)
pop3.set_volume(0.3)

# fps
fps = 60
clock = py.time.Clock()

# player
mewoPOWER = 1
mewoHOVER = False
mewoX = width / 2
mewoY = height / 2
MEWO_BASE = int(min(500, width * 0.7, height * 0.45))
MEWO_PRESSED = int(MEWO_BASE * 1.05)
mewoSIZE = MEWO_BASE
mewoDRAWNSIZE = MEWO_BASE
mewo = py.transform.scale(mewoBASE, (mewoSIZE, mewoSIZE)).convert_alpha()
mewoHITBOX = mewo.get_rect(center=(mewoX, mewoY))

# click text
gravity = 5
up = 30
text = []
textX = []
textY = []
textXCH = []
textYCH = []
font = py.font.Font("Assets/KOMIKAX_.ttf", 61)

# conversion
formats = [
    "",
    "K",
    "M",
    "B",
    "T",
    "Qa",
    "Qi",
    "Sx",
    "Sp",
    "Oc",
    "No",
    "De",
    "UDe",
    "DDe",
    "TDe",
]


# This is copy pasted stuff
def human_format(num):
    global formats
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    if magnitude < len(formats):
        return "{}{}".format(
            "{:f}".format(num).rstrip("0").rstrip("."), formats[magnitude]
        )
    return "{:.2f}e{}".format(num, magnitude * 3)


# money
moneyX = width / 2
moneyY = height * 0.13
money = 0


font_cache = {}


def show_money(x, y, money, size, color, center=True, surface=None):
    surface = surface if surface is not None else screen
    font = font_cache.get(size)
    if font is None:
        font = font_cache[size] = py.font.Font("Assets/KOMIKAX_.ttf", size)
    moneyTEXT = font.render(str(money), True, color)
    if center:
        moneyRECT = moneyTEXT.get_rect(center=(x, y))
        surface.blit(moneyTEXT, moneyRECT)
    else:
        surface.blit(moneyTEXT, (x, y))


# store
storeIMG = py.transform.scale(
    py.image.load("Assets/store.png"), (200, 200)
).convert_alpha()
storeHITBOX = storeIMG.get_rect(bottomright=(width - 50, height - 50))

buyIMG = py.transform.scale(py.image.load("Assets/buy.png"), (120, 120)).convert_alpha()
pr_buyIMG = py.transform.scale(
    py.image.load("Assets/pr_buy.png"), (120, 120)
).convert_alpha()


STORE_MARGIN = 16
STORE_GAP = 24
STORE_HEIGHT = 0.7
STORE_COLS = 2 if width >= 680 else 1
STORE_CARD_W = min(
    width / 2, (width - 2 * STORE_MARGIN - (STORE_COLS - 1) * STORE_GAP) / STORE_COLS
)
STORE_CARD_H = int(STORE_CARD_W * STORE_HEIGHT)
STORE_ICON = int(min(STORE_CARD_W * 0.4, STORE_CARD_H * 0.5))
STORE_FONT = max(12, int(STORE_CARD_H * 0.21))
STORE_HUD = 120
STORE_BOTTOM = 270
STORE_SCROLL = 0


def store_pos(index):
    col = index % STORE_COLS
    row = index // STORE_COLS
    grid_w = STORE_COLS * STORE_CARD_W + (STORE_COLS - 1) * STORE_GAP
    return (
        (width - grid_w) / 2 + col * (STORE_CARD_W + STORE_GAP),
        STORE_MARGIN + row * (STORE_CARD_H + STORE_GAP),
    )


cps = 0


# item class
class item:
    def __init__(self, image, price, power, pos):
        global buyIMG
        global pr_buyIMG
        self.X = pos[0]
        self.Y = pos[1]
        self.baseY = pos[1]
        self.image = image
        self.price = price
        self.power = power
        self.amount = 0
        self.button = Button(0, 0, buyIMG, pr_buyIMG, STORE_ICON / 120)

    def handle(self, scr, events=()):
        global money
        global cps
        global click3

        self.Y = self.baseY + STORE_SCROLL
        if self.Y + STORE_CARD_H < 0 or self.Y > height:
            return
        icon_x = self.X + STORE_CARD_W * 0.08
        icon_y = self.Y + STORE_CARD_H * 0.08
        self.button.rect.topleft = (self.X + STORE_CARD_W * 0.56, icon_y)
        py.draw.rect(
            scr,
            (0, 189, 100),
            (self.X, self.Y, STORE_CARD_W, STORE_CARD_H),
            border_radius=int(STORE_CARD_H / 12),
        )

        show_money(
            self.X + STORE_CARD_W * 0.74,
            self.Y + STORE_CARD_H * 0.75,
            human_format(self.price),
            STORE_FONT,
            (0, 0, 0),
            surface=scr,
        )
        show_money(
            self.X + STORE_CARD_W * 0.28,
            self.Y + STORE_CARD_H * 0.75,
            human_format(self.amount),
            STORE_FONT,
            (0, 0, 0),
            surface=scr,
        )

        scr.blit(self.image, (icon_x, icon_y))
        if self.button.draw(scr, events):
            if money >= self.price:
                self.amount += 1
                money -= self.price
                cps += self.power
                self.price = round(self.price * 1.10)
                soundchoice = str(rd.randint(1, 3))
                eval("click" + soundchoice + ".set_volume(1)")
                eval("click" + soundchoice + ".play()")
                eval("click" + soundchoice + ".set_volume(1)")


# store items
# hand
hand = item(
    py.transform.scale(
        py.image.load("Assets/store items/hand.png"), (STORE_ICON, STORE_ICON)
    ).convert_alpha(),
    25,
    0.2,
    store_pos(0),
)

# slave mewo
slavemewo = item(
    py.transform.scale(
        py.image.load("Assets/store items/slave mewo.png"), (STORE_ICON, STORE_ICON)
    ).convert_alpha(),
    125,
    2,
    store_pos(1),
)

# sword
sword = item(
    py.transform.scale(
        py.image.load("Assets/store items/sword.png"), (STORE_ICON, STORE_ICON)
    ).convert_alpha(),
    750,
    10,
    store_pos(2),
)

# fish
fish = item(
    py.transform.scale(
        py.image.load("Assets/store items/fish.png"), (STORE_ICON, STORE_ICON)
    ).convert_alpha(),
    4000,
    50,
    store_pos(3),
)

# pig
pig = item(
    py.transform.scale(
        py.image.load("Assets/store items/pig.png"), (STORE_ICON, STORE_ICON)
    ).convert_alpha(),
    20000,
    250,
    store_pos(4),
)

# butterfly
butterfly = item(
    py.transform.scale(
        py.image.load("Assets/store items/butterfly.png"), (STORE_ICON, STORE_ICON)
    ).convert_alpha(),
    100000,
    1000,
    store_pos(5),
)

storeItems = [hand, slavemewo, sword, fish, pig, butterfly]

# achievment
achPLATE = py.transform.scale(
    py.image.load("Assets/achievment display.png"), (500, 500)
).convert_alpha()


# achievment class
class achievment:
    def __init__(self, name, type, amount, reward):
        self.name = name
        self.type = type
        self.amount = amount
        self.reward = reward
        self.gained = False
        self.X = -500
        self.done = False
        self.timer = 0

    def handle(self):
        global money
        global achPLATE
        if self.type == "Clicked":
            if money >= self.amount:
                if not self.gained:
                    money += self.reward
                    self.gained = True
                if self.X < width:
                    self.X += 5
                    screen.blit(achPLATE, (self.X, -200))

                    show_money(self.X + 100, 25, self.name, 41, (0, 0, 0), center=False)


# achievments
mewo1 = achievment("Click 1 time", "Clicked", 1, 0)

mewo1K = achievment("Click 1K times", "Clicked", 1000, 100)

mewo1M = achievment("Click 1M times", "Clicked", 1000000, 100000)

mewo1B = achievment("Click 1B times", "Clicked", 1000000000, 100000000)

mewo1T = achievment("Click 1T times", "Clicked", 1000000000000, 100000000000)

mewo1Qa = achievment("Click 1Qa times", "Clicked", 1000000000000000, 100000000000000)

mewo1Qi = achievment(
    "Click 1Qi times", "Clicked", 1000000000000000000, 100000000000000000
)

mewo1Sx = achievment(
    "Click 1Sx times", "Clicked", 1000000000000000000000, 100000000000000000000
)

mewo1Sp = achievment(
    "Click 1Sp times", "Clicked", 1000000000000000000000000, 100000000000000000000000
)

mewo1Oc = achievment(
    "Click 1Oc times",
    "Clicked",
    1000000000000000000000000000,
    100000000000000000000000000,
)

mewo1No = achievment(
    "Click 1No times",
    "Clicked",
    1000000000000000000000000000000,
    100000000000000000000000000000,
)

mewo1De = achievment(
    "Click 1De times",
    "Clicked",
    1000000000000000000000000000000000,
    100000000000000000000000000000000,
)

mewo1UDe = achievment(
    "Click 1UDe times",
    "Clicked",
    1000000000000000000000000000000000000,
    100000000000000000000000000000000000,
)

mewo1DDe = achievment(
    "Click 1DDe times",
    "Clicked",
    1000000000000000000000000000000000000000,
    100000000000000000000000000000000000000,
)

mewo1TDe = achievment(
    "Click 1TDe times",
    "Clicked",
    1000000000000000000000000000000000000000000,
    100000000000000000000000000000000000000000,
)


achLIST = [
    mewo1,
    mewo1K,
    mewo1M,
    mewo1B,
    mewo1T,
    mewo1Qa,
    mewo1Qi,
    mewo1Sx,
    mewo1Sp,
    mewo1Oc,
    mewo1No,
    mewo1De,
    mewo1UDe,
    mewo1DDe,
    mewo1TDe,
]

# Gold mewo
goldmewo = py.transform.scale(
    py.image.load("Assets/goldmewo.png"), (120, 120)
).convert_alpha()
goldmewoHITBOX = goldmewo.get_rect()

appearin = time.time() + rd.randint(180, 600)
appeared = False
goldclicked = False
goldwait = 0
goldangle = 0


# main game
def maingame():
    global money
    global mewo
    global mewoSIZE
    global mewoHOVER
    global mewoHITBOX
    global mewoPOWER
    global mewoDRAWNSIZE
    global textXCH
    global goldmewoHITBOX
    global appearin
    global appeared
    global goldclicked
    global goldwait
    global goldmewo
    global goldangle

    running = True
    while running:
        dt = clock.tick(fps) / 1000
        screen.fill((0, 69, 42))
        mewoSIZE = MEWO_BASE

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            if event.type == py.MOUSEBUTTONDOWN:
                pos = event.pos

                if mewoHITBOX.collidepoint(pos):
                    mewoHOVER = True
                    text.append("+" + human_format(mewoPOWER))
                    textX.append(pos[0])
                    textY.append(pos[1])
                    textYCH.append(-up)
                    textXCH.append((pos[0] - width / 2) / 10)

                    money += mewoPOWER
                    eval("pop" + str(rd.randint(1, 3)) + ".play()")

                if storeHITBOX.collidepoint(pos):
                    soundchoice = str(rd.randint(1, 3))
                    eval("click" + soundchoice + ".set_volume(0.8)")
                    if store():
                        running = False
                        break
                    eval("click" + soundchoice + ".play()")
                    eval("click" + soundchoice + ".set_volume(0.1)")

                if goldmewoHITBOX.collidepoint(pos):
                    goldclicked = True

            elif event.type == py.MOUSEBUTTONUP:
                mewoHOVER = False
                goldclicked = False

        if mewoHOVER and py.mouse.get_pressed()[0]:
            mewoSIZE = MEWO_PRESSED
        else:
            mewoSIZE = MEWO_BASE

        mewoPOWER = 1 + cps / 20

        money += cps * dt

        if mewoSIZE != mewoDRAWNSIZE:
            mewo = py.transform.scale(mewoBASE, (mewoSIZE, mewoSIZE)).convert_alpha()
            mewoDRAWNSIZE = mewoSIZE
        mewoHITBOX = mewo.get_rect(center=(mewoX, mewoY))

        # achievment handling
        for name in achLIST:
            name.handle()

        # nothing here
        screen.blit(mewo, mewoHITBOX)
        show_money(
            moneyX,
            moneyY,
            human_format(int(money)),
            int(min(104, width * 0.145)),
            (0, 0, 0),
        )
        show_money(
            moneyX,
            moneyY + 100,
            str(human_format(cps)) + "/s",
            int(min(73, width * 0.11)),
            (0, 0, 0),
        )
        screen.blit(storeIMG, storeHITBOX)
        if time.time() >= appearin:
            if not appeared:
                goldpos = [rd.randint(0, width), rd.randint(0, height)]
                goldangle += 2 * dt
                goldrotation = 45 * sin(goldangle)
                randomscale = rd.randint(120, 200)
                randomscale = [randomscale, randomscale]
                transformedgoldmewo = py.transform.scale(goldmewo, randomscale)
                goldmewoHITBOX = transformedgoldmewo.get_rect(center=goldpos)
                screen.blit(transformedgoldmewo, goldmewoHITBOX)
                goldwait = time.time() + rd.randint(180, 600)
                appeared = True
            else:
                goldangle += 1 * dt
                goldrotation = 20 * sin(goldangle)
                transformedgoldmewo = py.transform.scale(goldmewo, randomscale)
                transformedgoldmewo = py.transform.rotate(
                    transformedgoldmewo, goldrotation
                )
                goldmewoHITBOX = transformedgoldmewo.get_rect(center=goldpos)
                screen.blit(transformedgoldmewo, goldmewoHITBOX)
                if goldclicked:
                    goldclicked = False
                    appeared = False
                    appearin = time.time() + rd.randint(5, 15)
                    eval("meow" + str(rd.randint(1, 3)) + ".play()")
                    if cps > 1:
                        money += round(rd.uniform(200 * cps, 600 * cps))
                    else:
                        money += round(rd.uniform(200, 600))
            if time.time() >= goldwait and not goldclicked:
                appearin = time.time() + rd.randint(180, 600)
                appeared = False

        # click handling
        for i in range(len(text) - 1, -1, -1):
            ctext = font.render(text[i], True, (100, 100, 0))
            ctextrect = ctext.get_rect(center=(textX[i], textY[i]))
            screen.blit(ctext, ctextrect)
            textX[i] += textXCH[i]
            textY[i] += textYCH[i]
            textYCH[i] += gravity
            if abs(textXCH[i]) <= 0.5:
                textXCH[i] = 0
            elif textXCH[i] > 0:
                textXCH[i] -= 0.5
            else:
                textXCH[i] += 0.5

            if textY[i] > height:
                text.pop(i)
                textY.pop(i)
                textX.pop(i)
                textYCH.pop(i)
                textXCH.pop(i)

        py.display.update()


# store
def store():
    global money
    global cps
    global STORE_SCROLL

    click2.play()
    click2.set_volume(0.1)
    dragging = False
    drag_start = 0
    drag_base = 0
    while True:
        dt = clock.tick(fps) / 1000
        screen.fill((145, 230, 210))

        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                return True
            if event.type == py.MOUSEWHEEL:
                STORE_SCROLL += event.y * 60
            elif event.type == py.KEYDOWN:
                if event.key == py.K_DOWN:
                    STORE_SCROLL -= 60
                elif event.key == py.K_UP:
                    STORE_SCROLL += 60
            elif event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                if storeHITBOX.collidepoint(event.pos):
                    return
                dragging = True
                drag_start = event.pos[1]
                drag_base = STORE_SCROLL
            elif event.type == py.MOUSEMOTION and dragging:
                STORE_SCROLL = drag_base + event.pos[1] - drag_start
            elif event.type == py.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            elif event.type == py.FINGERDOWN:
                fx, fy = event.x * width, event.y * height
                if storeHITBOX.collidepoint((fx, fy)):
                    return
                dragging = True
                drag_start = fy
                drag_base = STORE_SCROLL
            elif event.type == py.FINGERMOTION and dragging:
                STORE_SCROLL = drag_base + event.y * height - drag_start
            elif event.type == py.FINGERUP:
                dragging = False

        top = min(i.baseY for i in storeItems)
        bottom = max(i.baseY for i in storeItems) + STORE_CARD_H
        STORE_SCROLL = max(
            min(0, height - STORE_BOTTOM - bottom),
            min(max(0, STORE_MARGIN - top), STORE_SCROLL),
        )

        for i in storeItems:
            i.handle(screen, events)

        money += cps * dt

        show_money(
            STORE_HUD,
            height - STORE_MARGIN - STORE_HUD / 3,
            human_format(int(money)),
            int(min(73, width * 0.11)),
            (0, 0, 0),
        )
        screen.blit(storeIMG, storeHITBOX)

        py.display.update()


if __name__ == "__main__":
    maingame()
    py.quit()
