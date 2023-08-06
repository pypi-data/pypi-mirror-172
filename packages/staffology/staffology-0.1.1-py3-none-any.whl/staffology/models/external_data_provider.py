from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.auth_scheme import AuthScheme
from ..models.external_data_provider_id import ExternalDataProviderId
from ..models.external_data_provider_type import ExternalDataProviderType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExternalDataProvider")


@attr.s(auto_attribs=True)
class ExternalDataProvider:
    """
    Attributes:
        name (Union[Unset, None, str]):
        id (Union[Unset, ExternalDataProviderId]):
        auth_scheme (Union[Unset, AuthScheme]):
        logo_url (Union[Unset, None, str]):
        icon_url (Union[Unset, None, str]):
        connected (Union[Unset, bool]):
        connected_as (Union[Unset, None, str]):
        requires_config (Union[Unset, bool]):
        types (Union[Unset, None, List[ExternalDataProviderType]]):
    """

    name: Union[Unset, None, str] = UNSET
    id: Union[Unset, ExternalDataProviderId] = UNSET
    auth_scheme: Union[Unset, AuthScheme] = UNSET
    logo_url: Union[Unset, None, str] = UNSET
    icon_url: Union[Unset, None, str] = UNSET
    connected: Union[Unset, bool] = UNSET
    connected_as: Union[Unset, None, str] = UNSET
    requires_config: Union[Unset, bool] = UNSET
    types: Union[Unset, None, List[ExternalDataProviderType]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = self.id.value

        auth_scheme: Union[Unset, str] = UNSET
        if not isinstance(self.auth_scheme, Unset):
            auth_scheme = self.auth_scheme.value

        logo_url = self.logo_url
        icon_url = self.icon_url
        connected = self.connected
        connected_as = self.connected_as
        requires_config = self.requires_config
        types: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.types, Unset):
            if self.types is None:
                types = None
            else:
                types = []
                for types_item_data in self.types:
                    types_item = types_item_data.value

                    types.append(types_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if id is not UNSET:
            field_dict["id"] = id
        if auth_scheme is not UNSET:
            field_dict["authScheme"] = auth_scheme
        if logo_url is not UNSET:
            field_dict["logoUrl"] = logo_url
        if icon_url is not UNSET:
            field_dict["iconUrl"] = icon_url
        if connected is not UNSET:
            field_dict["connected"] = connected
        if connected_as is not UNSET:
            field_dict["connectedAs"] = connected_as
        if requires_config is not UNSET:
            field_dict["requiresConfig"] = requires_config
        if types is not UNSET:
            field_dict["types"] = types

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _id = d.pop("id", UNSET)
        id: Union[Unset, ExternalDataProviderId]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = ExternalDataProviderId(_id)

        _auth_scheme = d.pop("authScheme", UNSET)
        auth_scheme: Union[Unset, AuthScheme]
        if isinstance(_auth_scheme, Unset):
            auth_scheme = UNSET
        else:
            auth_scheme = AuthScheme(_auth_scheme)

        logo_url = d.pop("logoUrl", UNSET)

        icon_url = d.pop("iconUrl", UNSET)

        connected = d.pop("connected", UNSET)

        connected_as = d.pop("connectedAs", UNSET)

        requires_config = d.pop("requiresConfig", UNSET)

        types = []
        _types = d.pop("types", UNSET)
        for types_item_data in _types or []:
            types_item = ExternalDataProviderType(types_item_data)

            types.append(types_item)

        external_data_provider = cls(
            name=name,
            id=id,
            auth_scheme=auth_scheme,
            logo_url=logo_url,
            icon_url=icon_url,
            connected=connected,
            connected_as=connected_as,
            requires_config=requires_config,
            types=types,
        )

        return external_data_provider
