__author__ = 'bjoern.kobes@bonava.com'

import time

class Dauer:
    """Klasse zur Messung der Dauer des Vorgangs"""

    def __init__(self):
        self.start = time.time()

#    def neustart(self):
#        self.start = time.time()

    def zeitmessung(self):
        return time.time() - self.start

# Zeitmessung ------------------------------------------------------------------
dauer = Dauer()
# ------------------------------------------------------------------------------

import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB.UnitUtils import Convert

doc = __revit__.ActiveUIDocument.Document

wand_höhe = 1.39
ablage_walltype = 'GK 7.5'

def height_param(wand_höhe):
    """ElementSlowFilter (height)"""
    wand_konv_höhe = Convert(wand_höhe,DisplayUnitType.DUT_METERS,
                             DisplayUnitType.DUT_FEET_FRACTIONAL_INCHES)
    height_param_id = ElementId(DB.BuiltInParameter.WALL_USER_HEIGHT_PARAM)
    height_param_prov = DB.ParameterValueProvider(height_param_id)
    height_param_equality = DB.FilterNumericEquals()
    height_param_rule = DB.FilterDoubleRule(height_param_prov,
                                            height_param_equality,
                                            wand_konv_höhe,
                                            1E-6)
    height_param_filter = DB.ElementParameterFilter(height_param_rule)
    return height_param_filter

def name_param(ablage_walltype):
    """ElementSlowFilter ('name')"""
    name_param_id = ElementId(BuiltInParameter.ALL_MODEL_TYPE_NAME)
    name_param_prov = DB.ParameterValueProvider(name_param_id)
    name_param_equality = DB.FilterStringEquals()
    name_param_rule = DB.FilterStringRule(name_param_prov,
                                          name_param_equality,
                                          ablage_walltype,
                                          True)
    name_param_filter = DB.ElementParameterFilter(name_param_rule)
    return name_param_filter

def room_bounding():
    """ElementSlowFilter (room_bounding)"""
    room_bounding_id = ElementId(BuiltInParameter.WALL_ATTR_ROOM_BOUNDING)
    room_bounding_prov = DB.ParameterValueProvider(room_bounding_id)
    room_bounding_equality = DB.FilterNumericGreater()
    room_bounding_rule = DB.FilterIntegerRule(room_bounding_prov,
                                              room_bounding_equality,
                                              0)
    room_bounding_filter = DB.ElementParameterFilter(room_bounding_rule)
    return room_bounding_filter

def logical_and(first_filter, second_filter):
    """ElementLogicalFilter (height && 'name')"""
    collector = DB.LogicalAndFilter(first_filter,
                                      second_filter)

    return collector

# Durchlauf der Funktionen
height_param_filter = height_param(wand_höhe)
name_param_filter = name_param(ablage_walltype)
room_bounding_filter = room_bounding()

# Durchlauf der LogicalAndFilter
wall_collector = logical_and(height_param_filter, name_param_filter)
bound_collector = logical_and(room_bounding_filter, wall_collector)

# ToElements
walls = DB.FilteredElementCollector(doc) \
          .WherePasses(bound_collector) \
          .ToElements()

# Änderung der Parameter
for wall in walls:
    if wall:
        room_bounding = wall.get_Parameter(BuiltInParameter \
                                           .WALL_ATTR_ROOM_BOUNDING)
        t = DB.Transaction(doc, 'change WALL_ATTR_ROOM_BOUNDING')
        t.Start()
        room_bounding.Set(0)
        t.Commit()

# Zeitmessung ------------------------------------------------------------------
endzeit = dauer.zeitmessung()
print(endzeit)
# ------------------------------------------------------------------------------