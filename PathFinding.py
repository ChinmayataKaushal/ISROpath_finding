import cv2 
import numpy as np 
import matplotlib.pyplot as plt

b=[]
c=[]
d=[]
m=0
n=0
row=0
colm=0

#read and convert the main image and template to gray
img_rgb = cv2.imread('samplemain1.jpeg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template1 = cv2.imread('45righttemp.jpeg',0)
template2 = cv2.imread('45lefttemp.jpeg',0)
plus = cv2.imread('intersection.jpeg',0)
#gray_template1= cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)
#gray_template2= cv2.cvtColor(template2, cv2.COLOR_BGR2GRAY)
#gray_plus= cv2.cvtColor(template2, cv2.COLOR_BGR2GRAY)

#store the height and width of templates
w1,h1 = template1.shape[::-1]
w2,h2 = template2.shape[::-1]
w3,h3 = plus.shape[::-1]

#for 1st template

# Perform match operations. 
res1 = cv2.matchTemplate(img_gray,template1,cv2.TM_CCOEFF_NORMED) 
# Specify a threshold 
threshold = 0.8
# Store the coordinates of matched area in a numpy array 
loc1 = np.where( res1 >= threshold)  
  # Draw a rectangle around the matched region. 
for pt in zip(*loc1[::-1]): 
    cv2.rectangle(img_rgb, pt, (pt[0] + w1, pt[1] + h1), (0,255,0), 2) 
    b.append(pt)




#for 2nd template

# Perform match operations. 
res2 = cv2.matchTemplate(img_gray,template2,cv2.TM_CCOEFF_NORMED) 
# Specify a threshold 
threshold = 0.8
# Store the coordinates of matched area in a numpy array 
loc2 = np.where( res2 >= threshold)  
# Draw a rectangle around the matched region. 
for pt1 in zip(*loc2[::-1]): 
    cv2.rectangle(img_rgb, pt1, (pt1[0] + w2, pt1[1] + h2), (0,0,255), 2) 
    c.append(pt1)



#for the intersection

# Perform match operations. 
result = cv2.matchTemplate(img_gray,plus,cv2.TM_CCOEFF_NORMED) 
# Specify a threshold 
threshold = 0.8
# Store the coordinates of matched area in a numpy array 
loc3 = np.where( result >= threshold)  
# Draw a rectangle around the matched region. 
for pt2 in zip(*loc3[::-1]): 
    cv2.rectangle(img_rgb, pt2, (pt2[0] + w3, pt2[1] + h3), (255,0,0), 2)
    d.append(pt2)

num_of_intersections= len(d)
b.sort()
c.sort()
d.sort()

for i in range (0, num_of_intersections):
	if d[0][0]==d[i][0]:
		m+=1
n=int(num_of_intersections/m+1)
m=m+1
n=n+1
cv2.imshow('abcd',img_rgb)


#finding positions of the mirror
h=d[1][1]-d[0][1]
w=d[m][0]-d[0][0]


#insert mirrors in array
array=[]
array=[[0]*n for r in range(m)]
#for /
for i in range(0, len(b)):
	colm=int(b[i][0]/w)
	row=int(b[i][1]/h)
	array[row][colm]=2

#for \
for i in range(0, len(c)):
	colm1=int(c[i][0]/w)
	row1=int(c[i][1]/h)
	array[row1][colm1]=-2

print(array)


#currentposition row=a colm=b
a=0 
b=0
p1=0
q1=0
p2=0
q2=0
p=0
q=0

#define the functions for all directions and how the wave will move
def pathtrace(p1,q1,p2,q2):
	#set the axes 
	p=[-p1,-p2]
	q=[q1,q2]
	plt.plot(q,p,color='r',label='path')


def right(a,b):
	while b<n:
		b=b+1
		if b==n:
			pathtrace(a+0.5,b+0.5,a+0.5,b+1.5)
			exitcondition(a,b)
			
		elif array[a][b]== -2 :
			pathtrace(a+0.5,b+0.5,a+1.5,b+0.5)
			down(a,b)
			
		elif array[a][b]==2 :
			pathtrace(a+0.5,b+0.5,a-0.5,b+0.5)
			up(a,b)

		else:
			pathtrace(a+0.5,b+0.5,a+0.5,b+1.5)

			
		

def left(a,b):
	while b>-1:
		b=b-1
		if	b==-1:
			pathtrace(a+0.5,b+0.5,a+0.5,b-0.5)
			exitcondition(a,b)
			
		elif array[a][b]== -2:
			pathtrace(a+0.5,b+0.5,a-0.5,b+0.5)
			up(a,b)
			
		elif array[a][b]==2:
			pathtrace(a+0.5,b+0.5,a+1.5,b+0.5)
			down(a,b)

		else:
			pathtrace(a+0.5,b+0.5,a+0.5,b-0.5)
	

def up(a,b):
	while a>-1:
		a=a-1
		if a==-1:
			pathtrace(a+0.5,b+0.5,a-0.5,b+0.5)
			exitcondition(a,b)
			
		elif array[a][b]== -2:
			pathtrace(a+0.5,b+0.5,a+0.5,b-0.5)
			left(a,b)
			
		elif array[a][b]==2:
			pathtrace(a+0.5,b+0.5,a+0.5,b+1.5)
			right(a,b)

		else:
			pathtrace(a+0.5,b+0.5,a-0.5,b+0.5)
			
		

def down(a,b):
	while a<m:
		a=a+1
		if a==m:
			pathtrace(a+0.5,b+0.5,a+1.5,b+0.5)
			exitcondition(a,b)

		elif array[a][b]== -2:
			pathtrace(a+0.5,b+0.5,a+0.5,b+1.5)
			right(a,b)
		
		elif array[a][b]==2:
			pathtrace(a+0.5,b+0.5,a+0.5,b-0.5)
			left(a,b)
		
		else:
			pathtrace(a+0.5,b+0.5,a+1.5,b+0.5)


def exitcondition(a,b):
	if a==m and b==n:
		print(1)
		plt.show()
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		quit()
	else:
		print(-1)
		plt.show()
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		quit()
		

#starting from the first cell as it will not be covered in right()
a=0
b=0
pathtrace(a+0.5, b, a+0.5, b+ 0.5)
if array[a][b]==-2:
	pathtrace(a+0.5, b+0.5, a+1.5, b+0.5)
	down(a,b)
elif array[a][b]==2:
	pathtrace(a+0.5, b+0.5, a, b+0.5)
	exitcondition()
else:
	pathtrace(a+0.5, b+0.5, a+0.5, b+1.5)
	right(a,b)


	



