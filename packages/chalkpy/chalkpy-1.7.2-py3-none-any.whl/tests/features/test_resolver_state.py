from typing import Optional

from chalk import offline
from chalk.features import features
from chalk.state import State


@features
class HomeFeatures:
    home_id: str
    address: str
    price: int
    sq_ft: int


@offline
def get_address(hid: HomeFeatures.home_id, s: State[Optional[str]] = None) -> HomeFeatures.address:
    return "Bridge Street" if hid == 1 else "Filbert Street"


def test_multiple_output():
    pass
