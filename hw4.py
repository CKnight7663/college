import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as scig

ODE_tst = lambda x, y, z, **kwargs: (7*y**2) * x**3 
ODE_h_x = lambda x, y, z, **kwargs: (-26.2 * (kwargs.get('e') - kwargs.get('v')) * y)


#Constants


Vmax = 10**6                            #'Infinite' potential
half_width_box = 0.5 * (10**-9)         #half width of 1nm box
E_initial_guess = 1E19/26.2               #Initial guess for E
eta = 10**-15
step_size = eta**(.5) 


def V(x, a):
    if abs(x) <= a:
        return 0
    return Vmax




ODE_f_x = lambda x, y, z, **kwargs: z
ODE_h_x = lambda x, y, z, **kwargs: (-26.2 * (kwargs.get('e') - 0) * y)
ODE_g_x = lambda x, y, z, **kwargs: (-26.2 * (kwargs.get('e') - kwargs.get('v')) * y)

def Runge_Kutta(E, f, g, H, a, n, both, N, *args):
    #E is the energy value for thsi run of Runge_Kutta
    #f, g are teh functions associated with the two coupled
    #first order ODE's
    #H is a variable telling the method to go positive or negative
    #a is the distance from x=0 to 1 side of the well
    #n is the solution order, n=1 is ground state EVEN, and so on
    #both is a variable used to tell the method whether to only find
    #y values according to the H choice, or to do find both
    #N is the number of steps
    #*args allows us to pass in the positive soloutions when we 
    #loop back to do the negative solutions

    h = H * a / N               #step size
    
    if ((n-1) % 4) == 0:        #there are four solution types
        y_0 = 1                 #the first EVEN peaks at x=0
        z_0 = 0
    elif ((n-1) % 4) == 1:
        y_0 = 0                 #the first ODD has neg-slope at x=0
        z_0 = -1
    elif ((n-1) % 4) == 2:
        y_0 = -1                #the second EVEN troughs at x=0
        z_0 = 0
    elif ((n-1) % 4) == 3:
        y_0 = 0                 #the first ODD has pos-slope at x=0
        z_0 = 1
    

    #From here we apply the Runge_Kutta Method, straight forward
    x_ary = np.zeros(N)
    y_ary = np.zeros(N)
    z_ary = np.zeros(N)
    
    x_ary[0] = 0
    y_ary[0] = y_0
    z_ary[0] = z_0/a
    
    
    k1 = lambda x, y, z: h * f(x, y, z, e=E, v=V(x, a))    
    l1 = lambda x, y, z: h * g(x, y, z, e=E, v=V(x, a))

    k2 = lambda x, y, z: h * f(x + h/2, y + k1(x, y, z)/2, z + l1(x, y, z)/2, e=E, v=V(x, a))    
    l2 = lambda x, y, z: h * g(x + h/2, y + k1(x, y, z)/2, z + l1(x, y, z)/2, e=E, v=V(x, a))

    k3 = lambda x, y, z: h * f(x + h/2, y + k2(x, y, z)/2, z + l2(x, y, z)/2, e=E, v=V(x, a))    
    l3 = lambda x, y, z: h * g(x + h/2, y + k2(x, y, z)/2, z + l2(x, y, z)/2, e=E, v=V(x, a))

    k4 = lambda x, y, z: h * f(x + h, y + k3(x, y, z), z + l3(x, y, z), e=E, v=V(x, a))    
    l4 = lambda x, y, z: h * g(x + h, y + k3(x, y, z), z + l3(x, y, z), e=E, v=V(x, a))

      
    
    for i in range(N-1):
        x_ary[i+1] = x_ary[i] + h       #the sign of h determins the direaction the solution takes
                                        #no further alterations are needed when doing negatives
        y_ary[i+1] = (y_ary[i] + (k1(x_ary[i], y_ary[i], z_ary[i]) / 6) 
            + (k2(x_ary[i], y_ary[i], z_ary[i]) / 3) 
            + (k3(x_ary[i], y_ary[i], z_ary[i]) / 3)
            + (k4(x_ary[i], y_ary[i], z_ary[i]) / 6))

        z_ary[i+1] = (z_ary[i] + (l1(x_ary[i], y_ary[i], z_ary[i]) / 6) 
            + (l2(x_ary[i], y_ary[i], z_ary[i]) / 3) 
            + (l3(x_ary[i], y_ary[i], z_ary[i]) / 3)
            + (l4(x_ary[i], y_ary[i], z_ary[i]) / 6))



    if h > 0 and both:                  #Now if we have both==True, and our h is pos
        x_pos, y_pos = x_ary, y_ary     #Will need to save the pos solutions, 
        H = -1                          #Setup for neg-solutions
        x_neg, y_neg = Runge_Kutta(E, f, g, H, a, n, both, N, x_pos, y_pos)
        x_ary = np.append(x_neg, x_pos) #And it appends the pos to the end of the 
        y_ary = np.append(y_neg, y_pos) #negative solutions, though first the 
                                        #neg-sol will wass through elif bellow
    elif h < 0:
        x_ary = np.delete(x_ary, 0)     #Removes x=0 values, so that it doesnt double
        y_ary = np.delete(y_ary, 0)     #Count
        x_ary = x_ary[::-1]             #And inverts the arrays, so they allign with pos
        y_ary = y_ary[::-1]
        return x_ary, y_ary
    
                                        #Cant remeber why i return h aswell, it may be
    return x_ary, y_ary, h              #remenent of an older build of this function 



