print("Forloop example 1")
for i  in range(0,5):
	print(i)
print("Forloop example 2")
for i  in range(0,10+1,2):
	print(i)
print("Forloop example 3")
for x  in range(2,4+1):
	print("Value of x:" , x)
print("Forloop example 4")
for i in range(1,3+1):
	for j in range(1,3+1):
		print(i," ",j)
print("For loop example 5")
it = None
for it  in range(0,5):
	print(it)
a = 0
for i  in range(0,50):
	a=a+1
	if a==6:
		break
	elif a==7:
		continue
print(a)
