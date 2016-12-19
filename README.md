# smile-python
SMILE Lab python helper library.

## Installation

```bash
pip install smile
```

## Usage
This library aims to handle commad-line parameters. Its usage is described in a following example

In **example.py**, we have

```python
import smile as sm

sm.app.flags.DEFINE_string("param", "default_value", "some help infomation")

FLAGS = sm.app.flags.FLAGS


def main(_):
    print "param = " + FLAGS.param_name

if __name__ == "__main__":
    sm.app.run()

```

Then in terminal, use one of the following ways to passs new parameter to the variable of `param`

```bash
python example.py --param=new_value
```
or 

```bash
python example.py --param "new_value"
```