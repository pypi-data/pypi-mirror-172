# **GreatX**: Graph Reliability Toolbox

<p align="center">
  <img width = "600" height = "150" src="https://github.com/EdisonLeeeee/GreatX/blob/master/imgs/greatx.png" alt="banner"/>
  <br/>
</p>
<p align="center"><strong>GreatX is great!</strong></p>

<p align=center>
  <a href="https://greatx.readthedocs.io/en/latest/">
    [Documentation]
  </a>         
  |
  <a href="https://github.com/EdisonLeeeee/GreatX/blob/master/examples">
    [Examples]
  </a>  
</p>

<p align=center>
  <a href="https://www.python.org/downloads/release/python-360/">
    <img src="https://img.shields.io/badge/Python->=3.6-3776AB?logo=python" alt="Python">
  </a>    
  <a href="https://github.com/pytorch/pytorch">
    <img src="https://img.shields.io/badge/PyTorch->=1.8-FF6F00?logo=pytorch" alt="pytorch">
  </a>   
  <a href="https://pypi.org/project/greatx/">
    <img src="https://badge.fury.io/py/greatx.svg" alt="pypi">
  </a>       
  <a href="https://github.com/EdisonLeeeee/GreatX/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/EdisonLeeeee/GreatX" alt="license">
    <img src="https://img.shields.io/badge/Contributions-Welcome-278ea5" alt="Contrib"/>    
  </a>       
</p>
                                                                   
# ❓ What is Reliability on Graphs?
![threats](./imgs/threats.png)

It refers to robustness against the following threats:
+ Inherent noise
+ Distribution Shift
+ Adversarial Attacks

