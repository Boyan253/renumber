import os

import renumber


def test_natural_key_orders_numbers_properly():
    names = ["img10.jpg", "img2.jpg", "img1.jpg"]
    assert sorted(names, key=renumber.natural_key) == ["img1.jpg", "img2.jpg", "img10.jpg"]

def test_plan_numbers_sequentially():
    pairs = renumber.plan(["a.txt", "b.txt"], "{n:02d}{ext}")
    assert [os.path.basename(n) for _, n in pairs] == ["01.txt", "02.txt"]
