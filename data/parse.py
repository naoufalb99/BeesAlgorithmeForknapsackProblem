## dataset : http://artemisa.unicauca.edu.co/~johnyortega/instances_01_KP/
def generateData(fileName):
    weights=[]
    values =[]
    file = open("./data/dataset/"+fileName,"r")
    first_line = file.readline()  
    lines = file.readlines()
    file.close()

    #getting capacity
    params = []
    params = first_line.split( ) 
    capacity = int(params[1])
    
    for line in lines :
        values.append(int(line.split( )[0]))
        weights.append(int(line.split( )[1]))
    
    result = {'weights': weights, 'profits':values,'capacity':capacity}
    
    return result
        


