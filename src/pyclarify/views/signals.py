"""
Copyright 2022 Searis AS

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

from datetime import timedelta
from pydantic import BaseModel, Extra
from pydantic.fields import Optional
from pydantic.json import timedelta_isoformat
from typing import List, Dict
from pyclarify.fields.constraints import (
    TypeSignal,
    SourceTypeSignal,
    LabelsKey,
    InputID,
    ResourceID,
    IntegrationID,
    Annotations,
)
from pyclarify.fields.resource import BaseResource, RelationshipsDict
from pyclarify.query.query import ResourceQuery


class SignalInfo(BaseModel):
    """
    Base attributes shared by most signal structures.

    Parameters
    ----------
    name: string(len:1-128)
        A human-readable name for the resource.
    description: string(len:0-1000)
        A free-form description of the resource.
    labels: Labels
        A map of custom classification attributes. Filtering is done on label keys (labels.<key>).
    sourceType: string(enum)
        Classification of the data source. The value must be "aggregate", "measurement" or "prediction".
    valueType: string(enum)
        How to interpret time-series data points. The value must be "enum" or "numeric".
    engUnit: string
        Engineering unit for time-series data in numeric representations.
    enumValues: map(string => string(len:1-128))
        Map of numeric values to display text in enum representations. The key must represent an integer in range 0-9999.
    sampleInterval: Fixed Duration, null
        The expected distance between data points.
    gapDetection: Fixed Duration, null
        The maximum distance between two data-points before considering it to be a gap.
    """

    name: str
    description: str = ""
    labels: Dict[LabelsKey, List[str]] = {}
    sourceType: SourceTypeSignal = SourceTypeSignal.measurement
    valueType: TypeSignal = TypeSignal.numeric
    engUnit: str = ""
    enumValues: Dict[str, str] = {}
    sampleInterval: timedelta = None
    gapDetection: timedelta = None

    class Config:
        json_encoders = {timedelta: timedelta_isoformat}
        extra = Extra.forbid


class Signal(SignalInfo):
    """
    Extends ItemInfo class.

    Parameters
    ----------
    annotations: Annotations
        A key-value store where integrations can store programmatic meta-data about the resource instance.
        Filtering is done on member fields.
    """

    annotations: Optional[Annotations]


class SavedSignal(SignalInfo):
    input: str
    integration: Optional[IntegrationID]
    item: Optional[ResourceID]


class SignalSelectView(BaseResource):
    attributes: SavedSignal
    relationships: RelationshipsDict


class SelectSignalsParams(BaseModel):
    integration: IntegrationID
    query: ResourceQuery
    include: List[str] = []
    groupIncludedByType: bool = True


class SaveSignalsParams(BaseModel, extra=Extra.forbid):
    integration: IntegrationID
    inputs: Dict[InputID, Signal]
    createOnly: Optional[bool] = False


class SaveSummary(BaseModel, extra=Extra.forbid):
    id: ResourceID
    created: bool
    updated: bool


class SaveSignalsResponse(BaseModel, extra=Extra.forbid):
    signalsByInput: Dict[InputID, SaveSummary]