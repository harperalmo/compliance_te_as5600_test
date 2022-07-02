"""
as5600_test_01
This is the initial test of the as5600 absolute encoder module controlled as a
slave from an esp32 Huzzah module from Adafruit.

Seems very nice when tested with wooden support holding magnet on stick. The
magnet (N52) can be 0 to ~2mm away and get consistent readings. Is it possible
that the stepper motor will affect this when it moves?
TO DO: Test stepper motor environment.
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

reg_sizes = {ZMCO:1, ZPOS:2, MPOS:2,MANG:2,CONF:2, \
             RAW_ANGLE:2, ANGLE:2, STATUS:1, AGC:1,   \
             MAGNITUDE:2, BURN:1}
#Starting location for registers and their size in bytes. 
reg_list = [ (ZMCO,1), (ZPOS,2), (MPOS,2), (MANG,2), (CONF,2), (RAW_ANGLE,2), \
             (ANGLE,2),(STATUS,1), (AGC,1), (MAGNITUDE,2), (BURN, 1)]

CLICK_DELTA_ANGLE = 0.08789063
start_angle_deg = 0


def write_reg( id, register, value):
    i2c0.writeto_mem(id, register, value)
    
def print_reg(reg):
    vals = i2c0.readfrom_mem(AS5600_ID, reg, reg_sizes.get(reg))
    val_str = ""
    for i in vals:
        val_str += f"{i:08b} "
    print(f"{reg_names.get(reg)}= \t{val_str}")
    

def print_registers():
    for reg, size in reg_list:
        #print(f"reading {reg}, which is size {size}")
        vals = i2c0.readfrom_mem(AS5600_ID, reg, size)
        val_str = ""
        for i in vals:
            val_str += f"{i:08b} "
            
        print(f"{reg_names.get(reg)}= \t\t{val_str}")


def clicks_to_deg_angle( clicks ):
    return clicks*CLICK_DELTA_ANGLE


# print_angles('RAW_ANGLE', raw_vals, 'ANGLE', vals)
def print_angles(n1, word1, n2, word2):

    raw_angle = word1[0] << 8
    raw_angle += word1[1]
    raw_angle_degree = clicks_to_deg_angle( raw_angle )
    raw_final = raw_angle_degree - start_angle_deg
    if raw_final < 0:
        raw_final += 360.0
        
    angle = word2[0] << 8
    angle += word2[1]
    angle_degree = clicks_to_deg_angle( angle )
    final = angle_degree - start_angle_deg
    if final < 0:
        final += 360.0
    
    print(f"{n1}: {raw_final} | {n2}: {final}")  

def adjust_angle():
    print("\n\nReset initial angle position:")

    print("Changing zpos to raw angle...")
    vals = i2c0.readfrom_mem(AS5600_ID, RAW_ANGLE, reg_sizes.get(RAW_ANGLE))
    write_reg(AS5600_ID, ZPOS, vals)


def initialize_angle_pos():
    print('\n initialization vals')
    init_val = b'\x00\x00'
    write_reg(AS5600_ID, ZPOS, init_val)
    write_reg(AS5600_ID, MPOS, init_val)
    
def calc_starting_angle():
    global start_angle_deg
    
    raw_angle_bytes =     vals = i2c0.readfrom_mem(AS5600_ID, RAW_ANGLE, reg_sizes.get(RAW_ANGLE))
    msb = raw_angle_bytes[0] << 8
    lsb = raw_angle_bytes[1]
    raw_angle = msb+lsb
    start_angle_deg = raw_angle * CLICK_DELTA_ANGLE #360/4096
    
#configure I2C(0) for use. 
i2c0 = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=SCL_FREQ)

print('Wake Up vals')
print_registers()
calc_starting_angle()


#initialize_angle_pos(); print_registers()

utime.sleep_ms(200)
#adjust_angle()
utime.sleep_ms(200)
print_registers()

     
print("\n\nAngle:")

while True:
    raw_vals = i2c0.readfrom_mem(AS5600_ID, RAW_ANGLE, 2)
    vals = i2c0.readfrom_mem(AS5600_ID, ANGLE, 2)
    print_angles('RAW_ANGLE', raw_vals, 'ANGLE', vals)
    utime.sleep_ms(500)
    

