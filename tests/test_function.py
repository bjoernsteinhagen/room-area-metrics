from pydantic import SecretStr

from speckle_automate import (
    AutomationContext,
    AutomationRunData,
    AutomationStatus,
    run_function
)

from main import FunctionInputs, automate_function

from speckle_automate.fixtures import *


def test_function_run(test_automation_run_data: AutomationRunData, test_automation_token: str):
    automation_context = AutomationContext.initialize(
        test_automation_run_data, test_automation_token
    )
    automate_sdk = run_function(
        automation_context,
        automate_function,
        FunctionInputs(
            threshold=0.8,
            rooms_to_exclude="Stair, Utility, Elevator, Residential Lobby, Corridor, Storage, Machine RM, Roof Garden",
        ),
    )

    assert automate_sdk.run_status == AutomationStatus.SUCCEEDED
