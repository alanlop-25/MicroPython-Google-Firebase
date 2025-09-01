from machine import I2C
import framebuf

# ==== OLED SSD1306 Driver ====
class SSD1306:
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.buffer = bytearray(self.height * self.width // 8)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        for cmd in (
            0xAE, 0xA4, 0xD5, 0x80, 0xA8, self.height - 1,
            0xD3, 0x00, 0x40, 0x8D, 0x14, 0x20, 0x00,
            0xA1, 0xC8, 0xDA, 0x12, 0x81, 0xCF, 0xD9, 0xF1,
            0xDB, 0x40, 0xA6, 0xAF
        ):
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([0x80, cmd]))

    def write_data(self, buf):
        self.i2c.writeto(self.addr, bytearray([0x40]) + buf)

    def show(self):
        for page in range(0, self.height // 8):
            self.write_cmd(0xB0 | page)
            self.write_cmd(0x02)
            self.write_cmd(0x10)
            start = self.width * page
            end = start + self.width
            self.write_data(self.buffer[start:end])

    def fill(self, color):
        self.framebuf.fill(color)

    def line(self, x1, y1, x2, y2, color):
        self.framebuf.line(x1, y1, x2, y2, color)

# ==== POSICIONES (3 filas x 8 columnas) ====
class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

displayArray = [Pos(col*15, row*22) for row in range(3) for col in range(8)]

# ==== DIBUJOS DE CARACTERES (estilo simple 10x15 px) ====
def draw_box(pos):  # ayuda a ver los márgenes
    pass

# Letras A–Z (simplificadas con líneas rectas)
def A(p): oled.line(p.x,p.y+15,p.x+5,p.y,1); oled.line(p.x+5,p.y,p.x+10,p.y+15,1); oled.line(p.x+2,p.y+8,p.x+8,p.y+8,1)
def B(p): oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x,p.y,p.x+7,p.y,1); oled.line(p.x,p.y+7,p.x+7,p.y+7,1); oled.line(p.x,p.y+15,p.x+7,p.y+15,1); oled.line(p.x+7,p.y,p.x+7,p.y+15,1)
def C(p): oled.line(p.x+10,p.y,p.x,p.y,1); oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x,p.y+15,p.x+10,p.y+15,1)
def D(p): oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x,p.y,p.x+8,p.y,1); oled.line(p.x+8,p.y,p.x+8,p.y+15,1); oled.line(p.x,p.y+15,p.x+8,p.y+15,1)
def E(p): oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x,p.y,p.x+10,p.y,1); oled.line(p.x,p.y+7,p.x+8,p.y+7,1); oled.line(p.x,p.y+15,p.x+10,p.y+15,1)
def F(p): oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x,p.y,p.x+10,p.y,1); oled.line(p.x,p.y+7,p.x+8,p.y+7,1)
def G(p): oled.line(p.x+10,p.y,p.x,p.y,1); oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x,p.y+15,p.x+10,p.y+15,1); oled.line(p.x+10,p.y+8,p.x+5,p.y+8,1); oled.line(p.x+10,p.y,p.x+10,p.y+8,1)
def H(p): oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x+10,p.y,p.x+10,p.y+15,1); oled.line(p.x,p.y+7,p.x+10,p.y+7,1)
def I(p): oled.line(p.x+5,p.y,p.x+5,p.y+15,1)
def J(p): oled.line(p.x+10,p.y,p.x+10,p.y+15,1); oled.line(p.x,p.y+15,p.x+10,p.y+15,1)
def K(p): oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x,p.y+7,p.x+10,p.y,1); oled.line(p.x,p.y+7,p.x+10,p.y+15,1)
def L(p): oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x,p.y+15,p.x+10,p.y+15,1)
def M(p): oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x+10,p.y,p.x+10,p.y+15,1); oled.line(p.x,p.y,p.x+5,p.y+7,1); oled.line(p.x+5,p.y+7,p.x+10,p.y,1)
def N(p): oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x+10,p.y,p.x+10,p.y+15,1); oled.line(p.x,p.y,p.x+10,p.y+15,1)
def O(p): oled.line(p.x,p.y,p.x+10,p.y,1); oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x+10,p.y,p.x+10,p.y+15,1); oled.line(p.x,p.y+15,p.x+10,p.y+15,1)
def P(p): oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x,p.y,p.x+10,p.y,1); oled.line(p.x+10,p.y,p.x+10,p.y+7,1); oled.line(p.x,p.y+7,p.x+10,p.y+7,1)
def Q(p): O(p); oled.line(p.x+5,p.y+8,p.x+10,p.y+15,1)
def R(p): P(p); oled.line(p.x+5,p.y+7,p.x+10,p.y+15,1)
def S(p): oled.line(p.x+10,p.y,p.x,p.y,1); oled.line(p.x,p.y,p.x,p.y+7,1); oled.line(p.x,p.y+7,p.x+10,p.y+7,1); oled.line(p.x+10,p.y+7,p.x+10,p.y+15,1); oled.line(p.x+10,p.y+15,p.x,p.y+15,1)
def T(p): oled.line(p.x,p.y,p.x+10,p.y,1); oled.line(p.x+5,p.y,p.x+5,p.y+15,1)
def U(p): oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x+10,p.y,p.x+10,p.y+15,1); oled.line(p.x,p.y+15,p.x+10,p.y+15,1)
def V(p): oled.line(p.x,p.y,p.x+5,p.y+15,1); oled.line(p.x+5,p.y+15,p.x+10,p.y,1)
def W(p): oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x+10,p.y,p.x+10,p.y+15,1); oled.line(p.x,p.y+15,p.x+5,p.y+7,1); oled.line(p.x+5,p.y+7,p.x+10,p.y+15,1)
def X(p): oled.line(p.x,p.y,p.x+10,p.y+15,1); oled.line(p.x+10,p.y,p.x,p.y+15,1)
def Y(p): oled.line(p.x,p.y,p.x+5,p.y+7,1); oled.line(p.x+10,p.y,p.x+5,p.y+7,1); oled.line(p.x+5,p.y+7,p.x+5,p.y+15,1)
def Z(p): oled.line(p.x,p.y,p.x+10,p.y,1); oled.line(p.x+10,p.y,p.x,p.y+15,1); oled.line(p.x,p.y+15,p.x+10,p.y+15,1)

