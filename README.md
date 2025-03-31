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