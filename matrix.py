import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

def dot_product(vector_one, vector_two):
    """
    Returns the dot product of two vectors
    """
    dot_prod = 0
    for i in range(len(vector_one)):
        dot_prod = dot_prod +  vector_one[i]*vector_two[i]
    return dot_prod
    
class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if (self.h == 1 and self.w == 1) :
            return self[0][0]
        elif self.h == 2:
            a = self[0][0]
            b = self[0][1]
            c = self[1][0]
            d = self[1][1]
            return (a*d - b*c)
        else:
            return

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")

        Sum = 0
        for i in range(self.h):
            Sum = Sum + self.g[i][i]
        
        return Sum

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        Inv = []
        Temp_det=self.determinant()
        Temp_trc=self.trace()
        Idnty=identity(self.h)
        Temp_Idnty=Temp_trc*Idnty
        if(self.h == 1):
            Inv = [[1/self.g[0][0]]]
            return Matrix(Inv)

        else:
            Diff=zeroes(self.h,self.w)
            Diff=Temp_Idnty - Matrix(self.g)
            Out_Diff=[]
            for i in range(self.h):
                Out_Diff_row=[]
                for j in range(self.w):
                    Out_Diff_row.append(Diff[i][j]/Temp_det)
                Out_Diff.append(Out_Diff_row)
                    
        
        return Matrix(Out_Diff)



    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        matrix_transpose = []
        for i in range(self.w):
            row = []
            for j in range(self.h):
                row.append(self[j][i])
            matrix_transpose.append(row)
        return Matrix(matrix_transpose)

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.
        Example:
        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]
        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        new_matrix = []
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(self.g[i][j] + other.g[i][j])
            new_matrix.append(row)
        
        return Matrix(new_matrix)
    
    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)
        Example:
        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        new_matrix = []
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(-1*self.g[i][j])
            new_matrix.append(row)
        
        return Matrix(new_matrix)

    def __sub__(self, other):
        Sub_out=[]
        Sub_out_temp=[]
        """
        Defines the behavior of - operator (as subtraction)
        """
        Sub_out_temp = (-other)
        Sub_out = self + Sub_out_temp
        return (Sub_out)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        product = []

        other_T = other.T()
    
        for i in range(self.h):
            row = []
            for j in range(other_T.h):
                row.append(dot_product(self.g[i],other_T.g[j]))
            product.append(row)
                
        return Matrix(product)

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.
        Example:
        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            new_matrix = []
            for i in range(self.h):
                row = []
                for j in range(self.w):
                    row.append(other*self[i][j])
                new_matrix.append(row)
            return Matrix(new_matrix)