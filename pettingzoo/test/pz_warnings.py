"""Warnings for tests that fail.

These are warnings for specific cases that are not expected in the API.
They are used by several of the test functions.

Each class can be individually ignored in an environment by using the
environment's metadata variable to silence specific warnings during the
api tests.

This should be done when the behaviour of the environment would normally
raise a warning, but that beahviour is expected in this environment for
whatever reason.

As an example of usage, normally an observation that is all zeros would
raise a warning during the api_test as a sign that something may be
wrong. However, if this is expected for your environment, you may not
want that warning to occur as it is not useful. You can do the
following to prevent the warning:

```
class CustomEnv(AECEnv):
    metadata = {
        "ignore_warnings": [
            "ObservationAllZerosWarning",  # <--- ignore this warning
        ],
    }
    ... rest of environment code ...
```

This will disable that specific warning. The ignore_warnings value
should be a list of the warning classes to ignore (as strings).
It is optional, if there are no warnings you wish to ignore, just
omit the ignore_warnings metadata.
"""

import inspect
import sys
import warnings


class PZWarning(Warning):
    msg = "Generic Petting Zoo warning"

    def __str__(self) -> str:
        return self.warning


class ObservationNotNumPyWarning(PZWarning):
    warning = "Observation is not a NumPy array"


class ActionMaskAllZerosWarning(PZWarning):
    warning = "Action mask numpy array is all zeros (no legal actions)."


class ObservationAllZerosWarning(PZWarning):
    warning = "Observation numpy array is all zeros."


class StateAllZerosWarning(PZWarning):
    warning = "State numpy array is all zeros."


class ObservationSpaceWarning(PZWarning):
    warning = "Observation space for each agent probably should be gymnasium.spaces.box or gymnasium.spaces.discrete"


class BadGraphicObservationWarning(PZWarning):
    warning = "The observation contains negative numbers and is in the shape of a graphical observation. This might be a bad thing."


class BadGraphicStateWarning(PZWarning):
    warning = "The state contains negative numbers and is in the shape of a graphical observation. This might be a bad thing."


class DifferentObservationShapeWarning(PZWarning):
    warning = "Observations are different shapes"


class DifferentObservationSpaceSizeWarning(PZWarning):
    warning = "Agents have different observation space sizes"


class InfinityMaxObservationSpaceWarning(PZWarning):
    warning = (
        "Agent's maximum observation space value is infinity. This is probably too high"
    )


class NegInfinityMinObservationSpaceWarning(PZWarning):
    warning = "Agent's minimum observation space value is -infinity. This is probably too low."


class InfinityMaxStateSpaceWarning(PZWarning):
    warning = (
        "Environment's maximum state space value is infinity. This is probably too high"
    )


class NegInfinityMinStateSpaceWarning(PZWarning):
    warning = "Environment's minimum state space value is -infinity. This is probably too low."


class NonStandardNameWarning(PZWarning):
    warning = 'We recommend agents to be named in the format <descriptor>_<number>, like "player_0"'


class MissingPossibleAgentsWarning(PZWarning):
    warning = """This environment does not have possible_agents defined.
    This is not a required part 'of the API as environments with procedurally
    generated agents cannot always have this property defined. However, this is
    very uncommon and these features should be included whenever possible as all
    standard learning code requires these properties. Also not that if you do not
    have possible_agents it should also not be possible for you to expose the
    possible_agents list and observation_spaces, action_spaces dictionaries."""


def add_warning_filters_from_env(env) -> None:
    """Add the warning filters, if any, from the environment"""
    try:
        warning_filters = env.metadata.get("ignore_warnings", [])
    except AttributeError:
        warning_filters = []  # no metadata, ignore that here

    for filter_ in warning_filters:
        try:
            warning_class = warning_classes[filter_]
        except KeyError as e:  # the str given isn't a warning class
            raise KeyError(f"{e} is not a known petting zoo warning class")
        warnings.simplefilter("ignore", warning_class)


def _is_class_in_this_module(obj) -> bool:
    """Return true is the obj is a class defined in this module."""
    return inspect.isclass(obj) and obj.__module__ == __name__


# this makes a dictionary with keys being the string version of each of the classes
# above and the values being the class type itself. There is probably a smarter way
# to pull this off, but it's not occuring to me right now.
# This is to allow warnings to be given as strings rather than classes (which would
# need to be imported from the test module)
warning_classes = dict(
    inspect.getmembers(sys.modules[__name__], _is_class_in_this_module)
)
