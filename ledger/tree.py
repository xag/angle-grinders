"""The decisions angle-grinders is bound by, as a ledger. Read it with `uv run quern brief .`, never whole.

Vocabulary: ledger@0.8.0 and grounding@1.2.0, pinned in quern.lock.
"""

from __future__ import annotations

import os
from pathlib import Path

import quern.grounding  # noqa: F401
from quern import Node, Quern
from quern.library import consume

OWNER = ("Il faudrait sourcer toutes les infos nécessaires et les intégrer aux packages. Pour la coupe et le "
         "montage. Voici déjà des outils. / Two new public repos (Recommended)")


def _alt(id_: str, name: str, why: str) -> Node:
    return Node(id=id_, kind="alternative", name=name, payload={"why": why})


def entries() -> list[Node]:
    return [
        Node(
            id="grinders-and-their-discs-are-one-package", kind="decision",
            name="Angle grinders and the cut-off discs they take are one package, angle-grinders, which requires "
                 "furniture-design and adds each grinder and each disc as a tool under tools/ with its maker's "
                 "documents as sources; a grinder links follows to furniture-design's general method "
                 "(tools/angle-grinder) and says only what is its own; it names no shop and no piece",
            payload={"decided_on": "2026-11-15", "the_owner": OWNER,
                     "why": "furniture-design names no maker (its ledger: makers-products-are-in-packages-outside-"
                            "furniture-design), and its ledger's a-makers-machine-follows-the-general-method-of-its-"
                            "kind puts the general method there and the maker's settings beside the machine. A "
                            "grinder is not a saw: it cuts with a disc it does not come bound to, and the disc "
                            "decides the cut and what it cuts."},
            children=[
                _alt("in-saws", "Put the grinder in saws, as a saw of another kind",
                     "saws holds saws and their blades; a grinder and its abrasive discs are another kind of "
                     "product, and the package's name would stop saying what it holds."),
                _alt("a-package-per-maker", "One unofficial package per maker (Parkside, PFERD, Klingspor)",
                     "Three packages of one or two tools each, every one read the same way."),
            ],
        ),
        Node(
            id="a-cut-off-discs-cut-is-its-printed-width", kind="decision",
            name="A cut-off disc's kerf is the width its maker prints (PFERD's column Width, Klingspor's Breite, "
                 "Parkside's Thickness of the disc it supplies), and a grinder's max_kerf the thickest cut-off "
                 "disc its maker says it takes (Parkside: cut-off wheels max. 1.2 mm), each checked against the copy "
                 "fetched",
            links={"rests_on": ["grinders-and-their-discs-are-one-package"]},
            payload={"decided_on": "2026-11-15", "the_owner": OWNER,
                     "why": "The cut decides how much a part loses, and furniture-design's rule "
                            "a-part-is-sawn-with-a-saw-that-states-its-cut refuses a cutting tool that states none. "
                            "A saw's teeth are set wider than its body (saws' ledger: body-as-kerf turned down), but "
                            "an abrasive disc has no teeth: the makers name its thickness its width."},
            children=[
                _alt("measure-the-cut", "State no kerf until the person measures a cut",
                     "Every disc maker prints the width, which no saw maker does for a portable saw's blade."),
                _alt("a-margin-over-the-width", "Count a margin over the printed width",
                     "A figure no maker prints."),
            ],
        ),
    ]


def build() -> Quern:
    root = Path(__file__).resolve().parents[1]
    lib, refs = consume(root, os.environ.get("QUERN_REGISTRY", root.parent / "quern-registry"))
    quern = Quern(packages=list(refs))
    quern = lib.effective(quern)
    quern.root.children = entries()
    return quern
