# udeka!

Udeka is a personal project of a website that allow a user to bookmark the internet as they learn.

## Setting up

Get the source code using the following:

$ git clone https://github.com/parleychat/udeka.git

You will need to create a virtual environment (for Mac users):

```
$ mkdir Environments
$ cd Environments
$ virtualenv <env_name>
$ source <env_name>/bin/activate
(Replace env_name with whatever you want to call it)
```

And then install all the necessary requirements using:
```
$ pip install -r requirements.txt
$ python app.py
```
The website should be running in your local network, so probably ```localhost:5000.```

PS: In case that you have some trouble with the git pull, see this [website](https://stackoverflow.com/questions/11696295/rejected-master-master-non-fast-forward)
