# pydeohub

![pydeohub](https://user-images.githubusercontent.com/37907774/195731748-53e8b78e-fc42-4e33-93c9-64b7ffa5bb33.png)

Python interface for ethernet-connected Blackmagic Design Smart Videohub SDI routers.

## Installation
```
pip install pydeohub
```

## Documentation
A full API reference and small walkthrough is available on [Read the Docs](http://pydeohub.readthedocs.io/).

## Example
```python
from pydeohub import Videohub

hub = Videohub('192.168.0.150')

hub.route(0, 0) # Note that input/output identifiers are 0-indexed.

hub.input_label(1, 'Camera 2')
hub.output_label(0, 'Switcher 1')
```

## Additional Information
This is a work in progress and while it implements the vast majority of the Videohub Ethernet Protocol, it does not do everything.  The infrastructure around locking inputs and oututs, video processors, and serial controllers is unimplemented.

Questions, comments, and contributions are welcome.
