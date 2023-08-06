from abc import abstractmethod
from typing import List, Union

from ._item_descriptor_base import OPAbstractItemDescriptor
from .item_section import OPItemField, OPSection


class OPFieldNotFoundException(Exception):
    pass


class OPAbstractItem(OPAbstractItemDescriptor):
    CATEGORY = None

    @abstractmethod
    def __init__(self, item_dict_or_json):
        super().__init__(item_dict_or_json)
        self._initialize_sections()
        self._field_map = self._initialize_fields()

    @property
    def sections(self) -> List[OPSection]:
        section_list = self.get("sections", [])
        return section_list

    def sections_by_label(self, label) -> List[OPSection]:
        """
        Returns a list of zero or more sections matching the given title.
        Sections are not required to have unique titles, so there may be more than one match.
        """
        matching_sections = []
        sect: OPSection
        for sect in self.sections:
            if sect.label == label:
                matching_sections.append(sect)

        return matching_sections

    def section_by_id(self, section_id) -> OPSection:
        section: OPSection
        for sect in self.sections:
            if sect.section_id == section_id:
                section = sect
                break
        return section

    def first_section_by_label(self, label) -> OPSection:
        sections = self.sections_by_label(label)
        section = None
        if sections:
            section = sections[0]
        return section

    def field_value_by_section_title(self, section_title: str, field_label: str):
        section = self.first_section_by_label(section_title)
        value = self._field_value_from_section(section, field_label)
        return value

    def field_by_id(self, field_id) -> OPItemField:
        try:
            field = self._field_map[field_id]
        except KeyError:
            raise OPFieldNotFoundException(
                f"Field not found with ID: {field_id}")
        return field

    def fields_by_label(self, field_label: str) -> List[OPItemField]:
        fields = []
        f: OPItemField
        for _, f in self._field_map.items():
            if f.label == field_label:
                fields.append(f)
        return fields

    def first_field_by_label(self, field_label: str) -> OPItemField:
        fields = self.fields_by_label(field_label)
        f = fields[0]
        return f

    def field_value_by_id(self, field_id):
        field = self.field_by_id(field_id)
        value = field.value
        return value

    def field_reference_by_id(self, field_id) -> Union[str, None]:
        field = self.field_by_id(field_id)
        ref = field.reference
        return ref

    def _field_value_from_section(self, section: OPSection, field_label: str):
        section_field: OPItemField = section.fields_by_label(field_label)[0]
        value = section_field.value
        return value

    def _initialize_sections(self):
        section_list = []
        _sections = self.get("sections")
        if _sections:
            for section_dict in _sections:
                s = OPSection(section_dict)
                section_list.append(s)
        self["sections"] = section_list

    def _initialize_fields(self):
        field_list = []
        field_map = {}
        _fields = self.get("fields", [])
        for field_dict in _fields:
            field = OPItemField(field_dict)
            section_dict = field.get("section")
            if section_dict:
                section_id = section_dict["id"]
                section = self.section_by_id(section_id)
                section.register_field(field_dict)
            field_list.append(field)
            field_map[field.field_id] = field
        self["fields"] = field_list
        return field_map
