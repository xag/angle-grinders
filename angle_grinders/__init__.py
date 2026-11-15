"""Angle grinders and their cut-off discs as data on furniture-design's kinds (source, clause, tool): the discs
each grinder takes and the width each disc cuts, as their makers print them. Unofficial: neither the makers
wrote nor endorsed it.

A grinder is one `tool` under tools/, payload saw_kind "angle grinder", linking `follows` to furniture-design's
general method (tools/angle-grinder) and saying in French and English only what is its own. Its params:

- kerf (mm): the width of the cut-off disc it comes with, as its maker prints it;
- max_kerf (mm): the thickest cut-off disc it takes;
- disc_diameter and bore (mm), speed (1/min): the discs it takes.

A cut-off disc is a `tool` too, payload saw_kind "cut-off disc", its kerf the width its maker prints (PFERD
heads the column "Width", Klingspor "Breite"): a disc has no teeth set wider than its body, so its width is its
cut. A part cut with a disc other than the grinder's own links `sawn_with` the disc.

Every document is copyrighted, so a clause carries its locator and values and no quote; the copies are kept
private and tests/test_values.py checks every value against them.

    from furniture_design.knowledge import knowledge as general, merge
    from angle_grinders import knowledge as grinders
    tree.root.children = merge(general(), grinders()) + [pieces]
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from quern.provenance import Quantity
from quern.tree import Node
from furniture_design.knowledge import with_authority

HERE = Path(__file__).parent
SOURCES = "sources"
TOOLS = "tools"
GENERAL = "tools/angle-grinder"


@lru_cache(maxsize=1)
def documents() -> dict[str, dict]:
    return {d["id"]: d for d in json.loads((HERE / "documents.json").read_text(encoding="utf-8"))["documents"]}


def _value(ref: str) -> dict:
    doc, clause, param = ref.split("/")
    return next(c for c in documents()[doc]["clauses"] if c["id"] == clause)["params"][param]


def _derived(ref: str) -> Quantity:
    v = _value(ref)
    return Quantity(value=float(v["value"]), unit=v["unit"], provenance="derived", grounded=True,
                    derived_from=[f"{SOURCES}/{ref}"], note=f"as printed: {v['printed']}")


def sources() -> list[Node]:
    """One source per document, one clause per table, row or passage read, its values as printed."""
    out = []
    for d in documents().values():
        clauses = [Node(id=c["id"], kind="clause",
                        payload={"locator": c["locator"], **({"rows": {k: v["printed"] for k, v in c["params"].items()}}
                                                             if c["params"] else {})},
                        params={k: Quantity(value=float(v["value"]), unit=v["unit"], provenance="published",
                                            grounded=True, source=c["locator"], note=f"printed: {v['printed']}")
                                for k, v in c["params"].items()})
                   for c in d["clauses"]]
        out.append(Node(id=d["id"], kind="source", name=f"{d['publisher']}: {d['title']}",
                        payload={"publisher": d["publisher"], "url": d["url"], "fetched": d["fetched"],
                                 "sha256": d["sha256"], "licence": "copyrighted",
                                 "capture": "private copy, identified by its sha256"},
                        children=clauses))
    return out


PARKSIDE = "parkside-pwsap-20-li-e6-manual"


def parkside() -> Node:
    """The Parkside PWSAP 20-Li E6: what its manual says of its discs, and the steps of the general method it
    adds to (its guard's attachment for cutting, its handle, its discs, its speed levels and feed)."""
    p = f"{SOURCES}/{PARKSIDE}"
    return Node(
        id="parkside-pwsap-20-li-e6", kind="tool", name="Parkside PWSAP 20-Li E6",
        params={"kerf": _derived(f"{PARKSIDE}/supplied-disc/kerf"),
                "max_kerf": _derived(f"{PARKSIDE}/technical-data/max_kerf"),
                "disc_diameter": _derived(f"{PARKSIDE}/technical-data/disc_diameter"),
                "bore": _derived(f"{PARKSIDE}/technical-data/bore"),
                "speed": _derived(f"{PARKSIDE}/technical-data/speed")},
        payload={"maker": "Parkside (Grizzly Tools)", "saw_kind": "angle grinder",
                 "does": "cuts a profile, a bar or a sheet with a 125 mm cut-off disc, on its X 20 V Team battery",
                 "say": {
                     "fr": {"name": "Meuleuse d'angle Parkside PWSAP 20-Li E6", "method": [
                         "Pour tronçonner, monter le capot de protection (4) avec son recouvrement (15) : jamais "
                         "le capot seul.",
                         "Visser la poignée auxiliaire (2) à gauche, à droite ou dessus selon le travail : la "
                         "meuleuse ne s'utilise qu'avec elle.",
                         "N'employer que des disques à tronçonner renforcés de fibres, de 125 mm, alésage "
                         "22,23 mm, d'au plus 1,2 mm d'épaisseur, l'étiquette du disque tournée vers la machine.",
                         "Choisir la vitesse sur l'un des 6 niveaux, et faire tourner la meuleuse à vide avant de "
                         "commencer et après chaque changement de disque.",
                         "Travailler en sens inverse de la rotation, avec une faible avance et une pression "
                         "modérée ; ne pas couper en courbe."]},
                     "en": {"name": "Parkside PWSAP 20-Li E6 angle grinder", "method": [
                         "For cutting, fit the guard cover (4) with its attachment (15): never the guard cover "
                         "alone.",
                         "Screw the auxiliary handle (2) on the left, right or top as the work needs: the grinder "
                         "is only used with it.",
                         "Use only fibre-reinforced cut-off discs of 125 mm, bore 22.23 mm, no thicker than "
                         "1.2 mm, the disc's label towards the machine.",
                         "Choose one of the 6 speed levels, and run the grinder without load before starting and "
                         "after each change of disc.",
                         "Work against the rotation, with a small feed and moderate pressure; make no curved "
                         "cuts."]}}},
        links={"follows": [GENERAL],
               "per": [f"{p}/cutting-disc", f"{p}/handle", f"{p}/technical-data", f"{p}/changing-the-disc",
                       f"{p}/speed", f"{p}/cutting"]})


# (id, name, does, the clause printing its width, the clauses saying what it cuts)
DISCS = [
    ("pferd-eht-125-1-0-sg-alu", "PFERD EHT 125-1,0 SG ALU",
     "cuts aluminium and other non-ferrous metals without clogging; 125 mm, bore 22.23 mm",
     "pferd-sg-alu-page/eht-125-1-0/kerf", ["pferd-sg-alu-page/eht-125-1-0", "pferd-catalogue-6/sg-alu"]),
    ("klingspor-kronenflex-edge-125-1-2", "Klingspor Kronenflex EDGE 125 x 1.2",
     "cuts steel, stainless steel and aluminium; 125 mm, bore 22.23 mm",
     "klingspor-kronenflex-edge-flyer/edge-125/kerf", ["klingspor-kronenflex-edge-flyer/edge-125"]),
]


def discs() -> list[Node]:
    return [Node(id=id_, kind="tool", name=name, params={"kerf": _derived(ref)},
                 payload={"maker": documents()[ref.split("/")[0]]["publisher"], "saw_kind": "cut-off disc",
                          "does": does},
                 links={"per": [f"{SOURCES}/{c}" for c in per]})
            for id_, name, does, ref, per in DISCS]


def tools() -> list[Node]:
    return [parkside(), *discs()]


# Who stands behind each source (furniture-design's AUTHORITIES).
AUTHORITY = {d: "maker" for d in ("parkside-pwsap-20-li-e6-manual", "pferd-sg-alu-page", "pferd-catalogue-6",
                                  "klingspor-kronenflex-edge-flyer")}


def knowledge() -> list[Node]:
    """The branches to merge beside furniture-design's: the sources and the grinders and discs."""
    return [Node(id=SOURCES, kind="", children=with_authority(sources(), AUTHORITY)),
            Node(id=TOOLS, kind="", children=tools())]
