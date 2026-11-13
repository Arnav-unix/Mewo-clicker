import pygame as py
from pygame import mixer
from button import Button
import tomllib
import tomli_w
from math import sin
import random as rd
import time
import os
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
    if sys.platform == "darwin":
        DATA_DIR = os.path.join(
            os.path.expanduser("~"), "Library", "Application Support", "Mewo Clicker"
        )
        os.makedirs(DATA_DIR, exist_ok=True)
    else:
        DATA_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = BASE_DIR
    os.chdir(BASE_DIR)
ASSET_DIR = os.path.join(BASE_DIR, "Assets")


def asset(path):
    return os.path.join(ASSET_DIR, path)


py.init()
mixer.init()

# Save system


def get_save_path():
    try:
        from android.storage import app_storage_path

        base_dir = app_storage_path()
    except ImportError:
        base_dir = DATA_DIR
    return os.path.join(base_dir, "save.toml")


save_file = get_save_path()


def save_data(data):
    tmp_file = save_file + ".tmp"
    with open(tmp_file, "wb") as file:
        tomli_w.dump(data, file)
    os.replace(tmp_file, save_file)


def load_game():
    if os.path.exists(save_file):
        try:
            with open(save_file, "rb") as file:
                return tomllib.load(file)
        except (OSError, tomllib.TOMLDecodeError):
            pass
    return {
        "main": {
            "money": 0,
            "cps": 0,
            "mewoPOWER": 1,
            "time": 0,
        },
        "store": {
            "hand": 0,
            "hand_price": 25,
            "slavemewo": 0,
            "slavemewo_price": 125,
            "sword": 0,
            "sword_price": 750,
            "fish": 0,
            "fish_price": 4000,
            "pig": 0,
            "pig_price": 20000,
            "butterfly": 0,
            "butterfly_price": 100000,
        },
        "achievment": {
            "mewo1": 0,
            "mewo1K": 0,
            "mewo1M": 0,
            "mewo1B": 0,
            "mewo1T": 0,
            "mewo1Qa": 0,
            "mewo1Qi": 0,
            "mewo1Sx": 0,
            "mewo1Sp": 0,
            "mewo1Oc": 0,
            "mewo1No": 0,
            "mewo1De": 0,
            "mewo1UDe": 0,
            "mewo1DDe": 0,
            "mewo1TDe": 0,
        },
    }


def save_game():
    save["main"]["cps"] = cps
    save["main"]["money"] = money
    save["main"]["mewoPOWER"] = mewoPOWER
    save["main"]["time"] = time.time()
    for i in storeItems:
        save["store"][i.name] = i.amount
        save["store"][i.name + "_price"] = i.price
    for i in achLIST:
        save["achievment"][i.achNAME] = i.gained
        save_data(save)


save = load_game()


# Window settings
if os.environ.get("ANDROID_ARGUMENT"):
    screen = py.display.set_mode((0, 0), py.FULLSCREEN)
else:
    # (0, 0) means fullscreen, so use a normal resizable window instead.
    LOGICAL_W, LOGICAL_H = 1280, 720
    desktop_w, desktop_h = py.display.get_desktop_sizes()[0]
    win_w = min(LOGICAL_W, int(desktop_w * 0.9))
    win_h = int(win_w * LOGICAL_H / LOGICAL_W)
    if win_h > desktop_h * 0.9:
        win_h = int(desktop_h * 0.9)
        win_w = int(win_h * LOGICAL_W / LOGICAL_H)
    screen = py.display.set_mode((win_w, win_h), py.RESIZABLE)
width, height = screen.get_size()

# title and logo
mewoBASE = py.image.load(asset("mewo.png")).convert_alpha()
mewo = mewoBASE
py.display.set_caption("Mewo Clicker")
py.display.set_icon(mewo)

# ------------work-------------
# sounds
click1 = mixer.Sound(asset("click1.wav"))
click2 = mixer.Sound(asset("click2.wav"))
click3 = mixer.Sound(asset("click3.wav"))

