from pyunitx._api import make_compound_unit, make_compound_dimension, si_unit
from pyunitx.current import Current, amperes
from pyunitx.voltage import Potential, volts


Resistance = make_compound_dimension(name="Resistance", exponents={Potential: 1, Current: -1})

ohms = make_compound_unit(
    name="ohms",
    abbrev="Ω",
    exponents={volts: 1, amperes: -1},
    scale=1,
    doc="""\
    A current of one ampere traveling through one ohm of resistance drops its
    potential by one volt.
    """
)

generated = si_unit(base_unit=ohms)

__all__ = [
              "Resistance",
              "ohms"
          ] + list(generated.keys())
