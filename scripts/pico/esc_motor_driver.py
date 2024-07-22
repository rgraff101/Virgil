from machine import Pin, PWM

class MotorDriver:
    def __init__(
        self,
        pwm_pin_id: int,
        pw_stall: int = int(1.25e6), # motor stop pulse width, ns
        pw_fwd_max: int = int(1.8e6), # maximum forward pulse width, ns
        pw_rev_max: int = int(1e6), # maximum reverse pulse width, ns
    ) -> None:
        # Config pin
        self.PWM_PIN = PWM(Pin(pwm_pin_id))
        self.PWM_PIN.freq(50)
        # Properties
        self._pw_stall = pw_stall
        self._pw_rev_max = pw_rev_max
        self._pw_fwd_max = pw_fwd_max
        
    def forward(self, speed=0.):
        """
        Adjust speed in range 0~1
        """
        self.PWM_PIN.duty_ns(int((self._pw_fwd_max - self._pw_stall) * speed) + self._pw_stall)

    def backward(self, speed=0.):
        self.PWM_PIN.duty_ns(self._pw_stall - int((self._pw_stall - self._pw_rev_max) * speed))

    def stop(self):
        self.PWM_PIN.duty_ns(self._pw_stall)
        
# Test
if __name__ == '__main__':
    from time import sleep
    m = MotorDriver(15)
    for sp in range(100):
        m.forward(sp / 100)
        sleep(0.05)
    for sp in reversed(range(100)):
        m.forward(sp / 100)
        sleep(0.05)
    m.stop()