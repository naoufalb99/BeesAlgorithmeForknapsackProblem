import numpy as np
import random
from pprint import pprint
from data.parse import generateData

dataset = 'f3_l-d_kp_4_20'

ne = 20
nb = 50
nre = 70    #parametres a changer 
nrb = 20 
stlim = 100

shrinking = 2

ns = nb + 50
n = ns + ne * nre + (nb - ne) * nrb

patch = []

##### dataset example #######
# capacity = 165              #optimum = 309
# weights = np.array([23, 31, 29, 44, 53, 38, 63, 85, 89, 82])
# profits = np.array([92, 57, 49, 68, 60, 43, 67, 84, 87, 72])



capacity = generateData(dataset)['capacity']
weights = np.array(generateData(dataset)['weights'])
profits = np.array(generateData(dataset)['profits'])


selected = np.zeros(len(weights))


class InvalidConstraint(Exception):
    pass

def fitness(x):
    totalWeights = sum([ weights[i] * x[i] for i in range(len(weights)) ])
    totalProfits = sum([ profits[i] * x[i] for i in range(len(profits)) ])
    if totalWeights > capacity:
        raise InvalidConstraint()
    return totalProfits

def fixedShuffle(list, pivot):
    start = int((len(list) - pivot) / 2)
    end = len(list) - start
    tmp = list[start:end]
    return list[0:start] + random.sample(tmp, k=len(tmp)) + list[end:len(list)]

def generateNeighbors(patch):
    solution = list(patch['scout'][0])
    neighbors = []
    for i in range(patch['foragers']):
        valide = False
        while(not valide):
            try:
                neighbor = fixedShuffle(solution, patch['neighborhood'])
                score = fitness(neighbor)
                valide = True
                neighbors.append([neighbor, score])
            except:
                pass
    return neighbors

def getValidSolution():
    valide = False
    while(not valide):
        try:
            solution = np.random.randint(0, 2, len(weights))
            score = fitness(solution)
            valide = True
        except:
            pass
    return [solution, score]

def newPatchElement():
    return {
        'scout': getValidSolution(), # [solution , fitness]
        'foragers': 0,
        'neighborhood': len(weights),
        'stgn': True,
        'stgnCounter': 0
    }

def initialisation():
    for i in range(ns):
        patch.append(newPatchElement())

def foragingStep():
    waggleDance()
    localSearch()
    neighborhoodShrinking()
    siteAbandonment()

def waggleDance():
    patch.sort(key = lambda x: x['scout'][1], reverse=True)
    for i in range(ne):
        patch[i]['foragers'] = nre

    for i in range(ne, nb):
        patch[i]['foragers'] = nrb
    

def localSearch():
    for i in range(nb):
        patch[i]['stgn'] = True
        neighbors = generateNeighbors(patch[i])
        sortedNeighbors = sorted(neighbors, key = lambda x: x[1], reverse=True)
        if sortedNeighbors[0][1] > patch[i]['scout'][1]:
            patch[i]['scout'][0] = sortedNeighbors[0][0]
            patch[i]['scout'][1] = sortedNeighbors[0][1]
            patch[i]['stgn'] = False


def neighborhoodShrinking():
    for i in range(nb):
        if(patch[i]['stgn'] == True):
            patch[i]['neighborhood'] -= shrinking

def siteAbandonment():
    for i in range(nb):
        if(patch[i]['stgn'] == True):
            if(patch[i]['stgnCounter'] < stlim):
                patch[i]['stgnCounter'] += 1
            else:
                patch[i] = newPatchElement()


def globalSearch():
    for i in range(nb, ns):
        patch[i] = newPatchElement()


initialisation()
foragingStep()

sortedPatch = sorted(patch, key = lambda x: x['scout'][1], reverse=True)
print(sortedPatch[0])


