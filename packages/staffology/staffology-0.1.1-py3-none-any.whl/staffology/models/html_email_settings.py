from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="HtmlEmailSettings")


@attr.s(auto_attribs=True)
class HtmlEmailSettings:
    """
    Attributes:
        body_css_style (Union[Unset, None, str]):
        font_css_style (Union[Unset, None, str]):
        button_css_style (Union[Unset, None, str]):
        header_html (Union[Unset, None, str]):
        footer_html (Union[Unset, None, str]):
    """

    body_css_style: Union[Unset, None, str] = UNSET
    font_css_style: Union[Unset, None, str] = UNSET
    button_css_style: Union[Unset, None, str] = UNSET
    header_html: Union[Unset, None, str] = UNSET
    footer_html: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        body_css_style = self.body_css_style
        font_css_style = self.font_css_style
        button_css_style = self.button_css_style
        header_html = self.header_html
        footer_html = self.footer_html

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if body_css_style is not UNSET:
            field_dict["bodyCssStyle"] = body_css_style
        if font_css_style is not UNSET:
            field_dict["fontCssStyle"] = font_css_style
        if button_css_style is not UNSET:
            field_dict["buttonCssStyle"] = button_css_style
        if header_html is not UNSET:
            field_dict["headerHtml"] = header_html
        if footer_html is not UNSET:
            field_dict["footerHtml"] = footer_html

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        body_css_style = d.pop("bodyCssStyle", UNSET)

        font_css_style = d.pop("fontCssStyle", UNSET)

        button_css_style = d.pop("buttonCssStyle", UNSET)

        header_html = d.pop("headerHtml", UNSET)

        footer_html = d.pop("footerHtml", UNSET)

        html_email_settings = cls(
            body_css_style=body_css_style,
            font_css_style=font_css_style,
            button_css_style=button_css_style,
            header_html=header_html,
            footer_html=footer_html,
        )

        return html_email_settings
