import sys

from crossword import *
from operator import itemgetter


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Iterate over all the variables in self.domains.
        for var in self.domains:
            # Iterate over the possibles values for each variable, adding to 
            # wrong_words any values whose length is not equal to the variable's length.
            wrong_words = set([word for word in self.domains[var] 
                               if len(word) != var.length])
            # Update self.domains[var].
            for wrong_word in wrong_words:
                self.domains[var].remove(wrong_word)
                    
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap:
            i = overlap[0]
            j = overlap[1]
            
            # Add to wrong_words values from 'self.domains[x]' for which 
            # there is no possible corresponding value for 'y' in 'self.domains[y]'.
            wrong_words = set()
            for word_x in self.domains[x]:
                if word_x[i] not in [word_y[j] for word_y in self.domains[y]]:
                    wrong_words.add(word_x)
            # Remove from self.domains[x] words that make 'x' arc inconsistent with 'y'.
            if wrong_words:
                for wrong_word in wrong_words:
                    self.domains[x].remove(wrong_word)
                revised = True
                
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If arcs is None, begin with initial list of all arcs in the problem.        
        if arcs == None:
            arcs = [(x, y) for x in self.crossword.variables
                    for y in self.crossword.neighbors(x)]
        # AC3 algorithm.
        while arcs:
            x, y = arcs.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y} :
                    arcs.append((z, x))
        return True
        
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            # If a 'Variable' object is not in assignment, return False.
            if var not in assignment:
                return False
            # If a 'Variable' object doesn't have a value assigned, return False.
            if assignment[var] not in self.crossword.words:
                return  False
        return True
    
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """  
        # 1. All values must be distinct.
        distinct_words = {word for word in assignment.values()}
        if len(distinct_words) != len(assignment):
            return False
        
        # x and y will represent different variables.
        for x in assignment:
            # 2. Every value must be the correct length.
            if x.length != len(assignment[x]):
                return False
            # 3. There must not be conflicts between neighboring variables.
            for y in self.crossword.neighbors(x):
                overlap = self.crossword.overlaps[x, y]
                i = overlap[0]
                j = overlap[1]
                if y in assignment:
                    if assignment[x][i] != assignment[y][j]:
                        return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Ignore variables that already have a value asigned (are present in 
        # assignment).
        neighbors = [neighbor for neighbor in self.crossword.neighbors(var)
                     if neighbor not in assignment]

        # Create a list of tuples (word, count) where 'count' is the number of words that
        # would be eliminated from the domain of neighboring variables 'neighbors' if 'word' 
        # is asigned to 'var'.
        ls = []
        for word_1 in self.domains[var]:
            # Count the number of words that would be eliminated from the domain 
            # of neighboring variables if a word (word_1) is chosen.
            count = 0
            for neighbor in neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                i = overlap[0]
                j = overlap[1] 
                for word_2 in self.domains[neighbor]:
                    if word_1[i] != word_2[j]:
                        count += 1            
            ls.append((word_1, count))

        # Return a list of words in 'ls' sorted by 'count'.
        return [word for word, count in sorted(ls, key=itemgetter(1))]
 
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Create a list of tupples (var, values, degrees) where var is a 'Variable' 
        # object not already part of 'assignment'.
        ls = [(var, len(self.domains[var]), len(self.crossword.neighbors(var))) 
              for var in self.crossword.variables if var not in assignment]

        # Sort 'ls' by the number of remaining values in the domain of each variable.
        ls_values = sorted(ls, key=itemgetter(1))
        ls_values = [t for t in ls_values if t[1] == ls_values[0][1]]
        # Return the value with the minimum number of remaining values if there isn't a tie.
        if len(ls_values) == 1:
            return ls_values[0][0]
        
        # If there is a tie, sort 'ls_values' by the number of degrees of each variable.
        ls_degrees = sorted(ls_values, key=itemgetter(2), reverse=True)
        ls_degrees = [t for t in ls_degrees if t[2] == ls_degrees[0][2]]
        # Return the value with the highest number of degrees.
        return ls_degrees[0][0]

        
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Backtrack algorithm.
        # If assignment is complete, return the assignment.
        if self.assignment_complete(assignment):
            return assignment
        # Else select the unassigned variable that has the highest degree.
        var = self.select_unassigned_variable(assignment)
        # Try to make a new assignment, assign a value (word) to var.
        for word in self.order_domain_values(var, assignment):
            # If the assignment is consistent return the assignmet, else return None.
            assignment[var] = word
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
        return None
         

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