meow1 = mixer.Sound(asset("meow1.ogg"))
meow2 = mixer.Sound(asset("meow2.ogg"))
meow3 = mixer.Sound(asset("meow3.ogg"))

pop1 = mixer.Sound(asset("pop1.ogg"))
pop2 = mixer.Sound(asset("pop2.ogg"))
pop3 = mixer.Sound(asset("pop3.ogg"))

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
mewoPOWER = save["main"]["mewoPOWER"]
mewoHOVER = False
mewoX = width / 2
mewoY = height / 2
MEWO_BASE = int(min(500, width * 0.7, height * 0.45))
MEWO_PRESSED = int(MEWO_BASE * 1.05)
mewoSIZE = MEWO_BASE
mewoDRAWNSIZE = MEWO_BASE
mewo = py.transform.scale(mewoBASE, (mewoSIZE, mewoSIZE)).convert_alpha()
mewoHITBOX = mewo.get_rect(center=(mewoX, mewoY))

# click text (px per second)
gravity = 845
up = 390
drag = 84.5
text = []
textX = []
textY = []
textXCH = []
textYCH = []
font = py.font.Font(asset("KOMIKAX_.ttf"), 61)

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
money = save["main"]["money"]


font_cache = {}


def show_money(x, y, money, size, color, center=True, surface=None):
    surface = surface if surface is not None else screen
    font = font_cache.get(size)
    if font is None:
        font = font_cache[size] = py.font.Font(asset("KOMIKAX_.ttf"), size)
    moneyTEXT = font.render(str(money), True, color)
    if center:
        moneyRECT = moneyTEXT.get_rect(center=(x, y))
        surface.blit(moneyTEXT, moneyRECT)
    else:
        surface.blit(moneyTEXT, (x, y))


# exitBASE = py.image.load(asset("exit.png")).convert_alpha()
# exitIMG = py.transform.scale(exitBASE, (200, 200))
# exitHITBOX = exitIMG.get_rect(bottomleft=(50, height - 50))

buyIMG = py.transform.scale(py.image.load(asset("buy.png")), (120, 120)).convert_alpha()
pr_buyIMG = py.transform.scale(
    py.image.load(asset("pr_buy.png")), (120, 120)
).convert_alpha()


STORE_MARGIN = 16
STORE_GAP = 24
storeBASE = py.image.load(asset("store.png")).convert_alpha()
storeIMG = py.transform.scale(storeBASE, (200, 200))
storeHITBOX = storeIMG.get_rect(bottomright=(width - 50, height - 50))
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


cps = save["main"]["cps"]

money += cps * (time.time() - save["main"]["time"])


# item class
class item:
    def __init__(self, name, image, price, power, amount, pos):
        self.name = name
        self.source = image
        self.price = price
        self.power = power
        self.amount = amount
        self.resize(pos)

    def resize(self, pos):
        self.image = py.transform.scale(
            self.source, (STORE_ICON, STORE_ICON)
        ).convert_alpha()
        self.button = Button(0, 0, buyIMG, pr_buyIMG, STORE_ICON / 120)
        self.X, self.baseY = pos
        self.Y = self.baseY

    def handle(self, scr, events=()):
        global money
        global cps

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


# store-items
hand = item(
    "hand",
    py.image.load(asset("store-items/hand.png")),
    save["store"].get("hand_price", 25),
    0.2,
    save["store"]["hand"],
    store_pos(0),
)

slavemewo = item(
    "slavemewo",
    py.image.load(asset("store-items/slave-mewo.png")),
    save["store"].get("slavemewo_price", 125),
    2,
    save["store"]["slavemewo"],
    store_pos(1),
)

sword = item(
    "sword",
    py.image.load(asset("store-items/sword.png")),
    save["store"].get("sword_price", 750),
    10,
    save["store"]["sword"],
    store_pos(2),
)

fish = item(
    "fish",
    py.image.load(asset("store-items/fish.png")),
    save["store"].get("fish_price", 4000),
    50,
    save["store"]["fish"],
    store_pos(3),
)

