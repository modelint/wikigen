## Class Model Description Wiki Template Generator

Here we take an *.xcm file (Executable Class Model) as input and output a set of class and relationship description markdown files into a local Github wiki directory.

This saves a lot of typing and cut and paste creating the wiki documentation of an Executable UML class model.

Let's say you have a file named elevator.xcm in the current working directory

Just do this:

`% wikigen -m elevator.xcm -w ev_wiki`

`-m` specifies the path to your xcm file

`-w` specifies the target wiki directory, it will be created if it does not exist

Any files in the target directory will be overwritten each time you run the command.

There are some debug options, version etc.

Type:

`% wikigen -help`

To get the most up to date list of options

### Installation

I recommend creating a virtual environment with python 3.13

(download python 3.13 and ensure that this is the current version)

% python3 venv wiki_env

Activate the environment

`% source wiki_env/bin/activate`

Then with that environment activated (as indicated by the parenthesis before the shell prompt below):

`(wikigen) % pip install xcm-wiki-gen`

Now you've got the package installed in your environment.
At this point you can deactivate your environment if you like:

`(wikigen) % deactivate`

`% `

Later you can always reactivate the environment and upgrade to the latest version with:

`% source wiki_env/bin/activate`

`(wikigen) % pip install xcm-wiki-gen -U`

The binary command is in wiki_env/bin directory. To elminate the need to go back and keep activating the environment, just create a symbolic link to the command whereever you keep your local bin files. I do this:

`% cd ~/bin`

`% ln -s wiki_env/bin/wikigen .`

Now open a new terminal window (or refresh your shell environment) and the command should be available. A quick test is just to check the version.

`% wikigen -V`

`Blueprint Class Model Wiki Generator version: 0.1.2`

`%`


