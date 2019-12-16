#!/usr/bin/env python
#encoding: utf8
import rospy, os, socket
import new_motor_speed
import servo_motor
import time

class JuliusReceiver:
	def __init__(self):
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			try:
				self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.sock.connect(("localhost", 10500))
				break
			except:
				rate.sleep()

		rospy.on_shutdown(self.sock.close)

	def get_line(self):
		line = ""
		while not rospy.is_shutdown():
			v = self.sock.recv(1)
			if v == '\n':
				return line
			line += v

	def get_command(self, th):
		line = self.get_line()

		if "WHYPO" not in line:
			return None

		score_str = line.split('CM="')[-1].split('"')[0]
		if float(score_str) < th:
			return None

		command = None
		if "左に曲がれ" in line:command = "left"
		elif "右に曲がれ" in line:command = "rigth"
		elif "前に進め" in line:command = "forward"
		elif "後ろに進め" in line:command = "back"
		elif "止まれ" in line:command = "stop"
		elif "こんにちは" in line:command = "hello"

		return command

if __name__ == '__main__':
	rospy.init_node("voice_to_command")
	j = JuliusReceiver()
	while not rospy.is_shutdown():
		new_motor_speed.init()
		com = j.get_command(0.999)
		if com != None:
			print com
			if com == "left":new_motor_speed.move_left_wheel(7500)
			elif com == "right":new_motor_speed.turn_right_forward(7500)
			elif com == "forward":
				new_motor_speed.move_both_wheels(-7500,-7500)
				servo_motor.FlyAway()
			elif com == "back":new_motor_speed.move_both_wheels(7500,7500)
			elif com == "stop":
				new_motor_speed.move_both_wheels(0,0)
				servo_motor.stop()
			elif com == "hello":
				servo_motor.Neck()
