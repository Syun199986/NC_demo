# 変数定義
now_V = 0
now_H = 0
i = 0
j = 0
TKSK_flag = False

print("--------コヅメ当たり面0合わせ--------")

DIC1 = 186.9 #D7
DIA1 = 179.9 #D8 → デフォルト値
# DIA1 = 179.9 #D8 → DIC1 = DIA1の値(例外処理の適用チェック)
DIA2 = 151.1 #D9
DIA3 = 40.0 #D10
DIA4 = 14.450 #D11
DIA5 = 16.0 #D12
DIA6 = 35.0 #D13
DIB2 = 0.7 #D14
DIB8 = 3.0 #D15
DIB4 = 1.5 #D16


# 関数定義
def V(v):
    global now_V
    now_V = v
    print("V = " + str(v) + "(" + str(v/2) + ")")

def H(h):
    global now_H
    now_H = h
    print("H = " + str(h))

def V_relpos(vr):
    global now_V
    half_vr = vr / 2
    now_V = (now_V / 2) + half_vr
    return now_V * 2

def slope(v, h):
    print("斜めの値：V = " + str(v) + "(" + str(v/2) + ")" + ", H = " + str(h))


# 加工処理
V(500)
H(200)

print("--------加工準備--------")

H(DIA3 + 3)
V(DIC1)
DIA9 = DIA1
DIB1 = DIA4

print("--------外径舐め加工--------")

DIB3 = DIA4 * DIB2
DIA7 = DIA3 - DIA5 - DIB3 # DIA7 → SYABU END ICHI Z
H(DIA7 + 0.3) # SYABU END ICHI Z + 0.3

V(V_relpos(DIB8))

H(DIA3 + 3)
V(DIC1)

DIC6 = DIC1

while 1:
    if DIC1 == DIA1:
        print("--------特殊形状粗ループ加工：DIC1 = DIA1のため終了--------")
        break
    i += 1
    print("--------特殊形状粗ループ加工：" + str(i) + "回目--------")
    DIC6 = DIC6 - DIB8
    # print("DIC6 = " + str(DIC6))
    if DIC6 <= DIA1:
        print("--------特殊形状粗ループ加工：DIC6 < DIA1のため終了--------")
        break
    else:
        V(V_relpos(DIB8 * -1))
    
        H(DIA7 + 0.3)

        V(V_relpos(DIB8))

        H(DIA3 + 3)

        V(V_relpos(DIB8 * -1))


    if DIC6 < (DIA1 + DIB8):
        print("--------特殊形状粗ループ加工：繰り返し終了--------")
        break

# DIC6 = DIA1 # DIC6 = DIA1の値(例外処理の適用チェック)

if not(DIC6 == DIA1):
    TKSK_flag = True
    print("--------特殊形状仕上げ加工--------")

    V(DIA1)
    H(DIA7 + 0.3)

    slope(DIA1 + DIB8, DIA3 + 3)

if TKSK_flag == False:
    print("--------DIC6 = DIA1のため、特殊形状仕上げ加工なし--------")


while 1:
    j += 1
    print("--------テーパー部粗ループ加工：" + str(j) + "回目--------")

    DIA9 = DIA9 - DIB8
    DIB1 = DIB1 - DIB4

    DIB5 = DIB1 * DIB2
    V(DIA9)
    H(DIA3 + 3)

    H(DIA3 - DIA5 - DIB5 + 0.3)

    V(V_relpos(DIB8))

    H(DIA3 + 3)

    if DIA9 < (DIA2 + DIB8):
        print("--------テーパー部粗ループ加工：繰り返し終了--------")
        break

print("--------テーパー部仕上げ加工--------")

V(DIA2 - 6)
H(DIA3 + 2)

slope(DIA2, DIA3 - 1)
H(DIA3 - DIA5)
slope(DIA1, DIA7)
V(DIC1 + 2)

print("--------エンド--------")

V(500)
H(200)