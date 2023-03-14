from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Union, List


class RepositoryAnalyzeValidator(BaseModel):
    url: Union[str, List[str]]
    start_date: Optional[datetime]
    end_date: Optional[datetime]


