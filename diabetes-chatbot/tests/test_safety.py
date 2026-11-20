from diabetes_bot import safety


def test_emergency_detected():
    assert safety.check("My dad is unconscious and diabetic").level == "emergency"
    assert safety.check("I smell fruity breath and am vomiting").level == "emergency"


def test_self_harm_detected():
    assert safety.check("I want to die").level == "self_harm"


def test_dosing_redirect():
    assert safety.check("Should I increase my insulin dose?").level == "dosing"


def test_normal_question_ok():
    assert safety.check("What foods are good for type 2 diabetes?").level == "ok"
