# angle-grinders

Angle grinders and their cut-off discs as data for [furniture-design](https://github.com/xag/furniture-design): the discs each grinder takes, the width each disc cuts and what it cuts, and what a grinder adds to the general method of cutting with one, as their makers print them. **Unofficial**: the makers did not write or endorse it, and nothing here speaks for them.

## What is here

One `tool` per grinder and per disc under `tools/`:

- `parkside-pwsap-20-li-e6`, the Parkside PWSAP 20-Li E6 cordless grinder (X 20 V Team): payload `saw_kind` "angle grinder", `kerf` 1.2 mm (the WA60 T BF disc it comes with), `max_kerf` 1.2 mm (the thickest cut-off wheel it takes), `disc_diameter` 125 mm, `bore` 22.23 mm, `speed` 10000 /min. It links `follows` to furniture-design's `tools/angle-grinder`, the general method of cutting with an angle grinder, and says in French and English only what is its own: the guard cover with its attachment for cutting, the auxiliary handle, the discs it takes, its six speed levels and a trial run, and the feed against the rotation with no curved cuts.
- `pferd-eht-125-1-0-sg-alu` (1.0 mm) and `klingspor-kronenflex-edge-125-1-2` (1.2 mm): cut-off discs for aluminium, payload `saw_kind` "cut-off disc", `kerf` the width their makers print. PFERD's SG ALU is made for aluminium and other non-ferrous metals and not to clog; Klingspor's EDGE cuts steel, stainless steel and aluminium.

A disc's cut is its printed width: an abrasive disc has no teeth set wider than its body, and its makers name its thickness its width. A part cut with the grinder's own disc links `sawn_with` the grinder; a part cut with another disc links the disc.

No kinds and no rules of its own: furniture-design's rules judge a part cut with these, and its cutting sheet leaves their cut between the parts.

## Sources

The Parkside manual (IAN 426004_2301), PFERD's SG ALU product page and catalogue 6, and Klingspor's Kronenflex EDGE flyer, fetched on 2026-11-15. They are copyrighted, so they are cited by locator and values and never quoted. The copies as fetched are kept in a private repo, each original beside its text, and `tests/test_values.py` checks every value against them: clone that repo beside this one, or set `FURNITURE_REPO`, or that test fails and says why. Two originals over 15 MB (the Parkside manual and PFERD's catalogue) are kept there as text only; the test checks the text's sha256, and the original's when it is present.

## Using it

```python
from furniture_design.knowledge import knowledge as general, merge
from angle_grinders import knowledge as grinders

tree.root.children = merge(general(), grinders()) + [pieces]
```

## Design ledger

```sh
uv sync
uv run quern brief .
uv run quern check
```

There is no flight-recorder boundary: nothing here touches storage, the network, the clock or randomness at run time.

## Licence

- **The code** (`angle_grinders/*.py`, `tests/`, `ledger/`) is licensed under the [GNU Affero General Public License v3.0 or later](LICENSE), copyright 2026 Xavier Grehant.
- **The knowledge base**, the database `angle_grinders.knowledge()` returns (documents.json and every value on its nodes), is licensed under [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0](LICENSE-DATA), database rights included, with one added permission: designing, building and selling furniture with it is allowed. An improvement is published here, through [CONTRIBUTING.md](CONTRIBUTING.md).
- The makers' values are cited from their documents, not licensed.

## Tests

`uv run pytest` runs the tests whose code, data or packages changed since they passed, last failures first then the fastest, under a time budget (testplan); `uv run pytest --all` runs them all, once a day. Both stop at the first failure.
