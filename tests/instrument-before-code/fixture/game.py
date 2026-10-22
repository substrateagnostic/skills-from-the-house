CHARGE_SECONDS = 0.7

class ChargeButton:
    """Hold the button for CHARGE_SECONDS of real (delta) time to fire."""
    def __init__(self):
        self.held = 0.0
        self.fired = False

    def update(self, dt, pressed):
        if pressed:
            self.held += dt
            if self.held >= CHARGE_SECONDS:
                self.fired = True
        else:
            self.held = 0.0
