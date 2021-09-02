## CASSCF计算
在一个正确的CASSCF计算的基础上，CASPT2/NEVPT2/MRCI计算基本上是黑箱的。所以成功的关键在于CASSCF计算。

CASSCF计算基本流程：

* RHF -> 选择轨道 -> CASSCF
* UHF -> UNO -> CASSCF

RHF选择轨道的步骤也可以通过一定的算法来自动化完成。UNO则本身就是自动的，前提是UHF需要收敛到最低的稳定的解。
下面介绍**UHF收敛方法**

**使用高斯**：一般方法`guess=mix stable=opt`, 进阶方法需要片段初猜：

```
#p uhf guess(fragment=2)

title

0 1 0 4 0 -4
N(fragment=1) 0.0 0.0 0.0
N(fragment=2) 0.0 0.0 4.0

--link1--
%chk=xxx.chk
#p uhf stable=opt guess=read grom=allcheck
```
这里在整体的电荷和自旋多重度`0 1`后面指定了两个片段的电荷和自旋多重度。为了使alpha、beta电子数守恒，第二个片段需要有三个beta单电子，而不是alpha单电子，这样的自旋多重度用负数表示。

**使用pyAutoMR**：有三种初猜方法
* general，不改变PySCF默认初猜。“0， 0” 表示电荷和自旋。注意自旋为2S，不是2S+1.
```python
from automr import guess

xyz = '''F 0.0 0.0 0.0; F 0.0 0.0 1.0'''
bas = 'cc-pvtz'

mf = guess.gen(xyz, bas, 0, 0) 
```
* mix, 相当于高斯的`guess=mix`
```
mf = guess.mix(xyz, bas, conv='tight')
```
* fragment，相当于高斯的`guess=fragment`。`[[0],[1]]`表示两个片段包含的原子编号；`[0,0]`表示两个片段的电荷，`[3,-3]`表示两个片段的自旋。
```
mf = guess.from_frag_tight(xyz, bas, [[0],[1]], [0,0], [3,-3])
```
`mix`和`from_frag_tight`都会自动做`stable=opt`。手动做的方法是
```
mf = guess.check_stab(mf)
```

下面我们可以做**CASSCF**计算
* 使用pyAutoMR
```
from automr import autocas
mf2 = autocas.cas(mf, (6,(3,3)))
```
Tip：autocas.cas可以自动判断活性空间，但是做扫描的时候为了保证活性空间一致，需要指定一个参数，这里的参数表示6个活性轨道，3个alpha活性电子，3个beta活性电子。不需要指定自旋多重度，如果算三重态就是(6,(4,2))。
* 使用MOKIT
```
%nproc=8
%mem=10gb
# CASSCF(2,2)/cc-pvtz 

mokit{}

0 1 
F 0.0 0.0 0.0
F 0.0 0.0 1.5
```
MOKIT的输入格式与高斯类似，程序选项写在mokit后的花括号内。此处我们使用默认选项，什么都不用写。
MOKIT会自动做RHF/UHF -> GVB -> CASSCF计算，自动程度比pyAutoMR高。