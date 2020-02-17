surface = []

with open('aveSuccess.txt', 'r') as data:

    for i in range(0,21):
        for j in range(1,21):
            success = float(data.readline().rstrip())
            surface.append((i, j, success))

with open('surface.dat', 'w') as out:
    for vert in surface:
        for i in range(0,2):
            out.write(str(vert[i]))
            out.write(",")
        out.write(str(vert[2]))
        out.write("\n")