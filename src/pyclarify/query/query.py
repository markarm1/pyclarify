"""
Copyright 2023 Searis AS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from pydantic.fields import Optional
from pydantic import BaseModel, Extra
from typing import Union, List, Dict
from datetime import timedelta
from typing_extensions import Literal


class DataQuery(BaseModel, extra=Extra.forbid):
    filter: Optional[Dict] = {}
    last: Optional[int] = -1
    rollup: Union[timedelta, Literal["window"]] = None


class ResourceQuery(BaseModel, extra=Extra.forbid):
    filter: Optional[Dict] = {}
    sort: Optional[List[str]]
    limit: Optional[int]
    skip: Optional[int]
    total: Optional[bool]
