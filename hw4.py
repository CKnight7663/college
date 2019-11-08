import numpy as np
import matplotlib.pyplot as plt


#Constants


Vmax = 10**6                            #'Infinite' potential
half_width_box = 0.5 * (10**-9)         #half width of 1nm box
E_initial_guess = 1/ 26.2               #Initial guess for E
eta = 10**-15
step_size = eta**(.5) 


def V(x, a):
    if abs(x) <= a:
        return 0
    return Vmax



ODE_f_x = lambda x, y, **kwargs: (-26.2 * (kwargs.get('e') - kwargs.get('v')) * y)


ODE_tst = lambda x, y, **kwargs: (-y) 

def Runge_Kutta(E, f, h, interval):
    a = interval
    N = 1000
    h = a / N
    y_ary = np.zeros(N)
    x_ary = np.zeros(N)
    y_ary[0] = 1
    x_ary[0] = 0
    k1 = lambda x, y: h * f(x, y, e=E, v=V(x, a))
    k2 = lambda x, y: h * f(x + h/2, y + k1(x, y)/2, e=E, v=V(x, a))
    k3 = lambda x, y: h * f(x + h/2, y + k2(x, y)/2, e=E, v=V(x, a))
    k4 = lambda x, y: h * f(x + h, y + k3(x, y), e=E, v=V(x, a))
    for i in range(N-1):
        x_ary[i+1] = x_ary[i] + h
        y_ary[i+1] = (y_ary[i] + (k1(x_ary[i], y_ary[i]) / 6) 
            + (k2(x_ary[i], y_ary[i]) / 3) 
            + (k3(x_ary[i], y_ary[i]) / 3)
            + (k4(x_ary[i], y_ary[i]) / 6))
    
    print(y_ary[-1])
    plt.plot(x_ary, y_ary)
    plt.show()

Runge_Kutta(E_initial_guess*10, ODE_f_x, step_size, 10)











'''
def schro(x, n):
    phi = 1+ np.sin(n * x * np.pi/a)
    return phi

x = np.linspace(0, a, 101)
for i in range(1, 5):
    y = schro(x, i)
    plt.plot(x, y)
    plt.show()
'''