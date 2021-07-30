# NEVPT2/MRCI计算

## NEVPT2
方法一：直接使用PySCF
```python
from pyscf import gto, scf, mcscf, mrpt

mol = gto.Mole()
mol.atom = '''N 0.0 0.0 0.0; N 0.0 0.0 1.0'''
mol.basis = 'cc-pvtz'
mol.build()

mf = scf.RHF(mol)
mf.kernel()

mf2 = mcscf.CASSCF(mf, 6,(3,3))
mf2.fix_spin_(ss=0)
mf2.fcisolver.max_cycle = 100
mf2.natorb = True
mf2.kernel()

mf3 = mrpt.NEVPT(mf2)
mf3.kernel()
```
此方法的缺点：HOMO LUMO附近的6个轨道可能不是想要的活性轨道，需要手动调整。

方法二：使用pyAutoMR

```
from automr import guess, autocas

xyz = '''N 0.0 0.0 0.0; N 0.0 0.0 2.0'''
bas = 'cc-pvtz'

mf = guess.from_frag_tight(xyz, bas, [[0],[1]], [0,0], [3,-3])
mf2 = autocas.cas(mf, (6,(3,3)))
mf4 = autocas.nevpt2(mf2)
```
N2解离当中键长很长时需要用到fragment，所以我们可以偷懒对所有的点都用fragment（但这个手段对C2并不适用）


## MRCI
方法一：直接使用orca。
```
! cc-pvtz pal8
%maxcore 6000
%casscf
 nel 2
 norb 2
end
%autoci
 CItype FICMRCI
 nel 2
 norb 2
 mult 1
 nroots 1
 DavidsonOpt 1
 MaxIter 100
end
%method
 FrozenCore FC_NONE
end
*xyz 0 1
F 0.0 0.0 0.0
F 0.0 0.0 1.2
*
```
如何判断orca的结果是否正确？
看LOEWDIN ORBITAL-COMPOSITION，是否有足够数目的轨道占据数偏离整数。比如对于上面这个例子，8号、9号自然轨道占据数1.95、0.05，就是正常的。其次看这两个轨道的成分，是否是想要的活性轨道。比如这里两个轨道是sigma成键、sigma反键，符合要求。当键长缩短到1.0时，orca的初猜也会出问题，会把pi反键排到8号，sigma成键排到6号，这时需要手动调换轨道：
```
%scf
 rotate {6,8} end
end
```
Tip: orca的轨道排序从0开始。


方法二：使用MOKIT调用orca

输入文件：
```
%nproc=8
%mem=10gb
# MRCISD(2,2)/cc-pvtz 

mokit{mrcisd_prog=orca, ctrtype=3}

0 1 
F 0.0 0.0 0.0
F 0.0 0.0 1.5
```
命令行
```
automr f2-1.5.inp > f2-1.5.out
```
缺点：需要安装GAMESS。

MOKIT的默认UHF算法是mix。如果要用fragment需要手动指定（见下一节）。

## F2和N2具体计算
F2：1.0-1.3需手动调换轨道，1.4以上可以用mix（pyAutoMR的guess.mix或MOKIT的默认算法）。
```
mf = guess.gen(xyz, bas, 0, 0)
mf2 = autocas.cas(mf, (2,(1,1)), lmo=False, sort=[7,10])
```
这里[7,10]表示把7,10号轨道放入活性空间（轨道从1开始数）。

N2：pyAutoMR可以全部用fragment，MOKIT自动算法在键长长的时候失效，需要用fragment。
```
# MRCISD(2,2)/cc-pvtz guess(fragment=2)

mokit{mrcisd_prog=orca, ctrtype=3}

0 1 0 4 0 -4
N(fragment=1) 0.0 0.0 0.0
N(fragment=2) 0.0 0.0 4.0
```

