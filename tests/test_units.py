from BGE_app.project import area_acc, area_food

def test_area_acc():
    assert area_acc("Left Bottom") == "left_bot_acc"
    assert area_acc("Right Middle") == "right_mid_acc"
    assert area_acc("Top Shelf") == None

def test_area_food():
    assert area_food("Top") == "top_food"
    assert area_food("Left Middle") == "left_mid_food"
    assert area_food("Bird") == None