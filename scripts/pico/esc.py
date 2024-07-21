from machine import Pin, PWM

class MotorDriver:
    def __init__(
        self,
        pwm_pin_id: int,
        pw_stall: int, # motor stop pulse width, ns
        pw_rev_max: int, # maximum reverse pulse width, ns
        pw_fwd_max: int, # maximum forward pulse width, ns
    ) -> None:
        # Config pin
        self.PWM_PIN = PWM(Pin(pwm_pin_id))
        self.PWM_PIN.freq(50)
        # Properties
        self._pw_stall = pw_stall
        self._pw_rev_max = pw_rev_max
        self._pw_fwd_max = pw_fwd_max
        
    def forward(self):
        pass

    def backward(self):
        pass

    def stop(self):
        self.PWM_PIN.duty_ns(self._pw_stall)
        