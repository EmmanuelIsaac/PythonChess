import numpy
#### quad hash comments are notes for future variant implementation

#### we want to be able to create all kinds of weird pieces
#### name is a current placeholder for the fundamental 'core' of a piece.
#### i.e. pieces with the same name are the same - name will likely be a 'moveset' class eventually
class piece:

    def __init__(self, name, visual, is_white):
        self.name = name
        self.visual = visual #string for cmd print
        self.is_white = is_white #boolean
        self.square = "" #will point to the square the piece occupies

    ## square the piece is occupying
    def changeSquare(self, sq):

        self.square = sq

    ## returns True, if white
    def isWhite(self):

        return self.is_white

    ## returns visual of piece
    def reVisual(self):

        return self.visual
    
    ## returns name of piece
    def reName(self):

        return self.name
    
    ## returns square piece is occupying
    def reSquare(self):

        return self.square

#### likely need a removePiece method 
class square:

    def __init__(self, point):
     #### extend the adjX to be lists, so that we can have multiple of the same kind of adjacency?
        self.point = point #each square knows its coordinate on the board
        self.adjN = "" #empty string default value, will store square objects
        self.adjNE = ""
        self.adjE = ""
        self.adjSE = ""
        self.adjS = ""
        self.adjSW = ""
        self.adjW = ""
        self.adjNW = ""

        self.pieces = [] #for list of pieces on square
        self.main_visual = "-" #string for cmd print
        self.move_visual = "-" #different string for the move display board
    
    ## takes in either 0 or a square for each variable. 
    ## variables start with north (adjN) then progress clockwise.
    def addCompassAdj(self, adjN, adjNE, adjE, adjSE, adjS, adjSW, adjW, adjNW):
        
        #if value is not 0, update pointer
        if adjN != 0:
            self.adjN = adjN
        if adjNE != 0:    
            self.adjNE = adjNE
        if adjE != 0:
            self.adjE = adjE
        if adjSE != 0:
            self.adjSE = adjSE
        if adjS != 0:
            self.adjS = adjS
        if adjSW != 0:
            self.adjSW = adjSW
        if adjW != 0:
            self.adjW = adjW
        if adjNW != 0:
            self.adjNW = adjNW

    ## append piece to piece list
    def addPiece(self, piece):

        self.pieces.append(piece)
    
    ## explicitly for adding moveset visual
    def addMoveVisual(self, visstr):

        self.move_visual = visstr

    ## dir = "8","9","6","3","2","1","4","7" (num pad directions)
    ## check if square has adjacency in direction
    def hasCompassAdj(self, dir):
        if dir == "8":
            if self.adjN == "":
                return False
            else:
                return True
        if dir == "9":
            if self.adjNE == "":
                return False
            else:
                return True
        if dir == "6":
            if self.adjE == "":
                return False
            else:
                return True
        if dir == "3":
            if self.adjSE == "":
                return False
            else:
                return True
        if dir == "2":
            if self.adjS == "":
                return False
            else:    
                return True
        if dir == "1":
            if self.adjSW == "":
                return False
            else: 
                return True
        if dir == "4":
            if self.adjW == "":
                return False
            else: 
                return True
        if dir == "7":
            if self.adjNW == "":
                return False
            else: 
                return True

    ## check if square has any piece
    def hasPiece(self):
        if self.pieces == []:
            return False
        else: 
            return True

    def clearPieces(self):

        self.pieces = []


    ## reFunctions each return desired property

    ## returns square adjacency in required direction
    def reCompassAdj(self, dir):
        if dir == "8":
            return self.adjN
        if dir == "9":
            return self.adjNE
        if dir == "6":
            return self.adjE
        if dir == "3":
            return self.adjSE
        if dir == "2":
            return self.adjS
        if dir == "1":
            return self.adjSW
        if dir == "4":
            return self.adjW
        if dir == "7":
            return self.adjNW

    #### may be useful, not coded yet
    def reAllCompassAdj(self):

        return ""

    def rePiece(self):

        return self.pieces

    def rePoint(self):

        return self.point  

    ## main board visual, i.e. piece visual or default visual
    def reVisual(self):

        if len(self.pieces) == 0:
            return "-"
        elif len(self.pieces) == 1:
            return self.rePiece()[0].reVisual()
        else:
            return
    
    def reMoveVisual(self):

        return self.move_visual
       
    
