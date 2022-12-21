### Set Virtualenv

python -m venv ./venv
./venv/bin/activate

## For Mac (Intel) users
Before running `pip` command, it is required to install `brew install postgresql` first!

## For Mac (Silicon) users
Before running `pip` command, it is required to run below commands:

```
brew install libpq --build-from-source
brew install openssl

export LDFLAGS="-L/opt/homebrew/opt/openssl@1.1/lib -L/opt/homebrew/opt/libpq/lib"

export CPPFLAGS="-I/opt/homebrew/opt/openssl@1.1/include -I/opt/homebrew/opt/libpq/include"
```