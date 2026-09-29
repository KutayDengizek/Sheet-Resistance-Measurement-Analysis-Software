# Component: parser (`src/sheetres/parser.py`)
Status: **not started** (Phase 1, needs the example data)

**Purpose.** Turn a sample folder into 4 validated `Measurement` records. It is the only
component that touches the filesystem on the input side.

**Proposed interface.**
```python
@dataclass(frozen=True)
class Measurement:
    sample: str  # "260918_E4"
    index: int  # 1..4
    path: Path
    rs_ohm_sq: float  # "Mean Sheet Resistance (Ohm/square)"
    rs_sd_ohm_sq: float  # within-file "Standard Deviation"
    extra: Mapping[str, float]  # every other summary variable, keyed by its exact name


def load_sample(folder: Path, expected_count: int = 4) -> list[Measurement]: ...
```

**Errors.** Use a dedicated hierarchy (`InputFormatError` → `WrongFileCount`, `NameMismatch`,
`MissingVariable`, `NonNumericValue`). Messages include the file path and the line number.

**Invariants.** Never skip a file. Never coerce a bad value. Sort results by `index`.

**Quirks.** Fill in once the example data arrives. See [[../domain/input-format]] and MEMORY.md pitfalls.
