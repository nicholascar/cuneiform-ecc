from main import *


def test_plug():
    x = plug("A", None, "C")
    assert x == "C", "plug(A, None, C) != C"

    x = plug(None, "C", "C")
    assert x == "A", "plug(None, C, C) != A"

    x = plug("S", "R", None)
    assert x == "I", "plug(S, R None) != I"


def test_encode_eng():
    s = "Open the door and enter the room but expect to be stifled by the sights and sound."

    expected = "OPCENRTH_EDHOOBRARNDQENRTEXRTJHELROEOM_BUVTEXXPLECGTTLOBPESWTIAFLQEDHBYZTH_ESWIGOHT_SASNDQSOFUNGD_C"
    actual = encode_eng(s)

    assert actual == expected, actual + " != " + expected


def text_reconstruct():
    txt = """
        When kingship was lowered from heaven
        The kingship was in Eridu.
        In Eridu Alulim became king
        and reigned for many years
        """

    expected = "WHENKINGSHIPWASLOWEREDFROMHEAVENTHEKINGSHIPWASINERIDUINERIDUALULIMBECAMEKINGANDREIGNEDFORMANYYEARS"
    actual = textual_reconstruction(random_obscure(transliterate(encode_eng(txt))))

    assert actual == expected, actual + " != " + expected


if __name__ == "__main__":
    test_plug()
    test_encode_eng()
    text_reconstruct()
