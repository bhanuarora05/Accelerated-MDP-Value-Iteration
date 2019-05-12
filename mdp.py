import numpy as np
import time
import scipy.signal
begin = time.time()
file = open("input9.txt","r")
i=0  
for line in file:
    line = line.strip()
    if i==0:
        S=int(line)            
    elif i==1:
        N=int(line)
    elif i==2:
        O=int(line)
        break
    i+=1
Matrix = np.array([[-1 for i in range(S)] for j in range(S)])
i = 0
for line in file:
    line = line.strip()
    x,y = [int(l) for l in line.split(',')[::-1]]
    if i<O:
        Matrix[x][y] = -101
    if i==O-1:
        break
    i += 1

i = 0
Cars = [(-1,-1)]*N
for line in file:
    line = line.strip()
    x,y = [int(l) for l in line.split(',')[::-1]]
    if i<N:
        Cars[i] = (x,y)
    if i==N-1:
        break
    i += 1

i = 0
Ends = [(-1,-1)]*N
for line in file:
    line = line.strip()
    x,y = [int(l) for l in line.split(',')[::-1]]
    if i<N:
        Ends[i] = (x,y)
    if i==N-1:
        break
    i += 1

file.close()

GoToSwitch = {'Up'    : (-1,0),
              'Down'  :  (1,0),
              'Right' :  (0,1),
              'Left'  : (0,-1)}

def OutOfBounds(s):
    if s[0]>=0 and s[1]>=0 and s[0]<=S-1 and s[1]<=S-1:
        return False
    else:
        return True

def GoTo(s,action):
    Temp = (s[0]+GoToSwitch[action][0],s[1]+GoToSwitch[action][1])
    if not OutOfBounds(Temp):
        return Temp
    else:
        return s

GoLeftSwitch = {'Up'    : 'Left',
              'Down'  :  'Right',
              'Right' :  'Up',
              'Left'  : 'Down'}

costs = [0]*N
Actions = np.array(['Up','Down','Right','Left'],object)

def convolve2d(input,filter):
    return scipy.signal.correlate2d(input,filter,'same','symm')

for c in range(N):
    R = np.array(Matrix)
    R[Ends[c][0],Ends[c][1]] = 99
    V = np.array(R)
    Pi = np.zeros_like(V,object)
    for i in range(S):
        for j in range(S):
            Pi[i,j] = 'Up'
            
    Pi[Ends[c][0],Ends[c][1]] = ''

    check = True
    while check:
        Up = convolve2d(V,np.array([[0,0.7,0],[0.1,0,0.1],[0,0.1,0]]))
        Down = convolve2d(V,np.array([[0,0.1,0],[0.1,0,0.1],[0,0.7,0]]))
        Right = convolve2d(V,np.array([[0,0.1,0],[0.1,0,0.7],[0,0.1,0]]))
        Left = convolve2d(V,np.array([[0,0.1,0],[0.7,0,0.1],[0,0.1,0]]))

        MaxPool = np.stack([Up,Down,Right,Left],0)
        CopyV = V.copy()

        V = R + (1-0.1)*MaxPool.max(0)
        V[Ends[c][0],Ends[c][1]] = 99

        Pi = MaxPool.argmax(0)
        Pi = Actions[Pi]
        Pi[Ends[c][0],Ends[c][1]] = ''

        if np.abs(V - CopyV).max() < (1/90.0):
            check = False


    #print Pi 
    cost = 0
    for i in range(10):
        currentPos = Cars[c]
        np.random.seed(i)
        swerve = np.random.random_sample(1000000)
        k = 0
        while currentPos!=Ends[c]:
            currentMove = Pi[currentPos[0],currentPos[1]]
            if swerve[k]>0.7:
                if swerve[k]>0.8:
                    if swerve[k]>0.9:
                        currentMove = GoLeftSwitch[GoLeftSwitch[currentMove]]
                    else:
                        currentMove = GoLeftSwitch[GoLeftSwitch[GoLeftSwitch[currentMove]]]
                else:
                    currentMove = GoLeftSwitch[currentMove]

            currentPos = GoTo(currentPos,currentMove)
            cost += R[currentPos[0],currentPos[1]]
            k += 1

    print int(np.floor(cost/10))
    costs[c] = int(np.floor(cost/10))

file1 = open("output.txt","w")
for cost in costs:
    file1.write(str(cost))
    file1.write("\n")
file1.close() 
print time.time()-begin