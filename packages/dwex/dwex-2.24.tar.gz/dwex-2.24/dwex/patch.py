import elftools.dwarf.structs
from elftools.construct.macros import Array
import elftools.dwarf.locationlists
from elftools.common.exceptions import DWARFError

# Fixes to pyelftools that are not in the released version yet
# Not sure about form_indirect, no binaries.
def monkeypatch():
    # Not sure about DW_FORM_indirect - need a test binary
    # This patches DW_FORM_data16
    def _create_dw_form_ex(self):
        self._create_dw_form_base()
        self.Dwarf_dw_form['DW_FORM_data16'] = Array(16, self.Dwarf_uint8(''))
            
    elftools.dwarf.structs.DWARFStructs._create_dw_form_base = elftools.dwarf.structs.DWARFStructs._create_dw_form
    elftools.dwarf.structs.DWARFStructs._create_dw_form = _create_dw_form_ex

    def get_location_list_at_offset_ex(self, offset, die=None):
        if die is None:
            raise DWARFError("For this binary, \"die\" needs to be provided")
        section = self._loclists if die.cu.header.version >= 5 else self._loc
        return section.get_location_list_at_offset(offset, die)
    elftools.dwarf.locationlists.LocationListsPair.get_location_list_at_offset = get_location_list_at_offset_ex