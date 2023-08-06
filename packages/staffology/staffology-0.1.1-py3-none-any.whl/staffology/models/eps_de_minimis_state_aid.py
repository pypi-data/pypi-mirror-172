from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EpsDeMinimisStateAid")


@attr.s(auto_attribs=True)
class EpsDeMinimisStateAid:
    """Used on an EPS to declare an Employment Allowance DeMinimis State Aid information

    Attributes:
        agri (Union[Unset, bool]):
        fisheries_aqua (Union[Unset, bool]):
        road_trans (Union[Unset, bool]):
        indust (Union[Unset, bool]):
    """

    agri: Union[Unset, bool] = UNSET
    fisheries_aqua: Union[Unset, bool] = UNSET
    road_trans: Union[Unset, bool] = UNSET
    indust: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        agri = self.agri
        fisheries_aqua = self.fisheries_aqua
        road_trans = self.road_trans
        indust = self.indust

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if agri is not UNSET:
            field_dict["agri"] = agri
        if fisheries_aqua is not UNSET:
            field_dict["fisheriesAqua"] = fisheries_aqua
        if road_trans is not UNSET:
            field_dict["roadTrans"] = road_trans
        if indust is not UNSET:
            field_dict["indust"] = indust

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        agri = d.pop("agri", UNSET)

        fisheries_aqua = d.pop("fisheriesAqua", UNSET)

        road_trans = d.pop("roadTrans", UNSET)

        indust = d.pop("indust", UNSET)

        eps_de_minimis_state_aid = cls(
            agri=agri,
            fisheries_aqua=fisheries_aqua,
            road_trans=road_trans,
            indust=indust,
        )

        return eps_de_minimis_state_aid
