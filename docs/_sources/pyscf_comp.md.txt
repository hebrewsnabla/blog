# PySCF 1.7.5 安装
## 安装环境
gcc 8.3.0, cmake 3.14.3, intel MKL 2019u3, python 3.7.4
## 下载
* 下载依赖程序

推荐：libcint >= 4.0.7, libxc = 4.3.4, xcfun 用开发者修改的版本
```bash
cd ~
wget https://github.com/sunqm/libcint/archive/v4.1.0.tar.gz -O libcint-4.1.0.tar.gz
wget https://gitlab.com/libxc/libxc/-/archive/4.3.4/libxc-4.3.4.tar.gz
wget https://github.com/fishjojo/xcfun/archive/cmake-3.5.tar.gz -O xcfun-2.1.1.tar.gz
tar xzvf libcint-4.1.0.tar.gz
tar xzvf libxc-4.3.4.tar.gz
tar xzvf xcfun-2.1.1.tar.gz
```
如果不能联网，在可联网机器上下载再传到目标机器上解压
* 下载PySCF
```bash
git clone git@github.com:pyscf/pyscf
```
如果不能联网，可以在别处下载压缩包再解压
```
wget https://github.com/pyscf/pyscf/archive/master.zip
```
## 编译libcint
```bash
cd ~/libcint-4.1.0
mkdir build && cd build

cmake -DWITH_F12=1 -DWITH_RANGE_COULOMB=1 -DWITH_COULOMB_ERF=1 \
-DMIN_EXPCUTOFF=20 -DKEEP_GOING=1 \
-DCMAKE_INSTALL_PREFIX:PATH=$HOME/pyscf_deps \
-DCMAKE_INSTALL_LIBDIR:PATH=lib ..
make
make install
```
## 编译libxc
```bash
cd ~/libxc-4.3.4
autoreconf -i # release版本需要这一步
./configure --prefix=$HOME/pyscf_deps \
--libdir=$HOME/pyscf_deps/lib --enable-shared 
make 
make install
```
## 编译xcfun
```bash
cd ~/xcfun-cmake-3.5
mkdir build && cd build

cmake -DBUILD_SHARED_LIBS=1 -DXCFUN_MAX_ORDER=3 \
-DCMAKE_INSTALL_PREFIX:PATH=$HOME/pyscf_deps \
-DCMAKE_INSTALL_LIBDIR:PATH=lib ..
make 
make install
```
注意：老版本的`XC_MAX_ORDER`改成了`XCFUN_MAX_ORDER`

## 编译PySCF
在`~/.bashrc`中添加
```bash
export LD_LIBRARY_PATH=$HOME/pyscf_deps:$LD_LIBRARY_PATH
```
```bash
cd ~/pyscf/pyscf/lib
mkdir build && cd build

cmake -DBUILD_LIBCINT=0 \
-DBUILD_LIBXC=0 -DBUILD_XCFUN=0 \
-DCMAKE_INSTALL_PREFIX:PATH=$HOME/pyscf_deps ..

make
```
在`~/.bashrc`中添加
```bash
export PYTHONPATH=$HOME/pyscf:$PYTHONPATH
```
## 可能遇到的问题
* 找不到MKL

见[pyscf.org/pyscf/install.html#using-optimized-blas](http://pyscf.org/pyscf/install.html#using-optimized-blas)






