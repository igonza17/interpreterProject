"""
Course: CS3642
Student name: Ivan Gonzalez
Student ID: 000837578
Assignment #: #2
Due Date: November 1 2020
"""
import random
#Keeps solving until herustic reaches 0 and stops the program from running
def checkIfSolved(h):
    print("Heuristic with this board state ", h)
    print()
    if(h == 0):
        print("N queen puzzled solved!")
        exit(1)

#Creates the visual representation of each board state at each movement
def printChessBoard(chess):
    # assigning list with empty values
    list = []
    for i in range(len(chess)):
        temp = []
        for j in range(len(chess)):
            temp.append("| |")
        list.append(temp)
    # assigning list with queens
    for i in range(len(chess)):
        list[chess[i]][i] = "|Q|"
    list2 = []
    # Start matrix from bottom to top
    for i in range(len(chess) - 1, -1, -1):
        list2.append(list[i])
    #Print matrix with the values and matrix
    length2 = len(chess) - 1
    for i in range(len(chess)):
        print("  ", i, end="")
    print()
    for i in list2:
        print(length2, end=" ")
        for j in i:
            print(j, end=" ")
        print()
        length2 -= 1

#Using steepest hill algorithm this should always reach lowest heuristic cost
def hillClimb(chess):
    index={}
    for column in range(len(chess)):
        for row in range(len(chess)):
            # not necessary to evaluate since we know the cost of heuristic
            if chess[column] == row:
                continue
            #make copy of chess board and move queen to new row
            copyChess = list(chess)
            copyChess[column] = row
            index[(column,row)] = getH(copyChess)
    moves = []
    cheapestH = getH(chess)
    #search for the cheapest heuristic
    for i, j in index.items():
        if j < cheapestH:
            cheapestH = j
    #Adds the moves to the list that have the lowest heuristic
    for i, j in index.items():
        if j == cheapestH:
            moves.append(i)

    #From the best moves list choose any random move
    if len(moves) > 0:
        rand = random.randint(0, len(moves) - 1 )
        column = moves[rand][0]
        row = moves[rand][1]
        chess[column]=row

    #print the index of all queens
    print("New board state " , chess)
    print()
    printChessBoard(chess)
    checkIfSolved(cheapestH)

#getH is a function to calculate the current heuristic of the board for each move
def getH(chess):
    h=0
    #Loop to check for queens in the same row and increase heuristic
    for i in range(len(chess)):
        for j in range(i+1,len(chess)):
            if chess[i]==chess[j]:
                h+=1
            #check if queens are diagonally in the way and increase heuristic
            if chess[i] == chess[j] - (j-i) or chess[i] == chess[j] + (j-i):
                h+=1
    return h
#Main method that initiates the hill climbing technique
if __name__ == '__main__':
    #Chooses the indexes of the queens in random for producing different puzzles
    randomlist = []
    for i in range(0,8):
        n = random.randint(0,7)
        randomlist.append(n)
    print(randomlist)
    heuristic = 0
    while(getH != 0 ):
        hillClimb(randomlist)