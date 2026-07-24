# renumber

> Batch-rename files to a numbered pattern with a dry run you can trust.

## Why

Batch renamers either have a GUI or destroy your files. `renumber` is a dry run
by default, checks for collisions before it moves anything, and can swap names
that already exist.

## Usage

```
python renumber.py *.jpg                                   # dry run
python renumber.py *.jpg -p "holiday-{n:03d}{ext}" --apply
python renumber.py *.mp3 --sort mtime -p "{n:02d} - {name}{ext}" --apply
python renumber.py photos/* --start 100 --step 10
```

## Pattern fields

| field  | meaning |
|--------|---------|
| `{n}`  | the running number, starting at `--start` |
| `{i}`  | zero-based index |
| `{name}` | original filename without the extension |
| `{ext}`  | original extension, including the dot |

Standard format specs work, so `{n:03d}` gives `007`.

## Safety

- Nothing happens without `--apply`.
- Collisions (two files mapping to one name, or a target that already exists
  outside the set) are reported and abort the run.
- Renames go through temporary names, so rotating `a -> b -> c -> a` works.

## Tests

```
pip install pytest
pytest
```
