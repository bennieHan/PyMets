from anytree import NodeMixin, iterators, RenderTree, PreOrderIter
from pymets.model.euclidean_point import EuclideanPoint,Line
from pymets.model.swc_node import SwcTree
from pymets.metric.utils.edge_match_utils import get_match_edges_e,get_unmatch_edges_e,get_match_edges_e_fast
from pymets.metric.utils.config_utils import get_default_threshold
from pymets.io.read_json import read_json
from pymets.io.save_swc import save_as_swc,print_swc

import time


def length_metric_3(gold_swc_tree=None, test_swc_tree=None, DEBUG=False):
    test_swc_tree.get_lca_preprocess()
    match_fail = get_unmatch_edges_e(gold_swc_tree, test_swc_tree)

    return match_fail


def length_metric_2_1(gold_swc_tree=None, test_swc_tree=None, dis_threshold=0.1, DEBUG=False):
    match_edges = get_match_edges_e_fast(gold_swc_tree, test_swc_tree,dis_threshold, DEBUG=True)

    match_length = 0.0
    for line_tuple in match_edges:
        match_length += line_tuple[0].parent_distance()

    gold_total_length = round(gold_swc_tree.length(),8)
    match_length = round(match_length,8)

    if DEBUG:
        print("match_length a = {}, gold_total_length = {}"
              .format(match_length, gold_total_length))
    return match_length/gold_total_length


def length_metric_1(gold_swc_tree=None, test_swc_tree=None, DEBUG=False):
    gold_total_length = gold_swc_tree.length()
    test_total_length = test_swc_tree.length()

    if DEBUG:
        print("gold_total_length = {}, test_total_length = {}"
              .format(gold_total_length, test_total_length))
    return 1 - test_total_length/gold_total_length


def length_metric(gold_swc_tree, test_swc_tree, config):
    if "knn" in config.keys():
        knn = config["knn"]

    dis_threshold = 0.1
    if "thereshold" not in config.keys() or config["thereshold"] == "default":
        dis_threshold = get_default_threshold(gold_swc_tree)
    else:
        try:
            dis_threshold = float(config["thereshold"])
        except:
            raise Exception("[Error: ] Read config info threshold {}. suppose to be a float or \"default\"")

    if config["method"] == 1:
        return length_metric_1(gold_swc_tree=gold_swc_tree,
                               test_swc_tree=test_swc_tree)
    elif config["method"] == 2:
        print(length_metric_2_1(gold_swc_tree=gold_swc_tree,
                                test_swc_tree=test_swc_tree,
                                dis_threshold=dis_threshold,
                                DEBUG=True))
    elif config["method"] == 3:
        match_fail_tuple_set = length_metric_3(gold_swc_tree=gold_swc_tree,
                                                test_swc_tree=test_swc_tree,
                                                DEBUG=True)
        if config["detail"] != "":
            save_as_swc(match_fail_tuple_set, config["detail"])
        else:
            print_swc(match_fail_tuple_set)
        return True
    else:
        raise Exception("[Error: ] Read config info method {}. length metric only have 1 and 2 two methods")


if __name__ == "__main__":
    goldtree = SwcTree()
    goldtree.load("D:\gitProject\mine\PyMets\\test\data_example\gold\\34_23_10_gold.swc")

    testTree = SwcTree()
    testTree.load("D:\gitProject\mine\PyMets\\test\data_example\\test\\34_23_10_test.swc")
    start = time.time()
    print(length_metric(gold_swc_tree=goldtree,
                        test_swc_tree=testTree,
                        config=read_json("D:\gitProject\mine\PyMets\config\length_metric.json")))

    print(time.time() - start)