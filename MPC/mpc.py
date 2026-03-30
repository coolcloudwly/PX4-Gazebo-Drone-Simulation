import numpy as np
import casadi as ca

class MPCController:
    def __init__(self):
        self.dt = 0.1
        self.N = 20
        self.build()

    def build(self):
        opti = ca.Opti()

        x = opti.variable(6, self.N+1)
        u = opti.variable(3, self.N)

        x0 = opti.parameter(6)
        xr = opti.parameter(6)

        def f(x, u):
            return ca.vertcat(u[0], u[1], u[2], 0, 0, 0)

        opti.subject_to(x[:, 0] == x0)

        for k in range(self.N):
            x_next = x[:,k] + f(x[:,k], u[:,k])*self.dt
            opti.subject_to(x_next == x[:,k+1])

        # 加强权重，精准飞到目标点
        Q = ca.diag([200, 200, 150, 50, 50, 40])
        R = ca.diag([0.01, 0.01, 0.1])

        J = 0
        for k in range(self.N):
            e = x[:,k] - xr
            J += ca.dot(e, ca.mtimes(Q, e))
            J += ca.dot(u[:,k], ca.mtimes(R, u[:,k]))  # 这里修复了！

        opti.minimize(J)

        opti.subject_to(opti.bounded(-0.4, u[0,:], 0.4))
        opti.subject_to(opti.bounded(-0.4, u[1,:], 0.4))
        opti.subject_to(opti.bounded(-0.2, u[2,:], 0.2))

        opts = {"ipopt.print_level": 0, "print_time": 0}
        opti.solver("ipopt", opts)
        self.func = opti.to_function("mpc", [x0, xr], [u[:,0]])

    def compute(self, x_now, target):
        try:
            v_cmd = self.func(x_now, target)
            vx, vy, vz = np.array(v_cmd).full().ravel()
            return vx, vy, vz
        except:
            return 0.0, 0.0, 0.0

