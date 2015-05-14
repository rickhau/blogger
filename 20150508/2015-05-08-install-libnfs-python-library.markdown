---
layout: post
title: "Install libnfs-python library"
date: 2015-05-08 23:10:51 +0800
comments: true
categories: Python
---

## Install libnfs-python on Fedora 20
=====================================

### 0 - Pre-requisite

Before you start to install the libnfs-python package, you need to install the following packages. Otherwise, you might encounter some errors while running ./bootstrap on Fedora

```bash 
$ sudo yum install python-devel*
$ sudo yum install libtool*
$ sudo yum install automake*
$ sudo yum install autoconf*
$ sudo yum install aclocal*      # This can be ignored
$ sudo yum install autoheader*   # This can be ignored
```

### 1 - Install libnfs package/library

You have to install the libnfs package/library which libnfs-python needs.
libnfs-python relies on the libnfs library to support NFS protocol.

```bash
$ wget https://github.com/sahlberg/libnfs/archive/libnfs-1.9.7.tar.gz
$ tar -xzf libnfs-1.9.7.tar.gz
$ cd libnfs-1.9.7
$ ./bootstrap
$ ./configure --prefix=/usr
$ make
$ sudo make install
$ su -c 'echo /usr/local/lib > /etc/ld.so.conf.d/local-libs.conf'
$ sudo ldconfig
$ cd ..
```

### 2 - Install libnfs-python package/library

With libnfs library installed, you can start to install libnfs-python library now.    

If you follow the README to install the package, you might not be able to use the libnfs-python module successfully after installation. 

```bash
$ git clone https://github.com/sahlberg/libnfs-python.git
$ sudo python setup.py install
running install
running bdist_egg
running egg_info
writing libnfs.egg-info/PKG-INFO
writing top-level names to libnfs.egg-info/top_level.txt
writing dependency_links to libnfs.egg-info/dependency_links.txt
reading manifest file 'libnfs.egg-info/SOURCES.txt'
reading manifest template 'MANIFEST.in'
writing manifest file 'libnfs.egg-info/SOURCES.txt'
installing library code to build/bdist.linux-x86_64/egg
running install_lib
running build_py
running build_ext
creating build/bdist.linux-x86_64/egg
creating build/bdist.linux-x86_64/egg/libnfs
copying build/lib.linux-x86_64-2.7/libnfs/__init__.py -> build/bdist.linux-x86_64/egg/libnfs
copying build/lib.linux-x86_64-2.7/libnfs/_libnfs.so -> build/bdist.linux-x86_64/egg/libnfs
copying build/lib.linux-x86_64-2.7/libnfs/libnfs.py -> build/bdist.linux-x86_64/egg/libnfs
byte-compiling build/bdist.linux-x86_64/egg/libnfs/__init__.py to __init__.pyc
byte-compiling build/bdist.linux-x86_64/egg/libnfs/libnfs.py to libnfs.pyc
creating stub loader for libnfs/_libnfs.so
byte-compiling build/bdist.linux-x86_64/egg/libnfs/_libnfs.py to _libnfs.pyc
creating build/bdist.linux-x86_64/egg/EGG-INFO
copying libnfs.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
copying libnfs.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying libnfs.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying libnfs.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
writing build/bdist.linux-x86_64/egg/EGG-INFO/native_libs.txt
zip_safe flag not set; analyzing archive contents...
libnfs.libnfs: module references __file__
creating 'dist/libnfs-1.0_1-py2.7-linux-x86_64.egg' and adding 'build/bdist.linux-x86_64/egg' to it
removing 'build/bdist.linux-x86_64/egg' (and everything under it)
Processing libnfs-1.0_1-py2.7-linux-x86_64.egg
removing '/usr/lib64/python2.7/site-packages/libnfs-1.0_1-py2.7-linux-x86_64.egg' (and everything under it)
creating /usr/lib64/python2.7/site-packages/libnfs-1.0_1-py2.7-linux-x86_64.egg
Extracting libnfs-1.0_1-py2.7-linux-x86_64.egg to /usr/lib64/python2.7/site-packages
libnfs 1.0-1 is already the active version in easy-install.pth

Installed /usr/lib64/python2.7/site-packages/libnfs-1.0_1-py2.7-linux-x86_64.egg
Processing dependencies for libnfs==1.0-1
Finished processing dependencies for libnfs==1.0-1
```

You can try `import libnfs` to see if you hit any error.

```python
Python 2.7.5 (default, Nov  3 2014, 14:26:24)
[GCC 4.8.3 20140911 (Red Hat 4.8.3-7)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import libnfs
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "libnfs.py", line 28, in <module>
    _libnfs = swig_import_helper()
  File "libnfs.py", line 20, in swig_import_helper
    import _libnfs
ImportError: No module named _libnfs
```

If you run into the same ImportError like me, it needs to call the library which needs to be compiled under `libnfs-python/libnfs`.    

So, Go to [/home/fitbranded/libnfs-python/libnfs] and run `make`   


```bash
$ cd libnfs-python/libnfs
$ make
```

Then, re-run the python to import libnfs and test NFS service.

```python
import libnfs
nfs = libnfs.NFS('nfs://127.0.0.1/data/tmp/')
a = nfs.open('/foo-test', mode='w+')
a.write("Test string")
a.close()
print nfs.open('/foo-test', mode='r').read()
```

Congratulations!!! You can enjoy this powerful NFS python library.

### APPENDIX

1) Compile older libnfs library

  In the beginning, I did not install the latest libnfs package. I ran into some issue while doing the compilation. 
  
>- Need to add `-I/home/fitbranded/include` to Makefile

>```make
>  INCLUDE    = -I/usr/include -I/home/fitbranded/include
>```

**Note:**   
Please run the `make clean` before `make` again!  


2) Tells setup.py where to include the library for `libnfs-python` package

   Edit setup.py and add one more include file

```python
_libnfs = Extension(name='libnfs._libnfs',
                   sources=['libnfs/libnfs_wrap.c'],
                   libraries=['nfs'],
                   include_dirs = ['/home/fitbranded/include'],    # Add this one
)
```

3) GNU Autotools

   libnfs packages requires GNU Autotools. If you want to know more about it, you can refer to the following resources.
   
>- [ArchLinux](https://bbs.archlinux.org/viewtopic.php?id=161452)    
>- [Compile Kodi on Fedora](http://kodi.wiki/view/HOW-TO:Compile_Kodi_for_Linux_on_Fedora_Red_Hat_Enterprise_Linux_CentOS)

```
$ sudo pacman -S pkg-config xorg-server-devel libtool automake
$ libtoolize --force
```
Consider adding AC_CONFIG_MACRO_DIR([m4]) to configure.ac and re-run libtoolize --force.    
```
$ vim configure.ac
$ libtoolize --force
$ aclocal
$ autoheader
$ automake --force-missing --add-missing
$ autoconf
```

Reference    
1) [Discussion with Author](https://github.com/sahlberg/libnfs-python/issues/1)    
2) [Step-by-Step Video](https://asciinema.org/a/19474)   
3) [Python Build](https://docs.python.org/2/extending/building.html)