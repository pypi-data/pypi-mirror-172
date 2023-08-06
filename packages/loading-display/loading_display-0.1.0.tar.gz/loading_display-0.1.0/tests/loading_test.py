from loading_display import spinner, loading_bar


def test_spinner_frames(capfd):
    s = spinner()
    next(s)
    out1, _ = capfd.readouterr()
    next(s)
    out2, _ = capfd.readouterr()
    next(s)
    out3, _ = capfd.readouterr()
    next(s)
    out4, _ = capfd.readouterr()
    next(s)
    out5, _ = capfd.readouterr()
    all_frames = [out1, out2, out3, out4]
    # the first and the fifth frame should be the same
    assert out1 == out5
    # all frames should be unique
    assert len(list(set(all_frames))) == len(all_frames)


def test_loading_bar(capfd):
    loading_bar(1, 2, 12)
    half_bar1, _ = capfd.readouterr()
    loading_bar(50, 100, 12)
    half_bar2, _ = capfd.readouterr()
    loading_bar(1, 3, 12)
    one_third_bar, _ = capfd.readouterr()
    assert one_third_bar != half_bar1
