#MPU6050 Setup

#MPU_Init and read_raw_data functions courtesy of 

#http://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-piimport smbus

#System Management
import smbus
#Chip and Register Setup
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H =0x47

bus = smbus.SMBus(1) #I2C port 1
Device_Address = 0x68 #MPU6050 device address

#Initializes MPU so it can send data to PI for processing at runtime
def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    #Write Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)

    #Write to Configuration Register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    #ACcelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)

    #concatenate higher and lower value
    value = ((high << 8) | low)

    #to get signed value from mpu6050
    if(value> 32768):
        value = value - 65536
    return value



#Initializes MPU at Runtime
MPU_Init()


# returns x angular velocity in degrees per second    
def getGx():
    
    
    return read_raw_data(GYRO_XOUT_H)/131.0

# returns y angular velocity in degrees per second    
def getGy():
    
    
    return read_raw_data(GYRO_YOUT_H)/131.0

# returns z angular velocity in degrees per second
def getGz():
    
   
    
    return read_raw_data(GYRO_ZOUT_H)/131.0

# returns x acceleration in G-Force (g)
def getAx():
    
    
    return read_raw_data(ACCEL_XOUT_H)/16384.0


# returns y acceleration in G-Force (g)
def getAy():
    
    
    return read_raw_data(ACCEL_YOUT_H)/16384.0

# returns z acceleration in G-Force (g)
def getAz():
    
    
    return read_raw_data(ACCEL_ZOUT_H)/16384.0