For more details, please refer to our paper [**Recent Advances in Reliable Deep Graph Learning: Adversarial Attack, Inherent Noise, and Distribution Shift**](https://arxiv.org/abs/2202.07114)


# 💨 News
- June 30, 2022: GraphWar has been renamed to GreatX.
- ~~June 9, 2022: GraphWar **v0.1.0** has been released. We also provide the [documentation](https://greatx.readthedocs.io/en/latest) along with numerous [examples](https://github.com/EdisonLeeeee/GreatX/blob/master/examples)~~ .
- ~~May 27, 2022: GraphWar has been refactored with [PyTorch Geometric (PyG)](https://github.com/pyg-team/pytorch_geometric), old code based on [DGL](https://www.dgl.ai) can be found [here](https://github.com/EdisonLeeeee/GreatX/tree/dgl). We will soon release the first version of GreatX, stay tuned!~~

NOTE: GreatX is still in the early stages and the API will likely continue to change. 
If you are interested in this project, don't hesitate to contact me or make a PR directly.
# 🚀 Installation

Please make sure you have installed [PyTorch](https://pytorch.org) and [PyTorch Geometric (PyG)](https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html).


```bash
# Coming soon
pip install -U greatx
```

or

```bash
# Recommended
git clone https://github.com/EdisonLeeeee/GreatX.git && cd GreatX
pip install -e . --verbose
```

where `-e` means "editable" mode so you don't have to reinstall every time you make changes.

# ⚡ Get Started

Assume that you have a `torch_geometric.data.Data` instance `data` that describes your graph.

## How fast can we train and evaluate your own GNN?
Take `GCN` as an example:
```python
from greatx.nn.models import GCN
from greatx.training.trainer import Trainer
from torch_geometric.datasets import Planetoid
dataset = Planetoid(root='.', name='Cora') # Any PyG dataset is available!
data = dataset[0]
model = GCN(data.x.size(-1), data.y.max().item() + 1)
trainer = Trainer(model, device='cuda:0')
trainer.fit({'data': data, 'mask': data.train_mask})
trainer.evaluate({'data': data, 'mask': data.test_mask})
```
## A simple targeted manipulation attack

```python
from greatx.attack.targeted import RandomAttack
attacker = RandomAttack(data)
attacker.attack(1, num_budgets=3) # attacking target node `1` with `3` edges 
attacked_data = attacker.data()
edge_flips = attacker.edge_flips()

```

## A simple untargeted (non-targeted) manipulation attack

```python
from greatx.attack.untargeted import RandomAttack
attacker = RandomAttack(data)
attacker.attack(num_budgets=0.05) # attacking the graph with 5% edges perturbations
attacked_data = attacker.data()
edge_flips = attacker.edge_flips()
```


# 👀 Implementations

In detail, the following methods are currently implemented:

## ⚔ Adversarial Attack

### Graph Manipulation Attack (GMA)

#### Targeted Attack

| Methods          | Descriptions                                                                                                                                           | Examples                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| **RandomAttack** | A simple random method that chooses edges to flip randomly.                                                                                            | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/targeted/random_attack.py) |
| **DICEAttack**   | *Waniek et al.* [Hiding Individuals and Communities in a Social Network](https://arxiv.org/abs/1608.00375), *Nature Human Behavior'16*                 | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/targeted/dice_attack.py)   |
| **Nettack**      | *Zügner et al.* [Adversarial Attacks on Neural Networks for Graph Data](https://arxiv.org/abs/1805.07984), *KDD'18*                                    | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/targeted/nettack.py)       |
| **FGAttack**     | *Chen et al.* [Fast Gradient Attack on Network Embedding](https://arxiv.org/abs/1809.02797), *arXiv'18*                                                | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/targeted/fg_attack.py)     |
| **GFAttack**     | *Chang et al*.  [A Restricted Black - box Adversarial Framework Towards Attacking Graph Embedding Models](https://arxiv.org/abs/1908.01297), *AAAI'20* | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/targeted/gf_attack.py)     |
| **IGAttack**     | *Wu et al.* [Adversarial Examples on Graph Data: Deep Insights into Attack and Defense](https://arxiv.org/abs/1903.01610), *IJCAI'19*                  | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/targeted/ig_attack.py)     |
| **SGAttack**     | *Li et al.* [ Adversarial Attack on Large Scale Graph](https://arxiv.org/abs/2009.03488), *TKDE'21*                                                    | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/targeted/sg_attack.py)     |
#### Untargeted Attack

| Methods          | Descriptions                                                                                                                                   | Examples                                                                                                        |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **RandomAttack** | A simple random method that chooses edges to flip randomly                                                                                     | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/untargeted/random_attack.py) |
| **DICEAttack**   | *Waniek et al.* [Hiding Individuals and Communities in a Social Network](https://arxiv.org/abs/1608.00375), *Nature Human Behavior'16*         | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/untargeted/dice_attack.py)   |
| **FGAttack**     | *Chen et al.* [Fast Gradient Attack on Network Embedding](https://arxiv.org/abs/1809.02797), *arXiv'18*                                        | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/untargeted/fg_attack.py)     |
| **Metattack**    | *Zügner et al.* [Adversarial Attacks on Graph Neural Networks via Meta Learning](https://arxiv.org/abs/1902.08412), *ICLR'19*                  | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/untargeted/metattack.py)     |
| **IGAttack**     | *Wu et al.* [Adversarial Examples on Graph Data: Deep Insights into Attack and Defense](https://arxiv.org/abs/1903.01610), *IJCAI'19*          | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/untargeted/ig_attack.py)     |
| **PGD**          | *Xu et al.* [Topology Attack and Defense for Graph Neural Networks: An Optimization Perspective](https://arxiv.org/abs/1906.04214), *IJCAI'19* | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/untargeted/pgd_attack.py)    |
| **MinmaxAttack** | *Xu et al.* [Topology Attack and Defense for Graph Neural Networks: An Optimization Perspective](https://arxiv.org/abs/1906.04214), *IJCAI'19* | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/untargeted/minmax_attack.py) |

### Graph Injection Attack (GIA)
| Methods             | Descriptions                                                                                                    | Examples                                                                                                          |
| ------------------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **RandomInjection** | A simple random method that chooses nodes to inject randomly.                                                   | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/injection/random_injection.py) |
| **AdvInjection**    | The 2nd place solution of [KDD Cup 2020](https://www.biendata.xyz/competition/kddcup_2020/), team: ADVERSARIES. | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/injection/adv_injection.py)    |

### Graph Universal Attack (GUA)

### Graph Backdoor Attack (GBA)

| Methods         | Descriptions                                                                                                              | Examples                                                                                                     |
| --------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **LGCBackdoor** | *Chen et al.* [Neighboring Backdoor Attacks on Graph Convolutional Network](https://arxiv.org/abs/2201.06202), *arXiv'22* | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/backdoor/lgc_backdoor.py) |
| **FGBackdoor**  | *Chen et al.* [Neighboring Backdoor Attacks on Graph Convolutional Network](https://arxiv.org/abs/2201.06202), *arXiv'22* | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/attack/backdoor/fg_backdoor.py)  |



## Enhancing Techniques or Corresponding Defense

### Standard GNNs (without defense)

#### Supervised
| Methods                 | Descriptions                                                                                                                               | Examples                                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| **GCN**                 | *Kipf et al.* [Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907), *ICLR'17*              | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/gcn.py)   |
| **SGC**                 | *Wu et al.*  [Simplifying Graph Convolutional Networks](https://arxiv.org/abs/1902.07153), *ICLR'19*                                       | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/sgc.py)   |
| **GAT**                 | *Veličković et al.*  [Graph Attention Networks](https://arxiv.org/abs/1710.10903), *ICLR'18*                                               | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/gat.py)   |
| **DAGNN**               | *Liu et al.*  [Towards Deeper Graph Neural Networks](https://arxiv.org/abs/2007.09296), *KDD'20*                                           | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/dagnn.py) |
| **APPNP**               | *Klicpera et al.*  [Predict then Propagate: Graph Neural Networks meet Personalized PageRank](https://arxiv.org/abs/1810.05997), *ICLR'19* | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/appnp.py) |
| **JKNet**               | *Xu et al.*  [Representation Learning on Graphs with Jumping Knowledge Networks](https://arxiv.org/abs/1806.03536), *ICML'18*              | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/jknet.py) |
| **TAGCN**               | *Du et al.*  [Topological Adaptive Graph Convolutional Networks](https://arxiv.org/abs/1806.03536), *arXiv'17*                             | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/tagcn.py) |
| **SSGC**                | *Zhu et al.*  [Simple Spectral Graph Convolution](https://openreview.net/forum?id=CYO5T-YjWZV), *ICLR'21*                                  | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/ssgc.py)  |
| **DGC**                 | *Wang et al.*  [Dissecting the Diffusion Process in Linear Graph  Convolutional Networks](https://arxiv.org/abs/2102.10739), *NeurIPS'21*  | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/dgc.py)   |
| **NLGCN, NLMLP, NLGAT** | *Liu et al.*  [Non-Local Graph Neural Networks](https://ieeexplore.ieee.org/document/9645300), *TPAMI'22*                                  | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/nlgnn.py) |

#### Unsupervised/Self-supervise
| Methods | Descriptions                                                                          | Examples                                                                                                |
| ------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **DGI** | *Veličković et al.* [Deep Graph Infomax](https://arxiv.org/abs/1809.10341), *ICLR'19* | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/unsupervised/dgi.py) |

### Techniques Against Adversarial Attacks

| Methods                 | Descriptions                                                                                                                                                                                                                                | Examples                                                                                                          |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **MedianGCN**           | *Chen et al.* [Understanding Structural Vulnerability in Graph Convolutional Networks](https://www.ijcai.org/proceedings/2021/310), *IJCAI'21*                                                                                              | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/median_gcn.py)      |
| **RobustGCN**           | *Zhu et al.*  [Robust Graph Convolutional Networks Against Adversarial Attacks](http://pengcui.thumedialab.com/papers/RGCN.pdf), *KDD'19*                                                                                                   | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/robust_gcn.py)      |
| **SoftMedianGCN**       | *Geisler et al.* [Reliable Graph Neural Networks via Robust Aggregation](https://arxiv.org/abs/2010.15651), *NeurIPS'20*<br>*Geisler et al.* [Robustness of Graph Neural Networks at Scale](https://arxiv.org/abs/2110.14038), *NeurIPS'21* | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/soft_median_gcn.py) |
| **ElasticGNN**          | *Liu et al.* [Elastic Graph Neural Networks](https://arxiv.org/abs/2107.06996), *ICML'21*                                                                                                                                                   | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/elastic_gnn.py)     |
| **AirGNN**              | *Liu et al.* [Graph Neural Networks with Adaptive Residual](https://openreview.net/forum?id=hfkER_KJiNw), *NeurIPS'21*                                                                                                                      | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/air_gnn.py)         |
| **SimPGCN**             | *Jin et al.* [Node Similarity Preserving Graph Convolutional Networks](https://arxiv.org/abs/2011.09643), *WSDM'21*                                                                                                                         | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/simp_gcn.py)        |
| **SAT**                 | *Li et al.* [Spectral Adversarial Training for Robust Graph Neural Network](), *arXiv'22*                                                                                                                                                   | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/model/supervised/gcn_sat.py)          |
| **JaccardPurification** | *Wu et al.* [Adversarial Examples on Graph Data: Deep Insights into Attack and Defense](https://arxiv.org/abs/1903.01610), *IJCAI'19*                                                                                                       | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/defense/gcn_jaccard.py)               |
| **SVDPurification**     | *Entezari et al.* [All You Need Is Low (Rank): Defending Against Adversarial Attacks on Graphs](https://arxiv.org/abs/1903.01610), *WSDM'20*                                                                                                | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/defense/gcn_svd.py)                   |
| **GNNGUARD**            | *Zhang et al.* [GNNGUARD: Defending Graph Neural Networks against Adversarial Attacks](https://arxiv.org/abs/2006.08149), *NeurIPS'20*                                                                                                      | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/defense/gnn_guard.py)                 |
| **GUARD**               | *Li et al.* [GUARD: Graph Universal Adversarial Defense](https://arxiv.org/abs/2204.09803), *arXiv'22*                                                                                                                                      | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/defense/universal_defense.py)         |
| **RTGCN**               | *Wu et al.* [Robust Tensor Graph Convolutional Networks via T-SVD based Graph Augmentation](https://dl.acm.org/doi/abs/10.1145/3534678.3539436), *KDD'22*                                                                                   | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/model/supervised/rt_gcn.py)           |

More details of literatures and the official codes can be found at [Awesome Graph Adversarial Learning](https://github.com/gitgiter/Graph-Adversarial-Learning).

### Techniques Against Inherent Noise

| Methods                | Descriptions                                                                                                                                                            | Examples                                                                                                    |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **DropEdge**           | *Rong et al.* [DropEdge: Towards Deep Graph Convolutional Networks on Node Classification](https://arxiv.org/abs/1907.10903), *ICLR'20*                                 | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/drop_edge.py) |
| **DropNode**           | *You et al.* [Graph Contrastive Learning with Augmentations](https://arxiv.org/abs/2010.13902), *NeurIPS'20*                                                            | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/drop_node.py) |
| **DropPath**           | *Li et al.* [MaskGAE: Masked Graph Modeling Meets Graph Autoencoders](https://arxiv.org/abs/2205.10053), *arXiv'22*'                                                    | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/models/supervised/drop_path.py) |
| **FeaturePropagation** | *Rossi et al.* [On the Unreasonable Effectiveness of Feature propagation in Learning on Graphs with Missing Node Features](https://arxiv.org/abs/2111.12128), *ICLR'21* | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/defense/feature_propagation.py) |


## Miscellaneous
| Methods                             | Descriptions                                                                                                                                                                            | Examples                                                                            |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Centered Kernel Alignment (CKA)** | *Nguyen et al.* [Do Wide and Deep Networks Learn the Same Things? Uncovering How Neural Network Representations Vary with Width and Depth](https://arxiv.org/abs/2010.15327), *ICLR'21* | [[**Example**]](https://github.com/EdisonLeeeee/GreatX/blob/master/examples/cka.py) |



# ❓ Known Issues
+ Despite our best efforts, we still had difficulty reproducing the results of [GNNGUARD](https://arxiv.org/abs/2006.08149) in the paper. If you find any problems, please don't hesitate to contact me.
+ `Untargeted attacks` are suffering from performance degradation, as also in DeepRobust, when a validation set is used during training with model picking. Such phenomenon has also been revealed in [Black-box Gradient Attack on Graph Neural Networks: Deeper Insights in Graph-based Attack and Defense](https://arxiv.org/abs/2104.15061).
