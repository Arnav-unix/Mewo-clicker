import pygame as py
import random as rd
from button import Button
from pygame import mixer

py.init()


# Window settings
width = 720
height = 1600
screen = py.display.set_mode((width, height))

# title and logo
mewo = py.image.load("Assets/mewo.png")
py.display.set_caption("Mewo Clicker")
py.display.set_icon(mewo)

# ------------work-------------
# sounds
click1 = mixer.Sound("Assets/click1.wav")
click2 = mixer.Sound("Assets/click2.wav")
click3 = mixer.Sound("Assets/click3.wav")

click1.set_volume(0.3)
click2.set_volume(0.1)
click3.set_volume(0.3)

# fps
fps = 60
clock = py.time.Clock()

# player
mewoPOWER = 1
mewoHOVER = False
mewoX = 360
mewoY = 800
mewoSIZE = 400
mewo = py.transform.scale(mewo, (mewoSIZE, mewoSIZE)).convert_alpha()
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


def human_format(num):
    global formats
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    try:
        return "{}{}".format(
            "{:f}".format(num).rstrip("0").rstrip("."), formats[magnitude]
        )
    except:
        return "?"


# money
moneyX = 360
moneyY = 200
money = 0


def show_money(x, y, money, size, color, center=True):
    font = py.font.Font("Assets/KOMIKAX_.ttf", size)
    moneyTEXT = font.render(str(money), True, color)
    if center:
        moneyRECT = moneyTEXT.get_rect(center=(x, y))
        screen.blit(moneyTEXT, moneyRECT)
    else:
        screen.blit(moneyTEXT, (x, y))


# store
storeIMG = py.transform.scale(
    py.image.load("Assets/store.png"), (200, 200)
).convert_alpha()
storeHITBOX = storeIMG.get_rect(center=(600, 1350))

buyIMG = py.transform.scale(py.image.load("Assets/buy.png"), (120, 120)).convert_alpha()
pr_buyIMG = py.transform.scale(
    py.image.load("Assets/pr_buy.png"), (120, 120)
).convert_alpha()


def itemBG(X, Y):
    py.draw.rect(
        screen,
        (255, 109, 80),
        (X - storeSIZE / 2 - 20, Y - storeSIZE / 2 - 20, 250, 150),
        border_radius=20,
    )


storeSCX = 0
storeSCY = 100
cps = 0


# item class
class item:
    def __init__(self, image, price, power, pos):
        global buyIMG
        global pr_buyIMG
        self.X = pos[0]
        self.Y = pos[1]
        self.YCH = 0
        self.image = image
        self.price = price
        self.power = power
        self.amount = 0
        self.button = Button(self.X + 100, self.Y - 30, buyIMG, pr_buyIMG, 1)

    def handle(self, scr):
        global money
        global cps
        global click3

        self.Y += self.YCH
        py.draw.rect(
            screen,
            (0, 189, 100),
            (self.X - 60, self.Y - 50, 300, 300),
            border_radius=20,
        )

        show_money(self.X + 160, self.Y + 160, human_format(self.price), 46, (0, 0, 0))
        show_money(self.X + 25, self.Y + 160, human_format(self.amount), 46, (0, 0, 0))

        screen.blit(self.image, (self.X - 30, self.Y - 30))
        if self.button.draw(scr):
            if money >= self.price:
                self.amount += 1
                money -= self.price
                cps += self.power
                self.price += self.price // 5
                click3.set_volume(1)
                click3.play()
                click3.set_volume(0.3)


# store items
# hand
hand = item(
    py.transform.scale(
        py.image.load("Assets/store items/hand.png"), (120, 120)
    ).convert_alpha(),
    20,
    0.2,
    (storeSCX + 100, storeSCY),
)

# slave mewo
slavemewo = item(
    py.transform.scale(
        py.image.load("Assets/store items/slave mewo.png"), (120, 120)
    ).convert_alpha(),
    150,
    3,
    (storeSCX + 450, storeSCY),
)

# sword
sword = item(
    py.transform.scale(
        py.image.load("Assets/store items/sword.png"), (120, 120)
    ).convert_alpha(),
    1000,
    10,
    (storeSCX + 100, storeSCY + 350),
)

