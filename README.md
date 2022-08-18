# pwm_fan_control
Raspberry Pi hardware PWM fan control using rpi_hardware_pwm. Uses few resources and allows 25kHz PWM frequency. By default fan will start at 30% and scale linearly between MIN_TEMP and MAX_TEMP which are 50 and 70C by default. Once below IDLE_TEMP it will remain at 30%. Fan goes to 100% if exited. You may want to configure this to start on boot as a service or via cron.

Configure PWM channels by adding `dtoverlay=pwm-2chan` to `/boot/config.txt`

Install rpi-hardware-pwm library: `sudo pip3 install rpi-hardware-pwm`

`GPIO18` will become `PWM0` for controlling the fan speed. 

Credits:
- Hardware PWM implementation https://github.com/Pioreactor/rpi_hardware_pwm
- Fan control code https://github.com/DriftKingTW/Raspberry-Pi-PWM-Fan-Control
