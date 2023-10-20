# Copyright (C) 2023 Łebi

import os
import sys
import ezdxf
import functions


def process(file, path_output):
    try:
        doc = ezdxf.readfile(file)
    except IOError:
        functions.dxf_IOerror_message()
        sys.exit(1)
    except ezdxf.DXFStructureError:
        functions.dxf_StructureError_message()
        sys.exit(2)

# iterate over all entities in modelspace
    msp = doc.modelspace()
    count = 0
    for entity in msp:
        if entity.dxftype() == "LWPOLYLINE":
            new_doc = ezdxf.new("R2000", setup=True)
            new_doc.layers.new("SIMPLIFIED")
            new_msp = new_doc.modelspace()
            new_msp.add_lwpolyline(entity.get_points(format="xy"))
            new_doc.saveas(os.path.join(path_output, "lwpolyline%s.dxf" % count))
            print_entity(entity)
            count += 1
            print(count)
    msp = doc.modelspace()
    count = 0
    for e in msp:
        if e.dxftype() == "MTEXT":
            print_text(e)
            count += 1
            print(count)

# entity query for all LINE entities in modelspace
    #for e in msp.query("LWPOLYLINE"):
        #print_entity(e)


# helper function
def print_entity(entity):
    print("LWPOLYLINE on layer: %s" % entity.dxf.layer)
    print("Ilość wierzchołków: %s" % entity.dxf.count)
    print("Współrzędne: %s" % entity.get_points(format="xy"))

def print_text(e):
    print("Text on layer: %s" % e.dxf.layer)
    print("Kolejny Text: %s" % e.plain_text(split=False, fast=True))
    print("Współrzędne: %s" % e.dxf.insert)
