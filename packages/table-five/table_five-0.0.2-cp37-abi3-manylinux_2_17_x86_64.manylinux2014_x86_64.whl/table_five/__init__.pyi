from typing import List, Tuple

class TreeSet:
    """
    Specialized set of trees with LCA precomputed sharing the same taxon set.

    :param newick_path: path to the file with trees in Newick format, delimited by new line
    """
    def __init__(self, newick_path: str) -> None : ...

    def tally_single_quintet(self, five_taxa: Tuple[str, str, str, str, str]) -> List[int]:
        """
        Gets empirical gene tree topology counts across all trees.
        Element i denotes the number of gene trees that display topology number i on the five taxa.
        See the ADR paper, table 5 for how the topologies are numbered (but here we use 0-based indexing).

        :param five_taxa: tuple of five taxa names. The order matters.
        :return: a list of length 15 containing integer counts of the unrooted quintet topologies
        """