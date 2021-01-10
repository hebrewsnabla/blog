# Cremer's 4 Types of Non-dynamic Correlation

## Type 1 Single-C, Multi-D
### Example: distorted ethylene $\ce{C_2H_4}$
nel: 16, basis: def2-SVP(48), RHF occ:8 

GVB occ: 
>  2.0000000    2.0000000    2.0000000    2.0000000    2.0000000
>  2.0000000    2.0000000    1.0000482    0.9999518    0.0000000  ...

internal 7, active 2, external 39

initial CI state
```
ROOT   0:  E=     -77.9009266288 Eh
	0.50002 [     0]: 20
	0.49998 [     2]: 02
```
final CI state
```
ROOT   0:  E=     -77.9017594561 Eh
	0.50002 [     0]: 20
	0.49998 [     2]: 02
```
## Type 2 Multi-C, Single-D
### Example: singlet methylene
nel: 8, basis: def2-SVP(24), RHF occ: 4

GVB occ:
> 2.0000000    2.0000000    2.0000000    1.9180431    0.0819569

internal 3, active 2, external 19

initial CI state
```
ROOT   0:  E=     -38.8510136544 Eh
	0.95429 [     2]: 02
	0.04571 [     0]: 20
ROOT   1:  E=     -38.7900054943 Eh  1.660 eV  13389.7 cm**-1
	1.00000 [     1]: 11
```
final CI state
```ROOT   0:  E=     -38.8514204862 Eh
	0.95764 [     0]: 20
	0.04236 [     2]: 02
ROOT   1:  E=     -38.7912602095 Eh  1.637 eV  13203.7 cm**-1
	1.00000 [     1]: 11
```