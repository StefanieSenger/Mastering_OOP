from mastering_oop.outside_interaction.abstraction import AbstractSomeAlgorithm


def test_platform_based_import():
    algo = AbstractSomeAlgorithm()
    return algo

test_platform_based_import()
print(test_platform_based_import().value()) # not sure why that fails with AttributeError: 'AbstractSomeAlgorithm' object has no attribute 'value'