pig = item(
    "pig",
    py.image.load(asset("store-items/pig.png")),
    save["store"].get("pig_price", 20000),
    250,
    save["store"]["pig"],
    store_pos(4),
)

butterfly = item(
    "butterfly",
    py.image.load(asset("store-items/butterfly.png")),
    save["store"].get("butterfly_price", 100000),
    1000,
    save["store"]["butterfly"],
    store_pos(5),
)

storeItems = [hand, slavemewo, sword, fish, pig, butterfly]


def layout():
    global width, height, mewo, mewoX, mewoY, mewoHITBOX
    global MEWO_BASE, MEWO_PRESSED, mewoSIZE, mewoDRAWNSIZE
    global moneyX, moneyY, storeIMG, storeHITBOX
    global STORE_COLS, STORE_CARD_W, STORE_CARD_H, STORE_ICON, STORE_FONT

    width, height = screen.get_size()

    mewoX, mewoY = width / 2, height / 2
    MEWO_BASE = int(min(500, width * 0.7, height * 0.45))
    MEWO_PRESSED = int(MEWO_BASE * 1.05)
    mewoSIZE = mewoDRAWNSIZE = MEWO_BASE
    mewo = py.transform.scale(mewoBASE, (MEWO_BASE, MEWO_BASE)).convert_alpha()
    mewoHITBOX = mewo.get_rect(center=(mewoX, mewoY))

    moneyX, moneyY = width / 2, height * 0.13

    storeIMG = py.transform.scale(storeBASE, (200, 200)).convert_alpha()
    storeHITBOX = storeIMG.get_rect(bottomright=(width - 50, height - 50))

    STORE_COLS = 2 if width >= 680 else 1
    STORE_CARD_W = min(
        width / 2,
        (width - 2 * STORE_MARGIN - (STORE_COLS - 1) * STORE_GAP) / STORE_COLS,
    )
    STORE_CARD_H = int(STORE_CARD_W * STORE_HEIGHT)
    STORE_ICON = int(min(STORE_CARD_W * 0.4, STORE_CARD_H * 0.5))
    STORE_FONT = max(12, int(STORE_CARD_H * 0.21))

    for index, i in enumerate(storeItems):
        i.resize(store_pos(index))


layout()


# achievment
achPLATE = py.transform.scale(
    py.image.load(asset("achievment-display.png")), (500, 500)
).convert_alpha()


# achievment class
class achievment:
    def __init__(self, name, achNAME, typee, amount, reward, gained):
        self.name = name
        self.achNAME = achNAME
        self.typee = typee
        self.amount = amount
        self.reward = reward
        self.gained = gained
        self.X = -500
        self.done = False
        self.timer = 0
        self.draw = False

    def handle(self, dt):
        global money
        if self.typee == "Clicked":
            if money >= self.amount and not self.gained:
                money += self.reward
                self.draw = True
                self.gained = True
            if self.draw:
                if self.X <= width:
                    self.X += 65 * dt
                    screen.blit(achPLATE, (self.X, -200))
                    show_money(self.X + 100, 25, self.name, 41, (0, 0, 0), center=False)
                else:
                    self.draw = False


# achievments
mewo1 = achievment(
    "Click 1 time", "mewo1", "Clicked", 1, 0, save["achievment"]["mewo1"]
)

mewo1K = achievment(
    "Click 1K times", "mewo1K", "Clicked", 1000, 100, save["achievment"]["mewo1K"]
)

mewo1M = achievment(
    "Click 1M times", "mewo1M", "Clicked", 1000000, 100000, save["achievment"]["mewo1M"]
)

mewo1B = achievment(
    "Click 1B times",
    "mewo1B",
    "Clicked",
    1000000000,
    100000000,
    save["achievment"]["mewo1B"],
)

mewo1T = achievment(
    "Click 1T times",
    "mewo1T",
    "Clicked",
    1000000000000,
    100000000000,
    save["achievment"]["mewo1T"],
)

