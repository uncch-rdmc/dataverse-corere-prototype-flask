# CORE-RE

![Dataverse](https://user-images.githubusercontent.com/48030162/59379352-62f3e180-8d24-11e9-93b6-a7b28767bfb9.png)

## Description:
The main goal of the project is to make these verification tools cost-effective and easily accessible, so journals may implement and enforce more rigorous data policies. This will oblige researchers to in turn adopt more transparent practices and promote reproducible research of the highest quality and integrity throughout the scientific community. 


## Table of Contents:

* [Requirements](#Requirements)
* [Installation](#Installation)
* [Usage](#Usage)
* [Contributing](#Contributing)
* [Credits](#Credits)
* [License](#License)


## Requirements:
Python 3.7+ required

Anaconda is suggested but not required.

Kubernetes and Docker is required for running binderhub.
(https://binderhub.readthedocs.io/en/latest/)

@andreyodum/core2 jupyterlab extension to use with jupyterhub (installed automatically)

R and R server (automatically installed by binderhub)

## Installation:

The CORE-RE project consits of three components: CORE-RE server, binderhub server, and gitlab server.

The latter two can be downlaoded  and set up using the following sites:

https://about.gitlab.com/
https://binderhub.readthedocs.io/en/latest/


### Setting up CORE-RE server

Install the latest version of Python 3 if you haven't already.

Run the following command:
```python
pip install -r requirements.txt
```

This will install the following libraries:
```
authlib==0.10
flask==1.0.2
google-api-python-client
google-auth
virtualenv
```

Run `./run.sh` file to launch the server
or run the following commands in the terminal (change the URLS appropriately):

```github
export FN_AUTH_REDIRECT_URI=http://localhost:5000/google/auth
export FN_BASE_URI=http://localhost:5000
export FN_CLIENT_ID=GOOGLE_CLIENT_ID_GOES_HERE
export FN_CLIENT_SECRET=GOOGLE_CLIENT_SECRET_GOES_HERE

export FN_GITHUB_CLIENT_ID=GITHUB_CLIENT_ID_GOES_HERE
export FN_GITHUB_CLIENT_SECRET=GITHUB_CLIENT_SECRET_GOES_HERE

export FLASK_APP=index.py
export FLASK_DEBUG=1
export FN_FLASK_SECRET_KEY=RANDOMSECRETdsjaldsajio

export DATABASE_URL="postgresql://localhost/core"

python -m flask run -p 5000
```

### Setting up Binderhub server



### Setting up  GitLab Server





## Usage





## Contributing
Thank you for your interest in contributing to CORE-RE Project!  We welcome any contribution from anybody. If you have any questions, please feel free to reach out to us. If you want to add a feature, please create a fork, add the feature, and create a pull request. If you have an issue, please search if there are existing similar issues using the search bar in the issues tab. If an existing open issue exists, contribute to it. Otherwise, please create a new issue.

## Credits
Odum Institute 

University of North Carolina at Chapel Hill

## License
(MIT)

Copyright 2019 Odum Institute

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.