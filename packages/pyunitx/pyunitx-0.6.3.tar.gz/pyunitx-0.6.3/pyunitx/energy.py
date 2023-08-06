from pyunitx._api import make_compound_dimension, make_compound_unit, si_unit
from pyunitx.force import pounds
from pyunitx.length import Length, meters, feet
from pyunitx.mass import Mass, kilograms
from pyunitx.time import seconds, Time



Energy = make_compound_dimension({Mass: 1, Length: 2, Time: -2}, "Energy")

joules = make_compound_unit(
    name="joules",
    scale=1,
    exponents={kilograms: 1, meters: 2, seconds: -2},
    abbrev="J",
    doc="""\
    The joule is the base unit of energy in the SI system. It is the amount of
    work done on an object by pushing it with a 1 N force for 1 m. 
    """
)

generated = si_unit(base_unit=joules)
globals().update(generated)

calorie = make_compound_unit(
    name="calorie",
    scale="4.184",
    exponents=joules.composition.to_pairs(),
    abbrev="cal",
    doc="""\
    This is the gram calorie, the amount of heat energy necessary to heat 1 gram
    of water by 1 \xb0C. Nutritional calories are 1000 times larger, using a 
    kilogram in the calculation instead.
    """
)
btu = make_compound_unit(
    name="btu",
    abbrev="btu",
    scale="1.05435e3",
    exponents={feet: 1, pounds: 1},
    doc="""\
    There are many different possible definitions of the British Thermal Unit, 
    this is the thermochemical definition.
    """
)

__all__ = [
              "Energy",
              "joules",
              "calorie",
              "btu",
          ] + list(generated.keys())
