import json
import numpy as np
import sys

try:
        path = str(sys.argv[1])
        filetoread = str(sys.argv[2])
        filetowrite = str(sys.argv[3])
        xyzrotationsmatrix = str(sys.argv[4])
except:
        print('Irgendwas mit den Parametern stimmt nicht..')
        sys.exit()


#Bestimmen der PoseID zu jedem Foto
pianzahl = 3
file = open(path+filetoread,'r')
z = json.load(file)
print(json.dumps(z,sort_keys=False,indent=10))

l = 0
id = np.empty([len(z['views']),2],dtype='object')
print(str(len(z['views'])))
for  p in z['views']:
        print(l)
        print('poseId '+ p['poseId'])
        print('path '+ p['path'])
        id[l,0] = str(p['path'])

        schtring = ''
        for k in range(0,len(id[l,0]),1):
                if id[l,0][k] == 'p' and id[l,0][k+1] == 'i' and int(id[l,0][k+2]) in range(1,pianzahl+1,1) :
                        zaehl = 0
                        for h in range(k,len(id[l,0]),1):
                                print(h)
                                schtring = schtring+str(id[l,0][h]) 
                                zaehl += 1
                        print(schtring)
                        id[l,0] = schtring
                        break
        id[l,1] = str(p['poseId'])
        l += 1
print(id)
print(len(id))
#Austauschen der Rotationsmatrix und Ortsvektoren
x = np.genfromtxt(path+xyzrotationsmatrix,dtype='str')
for p in z['poses']:
        for k in range(0,id.shape[0],1):
                if id[k,1] == p['poseId']:
                        break
        #print(k)
        #print(p['poseId'])
        #print(x[i,:])
        for i in range(0,x.shape[0],1):
                #print(x[i,0])
                #print(str(id[k,0]))
                if str(x[i,0]) == str(id[k,0]):
                        break
        #print(i) 
        p['pose'] = {
                 'transform': {
                         'rotation': [
                                 format(x[i,4],'.15'),
                                 format(x[i,7],'.15'),
                                 format(x[i,10],'.15'),
                                 format(x[i,5],'.15'),
                                 format(x[i,8],'.15'),
                                 format(x[i,11],'.15'),
                                 format(x[i,6],'.15'),
                                 format(x[i,9],'.15'),
                                 format(x[i,12],'.15')
                         ],
                         'center' : [
                                format((float(x[i,1])*0.0012937233071295*1.5),'.15'), #0.0012937233071295
                                format((float(x[i,3])*0.0012937233071295*1.5),'.15'),
                                format((float(x[i,2])*0.0012937233071295*1.5),'.15')
                        ]},
                'locked' : '1'
                }
        #print('\n')
#z['featuresFolders'] = ''
#z['matchesFolders'] = ''
#Testweise nur Austausch der Ortsvektoren funktioniert noch nicht
#       for u in p['pose']:
#               for r in u:
#                       r['center'] = {[
#                               (float(x[i,1])*0.0012937233971295),
#                                (float(x[i,2])*0.0012937233971295),
#                                (float(x[i,3])*0.0012937233971295)
#                       ]}

#print(z)
file.close
ftw = open(path+filetowrite,'w')
ftw.write(json.dumps(z,sort_keys=False,indent=4))
ftw.close

