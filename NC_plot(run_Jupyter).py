%matplotlib inline
import matplotlib.pyplot as plt
from ipywidgets import interact
import numpy as np
import math

from IPython.core.display import display, HTML
display(HTML("<style>div.output_scroll { height: unset; }</style>"))

# 変数定義
now_V = 0
now_H = 0
i = 0
j = 0
index = 0
TKSK_flag = False
V_array = np.array([])
H_array = np.array([])

Process_output = True # 処理文の出力(Trueなら表示、Falseなら非表示)

if Process_output == True:
    print("--------コヅメ当たり面0合わせ--------")

DIC1 = 186.9 #D7→ デフォルト値
# DIC1 = 179.9 #D8 → DIC1 = DIA1の値(例外処理の適用チェック)
DIA1 = 179.9 #D8 
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
    global V_array
    global H_array
    global index
    now_V = v
    index += 1
    
    if Process_output == True:
        print(str(index) + ".", end='')
        print("V = " + str(v) + "(" + str(v/2) + ")：", end='')
        print("(V=" + str(now_V) + ",H=" + str(now_H) + ")")

    V_array = np.append(V_array , now_V/2)
    H_array = np.append(H_array , now_H)

def H(h):
    global now_H
    global V_array
    global H_array
    global index
    now_H = h
    index += 1
    
    if Process_output == True:
        print(str(index) + ".", end='')
        print("H = " + str(h) + "：", end='')
        print("(V=" + str(now_V) + ",H=" + str(now_H) + ")")

    V_array = np.append(V_array , now_V/2)
    H_array = np.append(H_array , now_H)

def V_relpos(vr):
    global now_V
    half_vr = vr / 2
    now_V = (now_V / 2) + half_vr
    return now_V * 2

def slope(v, h):
    global index
    global now_V
    global now_H
    now_V = v
    now_H = h
    index += 1
    
    if Process_output == True:
        print(str(index) + ".", end='')
        print("斜めの値：V = " + str(v) + "(" + str(v/2) + ")" + ", H = " + str(h) + "：", end='')
        print("(V=" + str(now_V) + ",H=" + str(now_H) + ")")
    
    global V_array
    global H_array
    V_array = np.append(V_array , v/2)
    H_array = np.append(H_array , h)


# 加工処理
V(500)
H(200)

if Process_output == True:
    print("--------加工準備--------")

H(DIA3 + 3)
V(DIC1)
DIA9 = DIA1
DIB1 = DIA4

if Process_output == True:
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
        if Process_output == True:
            print("--------特殊形状粗ループ加工：DIC1 = DIA1のため終了--------")
        break
    i += 1
    if Process_output == True:
        print("--------特殊形状粗ループ加工：" + str(i) + "回目--------")
    DIC6 = DIC6 - DIB8
    # print("DIC6 = " + str(DIC6))
    if DIC6 <= DIA1:
        if Process_output == True:
            print("--------特殊形状粗ループ加工：DIC6 < DIA1のため終了--------")
        break
    else:
        V(V_relpos(DIB8 * -1))
    
        H(DIA7 + 0.3)

        V(V_relpos(DIB8))

        H(DIA3 + 3)

        V(V_relpos(DIB8 * -1))


    if DIC6 < (DIA1 + DIB8):
        if Process_output == True:
            print("--------特殊形状粗ループ加工：繰り返し終了--------")
        break

# DIC6 = DIA1 # DIC6 = DIA1の値(例外処理の適用チェック)

if not(DIC6 == DIA1):
    TKSK_flag = True
    if Process_output == True:
        print("--------特殊形状仕上げ加工--------")

    V(DIA1)
    H(DIA7 + 0.3)

    slope(DIA1 + DIB8, DIA3 + 3)

if TKSK_flag == False:
    if Process_output == True:
        print("--------DIC6 = DIA1のため、特殊形状仕上げ加工なし--------")


while 1:
    j += 1
    if Process_output == True:
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
        if Process_output == True:
            print("--------テーパー部粗ループ加工：繰り返し終了--------")
        break

if Process_output == True:
    print("--------テーパー部仕上げ加工--------")

V(DIA2 - 6)
H(DIA3 + 2)

slope(DIA2, DIA3 - 1)
H(DIA3 - DIA5)
slope(DIA1, DIA7)
V(DIC1 + 2)

if Process_output == True:
    print("--------エンド--------")

V(500)
H(200)


V_plot_array = np.array([])
H_plot_array = np.array([])

@interact(n = (1, len(V_array)), m = (1, len(V_array)))
def NC_plot(n, m):
    global V_plot_array
    global H_plot_array
    i = 0
    j = 0
    array_size = m - n
    
    V_plot_array = np.empty(0)
    H_plot_array = np.empty(0)
    
    for i in range(n-1, m+1):
        for j in range(n-1, i):
            V_plot_array = np.append(V_plot_array , V_array[j])
            H_plot_array = np.append(H_plot_array , H_array[j])
            
#     plt.plot(H_plot_array, V_plot_array, marker='.', markerfacecolor="r", markeredgecolor="r", markersize=12) # 線描画あり(可変グラフ)
    plt.plot(H_plot_array, V_plot_array, '.', markerfacecolor="r", markeredgecolor="r", markersize=12) # 線描画なし(可変グラフ)

# plt.plot(H_array, V_array, marker='.', markerfacecolor="r", markeredgecolor="r", markersize=12) # 線描画あり(全体グラフ)
plt.plot(H_array, V_array, '.', markerfacecolor="r", markeredgecolor="r", markersize=12) # 線描画なし(全体グラフ)

# print("V = " + str(V_array))
# print("H = " + str(H_array))