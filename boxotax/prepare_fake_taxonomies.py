import fwn_lib
from nltk.corpus import wordnet as wn
import random

def should_retain_edge(p):
 """Bernoulli RV with mean p."""
 assert p <= 1 and p >= 0
 return random.uniform(0,1) < p

def find_acyclic_subgraphs(wn_graph, root):
  has_cyclic_subtree = set()
  for node in reversed(wn_graph.bfs_order(fwn_lib.Relation.HYPONYM, root)):
  # In reverse bfs order,
    for child in wn_graph.children(fwn_lib.Relation.HYPONYM, node):
      if child in has_cyclic_subtree:
        has_cyclic_subtree.add(node)
        break
    if len(wn_graph.children(fwn_lib.Relation.HYPERNYM, node)) > 1:
      has_cyclic_subtree.add(node)

  acyclic_subgraph_roots = []
  for node in wn_graph.bfs_order(fwn_lib.Relation.HYPONYM, root):
    if node not in has_cyclic_subtree:
      print "Y\t" + node + "\t" + str(len(
        wn_graph.bfs_order(fwn_lib.Relation.HYPONYM, node)))
      acyclic_subgraph_roots.append(
          (len(wn_graph.bfs_order(fwn_lib.Relation.HYPONYM, node)), node))
  return sorted(acyclic_subgraph_roots)

def thin_tree_out(relation_graph, inverse_relation_graph, root,
    probability_percent):
  """This is not guaranteed to work if the root is not the root of an acyclic
  subgraph in the relation graph."""
  bernoulli_percent = float(probability_percent)/100.0
  new_edge_list = []
  for parent, child in reversed(relation_graph.edge_pair_list(root)):
    if not should_retain_edge(bernoulli_percent):
      print("Deleting edge",parent, child)
      inverse_related_nodes = inverse_relation_graph.edges[parent]
      assert len(inverse_related_nodes) == 1
      new_edge_list.append((inverse_related_nodes[0], child))
    else:
      print("Retaining edge",parent, child)
      new_edge_list.append((parent, child))

  new_relation_graph = fwn_lib.RelationGraph(relation_graph.wn,
    relation_graph.synset_list,
    relation_graph.relation+"_"+str(probability_percent),
    edge_list=new_edge_list)
  return new_relation_graph


def main():
  random.seed(6)
  wn_graph = fwn_lib.WordnetGraph(wn)
  wn_graph.add_relation_subgraph(fwn_lib.Relation.HYPERNYM)
  wn_graph.add_relation_subgraph(fwn_lib.Relation.HYPONYM)

  p = wn_graph.edge_pair_list(fwn_lib.Relation.HYPONYM,
                               'igneous_rock.n.01')
  print(find_acyclic_subgraphs(wn_graph,
                                'igneous_rock.n.01'))

  new_rel_graph = thin_tree_out(wn_graph.relation_graphs[fwn_lib.Relation.HYPONYM],
                wn_graph.relation_graphs[fwn_lib.Relation.HYPERNYM],
                'igneous_rock.n.01', 50)
  print new_rel_graph.bfs_order('igneous_rock.n.01')
    
if __name__ == "__main__":
  main()

