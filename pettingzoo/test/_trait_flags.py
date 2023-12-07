"""Flags to indicate that specific tests are expected to fail.

These can be included within an environment's metadata variable
to silence specific warnings during the api tests. This should be done
when the behaviour of the environment would normally raise a warning,
but that beahviour is expected in this environment for whatever reason.

As an example of usage, normally an observation that is all zeros would
raise a warning during the api_test as a sign that something may be
wrong. However, if this is expected for your environment, you may not
want that warning to occur as it is not useful. You can do the
following to prevent the warning:

```
from pettingzoo.test import Traits


class CustomEnv(AECEnv):
    metadata = {
        "render_modes": ["human"],
        "name": "CustomEnv",
        "test_traits": [
            Traits.ALL_ZEROS_OBS,  # <------ disable all_zeros warning
        ],
    }

    ... rest of environment code ...
```

This will disable that specific warning. The test_traits value should
be a list of items from the Traits enum in the code below. It is
optional, if there are no warnings you wish to ignore, omit the
test_traits metadata.
"""

from enum import Enum

Traits = Enum(
    "Traits",
    [
        "ALL_ZEROS_OBS",  # observations may be all zero
        "OBS_DICTS",  # observations are a dictionary
        "OBS_SPACE",  # observations are not a gym box/discreate
    ],
)
