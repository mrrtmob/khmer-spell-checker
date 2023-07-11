import os
from typing import List
import xml.etree.cElementTree as ET
import sys

class Node:
    def __init__(self, word: str, children, parent=None) -> None:
        self.word = word
        self.parent = parent
        self.children = children

    def same_weight_child(self, weight: int):
        try:
            return self.children[[w for (w, node) in self.children].index(weight)][1]
        except:
            return None

def edit_distance(word1: str, word2: str) -> int:
    """ Calculates the Levenstein Distance between `word1` and `word2`.
    Args:
    ---
    - `word1`: The first word.
    - `word2`: The second word.

    Returns:
    ---
    The distance between `word1` and `word2`
    """
    num_cols = len(word1) + 1
    num_rows = len(word2) + 1

    memoize = [[None for c in range(num_cols)] for r in range(num_rows)]

    for col_idx in range(0, num_cols):
        memoize[0][col_idx] = col_idx

    for row_idx in range(0, num_rows):
        memoize[row_idx][0] = row_idx

    for row_idx in range(1, num_rows):
        for col_idx in range(1, num_cols):
            left_n = memoize[row_idx][col_idx-1]
            top_n = memoize[row_idx-1][col_idx]
            cross_n = memoize[row_idx-1][col_idx-1]

            neighbours = [left_n, top_n, cross_n]
            min_n = min(neighbours)

            if word1[col_idx-1] != word2[row_idx-1]:
                memoize[row_idx][col_idx] = min_n + 1
            else:
                memoize[row_idx][col_idx] = cross_n

    return memoize[num_rows-1][num_cols-1]


class SpellChecker:
    """ The spell check uses the popular combination of Levenstein Distance (Edit Distance) and the BK-Tree to quickly search for correct word suggestions. """

    def __init__(self, model_path: str = None) -> None:
        if model_path is None:
            model_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "model.xml")
            # print(ET.parse(model_path).getroot()[0])
        self.root = ET.parse(model_path).getroot()[0]

    def suggest(self, word: str, num_suggestions: int = 3, N: int = 2) -> List[str]:
        """ Suggests a list of corrections for `word`.

        Args
        ---
        - `word`: The word to get suggestions for.
        - `num_suggestions`: The number of suggestions to return.

        Returns
        ---
        A list of suggested corrections.
        """
        matches = []

        stack: List[ET.Element] = [self.root]

        while len(stack) != 0:
            curr_node = stack.pop()
            curr_node_word = curr_node.attrib["word"]
            distance_curr_node = edit_distance(word, curr_node.attrib["word"])
            if distance_curr_node <= N and (curr_node_word, distance_curr_node) not in matches:
                matches.append((curr_node_word, distance_curr_node))

            for child in curr_node.find("children"):
                child_weight = int(child.attrib["weight"])
                if child_weight >= (distance_curr_node - N) and child_weight <= (distance_curr_node + N):
                    stack.append(child)

        return [match[0] for match in sorted(matches, key=lambda x: x[1])][:num_suggestions]

spell_checker = SpellChecker()
word = 'សាលា'

print(spell_checker.suggest(word))
['គោលនាម', 'គោត្រនាម', 'កិតនាម']
['សាលា', 'សាល', 'សលា']