"""Every value and passage against the copy it was read from, and the grinder against furniture-design's rules.

The copies are copyrighted and live in the private repo xag/furniture, checked out beside this one (or at
$FURNITURE_REPO), under sources/angle-grinders/, each original beside its text. An original over 15 MB is not
kept there, only its text: its sha256 is checked when it is present, and its text's always. Without the
copies these tests fail, saying where they looked, and never skip.
"""

import hashlib
import os
import re
from pathlib import Path

from quern import Quern, run_rules
from quern.provenance import Quantity
from quern.tree import Node

from furniture_design.knowledge import knowledge as general, merge
from furniture_design.package import PACKAGE
from angle_grinders import DISCS, documents, knowledge

ROOT = Path(__file__).resolve().parents[1]
CAPTURES = Path(os.environ.get("FURNITURE_REPO", ROOT.parent / "furniture")) / "sources" / "angle-grinders"


def _text(doc: dict) -> str:
    original = CAPTURES / doc["file"]
    text = original.with_suffix(".txt")
    assert text.exists(), (f"the private copy {text} is missing: clone xag/furniture beside this repo or set "
                           "FURNITURE_REPO")
    assert hashlib.sha256(text.read_bytes()).hexdigest() == doc["text_sha256"], doc["id"]
    if original.exists():
        assert hashlib.sha256(original.read_bytes()).hexdigest() == doc["sha256"], doc["id"]
    return re.sub(r"\s+", " ", text.read_text(encoding="utf-8"))


def _numbers(printed: str) -> list[float]:
    return [float(n.replace(",", ".")) for n in re.findall(r"\d+(?:[.,]\d+)?", printed)]


def test_every_value_is_printed_in_the_document_fetched():
    for doc in documents().values():
        text = _text(doc)
        for clause in doc["clauses"]:
            for name, v in clause["params"].items():
                printed = re.sub(r"\s+", " ", v["printed"])
                assert printed in text, (doc["id"], clause["id"], name, printed)
                assert v["value"] in _numbers(printed), (doc["id"], clause["id"], name)


# A few words of each passage the Parkside's own sentences rest on, found in its manual's text
PARKSIDE_WORDS = {
    "cutting-disc": ["Only certified, fibre-reinforced cutting or", "In general, work with small scrubs",
                     "Always work in the counter-direction"],
    "handle": ["Screw the handle (2) tight on to the thread"],
    "changing-the-disc": ["The label on the"],
    "speed": ["The tool has 6 speed levels"],
    "cutting": ["Do not make curve cuts"],
}


def test_every_passage_the_parkside_rests_on_is_in_its_manual():
    doc = documents()["parkside-pwsap-20-li-e6-manual"]
    text = _text(doc)
    for clause, words in PARKSIDE_WORDS.items():
        assert clause in {c["id"] for c in doc["clauses"]}
        for w in words:
            assert w in text, (clause, w)


def _tools() -> dict[str, Node]:
    return {n.id: n for n in knowledge()[1].children}


def test_the_parkside_reads_its_discs_from_its_manual_and_follows_the_general_method():
    p = _tools()["parkside-pwsap-20-li-e6"]
    assert p.params["kerf"].value == 1.2 and p.params["max_kerf"].value == 1.2
    assert p.params["disc_diameter"].value == 125 and p.params["bore"].value == 22.23
    assert p.links["follows"] == ["tools/angle-grinder"]
    general_tools = {n.id for n in general() if n.id == "tools" for n in n.children}
    assert "angle-grinder" in general_tools
    for lang in ("fr", "en"):
        assert len(p.payload["say"][lang]["method"]) == len(p.payload["say"]["en"]["method"])


def test_a_disc_cuts_its_printed_width():
    t = _tools()
    assert {d[0] for d in DISCS} <= set(t)
    assert t["pferd-eht-125-1-0-sg-alu"].params["kerf"].value == 1.0
    assert t["klingspor-kronenflex-edge-125-1-2"].params["kerf"].value == 1.2


def _tree(sawn_with: str) -> Quern:
    tree = Quern(vocabulary=PACKAGE.vocabulary, rules=PACKAGE.rules, solvers=PACKAGE.solvers)
    part = Node(id="rail", kind="part", links={"uses": ["materials/birch-yellow"], "sawn_with": [sawn_with]},
                params={"thickness": Quantity(value=10, unit="mm", provenance="design-target")},
                payload={"shape": {"op": "box", "size": [10, 20, 1000]}})
    tree.root.children = merge(general(), knowledge()) + [
        Node(id="pieces", kind="", children=[Node(id="doors", kind="piece", children=[part])])]
    return tree


def test_a_part_cut_with_the_grinder_or_a_disc_states_its_cut():
    cut = "a-part-is-sawn-with-a-saw-that-states-its-cut"
    for tool in ("tools/parkside-pwsap-20-li-e6", "tools/pferd-eht-125-1-0-sg-alu", "tools/klingspor-kronenflex-edge-125-1-2"):
        verdict = next(r.verdict for r in run_rules(_tree(tool), "pieces/doors")
                       if r.rule == cut and r.node == "pieces/doors/rail")
        assert verdict == "holds", tool


def test_the_grinders_discs_and_sources_break_none_of_furniture_designs_rules():
    tree = Quern(vocabulary=PACKAGE.vocabulary, rules=PACKAGE.rules, solvers=PACKAGE.solvers)
    tree.root.children = merge(general(), knowledge())
    ours = {f"tools/{t.id}" for t in knowledge()[1].children} | {f"sources/{d}" for d in documents()}
    broken = [r for r in run_rules(tree, "") if not r.ok and any(r.node == p or r.node.startswith(p + "/") for p in ours)]
    assert not broken, broken


def test_every_source_says_its_authority_and_every_link_lands():
    tree = Quern(vocabulary=PACKAGE.vocabulary, rules=PACKAGE.rules, solvers=PACKAGE.solvers)
    tree.root.children = merge(general(), knowledge())
    ids = {f"sources/{s.id}/{c.id}" for s in tree.root.children[0].children for c in s.children}
    for s in knowledge()[0].children:
        assert s.payload["authority"] == "maker", s.id
    for t in knowledge()[1].children:
        for p in t.links["per"]:
            assert p in ids, (t.id, p)
