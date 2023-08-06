# manuscriptify

Compile Google docs into a manuscript


## Installation and Setup

#### 1. Install manuscriptify

    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ pip install manuscriptify

#### 2. Setup your project

    $ cat << EOF >> ~/.zshrc

    # manuscriptify project config
    export MSFY_SOURCE='my awesome novel'
    export MSFY_PSEUDONYM='Joe Bloggs'
    export MSFY_CATEGORY='YA' # Adult/Middle School/etc
    export MSFY_GENRE='Adventure Fantasy'
    export MSFY_TITLE='My Awesome Novel'
    export MSFY_REPLY_TO='Joe Bloggs'
    export MSFY_EMAIL='joe.bloggs@here.there'
    export MSFY_PHONE='+1 (555) 1234 5678'
    export MSFY_STREET1='555 Mulholland Dr'
    export MSFY_STREET2='Los Angeles CA 90055'
    EOF

    $ source ~/.zshrc

#### 3. If your source object is a folder

Place an integer value (to be used as the sort key) in the description  
field of each object in the folder tree. This will be used as a sort key.

&nbsp;  

![view details](tests/media1.png "View details")

&nbsp;  

![edit description](tests/media2.png "Edit description")

## Usage

    $ manuscriptify
    My Awesome Novel was manuscriptified

    # The contents of your source doc or folder
    # was assembled and placed in a new doc in
    # the manuscriptify folder in your Google
    # drive.
