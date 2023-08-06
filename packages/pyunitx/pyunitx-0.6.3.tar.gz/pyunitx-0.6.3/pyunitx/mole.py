from pyunitx._api import make_dimension, make_unit, si_unit

Quantity = make_dimension("Quantity")

moles = make_unit(
    name="moles",
    dimension=Quantity,
    scale=1,
    abbrev="mol",
    doc="""\
    A mole is the number of atoms in 12 grams of carbon-12.
    
    It basically is a dimensionless quantity, but is included in the SI system
    for its pragmatic usefulness in chemistry and fluid physics.
    """
)
generated = si_unit(base_unit=moles)
globals().update(generated)

__all__ = [
              "Quantity",
              "moles",
          ] + list(generated.keys())
