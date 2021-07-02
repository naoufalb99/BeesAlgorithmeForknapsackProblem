import os

datasetPath = os.path.join(os.path.dirname(__file__), 'dataset')

## dataset : http://artemisa.unicauca.edu.co/~johnyortega/instances_01_KP/
def generateData(fileName):
    weights=[]
    values =[]
    file = open(os.path.join(datasetPath, fileName),"r")
    first_line = file.readline()  
    lines = file.readlines()
    file.close()

    #getting capacity
    params = []
    params = first_line.split( ) 
    capacity = int(params[1])
    
    for line in lines :
        values.append(int(float(line.split( )[0])))
        weights.append(int(float(line.split( )[1])))
    
    result = {'weights': weights, 'profits':values,'capacity':capacity}
    
    return result

def chooseDataset():
    files = os.listdir(datasetPath)
    if(len(files) <= 0): exit()
    else: 
        print("Which data set would you run?")
        for i in range(len(files)):
            print("{index:<3} {fileName}".format(index = str(i + 1) + ")", fileName = files[i]))
        while True:
            try:
                selected = int(input("Please select one of the choices above: "))
                if(selected <= 0 or selected > len(files)):
                    raise ValueError
                else: 
                    return files[selected - 1] 
            except ValueError:
                print ("Invalid input")
    return None
