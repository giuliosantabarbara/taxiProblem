import gym
import aima.search as aima
import time
import numpy as np

locObstacleDx = [(0,1), (3,0), (3,2), (4,0), (4,2)]
locObstacleSx = [(0,2), (3,1), (3,3), (4,1), (4,3)]
env = gym.make('Taxi-v1')

class Taxi(aima.Problem):

    lambda h : h()

    def __init__(self, initial, goal=None):

        self.initial = initial
        self.goal = goal
        self.count=0;
        print("Initial State: " + str(self.initial))
        print("Goal State: " + str(self.goal))
        env.render()

    def actions(self, state):
        listAction = []
        x = state[0]
        y = state[1]

        if y > 0:
            listAction.append(3) #posso andare a sinistra
        if y < 4:
            listAction.append(2) #posso andare a destra

        if x > 0:
            listAction.append(1) #posso andare sopra
        if x < 4:
            listAction.append(0) #posso andare sotto

        if state in locObstacleDx:
            listAction.remove(2)
        elif state in locObstacleSx:
            listAction.remove(3)

        return listAction

    def result(self, state, action):

        x = state[0]
        y = state[1]

        if action == 0 :
            newstate = (x+1,y)
        elif action == 1:
            newstate = (x-1, y)
        elif action == 2 :
            newstate = (x, y+1)
        else :
            newstate = (x, y-1)

        print ("Vecchio stato: "+str(state))
        print ("Nuovo stato: " + str(newstate))
        print ("Azione: " + str(action))
        self.count = self.count+1
        return newstate

    def h(self, n):
        s = n.state
        x1 = s[0]
        y1 = s[1]

        x2 =self.goal[0]
        y2 = self.goal[1]
        #print(str(abs(x1 - x2) + abs(y1 - y2)))
        return abs(x1 - x2) + abs(y1 - y2)


    #def goal_test(self, state): Da non sovrascivere

def simulation():

    ricompense = []
    nodi = []
    start = time.clock()
    for ep in range (300):
        costo=0
        nodo=0
        nodo, costo = execute()
        ricompense.append(costo)
        nodi.append(nodo)

    tempo = time.clock() - start
    print("Nodi medi espansi: "+str(np.mean(nodi)))
    print ("Ricompensa media: "+str(np.mean(ricompense)))
    print("Tempo di simulazione(s): "+str(tempo))

def execute():


    initialDecode = list(decode(env.reset()))
    initialState = (initialDecode[0], initialDecode[1])  #posizione iniziale taxi
    goalPassengerState = location(initialDecode[2])   #posizione passeggero
    goalDestinationState = location(initialDecode[3]) #posizione destinazione
    costo = 0


    taxiPassenger = Taxi(initialState,goalPassengerState)
    #resPassenger = aima.breadth_first_search(taxiPassenger)
    #resPassenger = aima.depth_limited_search(taxiPassenger,8)
    #resPassenger = aima.iterative_deepening_search(taxiPassenger)

    #ricerca informata
    resPassenger = aima.astar_search(taxiPassenger)

    '''print ("**********Results passenger")
    print(resPassenger.path());'''

    actionsPassenger = resPassenger.solution()
    costo = len(actionsPassenger)
    '''print (actionsPassenger)'''


    '''for a in actionsPassenger:
        env.step(a)
        env.render()
    env.step(4) #pickup
    env.render()'''

    taxiDestination = Taxi(goalPassengerState, goalDestinationState)
    #resDestination = aima.breadth_first_search(taxiDestination)
    #resDestination = aima.depth_limited_search(taxiDestination,8)
    #resDestination = aima.iterative_deepening_search(taxiDestination)

    # ricerca informata
    resDestination = aima.astar_search(taxiDestination)


    '''print ("**********Results destination")
    print(resDestination.path())'''

    actionsDestination = resDestination.solution()
    costo = costo +len(actionsDestination)
    '''print (actionsDestination)
    for a in actionsDestination:
        env.step(a)
        env.render()
    env.step(5)  # dropoff
    env.render()'''

    conteggioFinale = taxiPassenger.count+taxiDestination.count
    ricompensaFinale = 20-costo
    #print ("Nodi espansi: "+str(conteggioFinale))
    #print("Ricompensa: "+str(ricompensaFinale))

    return conteggioFinale, ricompensaFinale


def decode(i):
    out = []
    out.append(i % 4)
    i = i // 4
    out.append(i % 5)
    i = i // 5
    out.append(i % 5)
    i = i // 5
    out.append(i)
    assert 0 <= i < 5
    return reversed(out)


def encode(self, taxirow, taxicol, passloc, destidx):
    # (5) 5, 5, 4
    i = taxirow
    i *= 5
    i += taxicol
    i *= 5
    i += passloc
    i *= 4
    i += destidx
    return i

def location(loc):
    if loc == 0:
        return (0, 0)
    elif loc == 1:
        return (0, 4)
    elif loc == 2:
        return (4, 0)
    else:
        return(4, 3)

if __name__ == '__main__':
    simulation()