# fish
fish = item(
    py.transform.scale(
        py.image.load("Assets/store items/fish.png"), (120, 120)
    ).convert_alpha(),
    8000,
    50,
    (storeSCX + 450, storeSCY + 350),
)

# pig
pig = item(
    py.transform.scale(
        py.image.load("Assets/store items/pig.png"), (120, 120)
    ).convert_alpha(),
    36000,
    200,
    (storeSCX + 100, storeSCY + 700),
)

# butterfly
butterfly = item(
    py.transform.scale(
        py.image.load("Assets/store items/butterfly.png"), (120, 120)
    ).convert_alpha(),
    120000,
    1000,
    (storeSCX + 450, storeSCY + 700),
)

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
                if self.X != width:
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


# main game
def maingame():
    global money
    global mewo
    global mewoSIZE
    global mewoHOVER
    global mewoHITBOX
    global mewoPOWER
    global textXCH

    running = True
    while running:
        screen.fill((0, 69, 42))
        mewoSIZE = 400

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            if event.type == py.MOUSEBUTTONDOWN:
                pos = py.mouse.get_pos()

                if mewoHITBOX.collidepoint(pos):
                    mewoHOVER = True
                    text.append("+" + human_format(mewoPOWER))
                    textX.append(pos[0])
                    textY.append(pos[1])
                    textYCH.append(-up)
                    try:
                        textXCH.append((pos[0] - width / 2) / 10)
                    except ZeroDivisionError:
                        textXCH.append(0)

                    money += mewoPOWER
                    choice = rd.choice([1, 2, 3])
                    if choice == 1:
                        click1.play()
                    elif choice == 2:
                        click2.play()
                    else:
                        click3.play()

                if storeHITBOX.collidepoint(pos):
                    click2.set_volume(0.8)
                    store()
                    click2.play()
                    click2.set_volume(0.1)

            elif event.type == py.MOUSEBUTTONUP:
                mewoHOVER = False

        if mewoHOVER == True:
            mewoSIZE = 420
        else:
            mewoSIZE = 400

        mewoPOWER = 1 + cps / 20

        money += cps / fps

        mewo = py.transform.scale(mewo, (mewoSIZE, mewoSIZE)).convert_alpha()
        mewoHITBOX = mewo.get_rect(center=(mewoX, mewoY))

        # achievment handling
        for name in achLIST:
            name.handle()

        # nothing here
        screen.blit(mewo, mewoHITBOX)
        show_money(moneyX, moneyY, human_format(int(money)), 104, (0, 0, 0))
        show_money(moneyX, moneyY + 100, str(human_format(cps)) + "/s", 73, (0, 0, 0))
        screen.blit(storeIMG, storeHITBOX)

        # click handling
        for i, v in enumerate(text):
            ctext = font.render(text[i], True, (100, 100, 0))
            ctextrect = ctext.get_rect(center=(textX[i], textY[i]))
            screen.blit(ctext, ctextrect)
            textX[i] += textXCH[i]
            textY[i] += textYCH[i]
            textYCH[i] += gravity
            if textXCH[i] > 0:
                textXCH[i] -= 0.5
            elif textXCH[i] < 0:
                textXCH[i] += 0.5

            if textY[i] > height:
                text.pop(i)
                textY.pop(i)
                textX.pop(i)
                textYCH.pop(i)
                textXCH.pop(i)

        clock.tick(fps)
        py.display.update()


# shop
def store():
    global money
    global cps
    global handPRICE

    storerunning = True
    click2.play()
    click2.set_volume(0.1)
    while storerunning:
        screen.fill((145, 230, 210))

        for event in py.event.get():
            if event.type == py.QUIT:
                storerunning = False
            if event.type == py.MOUSEBUTTONDOWN:
                pos = py.mouse.get_pos()
                if storeHITBOX.collidepoint(pos):
                    click2.set_volume(0.8)
                    return

        # store item handling
        hand.handle(screen)
        slavemewo.handle(screen)
        sword.handle(screen)
        fish.handle(screen)
        pig.handle(screen)
        butterfly.handle(screen)

        money += cps / fps

        screen.blit(storeIMG, storeHITBOX)

        clock.tick(fps)
        py.display.update()


if __name__ == "__main__":
    maingame()

py.quit()
