from typing import Optional
import xml.etree.ElementTree as ET
from ...xml.XmlReader import XmlReader as XR
from ..namespaces import COMMON
from ..namespaces import DATA
from ..dto.DeliveryNotes import DeliveryNotes


def deserialize_delivery_notes(element: ET.Element) -> Optional[DeliveryNotes]:
    if element is None:
        return None

    result = DeliveryNotes(
        delivery_note=[e.text for e in XR.find_all_child(element, 'deliveryNote', DATA)],
    )

    return result
