Installing matplotlib on Fedora for working with dvm-dos-tem visualization tools. 

Plan is to use a virtual environment and pip to manage all the various python libraries. But there is some stuff that must be compiled outside of python and we will use yum to manage those things.

Move to your home then install virtualenv.

    $ cd ~
    $ yum search virtualenv
    $ sudo yum install python-virtualenv


Now, create a new virtualenv called "science".

    $ mkdir venvs
    $ cd venvs/
    $ virtualenv science 

Now use yum to build all the dependencies for matplotlib

    $ sudo yum-builddep python-matplotlib

Now "turn on" your python environment. Note the change to the beginning of your prompt. Type "deactivate" to get out of the virtual environment.

    $ cd ~
    $ source ~/venvs/science/bin/activate

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