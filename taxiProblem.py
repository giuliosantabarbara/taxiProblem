import gym
import aima.search as aima

env = gym.make('Taxi-v1')

class Taxi(aima.Problem):

    def __init__(self, initial, goal=None):

        self.initial = initial
        self.goal = goal
        print("Initial State: " + str(self.initial))
        print("Goal State: " + str(self.goal))
        env.render()

    def actions(self, state):
        listAction = []

        if state[1]>0 :
            listAction.append(3) #posso andare a sinistra
        if state[1]<4 :
            listAction.append(2) #posso andare a destra
        if state[0]>0:
            listAction.append(1) #posso andare sopra
        if state[0]<4 :
            listAction.append(0) #posso andare sotto

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
        print ("Action: " + str(action))
        return newstate


    #def goal_test(self, state): DA non sovrascivere


def train():

    initialDecode = list(decode(env.reset()))
    initialState = (initialDecode[0], initialDecode[1])  # posizione iniziale taxi
    goalState = location(initialDecode[2]) #posizione passeggero

    t = Taxi(initialState,goalState)
    res = aima.breadth_first_search(t)

    print ("*************")
    print(res.path());

    actions = res.solution()
    print (actions)
    for a in actions:
        env.step(a)
        env.render()

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
    train()
