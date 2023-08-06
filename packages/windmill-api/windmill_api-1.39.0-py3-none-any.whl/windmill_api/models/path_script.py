from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.path_script_input_transforms import PathScriptInputTransforms
from ..models.path_script_type import PathScriptType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PathScript")


@attr.s(auto_attribs=True)
class PathScript:
    """ """

    path: str
    type: PathScriptType
    input_transforms: Union[Unset, PathScriptInputTransforms] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        type = self.type.value

        input_transforms: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.input_transforms, Unset):
            input_transforms = self.input_transforms.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "type": type,
            }
        )
        if input_transforms is not UNSET:
            field_dict["input_transforms"] = input_transforms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        type = PathScriptType(d.pop("type"))

        input_transforms: Union[Unset, PathScriptInputTransforms] = UNSET
        _input_transforms = d.pop("input_transforms", UNSET)
        if not isinstance(_input_transforms, Unset):
            input_transforms = PathScriptInputTransforms.from_dict(_input_transforms)

        path_script = cls(
            path=path,
            type=type,
            input_transforms=input_transforms,
        )

        path_script.additional_properties = d
        return path_script

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
