"""
Student: Amit Finzi
Assignment no. 6
Program: minesweeper.py
"""
from random import randint
import copy

class MSSquare:
    '''represents each square of the gameboard'''
    def __init__(self,has_mine,hidden,neighbor_mines):
        self.has_mine = has_mine
        self.hidden = hidden
        self.neighbor_mines = neighbor_mines
    @property
    def neighbor_mines(self):
        return self.__neighbor_mines
    @neighbor_mines.setter
    def neighbor_mines(self,neighbor_mines):
        if not isinstance(neighbor_mines, int):
            raise Exception('num of mines by the square must be an int')
        if neighbor_mines>8 or neighbor_mines<0:
            raise Exception('the number of mines by the square doesnt fit')
        self.__neighbor_mines = neighbor_mines
    @property
    def has_mine(self):
        return self.__has_mine
    @has_mine.setter
    def has_mine(self,has_mine):
        if not isinstance(has_mine, bool):
            raise Exception('mine existance has to be True or False')
        self.__has_mine = has_mine
    @property
    def hidden(self):
        return self.__hidden
    @hidden.setter
    def hidden(self,hidden):
        if not isinstance(hidden, bool):
            raise Exception('the square has to be hidden or exposed ')
        self.__hidden = hidden
    def __str__(self):
        if self.__hidden:
            return '   '
        else:
            if self.__has_mine:
                return ' X '
            return f' {self.__neighbor_mines} '

def neighbor_mines(size,r,c,mines_loc):
    '''checking if there are mines in the near squares and count them'''
    count=0
    avl=[]
    for i in range(-1,2,1):
        for j in range(-1,2,1):
            if r+i>0 and c+j>0 and r+i<=size and c+j<=size and [r+i,c+j]!=[r,c]:
                avl.append([r+i,c+j])
    for neighbors in avl:
        if neighbors in mines_loc:
            count+=1
    return count

def no_mines(size,r,c,mines_loc,content):
    '''find the closest square with a mine'''
    content[r-1][c-1].hidden = False
    content[r-1][c-1].neighbor_mines = neighbor_mines(size, r, c, mines_loc)
    if content[r-1][c-1].neighbor_mines>0:
        return content
    else:
        avl=[]
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                if r+i>0 and c+j>0 and r+i<=size and c+j<=size and [r+i,c+j]!=[r,c]:
                    if content[r+i-1][c+j-1].hidden:
                        avl.append([r+i,c+j])
        for neighbors in avl:
            no_mines(size, neighbors[0], neighbors[1], mines_loc,content)

def board(size,r,c,mines_loc,content):
    '''building the game board'''
    content[r-1][c-1].hidden = False
    print(' +',end='')
    print('---+'*size)
    for i in range(size):
        for j in range(size):
            if j==0:
                print(i+1,end='|')
            print(str(content[i][j])+'|',end='')
        print()
        print(' +',end='')
        print('---+'*size)
    for num in range(size):
        if num ==size-1:
            print(f'   {num+1}')
        else:
            print(f'   {num+1}',end='')

def main():
    size = int(input('Please enter the size of the board: '))
    if not isinstance(size, int):
        raise Exception('size must be an integer')
    if size>9 or size<4:
        raise Exception('size must be between 4-9')
    print(' +',end='')
    print('---+'*size)
    for i in range(size):
        for j in range(size):
            if j==0:
                print(i+1,end='|')
            print('   |',end='')
        print()
        print(' +',end='')
        print('---+'*size)
    for num in range(size):
        if num ==size-1:
            print(f'   {num+1}')
        else:
            print(f'   {num+1}',end='')
    mines_num = int(input('Please enter the number of mines: '))
    if not isinstance(mines_num,int):
        raise Exception('the number of mines must be an integer')
    if mines_num>2*size or mines_num<1:
        raise Exception(f'The number of the mines has to be in the range of 1-{2*size}')
    r = int(input("Enter the row (horizental) youd like to chose: "))
    if not isinstance(r,int):
        raise Exception('r must be an integer!')
    if r>size or r<1:
        raise Exception('row index out of range')
    c = int(input("Enter the column (vertical) youd like to chose: "))
    if not isinstance(c,int):
        raise Exception('c must be an integer!')
    if c>size or c<1:
        raise Exception('column index out of range')
    i = 0
    mines_loc = []
    while i<mines_num:
        x= [randint(1,size),randint(1,size)]
        if x not in mines_loc and x!=[r,c]:
            mines_loc.append(x)
            i+=1
    s=MSSquare(False,True,neighbor_mines(size, r, c, mines_loc))
    content = [[copy.copy(s) for i in range(size)] for j in range(size)]
    while True:
        exposed=0
        content[r-1][c-1].neighbor_mines = neighbor_mines(size, r, c, mines_loc)
        content[r-1][c-1].hidden = False
        if [r,c] in mines_loc:
            content[r-1][c-1].has_mine=True
        if content[r-1][c-1].neighbor_mines==0:
            no_mines(size, r, c, mines_loc, content)
        board(size, r, c, mines_loc, content)
        if content[r-1][c-1].has_mine and not content[r-1][c-1].hidden:
            for i in mines_loc:
                content[i[0]-1][i[1]-1].has_mine =True
                content[i[0]-1][i[1]-1].hidden = False
            board(size, r, c, mines_loc, content)
            print('you lost!')
            break
        for i in range(len(content)):
            for j in range(len(content[i])):
                if not content[i][j].hidden:
                    exposed+=1
        if (size**2)-mines_num==exposed:
            board(size, r, c, mines_loc, content)
            print('you won!')
            break
        if size**2-(mines_num+exposed)==1:
            print(f'{(size**2)-(mines_num+exposed)} square still hidden')
        else:
            print(f'{(size**2)-(mines_num+exposed)} squares still hidden')
        r = int(input("Enter the row (horizental) youd like to chose: "))
        if not isinstance(r,int):
            raise Exception('r must be an integer!')
        if r>size or r<1:
            raise Exception('row index out of range')
        c = int(input("Enter the column (vertical) youd like to chose: "))
        if not isinstance(c,int):
            raise Exception('c must be an integer!')
        if c>size or c<1:
            raise Exception('column index out of range')


if __name__=='__main__':
    main()




