![NLoed_Logo](/NLoed_Logo.png)

# NLoed
A Python package for nonlinear optimal experimental design.
 
* **[Description](#description)**
  * [Disclaimer](#disclaimer)
* **[Installation](#installation)**
  * [Do I have Python installed?](#do-i-have-python-installed?)
  * [How do I get the right version of Python/Pip installed?](#how-do-i-get-the-right-version-of-python/pip-installed?)
    * [OSX](#OSX)
      * [Use Homebrew](#use-homebrew)
      * [Use Pyenv](#use-pyenv)
    * [Linux (Ubuntu/Debian)](#linux-(ubuntu/debian))
    * [Windows](#windows)
* **[Dependencies](#dependencies)**
* **[Contributing](#contributing)**
* **[Credits](#credits)**
* **[License](#license)**

## Description
NLoed (suggested pronounciation: "en-load") is an open source Python package for building and 
optimizing experimental designs for fitting nonlinear models, with a specific emphasis on applications in systems 
biology. The package is primarily focused on generating optimal designs for improved parameter estimation
using a relaxed formulation of the design optimization problem. Objectives in NLoed are primarily based
on the expected Fisher information matrix.

NLoed is built on top of [Casadi](https://web.casadi.org/), an optimal control prototyping framework; users of NLoed construct their models using Casadi's symbolic classes. Casadi's symbolic interface allows the user to encode a wide variety of nonlinear mathematical structures into their NLoed model. NLoed supports both static and dynamic nonlinear models including systems of nonlinear differential equations. Casadi also provides a number of numerical
tools, such as automatic differentiation, and interfaces to nonlinear programming solvers, such as [IPOPT](https://github.com/coin-or/Ipopt),
which provide efficient performance.

In addition to design, NLoed provides a number of model-building tools including functions for maximum likelihood fitting, sensitivity analysis, data simulation, asymptotic and profile likelihoods, graphical identifiability diagnostics and quantification of prediction uncertainty. These tools, in conjunction with NLoed's core optimal design functionality, aim to provide a complete model building framework, enabling model construction, experimental design, model fitting and diagnostics to all be done within NLoed. This makes NLoed ideal for model builders heading into the lab or for those who wish to study model identifiability via simulation studies.

### Disclaimer
NLoed is still under development. A reasonable effort has been made to create a stable
functional interface and to test the current release however, users should  proceed with reasonable 
caution in writing code for publication or in developing other numerical tools using NLoed. The interface may be subject to change, especially in advance of the first non-beta (i.e. beta releases are any that preceed version 1.0. Also, the authours make no guarantee for the absolute correctness of all numerical routines implemented in NLoed (or its dependencies). Some reasonable testing of the package with the user's specific model, as well as some understanding of general OED theory are recommended when using the package (especiall before version 1.0). If you identify any bugs or numerical issues, please submit them
to the authours on Github, your error tickets are greatly appreciated! :) 

## Installation
NLoed is available on [PyPI](https://pypi.org/), so you can just use pip to install it!
To install with pip, run:
```sh
pip install nloed
```

Taadaa! You are done! You can then test that it worked by starting up python and importing NLoed with:
```sh
python
[something something something... python starts]
>>>import nloed
[no errors should be thrown]
```
After this it's a good idea to try some of the examples on Github.

### Do I have Python installed?
If you've never used python or pip before, you may want to check a few things first before trying to
 install NLoed.
First make sure you have python installed, that it is on your path, and the python version is appropriate.
To do this, run the following on the command line/prompt:
```sh
python -V
```
It should print out a python version number which must be greater than 3.6.1. If this is susccesful,
you should also have pip installed by default (it ships with python >3.4), to confirm this run:
```sh
pip -V
```
This should print out a similar version number as the one python did.

### How do I get the right version of Python/Pip installed?
If you don't have the right version of python on your system, you will need install it before
installed NLoed. For those unfamiliar with Python, here are some helpful pointers depending on 
your OS:

#### OSX
Macs ship with Python 2.7 by default which doesn't normally come with pip installed and isn't
compatible with NLoed. 

There are two simple options for getting Python >3.6.1 on Mac:

##### Use Homebrew
This is useful if you aren't doing much with Python other than NLoed, but it is a bit less flexible than some other options.
See the [Homebrew website](https://brew.sh/) for details .

* Make sure Xcode dependencies are installed (Homebrew needs these to do stuff):  
    ```sh
    xcode-select --install
    ```
* Install Homebrew; it's a package manager for installing software on Macs:
    ```sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
* Check that Homebrew is installed properly:
    ```sh
    brew --version
    [should print out a version number]
    ```
* Install Python 3 with:
    ```sh
    brew install python3
    ```
* Check python 3 is installed with:
    ```sh
    python3 -V
    ```
* As the command 'python' points to the native 2.7 installed by default on your Mac, you will
now need to use 'python3' to start the newer version installed with Homebrew. To install NLoed on
your python 3 installation specifically, run:
    ```sh
    $ pip3 install nloed
    ```
    Here Homebrew has setup 'pip3' to replace 'pip' in order to avoid confusion.

##### Use Pyenv
This method is better if you are going to do a lot of work in Python and want to organize many 
versions and dependencies. See the [pyenv Github](https://github.com/pyenv/pyenv) for more details.

* Make sure Homebrew is installed as above.
* Run the following to install some needed dependencies;
    ```sh
    brew install openssl readline sqlite3 xz zlib
    ```
* Install pyenv either with  
    a) Homebrew itself (with some changes to .bashrc and a shell restart):
    ```sh
    brew install pyenv
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
    exec "$SHELL"
    ```
    b) The [auto-installer script]((https://github.com/pyenv/pyenv-installer)):..
    ```sh
    curl https://pyenv.run | bash
    ```
* Confirm that pyenv is installed correctly:
    ```sh
    pyenv versions
    [prints out some version, likely just 'system']
    ```
* Install a version of python greater than 3.6.1, for example:
    ```sh
    pyenv install 3.7.0
    ```
* You then need to make this new version active, the easiest way to do it is to make it the global default by running:
    ```sh
    pyenv global 3.7.0
    ```
    Note the version number here should be the same one you installed in the previous step.
    You can check the pyenv documentation for more options for managing versions; it is very flexible.
*   Finally install the NLoed package on the new pyenv version by running:
    ```sh
    pip install nloed
    ```

#### Linux (Ubuntu/Debian)
Recent releases of Ubuntu should come with a version of Python 3.
* To check the version of Python 3 installed, in the terminal run:
    ```sh
    python3 -V
    ```
    This will print the version of the current Python 3 installation.
* If the version printed above is greater than or equal to 3.6.1, you are good to go. Install NLoed by running the following:
    ```sh
    pip3 install nloed
    ```
    Note, the OS has your Python 3 install and corresponding pip command aliased to 'python3' and 'pip3' to avoid confusion with any Python 2 installations on the same system. Use these commands going forward.
* If the version printed in the first step is less than 3.6.1, you will need to install an newer version of Python 3. The easiest way to do this is likely using pyenv. To install pyenv, first get the depenencies by running:
    ```sh
    sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
    ```
* Now use the [auto-installer script](https://github.com/pyenv/pyenv-installer) and restart the shell:
    ```sh
    curl https://pyenv.run | bash
    exec "$SHELL"
    ```
* Check that pyenv is installed correctly:
    ```sh
    pyenv versions
    [prints out some version, likely just 'system']
    ```
* Install a version of python greater than 3.6.1, for example:
    ```sh
    pyenv install 3.7.0
    ```
* You then need to make this new version active, the easiest way to do it is to make it the global default by running:
    ```sh
    pyenv global 3.7.0
    ```
    Note the version number here should match the installation in the previous step.
    Check the pyenv documentation for more options for managing versions; it is very flexible.
*   Finally install the NLoed package on the new pyenv version by running:
    ```sh
    pip install nloed
    ```

#### Windows
If you are using Windows 10, it's likely you do not have Python available in the command prompt by default.

* Go to https://www.python.org/downloads/windows/ and download the desired Python version's installer.
* Run the installer .exe and follow its prompts. Make sure you check the box 'Add Python 3.X to Path' so that the installed Python version will be available from the command prompt. This option is on the first page of the installer.
* Once the install is complete, open the command prompt and install NLoed with pip by running:
    ```sh
    pip install nloed
    ```

## Dependencies & Versions
NLoed requires Python 3.6.1 or newer; Python 2 is not supported.

NLoed uses the following (direct) dipendencies and has been tested with the versions indicated below:
* Casadi>=3.5.0
* Numpy>=1.17.0
* Pandas>=1.0.0
* Scipy
* Matplotlib

## Usage
NLoed consists of two core classes: the Model class and the Design class. NLoed's basic workflow involves
construcing a Model class instance to encode a user's mathematical model and then creating a Design
instance encoding an experimental design for the given Model. The Model and Design classes
can be used iterativly, as Model parameters and assumptions are refined after succesive experiments.
The majority of input and output data for NLoed is handled via Pandas dataframes, which makes
it easy to import data and export designs or simulations to third-party software. 

### Models
The Model class is used to encode all aspects of a model, connecting model inputs, parameters and
observation variables via the model equations and the assumed distributions of the observations variables.
The NLoed Model class supports multi-input, multi-output models with a variety of error distributions, including those for postively skewed, binary and count observation data types. Modelling of
observation hetroskedasticity is also supported, however  all observations are assumed to
be independent (in the current version). The Model class also enables some analysis tools including: fitting, sensitivity and uncertainty analysis, confidence intervals, fitting diagnostics, data simulation
and generating model predictions.

### Designs
The Design class in NLoed is used to generate optimal designs subject to various objectives and constraints specified by the user. Users pass their Model class instance to the Design class to generate an archetypal (relaxed) design for their model. Optimization of the design can be structured in a variety of ways depending on the design contraints and numerical considerations. The resulting Design class instance then provides the
user with functionality to generate a variety of implementable (exact) designs with a desired sample
size. 

Further examples can be found in the \example folder on NLoed's Github. A full description of the OED background, NLoed use cases, and function call formats can be found in the \docs folder on Github.

## Contributing
NLoed is maintained by the [Ingalls Lab](https://uwaterloo.ca/scholar/bingalls/), in the Department of Applied Math, at the University of Waterloo.

Inquiries about contributions and usage can be directed to [Brian Ingalls](https://uwaterloo.ca/applied-mathematics/people-profiles/brian-ingalls) at bingalls[at]uwaterloo.ca 

A detailed guide to setting a development environment for NLoed can be found in DevGuide.md on Github

Issues and feature suggestions can be submitted through Github.

## Credits
NLoed was written by Nathan Braniff and Brian Ingalls.

Special thanks to:
* Michael Astwood for early prototyping of the project
* Zixuan Liu and Taylor Pearce for testing some experimental designs generated by NLoed in the wetlab

## License
This software is released under the GNU Lesser Public Liscence V3
