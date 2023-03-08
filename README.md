# ADSII3ILV - Assignment 2

For this assignment, you need to apply some concepts about basic data structures, trees, and graphs to a realistic problem.

## Before you start
Before you start designing and implementing your assignment remember that you need to commit the `WHOAMI.MD` file with your name, surname and matriculation number inside. This file contain one line as follows:

```
Author: <YOUR_SURNAME> <YOUR_NAME> <YOUR_MATRICULATION_NUMBER>
```

>NOTE: The existence of this file is checked by a new GitHub action. The check on the file name is case sensitive!

## \[!\] What is typing and why you may want to use it
To make sure fewer type-related bugs might be hidden inside your code, 
as well as always knowing how to exactly invoke each function, 
this project now comes with python type stub files!

### Where
Each module now has a corresponding `*.pyi` file in the same directory.
These files are called type stubs and contain the type annotations for the module.
The easiest way to use them is to open the `pyi` file in your IDE and read the type annotations,
it will make checking for input and output types much easier, while also clarifying
what object is expected by a certain function call.

### What do I need to do?
#### Pre-defined functions, classed and methods:
Types are already provided for you, so you don't need to do anything.
You can check all types are valid by installing the [mypy package](https://pypi.org/project/mypy/) 
and running the following command:
```bash
mypy .
```
#### Your own functions, classes and methods:
You don't need to do anything, but you can add type annotations to your code if you wish to.
A gentle introduction to the typing module can be found [here](https://realpython.com/python-type-checking/).
Find the full documentation on the [python website](https://docs.python.org/3/library/typing.html).
> Note: You might want to add type annotations to the .pyi files instead of the .py files
> for consistency with the pre-defined types. This is not mandatory, though.

If you would like to have code completion, PyCharm offers a great support for stub files, 
VSCode has a [plugin](https://github.com/microsoft/pylance-release) that can be installed
and used, and many other IDEs/Editors have similar support.

### How and Why
[PEP404](https://peps.python.org/pep-0484/) and [PEP561](https://peps.python.org/pep-0561/)
introduced the concept of type stub files, which are basically files that contain 
the type annotations of a module.
In layman's terms, this means that you can now know exactly what type of data you are 
passing to a function, and what type of data you are receiving from a function.
This is helpful for two reasons:
- Better autocomplete: you can now call the appropriate methods to a function parameter
without guessing what type of data it is.
- Better tests: the tests provided in this repository were validated using type information,
which means that you can now just worry about functionality rather than fixing type errors.
> Note: Having stub files enables you to check for type errors on GitHub as well. 
> If you wish to do so, go to your project GitHub page, under the Action tab, 
> and start the type_checking action. 
> The action is **not** automatically triggered to avoid confusion.

### Are type annotations mandatory for my assignment?
They are not!
The main reason for their introduction into the codebase was to make sure that tests
were sound and that no hidden bugs were present in the template.
If you feel confident enough to use annotations, you can definitely use them, 
but you are not required to do so.

## Document your solution as you go

For this assignment, submitting the code and the tests is **not** enough. In fact, in addition to well commented code and test cases, to successfully complete Assignment 2 you must also commit a file called `SOLUTION.MD`.

Inside `SOLUTION.MD` you must describe in words and using various diagrams your solution. For instance, you must motivate the data structures that you used to implement the various components.

Do not copy, paste, and comment your code inside `SOLUTION.MD`; this is not want your are asked here! Instead, elaborate about your solution and the main choices you made to complete it.

Possible diagrams that you may include are:

- Data Flow
- UML Class Diagrams
- UML Sequence Diagrams
- UML Activity Diagrams
- UML State Machine Diagrams


>NOTE: The existence of this file is checked by a new GitHub action. The check on the file name is case sensitive!

## Problem Description

Your job is to design a **communication infrastructure** made of **nodes** linked by **bi-directional channels**. Each channel has a **cost** associated with its use, and all the nodes must be reachable.

**Persons** can `join` and `leave` the communication infrastructure anytime. When they `join`, they join via one of the existing nodes. 

The network is built before any person can join it; however, some nodes might be `removed` (i.e., break). All the persons associated with the removed node are deleted. Additionally, if other nodes become unreachable, the entire system stops with an error (`InvalidNetworkException`).

A **central registry** stores information about all the persons currently connected. The registry is updated when a new person joins, or an existing person leaves the network. 
The central registry contains the persons' unique names (`ids`), the unique `id` of the nodes on which they joined, and the (serialized) key they use to encode their messages. 

>NOTE: The registry should provide efficient access to those person-related information.

When a person `sends` a **message**, s/he uses the key to `encode` it into a ~morse code-like format~ made of dots, lines, spaces, and word breaks. 

When a person `receives` a message, s/he must `retrieve` the sender's key from the central registry, `deserialize` the key, and finally `decode` the messages. 

The **key** is built via a training procedure that ensures that characters that appear more frequently are represented with fewer dots/lines than characters that appear less frequently. The training procedure takes as input a text to compute those frequencies.

Consider that "a dot costs less than a line", and ties between chars are resolved using the natural alphabetical order: a-z1-9\<SPACE\>

Messages can contain only:

- lowercase letters
- digits
- blank spaces

> NOTE: All the valid characters that didn't appear in the training text are considered characters with _frequency==0_ and must be included in the key. The ties between chars are resolved using the natural alphabetical order: a-z1-9\<SPACE\>

Messages have a *priority* (high, medium, low) and can be sent either to another person or to all of the connected persons (using a single broadcast message). Furthermore, all messages should be sent using the cheapest path possible (that is, the path whose total cost is the lowest, if multiple paths exist).

Nodes can communicate only to the nodes they are attached to; thus, each node can `forward` messages to other nodes. 

Nodes serves the messages to the persons in the same order they receive them but taking into account messages' priority. Thus, each node stores a copy of the messages until the intended person (i.e., recipient) reads them or leaves the network. 

When a persons leaves the network, all the information related to that person and any (unread) messages are deleted.

# Tests
Now all the tests are located under the `tests` folder and are separated into 3 sub-folders:

- tests/public
- tests/personal
- tests/private

### Public tests
The `public` folder contains all public tests that are visible to everyone. **This folder should be considered untouchable** so that any additional changes can be made without harm to your project. 

### Personal tests
All tests that you write for yourself should be placed in this folder. The contents of this folder will only be changed by you.

### Private tests
All private tests that will be used for grading will be placed under this folder. **This folder also should be considered untouchable**

> NOTE: Files in different directories can have identical names, i.e. *tests/public/test_one.py* *tests/personal/test_one.py*


## Usage of Libraries and Existing Classes/Functions

The usage of libraries that implement the required data structures is in general forbidden. If you need a stack or a queue or a self-balancing binary tree, go on an implement it and do not rely on any existing classes or functions.

The only "external" libraries that you should need are the usual testing libraries: `pytest` and `pytest-cov`. However, in case you have any doubt, **ask the lecturer** in class, per email, or on MSTeams.

## Passing Requirements

You need to commit on GitHub the following files:

- WHOAMI.MD
- SOLUTION.MD
- The python scripts implementing your solution
- Unit tests (named after the usual `test_*.py` naming convention). The unit tests must *all* pass and must achieve at least 90% code coverage. 

> NOTE: If any of the tests you commit does not pass, then your solution cannot be considered correct or complete! 


