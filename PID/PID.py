import numpy as np

class PIDController:
    def __init__(self, kp, ki, kd, max_out=2.5):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_output = max_out
        self.error_last = 0.0
        self.integral = 0.0
        self.dt = 0.05

    def compute(self, target, current):
        error = target - current
        p_term = self.kp * error
        self.integral += error * self.dt
        i_term = self.ki * self.integral
        d_term = self.kd * (error - self.error_last) / self.dt
        self.error_last = error
        output = p_term + i_term + d_term
        return np.clip(output, -self.max_output, self.max_output)

