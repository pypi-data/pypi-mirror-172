from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List


class AnotherEnum(Enum):
    enum_field = "enum"


class CompoundField(BaseModel):
    bar: Optional[str] = Field(
        None,
        description="Another primitive field",
        multiple=False,
        typeClass="primitive",
        typeName="fooCompoundField",
    )


class InvalidBlock(BaseModel):

    foo: Optional[str] = Field(
        None,
        description="Some primitive field",
        multiple=False,
        typeClass="primitive",
        typeName="fooField",
    )

    compound: List[CompoundField] = Field(
        default_factory=list,
        description="Some compound field",
        multiple=False,
        typeClass="primitive",
        typeName="fooField",
    )

    some_enum: AnotherEnum = Field(
        default_factory=list,
        description="Some enum field",
        multiple=False,
        typeClass="primitive",
        typeName="fooEnum",
    )

    def add_compound(self, bar):
        self.compound.append(CompoundField(bar=bar))

    _metadatablock_name: Optional[str] = "invalidblock"
