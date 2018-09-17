import fwn_lib
from nltk.corpus import wordnet as wn

def find_largest_acyclic_subgraph(wn_graph, root):
  has_cyclic_subtree = set()
  for node in reversed(wn_graph.bfs_order(fwn_lib.Relation.HYPONYM, root)):
  # In reverse bfs order,
    print(node)
    print(wn_graph.children(fwn_lib.Relation.HYPERNYM, node))
    for child in wn_graph.children(fwn_lib.Relation.HYPONYM, node):
      if child in has_cyclic_subtree:
        has_cyclic_subtree.add(node)
        print("No")
        break
    if len(wn_graph.children(fwn_lib.Relation.HYPERNYM, node)) > 1:
      has_cyclic_subtree.add(node)
      print("No")
    else:  
      print("Yes")
   
  for node in wn_graph.bfs_order(fwn_lib.Relation.HYPONYM, root):
    if node not in has_cyclic_subtree:
      print node + "\t" + str(len(wn_graph.bfs_order(fwn_lib.Relation.HYPONYM,
                                                     node)))



def main():
  wn_graph = fwn_lib.WordnetGraph(wn)
  wn_graph.add_relation_subgraph(fwn_lib.Relation.HYPERNYM)
  wn_graph.add_relation_subgraph(fwn_lib.Relation.HYPONYM)

  print(len(wn_graph.bfs_order(fwn_lib.Relation.HYPONYM,
                               fwn_lib.ROOT_LEMMAS["Noun"].name())))
  find_largest_acyclic_subgraph(wn_graph,
                                fwn_lib.ROOT_LEMMAS[fwn_lib.PartOfSpeech.NOUN].name())

if __name__ == "__main__":
  main()

