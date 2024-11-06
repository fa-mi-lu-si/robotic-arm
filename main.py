import bluetooth
from machine import Pin, PWM, ADC, UART
from time import sleep
from micropython import const
from ble_setup import BLESimplePeripheral

ble = bluetooth.BLE()
bt = BLESimplePeripheral(ble)

# Whenever we read from the bluetooth module
def on_rx(value):
    print(f"RX{value}")
    base.duty_u16(analog_to_pwm_duty_cycle(int(value)))

bt.on_write(on_rx)

base = PWM(Pin("GP1"))
base.freq(50)

led = Pin("LED",Pin.OUT)

# Testing the arms
# base : full range
# bottom : 6000 - 3000
# middle : full
# top : full
# hand : 1670 - 2500 (close - open)

knob = ADC(Pin("GP28", Pin.PULL_UP))

def analog_to_pwm_duty_cycle(analog_value,  pulse_min=500, pulse_max=2500, pwm_frequency=50):
    period = 1_000_000 / pwm_frequency  # Converts Hz to microseconds
    
    # Map the analog value to the pulse width range
    pulse_width = pulse_min + (analog_value / 65535) * (pulse_max - pulse_min)
    
    # Calculate duty cycle
    duty_cycle = (pulse_width / period) * 65535
    
    return int(duty_cycle)

while True:
    knob_val = knob.read_u16()
    # base.duty_u16(analog_to_pwm_duty_cycle(knob_val))
    if bt.is_connected():
        led.on()
    else:
        led.off()
    sleep(0.02)
