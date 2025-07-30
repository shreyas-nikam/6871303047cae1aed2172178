import pytest
from definition_a3fabeafa53f4d27a81439696e142df4 import set_risk_appetite

@pytest.mark.parametrize("max_financial_loss, max_incidents, max_reputational_impact", [
    (1000000.0, 10, 5),  # Typical values
    (0.0, 0, 0),  # Zero values
    (float('inf'), 1000, 100),  # Very large values
    (-1000.0, -5, -1),  # Negative values
    (1000.5, 5.5, 2.5), # Float values
])
def test_set_risk_appetite(max_financial_loss, max_incidents, max_reputational_impact):
    # This test primarily checks that the function executes without error for various inputs.
    # More comprehensive testing would require inspecting global state or object attributes,
    # which depends on how the function stores the risk appetite.
    try:
        set_risk_appetite(max_financial_loss, max_incidents, max_reputational_impact)
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")