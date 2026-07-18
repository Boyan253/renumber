import os

import renumber


def test_natural_key_orders_numbers_properly():
    names = ["img10.jpg", "img2.jpg", "img1.jpg"]
    assert sorted(names, key=renumber.natural_key) == ["img1.jpg", "img2.jpg", "img10.jpg"]

def test_plan_numbers_sequentially():
    pairs = renumber.plan(["a.txt", "b.txt"], "{n:02d}{ext}")
    assert [os.path.basename(n) for _, n in pairs] == ["01.txt", "02.txt"]


def test_plan_supports_name_and_step():
    pairs = renumber.plan(["a.txt"], "{name}-{n}{ext}", start=5, step=5)
    assert os.path.basename(pairs[0][1]) == "a-5.txt"

def test_check_flags_collisions():
    pairs = [("a.txt", "same.txt"), ("b.txt", "same.txt")]
    assert renumber.check(pairs)


def test_check_passes_for_a_clean_plan(tmp_path):
    old = tmp_path / "a.txt"
    old.write_text("x", encoding="utf-8")
    pairs = renumber.plan([str(old)], "{n:02d}{ext}")
    assert renumber.check(pairs) == []

def test_apply_can_swap_two_names(tmp_path):
    a, b = tmp_path / "a.txt", tmp_path / "b.txt"
    a.write_text("A", encoding="utf-8")
    b.write_text("B", encoding="utf-8")
    renumber.apply([(str(a), str(b)), (str(b), str(a))])
    assert a.read_text(encoding="utf-8") == "B"
    assert b.read_text(encoding="utf-8") == "A"
