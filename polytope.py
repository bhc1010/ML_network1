from sympy.utilities.iterables import multiset_permutations
import numpy as np

class Polytope:
    
    def __init__(self, verts, picardNum, imbeddingDim):
        self.verts = verts
        self.imbeddingDim = imbeddingDim
        self.picardNum = picardNum
        self.baseVerts = [[self.verts]]
        self.altVerts = []          ## altVerts[[(_,_) , (_,_) , ...], [(_,_) , (_,_) , ...], ....] (no picard numbers)
        self.data = []              ## data[[([0,1,-1,-1,1,0,....], picardNum) , ...], ...]  

    def generateData(self):
        #### Imbed vectors into R^(imbeddingDim)
        if len(self.verts) != self.imbeddingDim:
            for i in range(len(self.verts), self.imbeddingDim, 1):
                self.verts.append((0,0))

        #### Construct transformations of base vectors and place each in a list wrapped in a master list
        ## Reflection across x-axis
        transformation = []
        for v in self.verts:
            x = v[0]
            y = v[1] * -1
            transformation.append((x,y))
        self.baseVerts.append([transformation])
        ## Reflection across y-axis
        transformation = []
        for v in self.verts:
            x = v[0] * -1
            y = v[1]
            transformation.append((x,y))
        self.baseVerts.append([transformation])
        ## Reflect x-coord and switch
        transformation = []
        for v in self.verts:
            x = v[1] 
            y = v[0] * -1
            transformation.append((x,y))
        self.baseVerts.append([transformation])       
        ## Reflect y-coord and switch     
        transformation = []
        for v in self.verts:
            x = v[1] * -1
            y = v[0]
            transformation.append((x,y))
        self.baseVerts.append([transformation])
        ## Reflection across x-axis and y-axis
        transformation = []
        for v in self.verts:
            x = v[0] * -1
            y = v[1] * -1
            transformation.append((x,y))
        self.baseVerts.append([transformation])
        ## Reflection across x-axis and y-axis and switch
        transformation = []
        for v in self.verts:
            x = v[1] * -1
            y = v[0] * -1
            transformation.append((x,y))
        self.baseVerts.append([transformation])

        #### Fill each transformation list with it's permutations
        for i in range(0, len(self.baseVerts)):
            temp = []
            for p in multiset_permutations(self.baseVerts[i][0]):
                temp.append(p)
            self.altVerts.append(temp)

        #### Vectorize each data point with it's 'picard number'
        vector = []
        R = []
        for i in range(0, len(self.altVerts)):
            for j in range(0, len(self.altVerts[i])):
                for v in self.altVerts[i][j]:
                    for elem in v:
                        vector.append(elem)
                R.append((vector, self.picardNum))
                vector = []
            self.data.append(R)
            R = []

# ## Testing new data formatting
# poly0 = Polytope([(0,1),(-1,-1)],[[1],[0]], 6)
# poly0.generateData()
# print("Base verts:")
# for i in range(0, len(poly0.baseVerts)):
#     for vert in poly0.baseVerts[i]:
#         print(vert)
# for i in range(0, len(poly0.data)):
#     print("Transformation {}: ".format(i))
#     for vert in poly0.data[i]:
#         print(vert)