# Números 0–9
def zero(p): oled.line(p.x,p.y,p.x+8,p.y,1); oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x+8,p.y,p.x+8,p.y+15,1); oled.line(p.x,p.y+15,p.x+8,p.y+15,1)
def one(p): oled.line(p.x+4,p.y,p.x+4,p.y+15,1)
def two(p): oled.line(p.x,p.y,p.x+8,p.y,1); oled.line(p.x+8,p.y,p.x+8,p.y+7,1); oled.line(p.x+8,p.y+7,p.x,p.y+7,1); oled.line(p.x,p.y+7,p.x,p.y+15,1); oled.line(p.x,p.y+15,p.x+8,p.y+15,1)
def three(p): oled.line(p.x,p.y,p.x+8,p.y,1); oled.line(p.x+8,p.y,p.x+8,p.y+15,1); oled.line(p.x,p.y+7,p.x+8,p.y+7,1); oled.line(p.x,p.y+15,p.x+8,p.y+15,1)
def four(p): oled.line(p.x,p.y,p.x,p.y+7,1); oled.line(p.x,p.y+7,p.x+8,p.y+7,1); oled.line(p.x+8,p.y,p.x+8,p.y+15,1)
def five(p): oled.line(p.x,p.y,p.x+8,p.y,1); oled.line(p.x,p.y,p.x,p.y+7,1); oled.line(p.x,p.y+7,p.x+8,p.y+7,1); oled.line(p.x+8,p.y+7,p.x+8,p.y+15,1); oled.line(p.x,p.y+15,p.x+8,p.y+15,1)
def six(p): oled.line(p.x+8,p.y,p.x,p.y,1); oled.line(p.x,p.y,p.x,p.y+15,1); oled.line(p.x,p.y+7,p.x+8,p.y+7,1); oled.line(p.x+8,p.y+7,p.x+8,p.y+15,1); oled.line(p.x,p.y+15,p.x+8,p.y+15,1)
def seven(p): oled.line(p.x,p.y,p.x+8,p.y,1); oled.line(p.x+8,p.y,p.x,p.y+15,1)
def eight(p): zero(p); oled.line(p.x,p.y+7,p.x+8,p.y+7,1)
def nine(p): oled.line(p.x+8,p.y,p.x+8,p.y+15,1); oled.line(p.x,p.y,p.x+8,p.y,1); oled.line(p.x,p.y,p.x,p.y+7,1); oled.line(p.x,p.y+7,p.x+8,p.y+7,1)

# Símbolos
def period(p): oled.line(p.x+4,p.y+14,p.x+5,p.y+14,1)
def colon(p): oled.line(p.x+4,p.y+4,p.x+5,p.y+4,1); oled.line(p.x+4,p.y+10,p.x+5,p.y+10,1)

# ==== MAPA DE CARACTERES ====
char_map = {
    "A":A,"B":B,"C":C,"D":D,"E":E,"F":F,"G":G,"H":H,"I":I,"J":J,"K":K,"L":L,"M":M,"N":N,
    "O":O,"P":P,"Q":Q,"R":R,"S":S,"T":T,"U":U,"V":V,"W":W,"X":X,"Y":Y,"Z":Z,
    "0":zero,"1":one,"2":two,"3":three,"4":four,"5":five,"6":six,"7":seven,"8":eight,"9":nine,
    ".":period, ":":colon
}

# ==== DISPLAY TEXT ====
def display(text, posArray):
    text = text.upper()
    for i, ch in enumerate(text):
        if i < len(posArray) and ch in char_map:
            char_map[ch](posArray[i])
    oled.show()

# ==== GLOBAL OLED (se define en main) ====
oled = None

