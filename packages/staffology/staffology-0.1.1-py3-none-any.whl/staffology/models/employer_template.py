from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.employer_template_type import EmployerTemplateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployerTemplate")


@attr.s(auto_attribs=True)
class EmployerTemplate:
    """
    Attributes:
        type (Union[Unset, EmployerTemplateType]):
        description (Union[Unset, None, str]): Explains the purpose of this template
        is_custom (Union[Unset, bool]): Indicates whether or not this template has been changed from the default
            content.
        content (Union[Unset, None, str]):
        subject (Union[Unset, None, str]):
        default_content (Union[Unset, None, str]): [readonly] The default content for this template
        default_subject (Union[Unset, None, str]): [readonly] The default subject for this template
        has_subject (Union[Unset, bool]): [readonly] If false then the Subject property is not relevant for this
            template type
        tokens (Union[Unset, None, List[str]]): [readonly] A list of tokens that can be used with this template.
            For example, if 'Employee.FirstName' is in the list then use '{Employee.FirstName}' in the Content or Subject
            and
            it'll be replaced with the relevant value when the template is parsed.
        tokens_expanded (Union[Unset, bool]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    type: Union[Unset, EmployerTemplateType] = UNSET
    description: Union[Unset, None, str] = UNSET
    is_custom: Union[Unset, bool] = UNSET
    content: Union[Unset, None, str] = UNSET
    subject: Union[Unset, None, str] = UNSET
    default_content: Union[Unset, None, str] = UNSET
    default_subject: Union[Unset, None, str] = UNSET
    has_subject: Union[Unset, bool] = UNSET
    tokens: Union[Unset, None, List[str]] = UNSET
    tokens_expanded: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        description = self.description
        is_custom = self.is_custom
        content = self.content
        subject = self.subject
        default_content = self.default_content
        default_subject = self.default_subject
        has_subject = self.has_subject
        tokens: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.tokens, Unset):
            if self.tokens is None:
                tokens = None
            else:
                tokens = self.tokens

        tokens_expanded = self.tokens_expanded
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if description is not UNSET:
            field_dict["description"] = description
        if is_custom is not UNSET:
            field_dict["isCustom"] = is_custom
        if content is not UNSET:
            field_dict["content"] = content
        if subject is not UNSET:
            field_dict["subject"] = subject
        if default_content is not UNSET:
            field_dict["defaultContent"] = default_content
        if default_subject is not UNSET:
            field_dict["defaultSubject"] = default_subject
        if has_subject is not UNSET:
            field_dict["hasSubject"] = has_subject
        if tokens is not UNSET:
            field_dict["tokens"] = tokens
        if tokens_expanded is not UNSET:
            field_dict["tokensExpanded"] = tokens_expanded
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, EmployerTemplateType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = EmployerTemplateType(_type)

        description = d.pop("description", UNSET)

        is_custom = d.pop("isCustom", UNSET)

        content = d.pop("content", UNSET)

        subject = d.pop("subject", UNSET)

        default_content = d.pop("defaultContent", UNSET)

        default_subject = d.pop("defaultSubject", UNSET)

        has_subject = d.pop("hasSubject", UNSET)

        tokens = cast(List[str], d.pop("tokens", UNSET))

        tokens_expanded = d.pop("tokensExpanded", UNSET)

        id = d.pop("id", UNSET)

        employer_template = cls(
            type=type,
            description=description,
            is_custom=is_custom,
            content=content,
            subject=subject,
            default_content=default_content,
            default_subject=default_subject,
            has_subject=has_subject,
            tokens=tokens,
            tokens_expanded=tokens_expanded,
            id=id,
        )

        return employer_template