class game:

    def __init__(self):

        self.board = []
        self.pieces = {}
        self.piece_moveset = {}
        self.white_turn = True
        self.turn_num = 1

    def createBoard(self, xdim, ydim):
        #### other kinds of board constructions>
        #### maybe add type variable?
        #### currently running on type = standard

        #### add edge case check?
        #### -> xdim, ydim > 0

        ## board is xdim by ydim array of squares
        self.board = numpy.empty(shape=(xdim, ydim), dtype=square)

        for i in range(xdim):
            for j in range(ydim):
                self.board[(i,j)] = square((i,j))
 
     ## takes in a point (of square which is being given adjacencies)
     ## and a list of numpad directions
     ## called 'Standard'Adj, as the adjacent square is found by moving one step in the cartesian plane
     ## (e.g. this wouldn't work for cylinder adjacencies, because the points would move off of the board)
    def addStandardAdj(self, point, list):

        N,NE,E,SE,S,SW,W,NW = 0,0,0,0,0,0,0,0

        if "8" in list:
            N = self.board[(point[0], point[1] + 1)]
        if "9" in list:
            NE = self.board[(point[0] + 1, point[1] + 1)]
        if "6" in list:
            E = self.board[(point[0] + 1, point[1])]
        if "3" in list:
            SE = self.board[(point[0] + 1, point[1] - 1)]
        if "2" in list:
            S = self.board[(point[0], point[1] - 1)]
        if "1" in list:
            SW = self.board[(point[0] - 1, point[1] - 1)]
        if "4" in list:
            W = self.board[(point[0] - 1, point[1])]
        if "7" in list:
            NW = self.board[(point[0] - 1, point[1] + 1)]

        self.board[(point)].addCompassAdj(N,NE,E,SE,S,SW,W,NW)


    ## set adjacencies on the board in a particular way
    ## standard => standard chess board
    def setAdjacencies(self, type):
        #### addStandardAdj method, maybe change to add"type"Adj.

        if type == "standard":
            xdim = self.board.shape[0]
            ydim = self.board.shape[1]

            #corner squares
            self.addStandardAdj((0,0),["8","9","6"]) #bottom left square
            self.addStandardAdj((xdim - 1,0),["4","7","8"]) #bottom right square
            self.addStandardAdj((0, ydim - 1),["6","3","2"]) #top left square
            self.addStandardAdj((xdim - 1, ydim - 1),["4","1","2"]) #top right square

            #edge squares (not including corners)
            for i in [(x, 0) for x in range(1, xdim - 1)]: #bottom row squares
                self.addStandardAdj(i,["4","7","8","9","6"])
            for i in [(x, ydim - 1) for x in range(1, xdim - 1)]: #top row squares
                self.addStandardAdj(i,["4","1","2","3","6"])
            for i in [(0, y) for y in range(1, ydim - 1)]: #left column squares
                self.addStandardAdj(i,["8","9","6","3","2"])
            for i in [(xdim - 1, y) for y in range(1, ydim - 1)]: #right column squares
                self.addStandardAdj(i,["8","7","4","1","2"])

            #all center squares
            for i in range(1,xdim-1):
                for j in range(1,ydim-1):
                    self.addStandardAdj((i,j),["8","9","6","3","2","1","4","7"])
    
    ## creates pieces, stored in a dictionary
    ## standard => standard piece set
    def createPieces(self,type):

        if type == "standard":

            #pawns
            for i in range(0,self.board.shape[0]):
                self.pieces["WP" + str(i + 1)] = piece("white_pawn","p",True)
                self.pieces["BP" + str(i + 1)] = piece("black_pawn","P",False)

            #minor/major pieces
            self.pieces["WR1"] = piece("rook","r",True)
            self.pieces["WN1"] = piece("knight","n",True)
            self.pieces["WB1"] = piece("bishop","b",True)
            self.pieces["WQ1"] = piece("queen","q",True)
            self.pieces["WK1"] = piece("king","k",True)
            self.pieces["WB2"] = piece("bishop","b",True)
            self.pieces["WN2"] = piece("knight","n",True)
            self.pieces["WR2"] = piece("rook","r",True)

            self.pieces["BR1"] = piece("rook","R",False)
            self.pieces["BN1"] = piece("knight","N",False)
            self.pieces["BB1"] = piece("bishop","B",False)
            self.pieces["BQ1"] = piece("queen","Q",False)
            self.pieces["BK1"] = piece("king","K",False)
            self.pieces["BB2"] = piece("bishop","B",False)
            self.pieces["BN2"] = piece("knight","N",False)
            self.pieces["BR2"] = piece("rook","R",False)


    ## sets up pieces on the board in a particular way
    ## standard => standard chess board setup
    #### should we give pieces a pointer back to the square they occupy??
    #### depends on the moveset calculations in the future.
    def setPieces(self, type):

        #### currently standard is only 8x8 restriction
        ## --> maybe add individual pieces one at a time, or parse a string which encodes the choices.
        if type == "standard":
            xdim = self.board.shape[0]
            ydim = self.board.shape[1]
            
            #we need to call another function to change the square of the piece
            #this is because a square does not point to itself, only it's point on the board
            ####might be something to change in the future
            ####the modified addPiece function would replace changeSquare function  

            #pawns
            for i in range(xdim):
                self.board[(i,1)].addPiece(self.pieces["WP" + str(i + 1)])
                self.pieces["WP" + str(i + 1)].changeSquare(self.board[(i,1)])
                self.board[(i, ydim - 2)].addPiece(self.pieces["BP" + str(i + 1)])
                self.pieces["BP" + str(i + 1)].changeSquare(self.board[(i, ydim - 2)])

            #minor/major pieces
            self.board[(0,0)].addPiece(self.pieces["WR1"])
            self.pieces["WR1"].changeSquare(self.board[(0,0)])
            self.board[(1,0)].addPiece(self.pieces["WN1"])
            self.pieces["WN1"].changeSquare(self.board[(1,0)])
            self.board[(2,0)].addPiece(self.pieces["WB1"])
            self.pieces["WB1"].changeSquare(self.board[(2,0)])
            self.board[(3,0)].addPiece(self.pieces["WQ1"])
            self.pieces["WQ1"].changeSquare(self.board[(3,0)])
            self.board[(4,0)].addPiece(self.pieces["WK1"])
            self.pieces["WK1"].changeSquare(self.board[(4,0)])
            self.board[(5,0)].addPiece(self.pieces["WB2"])
            self.pieces["WB2"].changeSquare(self.board[(5,0)])
            self.board[(6,0)].addPiece(self.pieces["WN2"])
            self.pieces["WN2"].changeSquare(self.board[(6,0)])
            self.board[(7,0)].addPiece(self.pieces["WR2"])
            self.pieces["WR2"].changeSquare(self.board[(7,0)])

            self.board[(0,ydim-1)].addPiece(self.pieces["BR1"])
            self.pieces["BR1"].changeSquare(self.board[(0,ydim-1)])
            self.board[(1,ydim-1)].addPiece(self.pieces["BN1"])
            self.pieces["BN1"].changeSquare(self.board[(1,ydim-1)])
            self.board[(2,ydim-1)].addPiece(self.pieces["BB1"])
            self.pieces["BB1"].changeSquare(self.board[(2,ydim-1)])
            self.board[(3,ydim-1)].addPiece(self.pieces["BQ1"])
            self.pieces["BQ1"].changeSquare(self.board[(3,ydim-1)])
            self.board[(4,ydim-1)].addPiece(self.pieces["BK1"])
            self.pieces["BK1"].changeSquare(self.board[(4,ydim-1)])
            self.board[(5,ydim-1)].addPiece(self.pieces["BB2"])
            self.pieces["BB2"].changeSquare(self.board[(5,ydim-1)])
            self.board[(6,ydim-1)].addPiece(self.pieces["BN2"])
            self.pieces["BN2"].changeSquare(self.board[(6,ydim-1)])
            self.board[(7,ydim-1)].addPiece(self.pieces["BR2"])
            self.pieces["BR2"].changeSquare(self.board[(7,ydim-1)])

    ##scouts out a linear path via adjacencies and noting info for each square.
    def linearScout(self, startpoint, dir):

        ####passing in startpoint is probably not optimal.
        ####currently just assuming there is one piece occupying square
        startcol = self.board[startpoint].rePiece()[0].isWhite()
        originalpoint = startpoint #needed for edge case, where path covers square piece already occupies
        scout_list = [] #of form [((point), direction, occupation), ...] each list is a particular linear path
        occupation = "" #will take value O for open, X for enemy, F for friendly.

        while self.board[startpoint].hasCompassAdj(dir): #while adjacent square exists (in given direction)
            startpoint = self.board[startpoint].reCompassAdj(dir).rePoint() #reset start point to the adjacent square.

            if self.board[startpoint].hasPiece(): #if there is a piece on the square
                if self.board[startpoint].rePiece()[0].isWhite() == startcol: #if piece is the same colour
                    occupation = "F" #friendly occupation
                else:
                    occupation = "X" #enemy occupation
            else: #### will likely need to add other kinds of occupation.
                occupation = "O" #otherwise open

            if not (startpoint, dir, occupation) in scout_list: #add newly scouted square to list, if not already in list 
                if not startpoint == originalpoint: #edge case, original square appears friendly occupied, but will free up during move.
                    scout_list.append((startpoint, dir, occupation))
                else:
                    scout_list.append((startpoint, dir, "O")) ####we can have an additional flag here, if we want to decide whether original square is open.
            else: #if we are back where we started, exit while loop.
                   break

        return scout_list

    ##very similar to linear path, but looping over a finite set sequence of directions.
    def pathScout(self, startpoint, dirstr):
        
        startcol = self.board[startpoint].rePiece()[0].isWhite() 
        originalpoint = startpoint
        scout_list = []
        occupation = ""

        for i in dirstr:
            if self.board[startpoint].hasCompassAdj(i): #check existance of adjacent square
                startpoint = self.board[startpoint].reCompassAdj(i).rePoint() #reset start point to the adjacent square.

                if self.board[startpoint].hasPiece(): #if there is a piece on the square
                    if self.board[startpoint].rePiece()[0].isWhite() == startcol: #if piece is the same colour
                        occupation = "F" #friendly occupation
                    else:
                        occupation = "X" #enemy occupation
                else: #### will likely need to add other kinds of occupation.
                    occupation = "O" #otherwise open

                if not (startpoint, i, occupation) in scout_list: #add newly scouted square to list, if not already in list 
                    if not startpoint == originalpoint: #edge case, original square appears friendly occupied, but will free up during move.
                        scout_list.append((startpoint, i, occupation))
                    else:
                        scout_list.append((startpoint, i, "O")) ####we can have an additional flag here, if we want to decide whether original square is open.
                else: #if we are back where we started, exit while loop.
                      break
            else:
                break #if there is no adjacent square, exit loop. 

        return scout_list

    ## currently only needs linearScout and pathScout for standard chess and many additional variants
    def fullScout(self):

        #### eventually need this to be dependent on active variants
        #### i.e. more scouting (=information) may need to be done for the later filters.

        fullscout = [] #will have form [(piece, [[linearScout list dir1],[linearScout list dir2],...]), ...]

        for piece in self.pieces.values(): #looping over pieces in pieces dictionary (game class init variable)
            fullscout.append((piece, [])) #appending new element of correct form

            #we scout differently depending on how each piece moves (####this will be made more general at some point)
            #fullscout_list[-1][1], accesses the second element of the tuple (the list) of the most recent element of the fullscout_list
            #i.e. we are modifying one new entry for each piece in the loop.
            if piece.reName() == "white_pawn": 
                for i in ["8","7","9"]:
                    fullscout[-1][1].append(self.linearScout(piece.reSquare().rePoint(), i))
            elif piece.reName() == "black_pawn":
                for i in ["2","1","3"]:
                    fullscout[-1][1].append(self.linearScout(piece.reSquare().rePoint(), i))
            elif piece.reName() == "knight":
                for i in ["886","884","668","662","226","224","448","442","866","844","688","622","244","266","488","422"]:
                    fullscout[-1][1].append(self.pathScout(piece.reSquare().rePoint(), i))
            elif piece.reName() == "bishop":
                for i in ["9","3","1","7"]:
                    fullscout[-1][1].append(self.linearScout(piece.reSquare().rePoint(), i))
            elif piece.reName() == "rook":
                for i in ["8","6","2","4"]:
                    fullscout[-1][1].append(self.linearScout(piece.reSquare().rePoint(), i))
            elif piece.reName() == "queen":
                for i in ["9","3","1","7","8","6","2","4"]:
                    fullscout[-1][1].append(self.linearScout(piece.reSquare().rePoint(), i))
            elif piece.reName() == "king":
                for i in ["9","3","1","7","8","6","2","4"]:
                    fullscout[-1][1].append(self.linearScout(piece.reSquare().rePoint(), i))
            else:
                continue

        return fullscout

    #### testing only returning list of points (e.g. no occupation)
    ## this filters the scoutpath to terminate at an occupied square
    ## enemyocc and friendlyocc determine whether the occupied square is included
    #### blockFilter, finiteblockFilter and captureblockFilter should likely all be merged.
    def blockFilter(self, enemyocc, friendlyocc, scoutlists):

        moverange = []

        for tuplelist in scoutlists:
            if not tuplelist == []:
                for tuples in tuplelist:
                    if tuples[2] == "X":
                        if enemyocc:
                            moverange.append(tuples[0])
                        break
                    elif tuples[2] == "F":
                        if friendlyocc:
                            moverange.append(tuples[0])
                        break
                    else: #if not enemy or friendly occupied => open ####for now
                        moverange.append(tuples[0])

        return moverange

    def finiteblockFilter(self, steps, enemyocc, friendlyocc, scoutlists):

        moverange = []
        
        #[(piece, [[linearScout list dir1],[linearScout list dir2],...]), ...]
        for tuplelist in scoutlists:
            i = 0
            if not tuplelist == []:
                for tuples in tuplelist:
                    if tuples[2] == "X":
                        if enemyocc:
                            moverange.append(tuples[0])
                        break
                    elif tuples[2] == "F":
                        if friendlyocc:
                            moverange.append(tuples[0])
                        break
                    else: #if not enemy or friendly occupied => open ####for now
                        moverange.append(tuples[0])
                        i += 1
                        if i == steps:
                            break

        return moverange

    def captureblockFilter(self, steps, enemyocc, friendlyocc, scoutlists):

        moverange = []
        
        #[(piece, [[linearScout list dir1],[linearScout list dir2],...]), ...]
        for tuplelist in scoutlists:
            i = 0
            if not tuplelist == []:
                for tuples in tuplelist:
                    if tuples[2] == "X":
                        if enemyocc:
                            moverange.append(tuples[0])
                        break
                    elif tuples[2] == "F":
                        if friendlyocc:
                            moverange.append(tuples[0])
                        break
                    else: #if not enemy or friendly occupied => open ####for now
                        #removed adding unocc squares
                        i += 1
                        if i == steps:
                            break

        return moverange

    def endFilter(self, enemyocc, friendlyocc, scoutlists):

        moverange = []

        for pathtuples in scoutlists:
            if len(pathtuples) > 0:
                if pathtuples[-1][2] == "X":
                    if enemyocc:
                        moverange.append(pathtuples[-1][0])
                elif pathtuples[-1][2] == "F":
                    if friendlyocc:
                        moverange.append(pathtuples[-1][0])
                else:
                    moverange.append(pathtuples[-1][0])

        return moverange



    def filterScout(self, fullscout, type):

        #### may be better to seperate white and black movesets
        

        if type == "standard":
            for piecescout in fullscout: #### we want the movesets to be passed in such a way that the seperate directions can be more easily filtered.
                if piecescout[0].reName() == "white_pawn":
                    
                    self.piece_moveset[piecescout[0]] = []    
                    for pathtuples in piecescout[1]:
                        if len(pathtuples) > 0:
                            if pathtuples[0][1] == "8": ### can the ((point), dir, occ) tuple be empty
                                if piecescout[0].reSquare().rePoint()[1] == 1: #if white pawn on second row
                                    self.piece_moveset[piecescout[0]].extend(self.finiteblockFilter(2, False, False, [pathtuples]))
                                else:
                                    self.piece_moveset[piecescout[0]].extend(self.finiteblockFilter(1, False, False, [pathtuples]))
                            elif pathtuples[0][1] == "7" or pathtuples[0][1] == "9":
                                self.piece_moveset[piecescout[0]].extend(self.captureblockFilter(1, True, False, [pathtuples]))


                elif piecescout[0].reName() == "black_pawn":

                    self.piece_moveset[piecescout[0]] = []    
                    for pathtuples in piecescout[1]:
                        if len(pathtuples) > 0:
                            if pathtuples[0][1] == "2": ### can the ((point), dir, occ) tuple be empty
                                if piecescout[0].reSquare().rePoint()[1] == 6: #if black pawn on second row
                                    self.piece_moveset[piecescout[0]].extend(self.finiteblockFilter(2, False, False, [pathtuples]))
                                else:
                                    self.piece_moveset[piecescout[0]].extend(self.finiteblockFilter(1, False, False, [pathtuples]))
                            elif pathtuples[0][1] == "1" or pathtuples[0][1] == "3":
                                self.piece_moveset[piecescout[0]].extend(self.captureblockFilter(1, True, False, [pathtuples]))

                elif piecescout[0].reName() == "knight":
                    self.piece_moveset[piecescout[0]] = self.endFilter(True, False, piecescout[1])
                if piecescout[0].reName() == "bishop":
                    self.piece_moveset[piecescout[0]] = self.blockFilter(True, False, piecescout[1])
                elif piecescout[0].reName() == "rook":
                    self.piece_moveset[piecescout[0]] = self.blockFilter(True, False, piecescout[1]) #list of board point tuples.
                elif piecescout[0].reName() == "queen":
                    self.piece_moveset[piecescout[0]] = self.blockFilter(True, False, piecescout[1])
                elif piecescout[0].reName() == "king":
                    self.piece_moveset[piecescout[0]] = self.finiteblockFilter(1, True, False, piecescout[1])
                else:
                    continue
    
    def movePiece(self, piece, dest_point):

        piece.reSquare().clearPieces()

        if self.board[dest_point].hasPiece():
            key = ""
            for k in self.pieces.keys():
                if self.pieces[k] == self.board[dest_point].rePiece()[0]:
                       key = k

            del self.pieces[key]
            self.board[dest_point].clearPieces()

        piece.changeSquare(self.board[dest_point])
        self.board[dest_point].addPiece(piece)
       

        self.white_turn = not self.white_turn
        self.turn_num += 1  

    def selectPieceSquare(self):

        valid_square = False

        self.printBoard()
        while not valid_square:
            strinput = input("Select a square contaning a friendly piece" + "\n")
            #strinput = "1 1"
            chosen_point = tuple(map(int, strinput.split(" ")))


            if self.board[chosen_point].hasPiece():

                piece = self.board[chosen_point].rePiece()[0]

                if piece.isWhite() == self.white_turn:
                    
                    valid_square = True
                    return chosen_point

                else:
                    if self.white_turn:
                        print("White to move, this is a black piece.")
                    else:
                        print("Black to move, this is a white piece.")

            else:
                print("This square does not contain a piece.")

    def selectDestSquare(self, point):

        piece = self.board[point].rePiece()[0]

        for p in self.piece_moveset[piece]:
            if self.board[p].hasPiece():
                if self.board[p].rePiece()[0].isWhite() != self.white_turn:
                    self.board[p].addMoveVisual("x")
                    #### currently leaving friendly occupation option
            else: 
                self.board[p].addMoveVisual("o")


        self.printBoardMove()

        strinput = input("Select a square to move to:" + " " + str(self.piece_moveset[piece]) + "\n")
        chosen_point = tuple(map(int, strinput.split(" ")))

        while not chosen_point in self.piece_moveset[piece]:
            print("")
            print("This square is not in range, please try again:")
            strinput = input("")
            chosen_point = tuple(map(int, strinput.split(" ")))
        
        for p in self.piece_moveset[piece]:
            self.board[p].addMoveVisual("-")

        return chosen_point


    def selectNotation(self):

        xdim = self.board.shape[0]
        ydim = self.board.shape[1]

        sqnotation = {} ####This should be a seperate function called 3 times (here and both the print functions)
        letter = {0 : "a", 1 : "b", 2 : "c", 3: "d", 4 : "e", 5 : "f", 6 : "g", 7 : "h"}

        for i in range(0, xdim):
            for j in range(0, ydim):
                sqnotation[letter[i] + str(j + 1)] = (i, j)

        nmap = {"white_pawn": "pawn", "black_pawn": "pawn", "knight":"knight", "bishop":"bishop", "rook":"rook", "queen":"queen", "king":"king"}
        pnotation = {"P": "pawn","N": "knight", "B":"bishop","R":"rook", "Q":"queen", "K":"king"}

        self.printBoard()
        notation = input("Input Move: ")


        keylist = []
        if len(notation) == 2:
            notation = "P" + notation

        if len(notation) == 3:
            if notation[0] in ["P","N","B","R","Q","K"]:
                for key, value in self.piece_moveset.items():
                    if nmap[key.reName()] == pnotation[notation[0]]:

                        if key.isWhite() == self.white_turn:
                    
                            if sqnotation[notation[1:3]] in value:
                                keylist.append(key)

        #    elif notation[0] in ["a","b","c","d","e","f","g","h"]: #dealing with pawn

        #if len(notation) == 4:
        #    if notation[0] in ["P","N","B","R","Q","K"]:

        

        if len(keylist) == 0: #then there are no pieces that contain the destination square
            print("This is an invalid move.")
            self.selectNotation() ##temp debug
        elif len(keylist) == 1: #then we have a non-ambiguous move
            
            self.movePiece(keylist[0], sqnotation[notation[1:3]])

        else: #len(keylist) > 1
            print("This move requires more specification.")
            ###actually give choices...
            self.selectNotation() ##temp debug


                   
    #### potentially generalises to 'addVariant(self,variant)'
    def addCylinder(self):

        xdim = self.board.shape[0]
        ydim = self.board.shape[1]

        #edge columns adding 3 adjacencies for each square.
        for i in range(1, ydim - 1):
            self.board[(0,i)].addCompassAdj(0,0,0,0,0,self.board[(xdim - 1,i - 1)],self.board[(xdim - 1,i)],self.board[(xdim - 1,i + 1)])
            self.board[(xdim - 1,i)].addCompassAdj(0,self.board[(0,i + 1)],self.board[(0,i)],self.board[(0,i - 1)],0,0,0,0)

        #corners are a seperate case, only adding 2 adjacencies for each corner
        self.board[(0,0)].addCompassAdj(0,0,0,0,0,0,self.board[(xdim - 1,0)],self.board[(xdim - 1,1)])
        self.board[(0,ydim-1)].addCompassAdj(0,0,0,0,0,self.board[(xdim - 1,ydim - 2)],self.board[(xdim - 1,ydim - 1)],0)
        self.board[(xdim-1,ydim-1)].addCompassAdj(0,0,self.board[(0,ydim - 1)],self.board[(0,ydim - 2)],0,0,0,0)
        self.board[(xdim-1,0)].addCompassAdj(0,self.board[(0,1)],self.board[(0,0)],0,0,0,0,0)

    def startGame(self):

        winCon = False

        while winCon == False:

            self.filterScout(self.fullScout(),"standard")

            piece_point = self.selectPieceSquare() #self.printBoard() in here
            print("--------------------------------------------------")
            dest_point = self.selectDestSquare(piece_point) #self.printMoveBoard() in here
            print("--------------------------------------------------")

            piece = self.board[piece_point].rePiece()[0] ####chess+ consideration
            ####passing in piece is more specific than piece_point.
            self.movePiece(piece, dest_point) #incrementing self.turn_num and switching self.white_turn

    def startQuickMoveGame(self):

        winCon = False

        while winCon == False:

            self.filterScout(self.fullScout(),"standard")

            self.selectNotation()
            print("--------------------------------------------------")

    def printBoard(self):

        xdim = self.board.shape[0]
        ydim = self.board.shape[1]

        d = {}
        letter = {0 : "a", 1 : "b", 2 : "c", 3: "d", 4 : "e", 5 : "f", 6 : "g", 7 : "h"}

        for i in range(0, xdim):
            for j in range(0, ydim):
                d[letter[i] + str(j + 1)] = self.board[(i,j)].reVisual()
                d[letter[i] + str(j + 1) + "2"] = self.board[(i,j)].reMoveVisual()

        if self.white_turn:
            colour = "White"
        else:
            colour = "Black"

        print("Move" + " " + str(self.turn_num) + " - " + colour + " to Play")
        print("\n")
        print("-8-  | " + d["a8"] + " | " + d["b8"] + " | " + d["c8"] + " | " + d["d8"] + " | " + d["e8"] + " | " + d["f8"] +" | " + d["g8"] + " | " + d["h8"] + " | " + "\n")
        print("-7-  | " + d["a7"] + " | " + d["b7"] + " | " + d["c7"] + " | " + d["d7"] + " | " + d["e7"] + " | " + d["f7"] +" | " + d["g7"] + " | " + d["h7"] + " | " + "\n")
        print("-6-  | " + d["a6"] + " | " + d["b6"] + " | " + d["c6"] + " | " + d["d6"] + " | " + d["e6"] + " | " + d["f6"] +" | " + d["g6"] + " | " + d["h6"] + " | " + "\n")
        print("-5-  | " + d["a5"] + " | " + d["b5"] + " | " + d["c5"] + " | " + d["d5"] + " | " + d["e5"] + " | " + d["f5"] +" | " + d["g5"] + " | " + d["h5"] + " | " + "\n")
        print("-4-  | " + d["a4"] + " | " + d["b4"] + " | " + d["c4"] + " | " + d["d4"] + " | " + d["e4"] + " | " + d["f4"] +" | " + d["g4"] + " | " + d["h4"] + " | " + "\n")
        print("-3-  | " + d["a3"] + " | " + d["b3"] + " | " + d["c3"] + " | " + d["d3"] + " | " + d["e3"] + " | " + d["f3"] +" | " + d["g3"] + " | " + d["h3"] + " | " + "\n")
        print("-2-  | " + d["a2"] + " | " + d["b2"] + " | " + d["c2"] + " | " + d["d2"] + " | " + d["e2"] + " | " + d["f2"] +" | " + d["g2"] + " | " + d["h2"] + " | " + "\n")
        print("-1-  | " + d["a1"] + " | " + d["b1"] + " | " + d["c1"] + " | " + d["d1"] + " | " + d["e1"] + " | " + d["f1"] +" | " + d["g1"] + " | " + d["h1"] + " | " + "\n")
        print("      " + "-A-" + " -B-" + " -C-" + " -D-" + " -E-" + " -F-" + " -G-" + " -H-" + "\n")

    ## this is gross, and only works for an 8x8 board. it will be generalised (n, m) and neat (e.g. looping print, rather than print per-line), when moving to graphic visualisation.
    def printBoardMove(self):

        xdim = self.board.shape[0]
        ydim = self.board.shape[1]

        d = {}
        letter = {0 : "a", 1 : "b", 2 : "c", 3: "d", 4 : "e", 5 : "f", 6 : "g", 7 : "h"}

        for i in range(0, xdim):
            for j in range(0, ydim):
                d[letter[i] + str(j + 1)] = self.board[(i,j)].reVisual()
                d[letter[i] + str(j + 1) + "2"] = self.board[(i,j)].reMoveVisual()
        
        if self.white_turn:
            colour = "White"
        else:
            colour = "Black"

        print("Move" + " " + str(self.turn_num) + " - " + colour + " to Play")
        print("\n")
        print("-8-  | " + d["a8"] + " | " + d["b8"] + " | " + d["c8"] + " | " + d["d8"] + " | " + d["e8"] + " | " + d["f8"] +" | " + d["g8"] + " | " + d["h8"] + " | " + "      " + "-8-  | " + d["a82"] + " | " + d["b82"] + " | " + d["c82"] + " | " + d["d82"] + " | " + d["e82"] + " | " + d["f82"] +" | " + d["g82"] + " | " + d["h82"] + " | " + "\n")
        print("-7-  | " + d["a7"] + " | " + d["b7"] + " | " + d["c7"] + " | " + d["d7"] + " | " + d["e7"] + " | " + d["f7"] +" | " + d["g7"] + " | " + d["h7"] + " | " + "      " + "-7-  | " + d["a72"] + " | " + d["b72"] + " | " + d["c72"] + " | " + d["d72"] + " | " + d["e72"] + " | " + d["f72"] +" | " + d["g72"] + " | " + d["h72"] + " | " + "\n")
        print("-6-  | " + d["a6"] + " | " + d["b6"] + " | " + d["c6"] + " | " + d["d6"] + " | " + d["e6"] + " | " + d["f6"] +" | " + d["g6"] + " | " + d["h6"] + " | " + "      " + "-6-  | " + d["a62"] + " | " + d["b62"] + " | " + d["c62"] + " | " + d["d62"] + " | " + d["e62"] + " | " + d["f62"] +" | " + d["g62"] + " | " + d["h62"] + " | " + "\n")
        print("-5-  | " + d["a5"] + " | " + d["b5"] + " | " + d["c5"] + " | " + d["d5"] + " | " + d["e5"] + " | " + d["f5"] +" | " + d["g5"] + " | " + d["h5"] + " | " + "      " + "-5-  | " + d["a52"] + " | " + d["b52"] + " | " + d["c52"] + " | " + d["d52"] + " | " + d["e52"] + " | " + d["f52"] +" | " + d["g52"] + " | " + d["h52"] + " | " + "\n")
        print("-4-  | " + d["a4"] + " | " + d["b4"] + " | " + d["c4"] + " | " + d["d4"] + " | " + d["e4"] + " | " + d["f4"] +" | " + d["g4"] + " | " + d["h4"] + " | " + "      " + "-4-  | " + d["a42"] + " | " + d["b42"] + " | " + d["c42"] + " | " + d["d42"] + " | " + d["e42"] + " | " + d["f42"] +" | " + d["g42"] + " | " + d["h42"] + " | " + "\n")
        print("-3-  | " + d["a3"] + " | " + d["b3"] + " | " + d["c3"] + " | " + d["d3"] + " | " + d["e3"] + " | " + d["f3"] +" | " + d["g3"] + " | " + d["h3"] + " | " + "      " + "-3-  | " + d["a32"] + " | " + d["b32"] + " | " + d["c32"] + " | " + d["d32"] + " | " + d["e32"] + " | " + d["f32"] +" | " + d["g32"] + " | " + d["h32"] + " | " + "\n")
        print("-2-  | " + d["a2"] + " | " + d["b2"] + " | " + d["c2"] + " | " + d["d2"] + " | " + d["e2"] + " | " + d["f2"] +" | " + d["g2"] + " | " + d["h2"] + " | " + "      " + "-2-  | " + d["a22"] + " | " + d["b22"] + " | " + d["c22"] + " | " + d["d22"] + " | " + d["e22"] + " | " + d["f22"] +" | " + d["g22"] + " | " + d["h22"] + " | " + "\n")
        print("-1-  | " + d["a1"] + " | " + d["b1"] + " | " + d["c1"] + " | " + d["d1"] + " | " + d["e1"] + " | " + d["f1"] +" | " + d["g1"] + " | " + d["h1"] + " | " + "      " + "-1-  | " + d["a12"] + " | " + d["b12"] + " | " + d["c12"] + " | " + d["d12"] + " | " + d["e12"] + " | " + d["f12"] +" | " + d["g12"] + " | " + d["h12"] + " | " + "\n")
        print("      " + "-A-" + " -B-" + " -C-" + " -D-" + " -E-" + " -F-" + " -G-" + " -H-" + "      " + "        " + "-A-" + " -B-" + " -C-" + " -D-" + " -E-" + " -F-" + " -G-" + " -H-" + "\n")



new_game = game()
new_game.createBoard(8,8)
new_game.setAdjacencies("standard")
##optionally add cylinder adjacencies to board
#new_game.addCylinder()
new_game.createPieces("standard")
new_game.setPieces("standard")

##starting a game this way uses quick chess notation
##e.g. "e4" pawn move, "Ne4" knight move
##there is no difference in notation for taking pieces
new_game.startQuickMoveGame()
##starting a game this way will show a visual of how each piece can move
##refer to squares with "x y" format, where 0 0 is the bottom left of board
#new_game.startGame()



