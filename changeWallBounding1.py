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

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
from Autodesk.Revit.DB import Transaction, TransactionGroup
from Autodesk.Revit.DB.UnitUtils import Convert

doc = __revit__.ActiveUIDocument.Document

walltype = 'GK 7.5'
height = Convert(1.39,DisplayUnitType.DUT_METERS,DisplayUnitType.DUT_FEET_FRACTIONAL_INCHES)

wall_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls) \
                                            .WhereElementIsNotElementType() \
                                            .ToElements()

for wall in wall_collector:

    wall_name = wall.Name
    height_value = wall.LookupParameter('Nicht verknüpfte Höhe').AsDouble()
    room_bounding = wall.LookupParameter('Raumbegrenzung')

    if wall_name and wall_name == walltype:

        if height_value and height_value == height:

            t = Transaction(doc, 'change Wall Params')
            t.Start()

            room_bounding.Set(0)

            t.Commit()

# Zeitmessung ------------------------------------------------------------------
endzeit = dauer.zeitmessung()
print(endzeit)
# ------------------------------------------------------------------------------