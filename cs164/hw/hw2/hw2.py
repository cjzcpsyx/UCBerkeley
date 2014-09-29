array = ["c", "a", "l"]
lambdas = []
for index in range(len(array)):
	lambdas.append((lambda x: array[x])(index))
print lambdas[0]
print lambdas[1]
print lambdas[2]
	