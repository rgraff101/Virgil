from machine import Pin, PWM

class Steering:
    def __init__(
        self,
        pwm_pin_id: int, # GPIO id on pico
        pw_center: int = int(1.5e6), # servo center pulse width, ns
        pw_range: int = int(5e5), # pwm range from center to limit, ns
    ) -> None:
        # Properties
        self._pw_center = pw_center
        self._pw_range = pw_range
        self._pw_ang_min = pw_center - pw_range
        self._pw_ang_max = pw_center + pw_range
        # Config pin
        self.PWM_PIN = PWM(Pin(pwm_pin_id))
        self.PWM_PIN.freq(50)
        self.center()
        
    def set(self, value: float = 0.):
        """
        Set steering's value in range: [-1, 1].
        """
        d_ns = self._pw_ang_min + int(self._pw_range * (value + 1))
        self.PWM_PIN.duty_ns(d_ns)
        # print(f"pulse width: {d_ns}")

    def center(self):
        self.PWM_PIN.duty_ns(self._pw_center)
        # print("CENTERING")
        
# Test
if __name__ == '__main__':
    from time import sleep
    s = Steering(16)
    for sp in range(0, 100, 5):
        s.set(sp / 100)
        sleep(0.05)
    for sp in reversed(range(0, 100, 5)):
        s.set(sp / 100)
        sleep(0.05)
    for sp in range(0, 100, 5):
        s.set(-sp / 100)
        sleep(0.05)
    for sp in reversed(range(0, 100, 5)):
        s.set(-sp / 100)
        sleep(0.05)
    s.center()    
