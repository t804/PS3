# coding:UTF-8
# 前進するときはcに正の値を入れ、後退するときは負の値を入れる
# Python3で動かすことを想定しています(inputのところ)

import wiringpi as wp
import sys
import struct

L6470_SPI_CHANNEL = 0

# args = sys.argv
# print(args)
# c = int(args[1])
# print("step count" + args[1])

if wp.wiringPiSPISetup(0, 1000000) < 0:
    print("SPI Setup failed:\n")
if wp.wiringPiSPISetup(1, 1000000) < 0:
    print("SPI Setup failed:\n")


def init():
    # MAX_SPEED設定。
    # レジスタアドレス。
    L6470_write(0x07)
    # 最大回転スピード値(10bit) 初期値は 0x41
    L6470_write(0x00)
    L6470_write(0x21)
    # KVAL_HOLD設定。
    # レジスタアドレス。
    L6470_write(0x09)
    # モータ停止中の電圧設定(8bit)
    L6470_write(0xFF)
    # KVAL_RUN設定。
    # レジスタアドレス。
    L6470_write(0x0A)
    # モータ定速回転中の電圧設定(8bit)
    L6470_write(0xFF)
    # KVAL_ACC設定。
    # レジスタアドレス。
    L6470_write(0x0B)
    # モータ加速中の電圧設定(8bit)
    L6470_write(0xFF)
    # KVAL_DEC設定。
    # レジスタアドレス。
    L6470_write(0x0C)
    # モータ減速中の電圧設定(8bit) 初期値は 0x8A
    L6470_write(0x40)
    # OCD_TH設定。
    # レジスタアドレス。
    L6470_write(0x13)
    # オーバーカレントスレッショルド設定(4bit)
    L6470_write(0x0F)
    # STALL_TH設定。
    # レジスタアドレス。
    L6470_write(0x14)
    # ストール電流スレッショルド設定(4bit)
    L6470_write(0x7F)
    L6470_write(0x02)
    L6470_write(0x00)
    L6470_write(0x17)
    L6470_write(0x00)


def L6470_write(data):
    wp.wiringPiSPIDataRW(L6470_SPI_CHANNEL, struct.pack("B", data))


def L6470_run(speed):
    # 方向検出。
    if speed < 0:
        dir = 0x50
        spd = -1 * speed
    else:
        dir = 0x51
        spd = speed

    # 送信バイトデータ生成。
    spd_h = ((0x0F0000 & spd) >> 16)
    spd_m = ((0x00FF00 & spd) >> 8)
    spd_l = (0x00FF & spd)
    # コマンド（レジスタアドレス）送信。
    L6470_write(dir)
    # データ送信。
    L6470_write(spd_h)
    L6470_write(spd_m)
    L6470_write(spd_l)

def move_both_wheels(left_speed, right_speed):
    global L6470_SPI_CHANNEL
    L6470_SPI_CHANNEL = 0
    # stepからmicrostepに変換
    L6470_run(left_speed)
    L6470_SPI_CHANNEL = 1
    L6470_run(-1*right_speed)

def move_left_wheel(speed):
    global L6470_SPI_CHANNEL
    L6470_SPI_CHANNEL = 0
    L6470_run(speed)

def move_right_wheel(speed):
    global L6470_SPI_CHANNEL
    L6470_SPI_CHANNEL = 1
    L6470_run(-1*speed)

def turn_left_forward(speed):
    global L6470_SPI_CHANNEL
    L6470_SPI_CHANNEL = 1
    L6470_run(-1*speed)
    L6470_SPI_CHANNEL = 0
    L6470_run(speed / 2)

def turn_right_forward(speed):
    global L6470_SPI_CHANNEL
    L6470_SPI_CHANNEL = 0
    L6470_run(speed)
    L6470_SPI_CHANNEL = 1
    L6470_run(-speed / 2)

def multiple_orders(direction, speed):
    global L6470_SPI_CHANNEL
    if direction == 'l':
        L6470_SPI_CHANNEL = 0
        L6470_run(speed)
    elif direction == 'r':
        L6470_SPI_CHANNEL = 1
        L6470_run(-1*speed)
    else:
        print('The direction is wrong.')
    
# L6470の初期化。
#L6470_SPI_CHANNEL = 0
#init()
#L6470_SPI_CHANNEL = 1
#init()
#
#print('both -> b, left -> l, right -> r')
#print('Speed Up -> 1, Speed Down -> 2, Stop -> 3')
#
#left_speed = 0
#right_speed = 0
#change = 2500
#
#while(1):
#    # 第一引数がどちらの車輪を回すか、第二引数がどれだけ回すスピードを変化させるか
#    direction, speed = input().split()
#
#    print('direction:', direction, 'speed:', speed)
#
#    # 両輪動かす
#    if direction == 'b':
#        if speed == '1':
#            left_speed += change
#            right_speed += change
#        elif speed == '2':
#            left_speed -= change
#            right_speed -= change
#        elif speed == '3':
#            left_speed = 0
#            right_speed = 0
#        else:
#            print('Please input the correct speed.')
#        print('left speed:', left_speed, ', right speed:', right_speed)
#        move_both_wheels(left_speed, right_speed)
#
#    # 左輪だけ動かす
#    elif direction == 'l':
#        if speed == '1':
#            left_speed += change
#        elif speed == '2':
#            left_speed -= change
#        elif speed == '3':
#            left_speed = 0
#        else:
#            print('Please input the correct speed.')
#        print('left speed:', left_speed, ', right speed:', right_speed)
#        move_left_wheel(left_speed)
#
#    # 右輪だけ動かす
#    elif direction == 'r':
#        if speed == '1':
#            right_speed += change
#        elif speed == '2':
#            right_speed -= change
#        elif speed == '3':
#            right_speed = 0
#        else:
#            print('Please input the correct speed.')
#        print('left speed:', left_speed, ', right speed:', right_speed)
#        move_right_wheel(right_speed)
#
#    else:
#        print('Please input the correct direction.')

    # if speed == '1':
    #     left_speed += 2500
    # elif speed == '2':
    #     left_speed -= 2500
    # elif speed == '3':
    #     left_speed = 0
    # else:
    #     print('Please input the correct speed.')

    # move_both_wheels(left_speed, left_speed)
    # move_left_wheel(c)
    # move_right_wheel(c)
    # turn_left_forward(c)
    # turn_right_forward(c)

    # L6470_SPI_CHANNEL = 0
    # stepからmicrostepに変換
    # L6470_run(c)
    # L6470_SPI_CHANNEL = 1
    # L6470_run(-1*c)
