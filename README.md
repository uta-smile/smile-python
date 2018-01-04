# smile-python
SMILE Lab python helper library.

## Installation

```bash
pip install smile
```

## Usage
This library aims to provide a general way to handle logging and command-line parameters.
Its usage is described in the following example:

In **example.py**, we have

```python
import smile as sm
from smile import flags
from smile import logging

flags.DEFINE_string("param", "default_value", "A general flag.")

with flags.Subcommand("echo", dest="action"):
    flags.DEFINE_string("echo_text", "", "The text to be echoed out.")

with flags.Subcommand("echo_bool", dest="action"):
    flags.DEFINE_bool("just_do_it", False, "some help infomation")

FLAGS = flags.FLAGS


def main(_):
    """Print out the FLAGS in the main function."""
    logging.info("param = %s", FLAGS.param)
    if FLAGS.action == "echo":
        logging.warn(FLAGS.echo_text)
    elif FLAGS.action == "echo_bool":
        logging.info("Just do it? %s", "Yes!" if FLAGS.just_do_it else "No :(")


if __name__ == "__main__":
    sm.app.run()
```

Then in terminal, use one of the following way to pass new parameters to the variable of `param`

```bash
python example.py --param=new_value echo --echo_text "Hello, SMILE!"
```
and **YESSSSS!**, we support:

  * **subcommands**: much like `git commit` or `git rm --cached huang.c`.
  * **positional arguments**: "abc.py" in `git add abc.py`
    
### More about logging

The `logging` module can be used together with flags to filter logs, e.g.,

```bash
python example.py --param=new_value echo --echo_text "Hello, SMILE!" --verbosity -1
```

This will filter out the INFO level logs and only display WARN level or below logs.

For more details, view [logging/__init__.py](https://github.com/abseil/abseil-py/blob/master/absl/logging/__init__.py).

## More examples

Please refer to [smoke_test.py](tests/smoke_tests/smoke_test.py).
