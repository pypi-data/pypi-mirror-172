from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

import attr

from ..extensions import NotPresentError
from ..models.linked_app_config_resource_mixin_linked_resource import LinkedAppConfigResourceMixinLinkedResource
from ..types import UNSET, Unset

T = TypeVar("T", bound="LinkedAppConfigResourceMixin")


@attr.s(auto_attribs=True, repr=False)
class LinkedAppConfigResourceMixin:
    """  """

    _linked_resource: Union[Unset, LinkedAppConfigResourceMixinLinkedResource] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("linked_resource={}".format(repr(self._linked_resource)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "LinkedAppConfigResourceMixin({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        linked_resource: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._linked_resource, Unset):
            linked_resource = self._linked_resource.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if linked_resource is not UNSET:
            field_dict["linkedResource"] = linked_resource

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_linked_resource() -> Union[Unset, LinkedAppConfigResourceMixinLinkedResource]:
            linked_resource: Union[Unset, Union[Unset, LinkedAppConfigResourceMixinLinkedResource]] = UNSET
            _linked_resource = d.pop("linkedResource")

            if not isinstance(_linked_resource, Unset):
                linked_resource = LinkedAppConfigResourceMixinLinkedResource.from_dict(_linked_resource)

            return linked_resource

        try:
            linked_resource = get_linked_resource()
        except KeyError:
            if strict:
                raise
            linked_resource = cast(Union[Unset, LinkedAppConfigResourceMixinLinkedResource], UNSET)

        linked_app_config_resource_mixin = cls(
            linked_resource=linked_resource,
        )

        linked_app_config_resource_mixin.additional_properties = d
        return linked_app_config_resource_mixin

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

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def linked_resource(self) -> LinkedAppConfigResourceMixinLinkedResource:
        if isinstance(self._linked_resource, Unset):
            raise NotPresentError(self, "linked_resource")
        return self._linked_resource

    @linked_resource.setter
    def linked_resource(self, value: LinkedAppConfigResourceMixinLinkedResource) -> None:
        self._linked_resource = value

    @linked_resource.deleter
    def linked_resource(self) -> None:
        self._linked_resource = UNSET
