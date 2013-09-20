Raspberry Pi Mothership client
==============================================================================

Konrad Markus <konker@luxvelocitas.com>

## Installation
Install dependencies as specified in requirements.txt
e.g.
    sudo apt-get install python-pip
    sudo pip install -r requirements.txt

Test it out
    ./client.py <optional id> <optionl notes>

This should result in something like:
    {"status": "OK", "body": "Contact made with mothership"}

Make sure that the client is executed on startup:
    edit /etc/rc.local
    add:
        /<full path to>/client.py <optional id> <optional notes>

## License
See LICENSE
