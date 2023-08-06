# bmmltools


### Installation

Temporary installation path in the anaconda propt.

```
> (base) conda create -n new_env python=3.8
> (base) conda activate new_env
> (new_env) conda install pytables
> (new_env) cd [PATH TO bmmltools FOLDER]
> (new_env) [PATH TO bmmltools FOLDER] pip install -r requirements.txt
> (new_env) [PATH TO bmmltools FOLDER] python setup.py install
```

To run the bmmlboard, write in the anaconda prompt

```
> (base) conda activate new_env
> (new_env) python -m bmmltools.run_bmmlboard
```

assuming that bmmltools is installed in the "new_env" environment.

## Example usage

See example folder