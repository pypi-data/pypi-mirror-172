# pyfilemv
This small python package provides an extension to the normal unix `mv` command. 

In addition to simply renaming a file or directory, **pymv** also searches through user-defined
directories and asks the user if he or she wants to update any reference to the file that was renamed. 
Thus, you do not have to manually update all scripts or documents that reference that file. 
For a showcase of the package, see the [Demonstration](#Demo) below.

## Installation
**pymv** can simply be installed via [PyPI](https://pypi.org/project/pyfilemv/) .
```bash
pip install pyfilemv
```

## Usage
Use `pymv` just like you would use `mv`, i.e. specify the file or directory which you want to rename as well as the new 
name as positional arguments. In addition you have to set a **root directory** using the `-r` flag.

`pymv` will then search through files **and** subdirectories that are part of the **root directory**. Only files that have a 
specific file extension (by default: R, Rmd, RMD, txt, py, ipynb, md, pl, cpp or java) will be evaulated. 

You can extend the list of extensions, either by adding file extensions with the `-e` flag, or by creating a file `.pyfilemv` file in 
your home directory, where each line corresponds to one file extension. 

You can also set the `-a` flag, if you only want to search and replace absolute paths. This might be helpful if you get to many 
'false positive' hits.

If `pymv` finds a match in any of the files, it shows you the old line and how the new line would look like if you want to
update the file. You can confirm that you want to do the replacement by typing `y`.

![showcase_img](https://github.com/nickhir/pyfilemv/raw/main/demo/showcase_img.PNG)

<br >

You can get help by running `pymv -h`

```bash
usage: pymv [-h] [-r ROOT] [-e EXTENSION [EXTENSION ...]] [-a] source destination

positional arguments:
  source                Source file.
  destination           Destination of the source file after the move.

optional arguments:
  -h, --help            show this help message and exit
  -r ROOT, --root ROOT  Specify the absolute path to a directory. All files that are part of that directory (and also subdirectories) are checked if
                        they contain the file you want to move.
  -e EXTENSION [EXTENSION ...], --extension EXTENSION [EXTENSION ...]
                        Specify file extensions which should be included in the search. Should look like this: -e ext1 ext2 ext3. By default, the
                        program searches in the following files: R, Rmd, RMD, txt, py, ipynb, md, pl, cpp, and java
  -a, --absolute        If you set this flag, the program will search for the absolute filepath.
```

## Demo
Below is a small demo to showcase the function of the package. Here, we use it to rename a results object 
and show that the documentation that we wrote for this object, was automatically updated.

![pymv_showcase](https://github.com/nickhir/pyfilemv/raw/main/demo/pyfilemv_demo.gif)