# test_main.py
from main import my_function

def test_my_function(capsys):
    my_function()
    captured = capsys.readouterr()
    assert captured.out.strip() == "ОПГ ТОЛЬЯТТИ ТОП"