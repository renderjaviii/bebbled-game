import numpy as np
import numpy.random as rn
import matplotlib.pyplot as plt  # to plot
import matplotlib as mpl


def annealing(estado_inicial, funcion_costo, siguiente_estado, acceptance_probability, temp_inicial,
              temp_decrease_factor, maxsteps=50, debug=True):
    """
    Params:
        estado_inicial -> Función que genera solución inicial
        funcion_costo -> Función de costo
        siguiente_estado -> Función que genera el siguiente estado que se puede obtener a partir del anterior
        acceptance -> Función de distribución de probabilidad
        temp_inicial -> Parametro, temperatura inicial
        temp_decrease_factor -> Parametro, factor de decrecimiento de temperatura [0.8- 0.98]
        maxsteps -> Número de interaciones por temperatura
        debug -> Debug Mode

    """
    state = estado_inicial()
    cost = funcion_costo(state)
    states, costs = [state], [cost]
    num_accep = []
    T = temp_inicial
    while T > 0.01:
        aceptances = 0
        for step in range(maxsteps):
            new_state = siguiente_estado(state)
            new_cost = funcion_costo(new_state)
            if acceptance_probability(cost, new_cost, T) > rn.random():
                state, cost = new_state, new_cost

                if(type(state) == list):
                    states.append(state[:])
                else:
                    states.append(state)

                costs.append(cost)
                aceptances += 1

        if debug: print("Temp : {}, state = {}, cost = {}".format(T, state, cost))
        T *= temp_decrease_factor
        num_accep.append(aceptances)

    best_sol_index = costs.index(min(costs))
    print("Mejor indice:", best_sol_index, "Mejor costo:", costs[best_sol_index], "Mejor estado:",
          states[best_sol_index])
    return states[best_sol_index], costs[best_sol_index], states, costs, num_accep


def cost_function(x):
    """ Función de costo Ejemplo 1"""
    return (5/2.0)+x**2



def algoritmo_metropolis(cost, new_cost, temperature):
    """ Función de probabilidad de aceptación Ejemplo 1"""
    if new_cost < cost:
        return 1
    else:
        p = np.exp(- (new_cost - cost) / temperature) # Función de probabilidad e Boltzman
        return p


intervalo = [-250, 250]
def estado_inicial():
    """ Punto aleatorio en el intervalo """
    a, b = intervalo
    return a + (b - a) * rn.random_sample()



def siguiente_estado(x):
    """ Moverlo un poco hacia cualquier dirección"""
    delta =  rn.random_sample() #Return random floats in the half-open interval [0.0, 1.0).
    if rn.random_sample() > 0.5:
        delta = -delta
    new_state = x + delta
    #Debe estar en el intervalo
    a, b = intervalo
    new_state = max(min(new_state, b), a)
    return new_state


state, c, states, costs, num_accep = annealing(estado_inicial, cost_function, siguiente_estado, algoritmo_metropolis,
          temp_inicial= 1000, temp_decrease_factor = 0.8, maxsteps=30, debug=False)
state, c

def see_annealing(states, costs, num_accep):
    plt.figure()
    plt.subplot(311)
    plt.plot(states, 'r')
    plt.title("Estados/Soluciones")
    plt.subplot(312)
    plt.plot(costs, 'b')
    plt.title("Costo")
    plt.subplot(313)
    plt.plot(num_accep, 'b')
    plt.title("Probabilidad de aceptación")
    plt.tight_layout()
    plt.show()


see_annealing(states, costs, num_accep)