# -*- coding: utf-8 -*-
import re
import math
import random
import argparse


POS = [
    "A",  # 0
    "B",
    "C",
    "D",
    "E",
    "F",  # 5
    "G",
    "H",
    "I",
    "J",
    "K",  # 10
    "L",
    "M",
    "N",
    "O",
    "P",  # 15
    "Q",
    "R",
    "S",
    "T",
    "U",  # 20
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "_",  # 26
]

CUNE = {
    "A": "𒀹",
    "B": "𒋡",
    "C": "𒆳",
    "D": "𒈦",
    "E": "𒀸",
    "F": "𒋰",
    "G": "𒐈",
    "H": "𒑊",
    "I": "𒉽",
    "J": "𒑖",
    "K": "𒐺",
    "L": "𒈫",
    "M": "𒑋",
    "N": "𒑉",
    "O": "𒇹",
    "P": "𒐀",
    "Q": "𒆜",
    "R": "𒃵",
    "S": "𒁇",
    "T": "𒁹",
    "U": "𒐁",
    "V": "𒍞",
    "W": "𒑈",
    "X": "𒄑",
    "Y": "𒐉",
    "Z": "𒀽",
    "_": "𒃰",
}


def gi(i):  # Galois Index
    return i % 27


def plug(i, j, k):
    if i is None:
        i_num = POS.index(k) - POS.index(j)
        return POS[i_num]
    elif j is None:
        j_num = POS.index(k) - POS.index(i)
        return POS[j_num]
    else:
        k_num = POS.index(i) + POS.index(j)
        return POS[gi(k_num)]


def encode_eng(txt):
    # remove spaces, newlines, ',' & '.'
    txt_subbed = re.sub(r"[\s.,]", "", txt.strip())

    # convert to upper case
    txt_caps = txt_subbed.upper()

    # add '_' if txt length isn't even
    txt_even = txt_caps + "_" if len(txt_caps) % 2 else txt_caps
    s_ecc = ""

    for x in range(0, len(txt_even), 2):
        i = POS.index(txt_even[x])
        j = POS.index(txt_even[x + 1])
        k = gi(i + j)
        s_ecc += "{}{}{}".format(txt_even[x], txt_even[x + 1], POS[k])

    return s_ecc


def transliterate(txt):
    return "".join([CUNE.get(x) for x in txt])


def random_obscure(txt):
    num_triplets = math.floor(len(txt) / 3)
    num_obsurations = random.randint(0, num_triplets)
    triplets_to_obscure = []

    def obscure_triplet(triplets):
        triplet = random.randint(0, num_triplets - 1)
        if triplet not in triplets:
            triplets.append(triplet)
        else:
            obscure_triplet(triplets)

    for i in range(0, num_obsurations):
        obscure_triplet(triplets_to_obscure)

    triplets_to_obscure.sort()
    lst = list(txt)
    for triplet in triplets_to_obscure:
        triple_member = random.randint(0, 2)
        lst[(triplet) * 3 + triple_member] = "-"

    return "".join(lst)


def triplet_print(txt):
    s2 = ""
    for x in range(0, len(txt) - 1, 3):
        s2 += txt[x] + txt[x + 1] + txt[x + 2] + ","
    print(s2.strip(","))


def tablet_print(txt, width=10):
    tab = ""
    for x in range(0, len(txt), width):
        tab += txt[x : x + width] + "\n"

    last_line = txt[len(txt) - (len(txt) % width) : len(txt)]
    ll_split = math.ceil(len(last_line) / 2)

    # make the last line the same length as 'width
    calig_last_line = (
        last_line[:ll_split] + ". " * (width - len(last_line)) + last_line[ll_split:]
    )

    if re.match(r"^[\.\s]+$", calig_last_line):
        calig_last_line = ''

    # replace last line
    print((tab.replace(last_line, "").strip() + "\n" + calig_last_line).strip())


def textual_reconstruction(obscured_txt):
    # remove linebreaks
    txt = obscured_txt.replace("\n", "")

    # remove spacing characters
    txt = txt.replace(". ", "")

    # make a list for filling with plugged chars
    lst = []

    # un-transliterate
    for symbol in txt:
        if symbol == "-":
            lst.append("-")
        else:
            for k, v in CUNE.items():
                if v == symbol:
                    lst.append(k)

    lst_recovered_ecc_removed = []

    # plug lost symbols
    for x in range(0, len(lst) - 1, 3):
        if "-" in lst[x : x + 3]:
            # missing char position
            pos = lst[x : x + 3].index("-")
            if pos == 0:
                recovered_symbol = plug(None, lst[x + 1], lst[x + 2])
            elif pos == 1:
                recovered_symbol = plug(lst[x], None, lst[x + 2])
            else:
                recovered_symbol = plug(lst[x], lst[x + 1], None)

            # place the recovered char back into the list of chars
            lst[x + pos] = recovered_symbol

        # remove ECC additions by copying other characters out
        lst_recovered_ecc_removed.append(lst[x + 0])
        lst_recovered_ecc_removed.append(lst[x + 1])

    # return the plugged list as a string
    return "".join(lst_recovered_ecc_removed)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'text',
        type=str,
        help='The input limited English text to encode',
        default="""
                    Irving had a little lamb,
                    its fleece was black as mud,
                    And everywhere Irving went,
                    the lamb left a little thud.
                """
    )
    parser.add_argument(
        '-w', '--width',
        type=int,
        help='The input limited English text to encode',
        default=10
    )

    parser.add_argument(
        '-o', '--no-obscuring',
        help='Prevents random character obscuring',
        action='store_true',
        dest='o'
    )

    parser.add_argument(
        '-t', '--triplet-printing',
        help='Enables triplet printing',
        action='store_true',
        dest='t'
    )

    parser.add_argument(
        '-p', '--no-printing',
        help='Prevents tablet printing',
        action='store_true',
        dest='p'
    )

    parser.add_argument(
        '-r', '--reconstruction-printing',
        help='Prints reconstructed text',
        action='store_true',
        dest='r'
    )

    args = parser.parse_args()
    enc = encode_eng(args.text)
    c = transliterate(enc)

    if not args.o:
        c = random_obscure(c)

    if args.t:
        triplet_print(c)

    if not args.p:
        tablet_print(c, width=args.width)

    if args.r:
        print(textual_reconstruction(c))
