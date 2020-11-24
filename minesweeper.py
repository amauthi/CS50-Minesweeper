import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    # Accessors
    def getCells(self):
        return self.cells
    
    def getCount(self):
        return self.count

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        setMines = set()
        
        for cell in self.cells:
            if self.is_mine(self, cell) == True:
                setMines.add(cell)
        
        return setMines


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        setSafes = set()
        
        for cell in self.cells:
            if self.is_mine(self, cell) == False:
                setSafes.add(cell)
                
        return setSafes


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            # remove cell from sentence
            self.cells.remove(cell)
            # we decrement the count value, since we found a mine
            print("mark a mine and decreasing of count for sentence")
            self.count-=1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.*
        """
        
        if cell in self.cells:
            # remove cell from sentence
            self.cells.remove(cell)
        
#        print("inside mark_safe")


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        
        
        safe cell, how many neighboring cells have mines in them.

        This function should:           
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`               
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
               
        """
        
        # 1 : mark the cell as a move that has been made
        self.moves_made.add(cell)
        
        # 2 : mark the cell as safe
        self.mark_safe(cell)#, cell)
        print("mark cell as safe :", cell)
        
        
        # 3 : add a new sentence to the AI's knowledge base
        #     based on the value of `cell` and `count`
        # we should add as many cells as the number of count
        # we must only add cells which are not labelled safe of mined
        
        i, j = cell
        # list of the neighboring cells
        cells = []
        for k in range(3):
            for l in range(3):
                # respect of the edges
                if i+k-1 < self.width and i+k-1 >= 0 and j+l-1 < self.height and j+l-1 >= 0:
                    cellToAdd = i+k-1, j+l-1
                    # adding cell if not a mine and not safe
                    if cellToAdd not in self.mines and cellToAdd not in self.safes:
                        print("adding to sentence : ", cellToAdd)
                        cells.append(cellToAdd)
                    # before adding the count to the sentence, we have to make 
                    # sure that there is no mines in the neighbors cells
                    # because the count would correspond to those mined cells
                    if cellToAdd in self.mines:
                        count-=1
                    
        
        # we add the neighboring cells (when there are) and the count of the 
        # center cell into a new sentence
        if len(cells) != 0:
            print("count to add in sentence = ", count)
            newSentence = Sentence(cells, count)
            self.knowledge.append(newSentence)

        
        for sentence in self.knowledge:
            # if a sentence contains no more cells, it is removed from the knowledge
            if len(sentence.getCells()) == 0:
                self.knowledge.remove(sentence)
            # print all sentences
            print("sentence : ")
            for c in sentence.getCells():
                print(c, end="")
            print(" count = ", sentence.getCount())
    
        
        # 4 : mark any additional cells as safe or as mines
        #     if it can be concluded based on the AI's knowledge base
        
        # 4.2 :if sentence.cell <= sentence.count, it means that all the cells  
        # are mines
        for sentence in self.knowledge:
            if sentence.getCount() != 0:
                if len(sentence.getCells()) <= sentence.getCount():
                    print("len sentence = ", len(sentence.getCells()))
                    print("count de la sentence =", sentence.getCount())
                    for c in sentence.getCells().copy():
                        print("!!!!!!!!!!!!!!!! adding as mined cell : ", c)
                        self.mark_mine(c)                     
         
        # 4.3 : if count != 0, we have to use knowledge    
        # if count != 0:
        #     # we search the sentence where cell appears
        #     for sentence in self.knowledge:
        #         if cell in sentence:
        
#        for sentence in self.knowledge:
            if sentence.getCount() == 0:
                for c in sentence.getCells().copy():
                    print("adding as safe cell : ", c)
                    self.mark_safe(c)
                self.knowledge.remove(sentence)
        
        # 5 : add any new sentences to the AI's knowledge base if they can be
        #     inferred from existing knowledge
        # if we have two sentences, with one being a componend of the other
        # for ex : s1 : "[A, B, C] = 3 and s2 = "[A, B] = 1"
        # then we can create a third sentence s3, with :
        # s3 : "[C] = 3-1 = 2"
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 != sentence2:
                    if len(sentence1.getCells()) > len(sentence2.getCells()):
                        # we want to remove the smallest from the biggest sentence
                        sentence1, sentence2 = sentence2, sentence1
                    # check if sentence1 is a subset of sentence2
                    if sentence1.getCells() and sentence1.getCells().issubset(sentence2.getCells()):
                        print("create new sentence from 2 sentences")
                        print("Sentence 1 : ")
                        for s in sentence1.getCells():
                            print(s, end='')
                        print("count = ", sentence1.getCount())
                        print("Sentence 2 : ")
                        for s in sentence2.getCells():
                            print(s, end='')
                        print("count = ", sentence2.getCount())
                        
                        newCells = set()
                        # building of a new sentence, we only add cells that are in sentence2
                        for c in sentence2.getCells():
                            if c not in sentence1.getCells():
                                newCells.add(c)
                                
                        newKnowledge = Sentence(newCells, 
                                                sentence2.getCount() -
                                                sentence1.getCount())
                        
                        # check that we don't create a sentence that aleady exist
                        isNewKnowledge = True
                        
                        for sentence in self.knowledge:
                            if newKnowledge == sentence:
                                isNewKnowledge = False
                            
                        
                        # if the sentence is not yet a part of knowledge, we add it
                        if isNewKnowledge:    
                            print("NEW SENTENCE : ")
                            for s in newCells:
                                print(s, end='')
                            print("count : ", newKnowledge.getCount())
                            self.knowledge.append(newKnowledge)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print("inside make_safe_move")
        
        # visualisation of all the moves we still have
        for cell in self.safes:
            if cell not in self.moves_made:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!! safe move = ", cell)
        
        # for move in self.moves_made:
        #     print("move = ", move)
        
        # visualisation of all the mines cells
        for cell in self.mines:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! mined cell", cell)

        for cell in self.safes:
            if cell not in self.moves_made:
                print("in make_safe_move, safe_move = ", cell)
                return cell  


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
    
        """
        
        
        print("inside make_random_move")
        
        move_ok = False
        
        while move_ok == False: 
            i = random.randrange(self.width)
            j = random.randrange(self.height)
            randomChoice = (i,j)
            if randomChoice not in self.mines:
                if randomChoice not in self.moves_made:
                    print("random Choice =", randomChoice)
                    return randomChoice
            else:
                return None
