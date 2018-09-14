#from nltk.corpus.reader import wordnet as wn2
from nltk.corpus import wordnet as wn

class PartOfSpeech(object):
  ADJECTIVE="ADJECTIVE"
  NOUN="NOUN"
  ADVERB="ADVERB"
  VERB="VERB"

class Relation(object):
  HYPERNYM = "HYPERNYM"
  HYPONYM = "HYPONYM"

RELATION_FUNCTIONS = {
  Relation.HYPERNYM : lambda synset:synset.hypernyms(),
  Relation.HYPONYM : lambda synset:synset.hyponyms()
}  

class GraphConfig(object):
  def __init__(self):
    pass

  
PARTS_OF_SPEECH = {
  'a': PartOfSpeech.ADJECTIVE,
  'n': PartOfSpeech.NOUN,
  'r': PartOfSpeech.ADVERB,
  'v': PartOfSpeech.VERB
}  


class WordNetNode(object):
  def __init__(self, synset):
    self.synset = synset
    self.children = []

class WordNetGraph(object):
  def __init__(self, wn, relation, root_synset):
    self.wn = wn
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
      queue+=front.children


ROOT_LEMMAS = {
  PartOfSpeech.NOUN : wn.synset('entity.n.01'),
}
