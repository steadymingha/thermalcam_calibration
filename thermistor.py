import board
import time
import busio
import math
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Constants
R_FIXED = 10000      # Fixed resistor in ohms
BETA = 3950          # Beta parameter of thermistor
T0 = 298.15          # 25°C in Kelvin
R0 = 10000           # Thermistor resistance at 25°C
VCC = 3.3            # Supply voltage (measured if possible)

# # Constants
# R_FIXED = 10000      # Fixed resistor in ohms
# BETA = 3435         # Beta parameter of thermistor
# T0 = 298.15          # 25°C in Kelvin
# R0 = 10000           # Thermistor resistance at 25°C
# VCC = 3.3           # Supply voltage (measured if possible)

class Thermistor:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)

        # Initialize all ADS1115 modules
        ads_modules = [
            ADS.ADS1115(i2c, address=0x48),
            ADS.ADS1115(i2c, address=0x49),
            ADS.ADS1115(i2c, address=0x4A)
        ]

        # Configure all modules
        for ads in ads_modules:
            ads.gain = 1
            ads.data_rate = 128#860

        # Define all active thermistor channels
        self.channels = []
        for index, ads in enumerate(ads_modules):
            if ads.i2c_device.device_address == 0x4A:
                # Only A0 used on 0x4A
                self.channels.append((f"{hex(ads.i2c_device.device_address)}-CH0", AnalogIn(ads, ADS.P0)))
                self.channels.append((f"{hex(ads.i2c_device.device_address)}-CH1", AnalogIn(ads, ADS.P1)))
            else:
                # A0~A3 used on 0x48, 0x49
                for ch in range(4):
                    self.channels.append((f"{hex(ads.i2c_device.device_address)}-CH{ch}", AnalogIn(ads, ch)))

    def read(self):
        temp_out = []
        for label, ch in self.channels:
            voltage = ch.voltage

            if 0.01 < voltage < VCC:
                resistance = R_FIXED * (VCC / voltage - 1)

                if resistance > 0:
                    temp_k = 1 / (1/T0 + (1/BETA) * math.log(resistance / R0))
                    temp_c = temp_k - 273.15
                    temp_c = 1.15 * temp_c - 3.665  # 보정 적용    

                    temp_out.append(round(temp_c,1))
        return temp_out


def main():
# Initialize I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Initialize all ADS1115 modules
    ads_modules = [
        ADS.ADS1115(i2c, address=0x48),
        ADS.ADS1115(i2c, address=0x49),
        ADS.ADS1115(i2c, address=0x4A)
    ]

    # Configure all modules
    for ads in ads_modules:
        ads.gain = 1
        ads.data_rate = 128#860

    # Define all active thermistor channels
    channels = []
    for index, ads in enumerate(ads_modules):
        if ads.i2c_device.device_address == 0x4A:
            # Only A0 used on 0x4A
            channels.append((f"{hex(ads.i2c_device.device_address)}-CH0", AnalogIn(ads, ADS.P0)))
            channels.append((f"{hex(ads.i2c_device.device_address)}-CH1", AnalogIn(ads, ADS.P1)))
        else:
            # A0~A3 used on 0x48, 0x49
            for ch in range(4):
                channels.append((f"{hex(ads.i2c_device.device_address)}-CH{ch}", AnalogIn(ads, ch)))

    while True:
        for label, ch in channels:
            voltage = ch.voltage

            if 0.01 < voltage < VCC:
                resistance = R_FIXED * (VCC / voltage - 1)

                if resistance > 0:
                    temp_k = 1 / (1/T0 + (1/BETA) * math.log(resistance / R0))
                    temp_c = temp_k - 273.15
                    temp_c = 1.15 * temp_c - 3.665  # 보정 적용    
                    # temp_c = 1.2 * temp_c - 3.665  # 보정 적용    

                    print(f"{label} - Voltage: {voltage:.3f} V, Resistance: {resistance:.1f} Ω, Temp: {temp_c:.2f} °C")
                else:
                    print(f"{label} - Invalid resistance")
            else:
                print(f"{label} - Voltage out of range")

        print("---")
        time.sleep(1)

def thermistor_init():
    i2c = busio.I2C(board.SCL, board.SDA)

    # Initialize all ADS1115 modules
    ads_modules = [
        ADS.ADS1115(i2c, address=0x48),
        ADS.ADS1115(i2c, address=0x49),
        ADS.ADS1115(i2c, address=0x4A)
    ]

    # Configure all modules
    for ads in ads_modules:
        ads.gain = 1
        ads.data_rate = 128#860

    # Define all active thermistor channels
    channels = []
    for index, ads in enumerate(ads_modules):
        if ads.i2c_device.device_address == 0x4A:
            # Only A0 used on 0x4A
            channels.append((f"{hex(ads.i2c_device.device_address)}-CH0", AnalogIn(ads, ADS.P0)))
            channels.append((f"{hex(ads.i2c_device.device_address)}-CH1", AnalogIn(ads, ADS.P1)))
        else:
            # A0~A3 used on 0x48, 0x49
            for ch in range(4):
                channels.append((f"{hex(ads.i2c_device.device_address)}-CH{ch}", AnalogIn(ads, ch)))

    return ads, channels
    
def thermistor():
    i2c = busio.I2C(board.SCL, board.SDA)

    # Initialize all ADS1115 modules
    ads_modules = [
        ADS.ADS1115(i2c, address=0x48),
        ADS.ADS1115(i2c, address=0x49),
        ADS.ADS1115(i2c, address=0x4A)
    ]

    # Configure all modules
    for ads in ads_modules:
        ads.gain = 1
        ads.data_rate = 128#860

    # Define all active thermistor channels
    channels = []
    for index, ads in enumerate(ads_modules):
        if ads.i2c_device.device_address == 0x4A:
            # Only A0 used on 0x4A
            channels.append((f"{hex(ads.i2c_device.device_address)}-CH0", AnalogIn(ads, ADS.P0)))
            channels.append((f"{hex(ads.i2c_device.device_address)}-CH1", AnalogIn(ads, ADS.P1)))
        else:
            # A0~A3 used on 0x48, 0x49
            for ch in range(4):
                channels.append((f"{hex(ads.i2c_device.device_address)}-CH{ch}", AnalogIn(ads, ch)))

    while True:
        temp_out = []
        for label, ch in channels:
            voltage = ch.voltage

            if 0.01 < voltage < VCC:
                resistance = R_FIXED * (VCC / voltage - 1)

                if resistance > 0:
                    temp_k = 1 / (1/T0 + (1/BETA) * math.log(resistance / R0))
                    temp_c = temp_k - 273.15
                    temp_c = 1.15 * temp_c - 3.665  # 보정 적용    

                    # print(f"{label} - Voltage: {voltage:.3f} V, Resistance: {resistance:.1f} Ω, Temp: {temp_c:.2f} °C")
                    temp_out.append(temp_c)
                else:
                    print(f"{label} - Invalid resistance")
            else:
                print(f"{label} - Voltage out of range")

        print("---")
        time.sleep(1)


if __name__ == "__main__":
    main()
    # thermistor()