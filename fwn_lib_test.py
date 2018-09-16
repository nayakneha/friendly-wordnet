import fwn_lib
from nltk.corpus import wordnet as wn

def setup_test_bfs_order():
  k = fwn_lib.WordnetGraph(wn)
  k.add_relation_subgraph(fwn_lib.Relation.HYPERNYM)
  assert len(k.synset_list.synset_list) == 117659

def test_bfs_order():
      assert 1 == 1

def teardown_module():
  print("B")

