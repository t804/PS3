# coding:UTF-8
import  Adafruit_PCA9685
import time
import sys

#サーボモーターをコントロールするためのクラス
class servo_Class:
    #ChannelはPCA9685のサーボモーターを繋いだチャンネル
    #ZeroOffsetはサーボモーターの基準の位置を調節するためのパラメーターです
    def __init__(self, Channel, ZeroOffset):
        self.Channel = Channel
        self.ZeroOffset = ZeroOffset

        #Adafruit_PCA9685の初期化
        self.pwm = Adafruit_PCA9685.PCA9685(address=0x40)
        self.pwm.set_pwm_freq(60)
    """角度を設定する関数です"""
    def SetPos(self,pos):
        #pulse = 150～650 : 0 ～ 180度
        #PCA9685はパルスで角度を制御しているため0~180のように角度を指定しても思った角度にはなりません
        #そこで角度の値からパルスの値へと変換します。PCA9685ではパルス150~650が角度の0~180に対応しているみたいです
        #下の式の(650-150)/180は1度あたりのパルスを表しています
        #それにpos(制御したい角度)を掛けた後、150を足すことでことで角度をパルスに直しています。
        #最後にZeroOffsetを足すことで基準にしたい位置に補正します
        pulse = (650-150)/180*pos+150+self.ZeroOffset
        pulse=int(pulse)
        self.pwm.set_pwm(self.Channel, 0,pulse)

def SetUpWing():
    rightWing = servo_Class(Channel=0, ZeroOffset=-5)
    leftWing = servo_Class(Channel=2, ZeroOffset=-5)
    return rightWing, leftWing

def SetUpFly():
    rightFly = servo_Class(Channel=1, ZeroOffset=-5)
    leftFly = servo_Class(Channel=3,ZeroOffset=-5)
    return rightFly, leftFly

def SetUpTail():
    tail = servo_Class(Channel=4,ZeroOffset=-5)
    return tail

def SetUpNeck():
    neck = servo_Class(Channel=5,ZeroOffset=-5)
    return neck

def FlyAway():
    """
    翼を動かす
    """
    global loop
    loop = True
    rightWing , leftWing = SetUpWing()
    rightFly , leftFly = SetUpFly()
    rightWing.SetPos(0)
    leftWing.SetPos(180)
    time.sleep(1)
    rightWing.SetPos(180)
    leftWing.SetPos(0)
    time.sleep(1)
    while loop:
    	rightFly.SetPos(0)
        leftFly.SetPos(180)
	time.sleep(0.7)
	rightFly.SetPos(180)
        leftFly.SetPos(0)
        time.sleep(0.7)

def Tail():
    global loop
    loop = True
    tail = SetUpTail()
    try:
       while loop:
             tail.SetPos(90)
             time.sleep(0.3)
             tail.SetPos(160)
             time.sleep(0.3)
    except KeyboardInterrupt :         #Ctl+Cが押されたらループを終了
             print("\nCtl+C")
    except Exception as e:
             print(str(e))

def Neck():
    neck = SetUpNeck()
    neck.SetPos(180)
    time.sleep(2)
    neck.SetPos(100)
    time.sleep(1)

def stop():
    global loop
    loop = False

"""制御を行うメインの部分です"""
if __name__ == '__main__':
    #今回はサーボモーターが3つあります
    args = sys.argv

    if args[1]=='F':
        FlyAway()
    elif args[1]=='T':
        Tail()
    elif args[1]=='N':
	Neck()
    else:
        stop()
