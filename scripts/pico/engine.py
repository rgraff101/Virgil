from machine import Pin, PWM

class Engine:
    def __init__(
        self,
        pwm_pin_id: int,
        pw_stall: int = int(1.21e6), # motor stop pulse width, ns
        pw_fwd_max: int = int(1.8e6), # maximum forward pulse width, ns
        pw_rev_max: int = int(1.09e6), # maximum reverse pulse width, ns
    ) -> None:
        # Config pin
        self.PWM_PIN = PWM(Pin(pwm_pin_id))
        self.PWM_PIN.freq(50)
        self.PWM_PIN.duty_ns(pw_stall)
        # Properties
        self._pw_stall = pw_stall
        self._pw_rev_max = pw_rev_max
        self._pw_fwd_max = pw_fwd_max
        
    def forward(self, speed: float = 0.):
        self.PWM_PIN.duty_ns(self._pw_stall + int((self._pw_fwd_max - self._pw_stall) * speed))

    def backward(self, speed: float = 0.):
        self.PWM_PIN.duty_ns(self._pw_stall - int((self._pw_stall - self._pw_rev_max) * speed))

    def stop(self):
        self.PWM_PIN.duty_ns(self._pw_stall)
        
# Test
if __name__ == '__main__':
    from time import sleep
    m = Engine(15)
    sleep(3)  # ESC calibrate
    for sp in range(100):
        m.forward(sp / 100)
        print(f"FORWARD: {sp}%")
        sleep(0.05)
    for sp in reversed(range(100)):
        m.forward(sp / 100)
        print(f"FORWARD: {sp}%")
        sleep(0.05)
    for sp in range(100):
        m.backward(sp / 100)
        print(f"BACKWARD: {sp}%")
        sleep(0.05)
    for sp in reversed(range(100)):
        m.backward(sp / 100)
        print(f"BACKWARD: {sp}%")
        sleep(0.05)
    m.stop()    
    print("STOP")
