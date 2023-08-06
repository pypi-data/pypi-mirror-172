# bmmltools

Current version 0.2.2

Last update 20/10/2022

PyPI: https://pypi.org/project/bmmltools/

Documentation: https://bmmltools.readthedocs.io/en/latest/

Author: Curcuraci L.

Contacts: Luca.Curcuraci@mpikg.mpg.de


This is a python library for 3d binary image segmentation developed at Max-Plank-Institute fuer Kolloid-und 
Grenzflaechenforschung. This library contains a series of tools which can be useful to segment 3d binary images
based on their structural/texture properties and extract information from the various regions identified,

### Installation

To install bmmltools use the Anaconda propt. In the propt, copy the lines below

```
> (base) conda create -n new_env python=3.8
> (base) conda activate new_env
> (new_env) conda install pytables=3.6.1
> (new_env) conda install hdbscan
> (new_env) pip install bmmltools
```

### Result visualization: bmmlboard

To inspect the intermediate results, a series of standard visualization tools has been developed. They are collected
in the **bmmlboard**, which is a web-browser based a graphical interface, which can be used to visualize the intermediate
results of bmmltools. To run the bmmlboard, write in the anaconda prompt

```
> (base) conda activate new_env
> (new_env) python -m bmmltools.run_bmmlboard
```

assuming that bmmltools is installed in the "new_env" environment.

## Example usage

A series of example scripts are available in the 'example folder' of this repository. A detailed explanation of what
they do can be founs in the "Miscellaneous" section of the bmmmltools documentation.
