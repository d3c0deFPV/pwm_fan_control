#! /usr/bin/env python3
import time
import signal
import sys
import logging
from rpi_hardware_pwm import HardwarePWM

# Credits:
# Hardware PWM implementation https://github.com/Pioreactor/rpi_hardware_pwm
# Fan control code https://github.com/DriftKingTW/Raspberry-Pi-PWM-Fan-Control

PWM_FREQ = 25000        # [Hz] PWM frequency
WAIT_TIME = 5           # [s] Time to wait between each refresh
IDLE_TEMP = 40          # [°C] Temperature below which to stop the fan
MIN_TEMP = 50           # [°C] Temperature above which to start inreasing fan speed
MAX_TEMP = 70           # [°C] Temperature at which to operate at max fan speed
FAN_LOW = 30            # [%] Lowest speed to spin fan
FAN_HIGH = 100          # [%] Max speed to spin fan
FAN_IDLE = 30           # [%] Set this to zero to stop fan completely. Keep this lower or equal to FAN_LOW
FAN_GAIN = float(FAN_HIGH - FAN_LOW) / float(MAX_TEMP - MIN_TEMP)

pwm = HardwarePWM(pwm_channel=0, hz=60) # GPIO 18 using pwm-2chan becomes pwm 0
logging.basicConfig(stream=sys.stderr, level=logging.ERROR) # Set level to debug for stderr output

def getCpuTemperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return float(f.read()) / 1000

def handleFanSpeed(temperature):
    if temperature > MIN_TEMP:
        delta = min(temperature, MAX_TEMP) - MIN_TEMP
        duty_cycle = FAN_LOW + delta * FAN_GAIN
        pwm.change_duty_cycle(duty_cycle)

    elif temperature < IDLE_TEMP:
        duty_cycle = FAN_IDLE
        pwm.change_duty_cycle(duty_cycle)
    else:
        duty_cycle = "unchanged"
    return duty_cycle

try:
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    pwm.change_frequency(PWM_FREQ)
    pwm.start(FAN_LOW) # Start fan at lowest speed
    current_fan_speed = FAN_LOW
    while True:
        current_temperature = getCpuTemperature()
        new_fan_speed = handleFanSpeed(current_temperature)
        if new_fan_speed != "unchanged":
            current_fan_speed = new_fan_speed
        logging.debug("Temp:" + str(current_temperature))
        logging.debug("Fan speed: " + str(current_fan_speed))
        time.sleep(WAIT_TIME)

except KeyboardInterrupt:
    logging.debug("Keyboard Interrupt")
    pass

finally:
    logging.debug("Exiting. Setting fan to high")
    pwm.change_duty_cycle(FAN_HIGH)