mewo1Qa = achievment(
    "Click 1Qa times",
    "mewo1Qa",
    "Clicked",
    1000000000000000,
    100000000000000,
    save["achievment"]["mewo1Qa"],
)

mewo1Qi = achievment(
    "Click 1Qi times",
    "mewo1Qi",
    "Clicked",
    1000000000000000000,
    100000000000000000,
    save["achievment"]["mewo1Qi"],
)

mewo1Sx = achievment(
    "Click 1Sx times",
    "mewo1Sx",
    "Clicked",
    1000000000000000000000,
    100000000000000000000,
    save["achievment"]["mewo1Sx"],
)

mewo1Sp = achievment(
    "Click 1Sp times",
    "mewo1Sp",
    "Clicked",
    1000000000000000000000000,
    100000000000000000000000,
    save["achievment"]["mewo1Sp"],
)

mewo1Oc = achievment(
    "Click 1Oc times",
    "mewo1Oc",
    "Clicked",
    1000000000000000000000000000,
    100000000000000000000000000,
    save["achievment"]["mewo1Oc"],
)

mewo1No = achievment(
    "Click 1No times",
    "mewo1No",
    "Clicked",
    1000000000000000000000000000000,
    100000000000000000000000000000,
    save["achievment"]["mewo1No"],
)

mewo1De = achievment(
    "Click 1De times",
    "mewo1De",
    "Clicked",
    1000000000000000000000000000000000,
    100000000000000000000000000000000,
    save["achievment"]["mewo1De"],
)

mewo1UDe = achievment(
    "Click 1UDe times",
    "mewo1UDe",
    "Clicked",
    1000000000000000000000000000000000000,
    100000000000000000000000000000000000,
    save["achievment"]["mewo1UDe"],
)

mewo1DDe = achievment(
    "Click 1DDe times",
    "mewo1DDe",
    "Clicked",
    1000000000000000000000000000000000000000,
    100000000000000000000000000000000000000,
    save["achievment"]["mewo1DDe"],
)

mewo1TDe = achievment(
    "Click 1TDe times",
    "mewo1TDe",
    "Clicked",
    1000000000000000000000000000000000000000000,
    100000000000000000000000000000000000000000,
    save["achievment"]["mewo1TDe"],
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
    py.image.load(asset("goldmewo.png")), (120, 120)
).convert_alpha()
goldmewoHITBOX = goldmewo.get_rect()

appearin = time.time() + rd.randint(180, 600)
appeared = False
goldclicked = False
goldwait = 0
goldangle = 0
buff = 0
buffed = False


