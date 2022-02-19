from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# In each of the above puzzles, each character is either a knight or a knave.
# Every sentence spoken by a knight is true, and every sentence spoken by a knave is false.
starting_knowledgebase = And(
    # Game conditions: each caracter is either a knight or a knave
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(CKnave, CKnight),
    Not(And(AKnave, AKnight)),
    Not(And(BKnave, BKnight)),
    Not(And(CKnave, CKnight))

    # Every sentence spoken by a knight is true, and every sentence spoken by a knave is false
    # -> This can be translated to two Implications where the sentence is either True (Knight) or False (Knave)
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    starting_knowledgebase,

    # A says "I am both a knight and a knave."
    Implication(AKnave, Not(And(AKnave, AKnight))),
    Implication(AKnight, And(AKnave, AKnight)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    starting_knowledgebase,

    # A says "We are both knaves."
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    starting_knowledgebase,

    # ->
    # A says "We are the same kind."
    Implication(AKnave, Or(Not(And(AKnave, BKnave)),
                Not(And(AKnight, BKnight)))),
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),

    # B says "We are of different kinds."
    Implication(BKnave, Or(Not(And(AKnave, BKnight)),
                Not(And(AKnight, BKnave)))),
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),

    # ->
    # A says "We are the same kind."
    Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),

    # B says "We are of different kinds."
    Implication(BKnave, Not(Or(And(AKnave, BKnight), And(AKnight, BKnave)))),
    Implication(BKnave, Or(And(AKnave, BKnight), And(AKnight, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    starting_knowledgebase,

    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    # -> This is already implemented in the starting_knowledgebase
    
    # B says "A said 'I am a knave'."
    Implication(BKnave, Implication(AKnave, Not(AKnight))),
    Implication(BKnave, Implication(AKnight, AKnight)),
    
    Implication(BKnight, Implication(AKnave, Not(AKnave))),
    Implication(BKnight, Implication(AKnight, AKnave)),

    # B says "C is a knave."
    Implication(BKnave, Not(CKnave)),
    Implication(BKnight, CKnave),

    # C says "A is a knight."
    Implication(CKnave, Not(AKnight)),
    Implication(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()