import subprocess
import os
import os.path
import shutil
from os import path
import pathlib
import matplotlib.pyplot as plt
circles= 300
parameters=2*circles
stuffin=parameters+1
tmp=subprocess.call(["./RV-GOMEA","-v","-w","-g", "14", "%d" % parameters, "0", "1", "0", "0.35", "10", "1000", "0.9", "1", "5000000" ,"10e-10", "35", "0", "300000"])


for i in range(0,parameters+1):
	try:
	    stuff_in_string="best_generation_0000{}.dat".format(parameters+1-i)
	    f = open("%s" % stuff_in_string,'r')
	    # Do something with the file
	    break;
	except IOError:
	    print("File not accessible")
	    
	



 


contents=f.read()
contents = contents.split()
print("Contents length is:")
print((len(contents)-3)/2);
print( "\n");

contentlength =len(contents)
rangecontent=(contentlength-3)/2


temp=float(contents[contentlength-1]);
rad= temp/(1+temp*2);
print("this is the radius");
print(rad)
fig, ax = plt.subplots() 
fig = plt.gcf()
ax = plt.gca()
for i in range(0,int(rangecontent)):
	
	x1=((float(contents[2*i])+temp)/(1+2*temp))
	y1=((float(contents[2*i+1])+temp)/(1+2*temp))
	
	
	ax.add_artist(plt.Circle((x1,y1),rad,color='blue'))
	plt.scatter(x1,y1)



#(xarr[k]+temp) /(1+2*temp)

plottext  = "3_2_Var_"+ ".png"
plt.xlim(0, 1)
plt.ylim(0, 1)
fig.savefig(plottext)
plt.show()
	
	
	
