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
