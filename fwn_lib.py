from nltk.corpus import wordnet as wn

class PartOfSpeech(object):
  ADJECTIVE = "Adjective"
  NOUN = "Noun"
  ADVERB = "Adverb"
  VERB = "Verb"

PARTS_OF_SPEECH = {
    'a': PartOfSpeech.ADJECTIVE,
    'n': PartOfSpeech.NOUN,
    'r': PartOfSpeech.ADVERB,
    'v': PartOfSpeech.VERB
}

class Relation(object):
  HYPERNYM = "HYPERNYM"
  HYPONYM = "HYPONYM"

RELATION_FUNCTIONS = {
    Relation.HYPERNYM : lambda synset: synset.hypernyms(),
    Relation.HYPONYM : lambda synset: synset.hyponyms()
}

class GraphConfig(object):
  def __init__(self):
    pass

class WordNetNode(object):
  def __init__(self, synset):
    self.synset = synset
    self.children = []

def print_edge(from_string, to_string, relation):
  print ("\t".join([from_string, to_string, relation]))

class StringTree(object):
  def __init__(self, wordnet_graph):
    self.root = StringNode(wordnet_graph.tree)
    self.relation = wordnet_graph.relation

  def dump_edges(self):
    root = self.root
    queue = [(None, root)]
    while queue:
      front_from, front_to = queue.pop()
      if front_from is not None:
        print_edge(front_from.name, front_to.name, self.relation)
      queue += [(front_to, child) for child in front_to.children]

  def dump_transitive_edges(self):
    pass


class StringNode(object):
  def __init__(self, wordnet_node):
    self.name = wordnet_node.synset.name()
    self.children = [StringNode(child) for child in wordnet_node.children]

class WordNetGraph(object):
  def __init__(self, relation, root_synset):
    self.relation = relation
    self.function = RELATION_FUNCTIONS[relation]
    self.root_synset = root_synset
    self.tree = self.make_tree()

  def make_tree(self):
    root = WordNetNode(self.root_synset)
    queue = [root]
    while queue:
      front = queue.pop()
      print front.synset.name()
      front.children = [WordNetNode(child) for child in
                        self.function(front.synset)]
      queue += front.children
    return root


ROOT_LEMMAS = {
    PartOfSpeech.NOUN : wn.synset('entity.n.01'),
}
