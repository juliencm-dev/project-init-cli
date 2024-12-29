from datetime import datetime, timezone
from cuid2 import Cuid as CUID2

def cuid() -> str:
    return CUID2().generate()

def nowutc() -> datetime:
    return datetime.now(timezone.utc)



