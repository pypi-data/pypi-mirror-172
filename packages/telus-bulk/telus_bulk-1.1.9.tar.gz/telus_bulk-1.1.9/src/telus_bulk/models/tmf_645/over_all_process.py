from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi_camelcase import CamelModel


class OverAllProcessStatus(Enum):
    """
    Statis for locations objects in over_all_process collection
    """

    PENDING = "pending"
    SENT = "sent"
    DONE = "done"
    PROCESSING = "processing"

    def __str__(self) -> str:
        return str(self.value)


class OverAllProcess(CamelModel):
    """
    docstring
    """

    location: Optional[str] = None
    status: Optional[str] = OverAllProcessStatus.PENDING.value
    csq_id: Optional[str] = None
    csq_ref: Optional[str] = None
    id: Optional[str] = None
    created_at = datetime.now()


OverAllProcess.update_forward_refs()


class OverAllData(CamelModel):
    """
    docstring
    """

    location_id: Optional[str] = None
    location_obj: Optional[dict] = None
    partner: Optional[str] = None
    to_whom: Optional[str] = None
    offers: Optional[list[dict]] = []
    csq_id: Optional[str] = None
    csq_ref: Optional[str] = None
    id: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[str] = None
    created_at_fancy: Optional[str] = None
    updated_at_fancy: Optional[str] = None


OverAllData.update_forward_refs()
