import importlib


def test_reverse_generators_are_importable_from_the_pytest_suite():
    module = importlib.import_module(
        "scripts.reverse.re702_unimplemented_source_behavior_contract_gate"
    )

    assert callable(module.build_gate)
