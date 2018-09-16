from nltk.corpus import wordnet as wn
import collections

class PartOfSpeech(object):  # pylint: disable=too-few-public-methods 
  ADJECTIVE = "Adjective"
  NOUN = "Noun"
  ADVERB = "Adverb"
  VERB = "Verb"

class Relation(object):   # pylint: disable=too-few-public-methods
  HYPERNYM = "HYPERNYM"
  HYPONYM = "HYPONYM"

PARTS_OF_SPEECH = {
    'a': PartOfSpeech.ADJECTIVE,
    'n': PartOfSpeech.NOUN,
    'r': PartOfSpeech.ADVERB,
    'v': PartOfSpeech.VERB
}

ROOT_LEMMAS = {
    PartOfSpeech.NOUN : wn.synset('alloy.n.01'),
}

RELATION_FUNCTIONS = {
    Relation.HYPERNYM : lambda synset: synset.hypernyms(),
    Relation.HYPONYM : lambda synset: synset.hyponyms()
}

INVERSE_FUNCTIONS = {
    Relation.HYPERNYM : lambda synset: synset.hyponyms(),
    Relation.HYPONYM : lambda synset: synset.hypernyms()
}

def print_edge(from_string, to_string, relation, dist=None):
  fields = [from_string, to_string, relation]
  if dist is not None:
    fields.append(str(dist))
  print ("\t".join(fields))

class StringNode(object):
  def __init__(self, wordnet_node):
    self.name = wordnet_node.synset.name()
    self.children = [StringNode(child) for child in wordnet_node.children]

class StringTree(object):
  def __init__(self, wordnet_graph):
    self.root = StringNode(wordnet_graph.tree)
    self.relation = wordnet_graph.relation

  def dump_edges(self):
    root = self.root
    # TODO: Create a dummy root
    queue = [(None, root)]
    while queue:
      front_from, front_to = queue.pop()
      if front_from is not None:
        print_edge(front_from.name, front_to.name, self.relation)
      queue += [(front_to, child) for child in front_to.children]

  def BFS(self, root, ancestors, seen):
    ancestors.append(root)
    for child in root.children:
      if child.name in seen:
        print("Seen: "+child.name)
        break
      distance = len(ancestors)
      for ancestor in ancestors:
        print "\t".join([ancestor.name, child.name, str(distance)])
        distance -= 1
      self.BFS(child, list(ancestors), seen)
    seen.add(root.name)

class WordNetNode(object):
  def __init__(self, synset):
    self.synset = synset
    self.children = []
    self.is_ancestor_to_cycle = False

class WordNetGraph(object):
  def __init__(self, relation, root_synset):
    self.relation = relation
    self.function = RELATION_FUNCTIONS[relation]
    self.inverse_function = INVERSE_FUNCTIONS[relation]
    self.root_synset = root_synset
    self.tree = self.make_tree()

  def make_tree(self):
    root = WordNetNode(self.root_synset)
    queue = [root]
    while queue:
      front = queue.pop()
      front.children = [WordNetNode(child) for child in
                        self.function(front.synset)]
      queue += front.children
    return root

  def BFS_order(self):
    bfs_order = []
    root = self.tree
    bfs_order.append(root)
    current_index = 0
    while current_index < len(bfs_order):
      children = bfs_order[current_index].children
      for child in children:
        if child not in bfs_order:
          bfs_order.append(child)
      current_index += 1
      print len(bfs_order)
    return bfs_order

  def label_cycles(self):
    for node in reversed(self.BFS_order()):
      print(node.synset.name())
      for child in node.children:
        if child.is_ancestor_to_cycle:
          node.is_ancestor_to_cycle = True
          continue
      print(node.synset.name())  
      print(self.inverse_function(node.synset))  
      if len(self.inverse_function(node.synset)) > 1:
        self.is_ancestor_to_cycle = True

  def print_whether_cycles(self):
    for node in self.BFS_order():
      print(node.synset.name()+"\t"+str(node.is_ancestor_to_cycle))
        

class LeanTree(object):
  def __init__(self, wn):
    synset_list = tuple(sorted(synset.name() for synset in wn.all_synsets()))
    assert len(synset_list) == len(set(synset_list))
    self.edge_lists = collections.defaultdict(dict)
    self.relations_represented = []

  def add_edges(self, relation):
    relation_function = RELATION_FUNCTIONS[relation]
    for synset in wn.all_synsets():
      self.edge_lists[relation][synset.name()] = [related_synset.name() 
                                                for related_synset in
                                                relation_function(synset)]

  def bfs_order(self, relation, root):
    bfs_order = [root]
    current_index = 0
    while current_index < len(bfs_order):
      children = self.edge_lists[relation][bfs_order[current_index]]
      for child in children:
        if child not in bfs_order:
          bfs_order.append(child)
      current_index += 1
    return bfs_order

class SynsetList(object):
  def __init__(self, wn):
    self.synset_list = tuple(sorted(synset.name() for synset in wn.all_synsets()))
    assert len(self.synset_list) == len(set(self.synset_list))

class RelationGraph(object):
  def __init__(self, wn, synset_list, relation
              ):
    self.wn = wn
    self.edges = {}
    self.relation = relation
    self.relation_function = RELATION_FUNCTIONS[relation]
    self.synset_list = synset_list
    self.add_edges()

  def add_edges(self):  
    for synset in wn.all_synsets():
      self.edges[synset.name()] = [related_synset.name() 
                                                for related_synset in
                                                self.relation_function(synset)]
    #print(self.edges.keys())
    print(self.edges['alloy.n.01'])

  def bfs_order(self, root):
    bfs_order = [root]
    current_index = 0
    while current_index < len(bfs_order):
      current_synset = bfs_order[current_index]
      if current_synset in self.edges:
        children = self.edges[bfs_order[current_index]]
        for child in children:
          if child not in bfs_order:
            bfs_order.append(child)
      current_index += 1
    return bfs_order

    

class WordnetGraph(object):
  def __init__(self, wn):
    self.synset_list = SynsetList(wn)
    self.wn = wn
    self.relation_graphs = {}

  def add_relation_subgraph(self, relation):
    self.relation_graphs[relation] = RelationGraph(self.wn, self.synset_list,
                                                   relation)

  def bfs_order(self, relation, root):
    return self.relation_graphs[relation].bfs_order(root)