# main game
def maingame():
    global money
    global mewo
    global mewoSIZE
    global mewoHOVER
    global mewoHITBOX
    global mewoPOWER
    global mewoDRAWNSIZE
    global goldmewoHITBOX
    global appearin
    global appeared
    global goldclicked
    global goldwait
    global goldangle
    global buff
    global buffed

    running = True
    while running:
        dt = clock.tick(fps) / 1000
        if screen.get_size() != (width, height):
            layout()
        screen.fill((0, 69, 42))
        mewoSIZE = MEWO_BASE

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            elif event.type in (
                py.APP_WILLENTERBACKGROUND,
                py.APP_DIDENTERBACKGROUND,
                py.APP_TERMINATING,
            ):
                save_game()
            if event.type == py.KEYDOWN and event.key == py.K_F11:
                py.display.toggle_fullscreen()
            if event.type == py.MOUSEBUTTONDOWN:
                pos = event.pos

                if mewoHITBOX.collidepoint(pos):
                    mewoHOVER = True
                    text.append("+" + human_format(mewoPOWER))
                    textX.append(pos[0])
                    textY.append(pos[1])
                    textYCH.append(-up)
                    textXCH.append((pos[0] - width / 2) / 10 * 13)

                    money += mewoPOWER
                    eval("pop" + str(rd.randint(1, 3)) + ".play()")

                if storeHITBOX.collidepoint(pos):
                    soundchoice = str(rd.randint(1, 3))
                    eval("click" + soundchoice + ".set_volume(0.8)")
                    save_game()
                    if store():
                        running = False
                    save_game()
                    eval("click" + soundchoice + ".play()")
                    eval("click" + soundchoice + ".set_volume(0.1)")

                # if exitHITBOX.collidepoint(pos):
                #     soundchoice = str(rd.randint(1, 3))
                #     eval("click" + soundchoice + ".set_volume(0.8)")
                #     running = False

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

        if buffed and time.time() >= buff:
            buffed = False

        money += cps * (3 if buffed else 1) * dt

        if mewoSIZE != mewoDRAWNSIZE:
            mewo = py.transform.scale(mewoBASE, (mewoSIZE, mewoSIZE)).convert_alpha()
            mewoDRAWNSIZE = mewoSIZE
        mewoHITBOX = mewo.get_rect(center=(mewoX, mewoY))

        # achievment handling
        for name in achLIST:
            name.handle(dt)

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
            str(human_format(cps * (3 if buffed else 1))) + "/s",
            int(min(73, width * 0.11)),
            (150, 100, 0) if buffed else (0, 0, 0),
        )
        screen.blit(storeIMG, storeHITBOX)
        # screen.blit(exitIMG, exitHITBOX)
        if time.time() >= appearin:
            if not appeared:
                goldsize = rd.randint(120, 200)
                goldpos = [
                    rd.randint(goldsize // 2, width - goldsize // 2),
                    rd.randint(goldsize // 2, height - goldsize // 2),
                ]
                goldscaled = py.transform.scale(goldmewo, (goldsize, goldsize))
                goldangle = 0
                goldwait = time.time() + rd.randint(5, 15)
                appeared = True

            goldangle += dt
            transformedgoldmewo = py.transform.rotate(goldscaled, 20 * sin(goldangle))
            goldmewoHITBOX = transformedgoldmewo.get_rect(center=goldpos)
            screen.blit(transformedgoldmewo, goldmewoHITBOX)

            if goldclicked:
                goldclicked = False
                appeared = False
                appearin = time.time() + rd.randint(180, 600)
                eval("meow" + str(rd.randint(1, 3)) + ".play()")
                choice = rd.randint(1, 2)
                if choice == 1:
                    if cps > 1:
                        money += round(rd.uniform(200 * cps, 600 * cps))
                    else:
                        money += round(rd.uniform(200, 600))
                else:
                    buffed = True
                    buff = time.time() + rd.randint(180, 600)
            elif time.time() >= goldwait:
                appeared = False
                appearin = time.time() + rd.randint(180, 600)

        # click handling
        for i in range(len(text) - 1, -1, -1):
            ctext = font.render(text[i], True, (100, 100, 0))
            ctextrect = ctext.get_rect(center=(textX[i], textY[i]))
            screen.blit(ctext, ctextrect)
            textX[i] += textXCH[i] * dt
            textY[i] += textYCH[i] * dt
            textYCH[i] += gravity * dt
            if abs(textXCH[i]) <= drag * dt:
                textXCH[i] = 0
            elif textXCH[i] > 0:
                textXCH[i] -= drag * dt
            else:
                textXCH[i] += drag * dt

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
    global STORE_SCROLL

    click2.play()
    click2.set_volume(0.1)
    dragging = False
    drag_start = 0
    drag_base = 0
    while True:
        dt = clock.tick(fps) / 1000
        if screen.get_size() != (width, height):
            layout()
        screen.fill((145, 230, 210))

        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                return False
            elif event.type in (
                py.APP_WILLENTERBACKGROUND,
                py.APP_DIDENTERBACKGROUND,
                py.APP_TERMINATING,
            ):
                save_game()

            if event.type == py.MOUSEWHEEL:
                STORE_SCROLL += event.y * 60
            elif event.type == py.KEYDOWN:
                if event.key == py.K_F11:
                    py.display.toggle_fullscreen()
                elif event.key == py.K_DOWN:
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
    try:
        maingame()
    finally:
        save_game()
    py.quit()
