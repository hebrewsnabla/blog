# Multireference Tutorial

## With pyAutoMR 
Current strategy of pyAutoMR:

If RHF is stable: use **RHF -> PM LMO -> CASSCF**;

Otherwise, use **UHF -> UNO -> CASSCF**.

"RHF stable" means E(RHF) = E(UHF).

### UHF case
```{code-block} python
from pyscf import lib
import guess, autocas, cidump

lib.num_threads(4)

xyz = 'N 0.0 0.0 0.0; N  0.0 0.0 1.9' #sys.argv[1]
bas = 'cc-pvdz'

mf = guess.from_frag(xyz, bas, [[0],[1]], [0,0], [3,-3], cycle=50)
guess.check_stab(mf)

mf2 = autocas.cas(mf)
cidump.dump(mf2)
```
For a stretched N2, we need to do UHF first. 
:::{Note}
Simple UHF guess will fall into RHF, and even `guess=mix` maybe doesn't work. A practical way is using fragment guess, i.e. `guess=fragment` in Gaussian, or `guess.from_frag` in pyAutoMR.
:::
Here, `[[0],[1]]` means the 0th atom belongs to frag0, and 1st atom belongs to frag1. `[0,0]` means charges of the 2 frags are 0,0 respectively. `[3,-3]` means the spin of the 2 frags. Note that spin equals 2S, or `n_a - n_b` in PySCF, not 2S+1. Also, we need to ensure that the total number of alpha/beta electrons equals that in total molecule, so the spin parameter cannot be `[3,3]`.
You can see output like
```
**** generating fragment guess ****
fragments: [('N', [0.0, 0.0, 0.0])] [('N', [0.0, 0.0, 1.9])]
converged SCF energy = -54.3911145621998  <S^2> = 3.7540306  2S+1 = 4.0020148
converged SCF energy = -54.3911145621998  <S^2> = 3.7540306  2S+1 = 4.0020148
       na   nb
atom1   5    2
atom2   2    5
```
Then, `check_stab` will do something like `stable=opt` in Gaussian, and `autocas.cas` will do UHF MO -> UNO, and estimate the size of active space.
Output file contains a clear illustration of the UNOs
```
UNO ON: [ 2.        2.        1.999103  1.997838  1.550306  1.174501  1.174501  0.825499  0.825499  0.449694  0.002162  0.000897  0.        0.        0.
  0.        0.        0.        0.        0.       -0.       -0.       -0.       -0.       -0.       -0.       -0.       -0.      ]
UNO in active space
             #0      #1      #2      #3      #4      #5     
  0 N 3s                                               0.184
  0 N 2px              0.154  -0.432  -0.487  -0.139        
  0 N 2py              0.432   0.154  -0.139   0.487        
  0 N 2pz     -0.442                                   0.565
  0 N 3px              0.106  -0.295  -0.323                
  0 N 3py              0.295   0.106           0.323        
  0 N 3pz     -0.295                                   0.390
  1 N 3s                                              -0.184
  1 N 2px              0.154  -0.432   0.487   0.139        
  1 N 2py              0.432   0.154   0.139  -0.487        
  1 N 2pz      0.442                                   0.565
  1 N 3px              0.106  -0.295   0.323                
  1 N 3py              0.295   0.106          -0.323        
  1 N 3pz      0.295                                   0.390
```
pyAutoMR will pick the orbitals having occupation number (ON) bewteen 1.98-0.02.
And it's clear that the six orbitals are: simga bonding, pi bonding, pi bonding, pi anti-bonding, pi anti-bonding, and sigma anti-bonding.

Without pyAutoMR, we need to manually view and pick these orbitals, but now it's automatic.

