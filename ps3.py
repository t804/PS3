#coding: utf-8
import struct
import logging
import lib.new_motor_speed as motor

device_path = "/dev/input/js0"

debug = 2

# unsigned long, short, unsigned char, unsigned char
EVENT_FORMAT = "LhBB"
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

'''
action

'''

def parse_event(event):
  (time, val, action_type, action_num) = struct.unpack(EVENT_FORMAT, event)
  action = ""
  # TODO: 要調査
  if action_num == 13 and val==1:
    # ○ボタン押す
    action = "forward"
  elif action_num == 13 and val==0:
    # ○ボタン離す
    action = "stop"
  elif action_type==2 and action_num == 0:
    action = "rotate"

  if debug==1:
    print("action {0} time: {1}, val: {2}, type: {3}, num: {4}"
          .format(action, time, val, action_type, action_num))
  return (action, time, val, action_type, action_num)

def convert_theta(controller_value):
  # raw value
  return controller_value

def step_action(action, action_value, state, state_value):
  '''
  Finite-State Automaton
  '''
  if action == "forward" and state == "stopped":
    state = "forward"
    state_value = convert_theta(0)
  elif action == "stop" and state == "forward":
    state = "stopping"  # stoppingを追加する
  elif state == "stopping":
    state = "stopped"
  elif action == "stop" and state == "stopped":
    pass  ## unreachable except for initial state
  elif action == "rotate" and state == "forward":
    state = "forward"
    state_value = convert_theta(action_value)
  elif debug and action:
    print("UNKNOWN ACTION: {0}, STATE: {1}".format(action, state))
  return (state, state_value)

def direction2speed(direction_value, default_speed = 7000):
  MAX_VAL = 32767  # assume right-most value
  MIN_VAL = -32767  # assume left-most value
  if direction_value == 0:
    return (default_speed, default_speed)

  if direction_value<MIN_VAL or MAX_VAL<direction_value:
    raise "ERROR: "

  left_bias = 0.
  right_bias = 0.
  if direction_value>0:
    right_bias = 0.5 + 0.5 * (direction_value / MAX_VAL)
    left_bias = 1. - right_bias
  elif direction_value<0:
    left_bias = 0.5 + 0.5 * (direction_value / MIN_VAL)
    right_bias = 1. - left_bias

  if debug==2:
    print("left_bias: {0}, right_bias: {1}".format(left_bias, right_bias))
  return (int(default_speed * left_bias),
          int(default_speed * right_bias))


def execute_action(state, state_value):
  if state == "forward":
      (left_speed, right_speed) = direction2speed(state_value)
      motor.move_both_wheels(left_speed, right_speed)
  if state == "stopped":
      motor.move_both_wheels(0, 0)

def routine(event, state, state_value):
  if event:
    (action, time, val, action_type, action_num) = parse_event(event)
  (state, state_value) = step_action(action, val, state, state_value)

  execute_action(state, state_value)
  return (state, state_value)

def main():
  motor.init()
  try:
    with open(device_path, "rb") as device:
      action = ""
      state = "stopped"
      state_value = 0
      while True:
        event = device.read(EVENT_SIZE)
        (state, state_value) = routine(event, state, state_value)
  except Exception as e:
    motor.move_both_wheels(0,0)
    logging.exception(e)

if __name__ == "__main__":
  main()


