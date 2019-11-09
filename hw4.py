import numpy as np
import matplotlib.pyplot as plt

ODE_tst = lambda x, y, z, **kwargs: (7*y**2) * x**3 
ODE_h_x = lambda x, y, z, **kwargs: (-26.2 * (kwargs.get('e') - kwargs.get('v')) * y)


#Constants


Vmax = 10**6                            #'Infinite' potential
half_width_box = 0.5 * (10**-9)         #half width of 1nm box
E_initial_guess = 1               #Initial guess for E
eta = 10**-15
step_size = eta**(.5) 


def V(x, a):
    if abs(x) <= a:
        return 0
    return Vmax




ODE_f_x = lambda x, y, z, **kwargs: z
ODE_h_x = lambda x, y, z, **kwargs: (-26.2 * (kwargs.get('e') - 0) * y)
ODE_g_x = lambda x, y, z, **kwargs: (-26.2 * (kwargs.get('e') - kwargs.get('v')) * y)

def Runge_Kutta(E, f, g, h, interval):
    a = interval
    N = 100
    h = a / N
    
    x_ary = np.zeros(N)
    y_ary = np.zeros(N)
    z_ary = np.zeros(N)
    
    x_ary[0] = 0
    y_ary[0] = 1
    z_ary[0] = 0
    
    
    k1 = lambda x, y, z: h * f(x, y, z, e=E, v=V(x, a))    
    l1 = lambda x, y, z: h * g(x, y, z, e=E, v=V(x, a))

    k2 = lambda x, y, z: h * f(x + h/2, y + k1(x, y, z)/2, z + l1(x, y, z)/2, e=E, v=V(x, a))    
    l2 = lambda x, y, z: h * g(x + h/2, y + k1(x, y, z)/2, z + l1(x, y, z)/2, e=E, v=V(x, a))

    k3 = lambda x, y, z: h * f(x + h/2, y + k2(x, y, z)/2, z + l2(x, y, z)/2, e=E, v=V(x, a))    
    l3 = lambda x, y, z: h * g(x + h/2, y + k2(x, y, z)/2, z + l2(x, y, z)/2, e=E, v=V(x, a))

    k4 = lambda x, y, z: h * f(x + h, y + k3(x, y, z), z + l3(x, y, z), e=E, v=V(x, a))    
    l4 = lambda x, y, z: h * g(x + h, y + k3(x, y, z), z + l3(x, y, z), e=E, v=V(x, a))

      
    
    for i in range(N-1):
        x_ary[i+1] = x_ary[i] + h
        y_ary[i+1] = (y_ary[i] + (k1(x_ary[i], y_ary[i], z_ary[i]) / 6) 
            + (k2(x_ary[i], y_ary[i], z_ary[i]) / 3) 
            + (k3(x_ary[i], y_ary[i], z_ary[i]) / 3)
            + (k4(x_ary[i], y_ary[i], z_ary[i]) / 6))

        z_ary[i+1] = (z_ary[i] + (l1(x_ary[i], y_ary[i], z_ary[i]) / 6) 
            + (l2(x_ary[i], y_ary[i], z_ary[i]) / 3) 
            + (l3(x_ary[i], y_ary[i], z_ary[i]) / 3)
            + (l4(x_ary[i], y_ary[i], z_ary[i]) / 6))
    '''
    print('y(a) = {0:.15}\nz(a) = {1:.4}'.format(y_ary[-1], z_ary[-1]))
    plt.plot(x_ary, y_ary)
    plt.show()
    '''
    return x_ary, y_ary
    '''    
    print('y(a) = {0:.15}\nz(a) = {1:.4}'.format(y_ary[-1], z_ary[-1]))
    plt.plot(x_ary, y_ary)
    plt.show()
    '''


change = 1
#Runge_Kutta(E_initial_guess*(change)*1E18, ODE_f_x, ODE_g_x, step_size, half_width_box)



difference = 1
y_a = 0
current_max = 0.5
while abs(difference) > 1E-8:
    current_max = current_max/10
    while abs(difference) > current_max:
        change += current_max*(np.sign(difference))
        x_val, y_val = Runge_Kutta(E_initial_guess*(change)*1E18, ODE_f_x, ODE_g_x, step_size, half_width_box)
        
        
        difference = y_val[-1]
        print('y(a) = {0:.15}\ndifference = {1:.5}\nEnergy = {2:.8}\n'.format(y_val[-1], difference, (E_initial_guess*(change)*1E18)))
        y_a = y_val[-1]

E_estimate = E_initial_guess*(change)*1E18
plt.plot(x_val, y_val)
plt.show()

