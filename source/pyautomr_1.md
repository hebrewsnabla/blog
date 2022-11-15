# 使用pyAutoMR做对称破缺计算

本公众号之前发过一系列的使用高斯做对称破缺计算的文章，如
片段组合波函数实例1.双原子分子，谈谈Gaussian软件中的guess=mix。
这些已经能满足日常使用的需要了，但是毕竟Gaussian是个闭源程序，用户对程序的操控并不能随心所欲。于是笔者写了一个基于PySCF的工作流程序pyAutoMR(顾名思义本来是做自动多参考计算的，这个以后再介绍)，力图覆盖所有的对称破缺波函数生成方法，及满足各种对称破缺计算的特殊需要。

pyAutoMR中已实现了mix，from_frag(片段组合)，flipspin，from_fch方法，下面一一介绍。本文涉及的例子可在源码仓库找到
> https://github.com/hebrewsnabla/pyAutoMR/blob/master/examples/tutorial

## mix方法
mix方法是一种混合HOMO和LUMO来获得自旋极化的方法。
示例
```
from automr import guess

xyz = '''H 0.0 0.0 0.0; H 0.0 0.0 2.0'''
bas = 'def2-svp'
mf = guess.mix(xyz, bas) # 只会做5圈SCF
mf = guess.mix_tight(xyz, bas) # 会跑完SCF并做stable=opt
```
主要的可选的参数及默认值

| | |
| :---: | :---: |
| charge | 0 |
| level_shift | 0.0 |
| xc | None |
| mix_param | numpy.pi/4 |

由于mix只用于做自旋极化单重态，所以不用设定自旋多重度。默认是做对称破缺UHF，如果要做UKS，可以用`xc`设定泛函。`mix_param`是下式中的 $\theta$ (Szabo 3.358-3.359)

$$\psi_{\text{HOMO}}^\alpha = \cos\theta\; \psi_{\text{HOMO}} + \sin\theta\; \psi_{\text{LUMO}}\\
\psi_{\text{HOMO}}^\beta = \cos\theta\; \psi_{\text{HOMO}} - \sin\theta\; \psi_{\text{LUMO}}$$
一般来说，取$\pi/4$可使极化的轨道最为局域。可根据需要调小（减少混入的LUMO成分）或调大。

### 进阶用法
有些时候，混合HOMO和LUMO并不能收敛到正确的对称破缺态，可能需要混合HOMO-1和LUMO，或混合多对轨道。

## 片段初猜方法
片段初猜方法将体系划分为两个（或多个）片段，对片段分别做UHF/UKS计算后，把轨道拼到一起组成整个体系的对称破缺初猜。
示例
```
from automr import guess

xyz = '''N 0.0 0.0 0.0; N 0.0 0.0 4.0'''
bas = 'cc-pvtz'
mf = guess.from_frag(xyz, bas， [[0],[1]], [0,0], [3,-3]) # 只会做2圈SCF
mf = guess.from_frag_tight(xyz, bas， [[0],[1]], [0,0], [3,-3]) # 会跑完SCF并做stable=opt
```
后三个参数的含义分别是
| | |
| :---: | :---: |
| frags=[[0],[1]] | 第一个片段含有0号原子，第二个片段含有1号原子 |
| chgs=[0,0] | 片段电荷依次为0,0 |
| spins | 片段的 $N_\alpha-N_\beta$ 依次为3,-3 |

注意此处spins采用的是PySCF的规则，等同于高斯的`4 -4`。

这个例子的能量约为`-108.801`，和MOKIT的例子`automr/05`是一致的。

### 进阶用法：尝试多种自旋多重度组合

### 进阶用法：手动计算片段波函数

## FlipSpin方法

