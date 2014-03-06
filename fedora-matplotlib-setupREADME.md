matplotlib on Fedora for ddtv
====================================

The plan is to use a virtual environment and `pip` to manage all the various python libraries. But there is some stuff that must be compiled outside of python and we will use `yum` (specifically `yum-builddep`) to manage those things.

Use yum to install `virtualenv`.

    $ yum search virtualenv
    $ sudo yum install python-virtualenv

Now use yum to build all the dependencies for matplotlib

    $ sudo yum-builddep python-matplotlib

Move to home and create a new virtual environment called "science". You can call it whatever you want. At a later date, we may find it useful to keep the virtualenv with a specific project. But for starters, it should be fine to make one in your home directory. You could reuse this environment for other projects.

    $ cd ~
    $ mkdir venvs
    $ cd venvs/
    $ virtualenv science 

Now "turn on" your python environment. Note the change to the beginning of your prompt. Type "deactivate" to get out of the virtual environment.

    $ cd ~
    $ source ~/venvs/science/bin/activate
    (science) $

 Now with your new environment activated, install the plotting stuff.
 
    (science) $ pip install matplotlib
    (science) $ pip install ipython

And finally, get the latest visualizations scripts:
    
    (science) $ git clone git@github.com:tobeycarman/ddtv.git
    (science) $ cd ddtv/
    (science) $ git checkout cal-prototype
    (science) $ cd cal-prototype/
    (science) $ ./plot_monthly_hydro.py 

And you should be able to see the graph!