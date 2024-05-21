# module with variant implementations

import sys

from mastering_oop.outside_interaction.abstraction import AbstractSomeAlgorithm

print(f"sys.platform: {sys.platform}")

if sys.platform.endswith("32"):
    # print(f"{sys.platform}: SHORT")
    from mastering_oop.outside_interaction.short_32_bit_version import Implementation_Short as SomeAlgorithm
    SomeAlgorithm = Implementation_Short
else:
    # print(f"{sys.platform}: LONG")
    from mastering_oop.outside_interaction.long_64_bit_version import Implementation_Long as SomeAlgorithm

# Some additional debugging to display the import behavior
print(f"{__name__}: {SomeAlgorithm.__module__}\n{SomeAlgorithm.__doc__}")