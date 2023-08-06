## installation ##
```
python3 -m pip install opprint
```

## usage ##
op(***arg***, ***var***=None, ***format***=False, ***yml***=False)
```
from opPrint import op
greeting = 'hello world!'

# basic
op(greeting)

# with label
op('op says...', greeting)

# with standard format
op(greeting, format=True)

# with yaml format
op(greeting, format=True, yml=True)

# with all params
op('op says...', greeting, format=True, yml=True)
```
