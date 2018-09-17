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
    PartOfSpeech.NOUN : wn.synset('physical_entity.n.01'),
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
 
class SynsetList(object):
  # TODO: rename the list in this thing...
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

  def children(self, root):
    return self.edges[root]
    

class WordnetGraph(object):
  # TODO: see if this wn can be removed?
  def __init__(self, wn):
    self.synset_list = SynsetList(wn)
    self.wn = wn
    self.relation_graphs = {}

  def add_relation_subgraph(self, relation):
    self.relation_graphs[relation] = RelationGraph(self.wn, self.synset_list,
                                                   relation)

  def bfs_order(self, relation, root):
    return self.relation_graphs[relation].bfs_order(root)

  def children(self, relation, root):
    return self.relation_graphs[relation].children(root)

