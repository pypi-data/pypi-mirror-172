from typing import Optional
import xml.etree.ElementTree as ET
from ...xml.XmlReader import XmlReader as XR
from ..namespaces import COMMON
from ..namespaces import DATA
from ..dto.ContractNumbers import ContractNumbers


def deserialize_contract_numbers(element: ET.Element) -> Optional[ContractNumbers]:
    if element is None:
        return None

    result = ContractNumbers(
        contract_number=[e.text for e in XR.find_all_child(element, 'contractNumber', DATA)],
    )

    return result
