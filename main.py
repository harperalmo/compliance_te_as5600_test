"""
as5600_test_01
This is the initial test of the as5600 absolute encoder module controlled as a
slave from an esp32 Huzzah module from Adafruit.
"""

from machine import I2C, Pin
import utime

#fixed id for the as5600. Cannot be changed. Use multiplexer for multiple
#as5600s on same i2c bus. If 2, probably could use the 2 i2c buses in the esp32.
AS5600_ID = 0x36

#Define the pins being used. These will change depending on specific esp32
#package being used. The default pins are:
#       I2C(0)      I2C(1)
#  scl    18          25
#  sda    19          26
SCL_PIN = 22; SCL_FREQ=400000
SDA_PIN = 23
DIR_PIN = 21

#as5600 Registers
ZMCO      = 0x00
ZPOS      = 0x01
MPOS      = 0x_03
MANG      = 0x05
CONF      = 0X07
RAW_ANGLE = 0X0C
ANGLE     = 0X0E
STATUS    = 0X0B
AGC       = 0X1A
MAGNITUDE = 0X1B
BURN      = 0XFF

reg_names = {ZMCO:'ZMCO', ZPOS:'ZPOS', MPOS:'MPOS',MANG:'MANG',CONF:'CONF', \
             RAW_ANGLE:'RAW_ANGLE', ANGLE:'ANGLE', STATUS:'STATUS', AGC:'AGC',   \
             MAGNITUDE:'MAGNITUDE', BURN:'BURN'}             
#Starting location for registers and their size in bytes. 
reg_list = [ (ZMCO,1), (ZPOS,2), (MPOS,2), (MANG,2), (CONF,2), (RAW_ANGLE,2), \
             (ANGLE,2),(STATUS,1), (AGC,1), (MAGNITUDE,2), (BURN, 1)]



def print_registers():
    for reg, size in reg_list:
        vals = i2c0.readfrom_mem(AS5600_ID, reg, size)
        val_str = ""
        for i in vals:
            val_str += f"{i:08b} "
            
        print(f"{reg_names.get(reg)}= \t{val_str}")
        
# print_angles('RAW_ANGLE', raw_vals, 'ANGLE', vals)
def print_angles(n1, word1, n2, word2):

    raw_angle = word1[0] << 8
    raw_angle += word1[1]
    angle = word2[0] << 8
    angle += word2[1]
    
    print(f"{n1}: {raw_angle} | {n2}: {angle}")
    
    
    print(angle)
    

#configuure I2C(0) for use. 
i2c0 = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=SCL_FREQ)

print_registers()
print("\nAngle:")

while True:
    raw_vals = i2c0.readfrom_mem(AS5600_ID, RAW_ANGLE, 2)
    vals = i2c0.readfrom_mem(AS5600_ID, ANGLE, 2)
    print_angles('RAW_ANGLE', raw_vals, 'ANGLE', vals)
    utime.sleep_ms(500)
    

