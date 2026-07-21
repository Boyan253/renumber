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