def Energy_finder(y_c, c, accuracy, guess, n):
    #y(x, b) with b some unknown constant. we know y(x=c)=y_c, so we alter b 
    #until we get y(x=c)=y_c within some degree of accuracy
    x_val, y_val, h = Runge_Kutta(guess, ODE_f_x, ODE_g_x, 1, half_width_box, n, False, 100)
    difference = abs(y_c - y_val[c])        #Finds how far off our value we are
    scatter_min, scatter_max = 0.2, 2       #In order to get a good estimate of the Energy
                                            #We setup a 'scatter' of values about 1, and 
                                            #multiply our guess by each scatter. We then 
                                            #make a new scatter at the best value of E
                                            #until we come within a good enough difference
    
    while difference > accuracy:
        
        guess_scatter = np.linspace(scatter_min, scatter_max, 10)       
        diff_guess = np.zeros(10)   
        for i in range(10):
            x_val, y_val, h = Runge_Kutta(guess * guess_scatter[i], ODE_f_x, ODE_g_x, 1, half_width_box, n, False, 100)
            
            diff_guess[i] = abs(y_c - y_val[c])     #We use abs, because we dont care if its above or bellow,
                                                    #just whats its value is.
        
        min_index = np.where(diff_guess == min(diff_guess))     #We grab the min value, and its index in the diff_guess
        difference = diff_guess[min_index[0]][0]                #array, this corresponds to the best scatter value index
        if min_index[0][0]==0 or min_index[0][0]==9:            #If the min/max scatter are the best, we need to do 
            i = min_index[0][0]                                 #something different(mostly unused, and dont want to 
            current_guess = guess * guess_scatter[i]            #break it right now)
            scatter_min = guess_scatter[i] - (guess_scatter[2]-guess_scatter[1])    #I may rework this, as if the
            scatter_max = guess_scatter[i] + (guess_scatter[2]-guess_scatter[1])    #guess is too far off,we fail
                                                                                    #to come converge right
        else:
            i = min_index[0][0]                         #But if its any other scatter value, we can use the scatter
            current_guess = guess * guess_scatter[i]    #value above and bellow as the new max, min
            scatter_min = guess_scatter[i-1]            #this ensures we hone in on a value
            scatter_max = guess_scatter[i+1]
        #print(min(diff_guess))
    guess = current_guess
    #print('\n\nEnergy= ', guess)    
    return guess
    
def plotter(x, y, n, Energy):
    plt.plot(x, y)
    plt.xlim(-1.2*half_width_box, 1.2*half_width_box)
    plt.ylim(1.1*min(y), 1.1*max(y))
    plt.xlabel('x')
    plt.ylabel(' \u03C8')
    plt.title('The {0} Soloution, with Energy = {1:.4}'.format(n, Energy))
    plt.axvline(x=-half_width_box, c='k')
    plt.axvline(x=half_width_box, c='k')
    plt.show()


def Schro_Infinite_Well(m):                 #Makes plotting for any m less clumsy
    
    E_estimate = Energy_finder(0, -1, 1E-15, (m**2)*E_initial_guess, m)
    x_val, y_val, h = Runge_Kutta(E_estimate, ODE_f_x, ODE_g_x, 1, half_width_box, m, True, 100)
    plotter(x_val, y_val, m, E_estimate)


Schro_Infinite_Well(1)
Schro_Infinite_Well(2)
Schro_Infinite_Well(3)
Schro_Infinite_Well(4)
