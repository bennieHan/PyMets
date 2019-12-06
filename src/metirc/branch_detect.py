from src.model.swc_node import SwcTree,get_match_edges,get_default_threshold
from src.io.read_json import read_json
import time


# calculate confusion matrix，count branch number
def branch_detect(gold_swc_tree=None, test_swc_tree=None, knn=3, DEBUG=False):
    # gold中匹配到的，顺便test中匹配到的也有了
    match_edge = get_match_edges(gold_swc_tree, test_swc_tree, knn, DEBUG)
    gold_size = gold_swc_tree.node_count()
    test_size = test_swc_tree.node_count()

    # 检测到的gold/test分支数目
    true_positive = len(match_edge.keys())
    # 未重合的gold分支数目
    false_negative = (gold_size-1) - true_positive
    # 未重合的test分支数目
    true_negative = (test_size-1) - true_positive

    print("matched gold branch = {}/{}, rate = {}".format(true_positive, gold_size, true_positive/gold_size))
    print("incorrectly detected branching regions ={}/{}, rate = {}".format(true_negative, gold_size, true_negative/gold_size))
    print("missing branches ={}/{}, rate = {}".format(false_negative, gold_size, false_negative/gold_size))


if __name__ == "__main__":
    gold_swc_tree = SwcTree()
    gold_swc_tree.load("D:\gitProject\mine\PyMets\\test\data_example\gold\ExampleGoldStandard.swc")
    test_swc_tree = SwcTree()
    test_swc_tree.load("D:\gitProject\mine\PyMets\\test\data_example\\test\ExampleTest.swc")

    branch_detect(gold_swc_tree=gold_swc_tree,
                  test_swc_tree=test_swc_tree)