# pylint: disable=too-few-public-methods

from __future__ import annotations
from typing import List, Optional, Dict

# BaseModel actually _does_ exist.
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class JobDiff(BaseModel):
    Fields: Optional[List[FieldDiff]]
    ID: str
    Objects: Optional[List[ObjectDiff]]
    TaskGroups: Optional[List[TaskGroupDiff]]
    Type: str


class TaskGroupDiff(BaseModel):
    Fields: Optional[List[FieldDiff]]
    Name: str
    Objects: Optional[List[ObjectDiff]]
    Tasks: Optional[List[TaskDiff]]
    Type: str
    Updates: Optional[Dict[str, int]]


class FieldDiff(BaseModel):
    Annotations: Optional[List[str]]
    Name: str
    New: str
    Old: str
    Type: str


class ObjectDiff(BaseModel):
    Fields: List[FieldDiff]
    Name: str
    Objects: Optional[List[ObjectDiff]]
    Type: str


class TaskDiff(BaseModel):
    Type: str
    Name: str
    Fields: Optional[List[FieldDiff]]
    Objects: Optional[List[ObjectDiff]]
    Annotations: Optional[List[str]]


ObjectDiff.update_forward_refs()
JobDiff.update_forward_refs()
TaskGroupDiff.update_forward_refs()
