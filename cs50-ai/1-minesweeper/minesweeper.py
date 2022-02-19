import itertools
import random
from copy import deepcopy


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

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        new_cells_set = self.cells
        if cell in self.cells:
            new_cells_set.remove(cell)
            self.count -= 1
        self.cells = new_cells_set
            
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        new_cells_set = self.cells
        if cell in self.cells:
            new_cells_set.remove(cell)
        self.cells = new_cells_set
        

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
        print('-----------------------------------------------------------------')
         
        # 1)
        self.moves_made.add(cell)
        
        # 2)
        self.mark_safe(cell)
                        
        # 3) 
        new_cells_set = set()
        counter_known_mines = 0
        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Check if (i, j) is a valid cell
                if 0 <= i <= self.height-1 and 0 <= j <= self.width-1:
                    # Only add cells to the sentence that have not been identified
                    if (i, j) in self.mines:
                        counter_known_mines += 1
                        continue
                    if (i, j) in self.safes:
                        continue
                    new_cells_set.add((i, j))
        new_sentence = Sentence(cells=new_cells_set, 
                               count=count-counter_known_mines)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)
        
        # Repeat steps 4 and 5 while KB changes
        while True:
            # Save a copy of the KB to check if it changes after steps 4 and 5
            copy_kb = deepcopy(self.knowledge)
            
            # 4)
            print('Printing KB:')
            self.update_knowledge()
            # 5)
            self.compare_sentences()
        
            # Break the loop if the KB has not changed in this process
            if copy_kb == self.knowledge:
                break
   
        print(f'Known mines: {len(self.mines)}')
        print(f'Known safes: {len(self.safes)}')
        print(f'Remaining safe moves: {len(self.safes - self.moves_made)}')
    
    def clean_kb(self):
        """
        Removes repeating and empty sentences in the KB
        """
        cleaned_kb = []
        for sentence in self.knowledge:
            if sentence not in cleaned_kb and len(sentence.cells) != 0:
                cleaned_kb.append(sentence)
        self.knowledge = cleaned_kb
        
    def compare_sentences(self):
        """
        Compare sentences in the KB in pairs (permutations) checking if 
        new knowledge can be infered.
    
        --> sent_1's set of cells being a subset of sent_2's set of cells
        sent_1 => {(3, 4), (3, 6)} = 1
        sent_2 => {(5, 1), (3, 4), (3, 6)} = 2
        new_sent => {(5, 1)} = 1
        
        """
        # Clean KB
        self.clean_kb()

        new_sentences = []
        for sentences in itertools.permutations(self.knowledge[:], 2):
            cells_1 = sentences[0].cells
            cells_2 = sentences[1].cells
            count_1 = sentences[0].count
            count_2 = sentences[1].count
            
            if cells_1.issubset(cells_2):
                new_sentences.append(Sentence(cells=cells_2 - cells_1, 
                                              count=count_2 - count_1))
                    
        for new_sentence in new_sentences:
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)
    
    def update_knowledge(self):
        """
        Loop through each sentence in the knowledge base to update the sentence
        if possible, removing cells that have been already identified
        """
        mines_set = set()
        safes_set = set()
        
        for sentence in self.knowledge:
            print(f'\t{sentence}')
            # Check if cells in the sentence have been identified as mines
            if sentence.known_mines():
                for cell_in_set in sentence.known_mines():
                    mines_set.add(cell_in_set)
            # Check if cells in the sentence have been identified as safes
            if sentence.known_safes():
                for cell_in_set in sentence.known_safes():
                    safes_set.add(cell_in_set)
                    
        # Update the KB                    
        for cell_mine in mines_set:
            self.mark_mine(cell_mine)
        for cell_safe in safes_set:
            self.mark_safe(cell_safe)
        
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Save all possible moves in a set
        possible_moves = set()
        for safe_move in self.safes:
            if safe_move not in self.moves_made:
                possible_moves.add(safe_move)
        # If no possible moves, return None
        if len(possible_moves) == 0:
            return None
        # Return a random possible move
        return random.choice(sorted(possible_moves))

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Save all possible moves in a set
        possible_moves = set()
        for i in range(0, self.height-1):
            for j in range(0, self.width-1):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possible_moves.add((i, j))            
        # If no possible moves return None
        if len(possible_moves) == 0:
            return None
        # Return a random possible move
        move = random.choice(sorted(possible_moves))
        print(f'AI about to make random move: {move}')
        return move
        
