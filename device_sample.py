import struct

device_path = "/dev/input/js0"

# unsigned long, short, unsigned char, unsigned char
EVENT_FORMAT = "LhBB";
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

with open(device_path, "rb") as device:
  event = device.read(EVENT_SIZE)
  while event:
    (ds3_time, ds3_val, ds3_type, ds3_num) = struct.unpack(EVENT_FORMAT, event)
    #if -1000<ds3_val and ds3_val<1000:
    if ds3_type==2 and ds3_num in (4,5,6):
      # gyrosensor
      pass
    elif ds3_type==2 and ds3_num==1:
      # left stick, vertical move
      pass
    else: 
      print( "time: {0}, value: {1}, type: {2}, number: {3}".format( ds3_time, ds3_val, ds3_type, ds3_num ) )
    
    event = device.read(EVENT_SIZE)
