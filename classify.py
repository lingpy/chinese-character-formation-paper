from sinopy import parse_baxter, parse_chinese_morphemes, baxter2ipa

def sandeng(syllable):
    """Check if a syllable belongs to the third děng.
    """
    bx = parse_baxter(syllable)
    if 'j' in bx[1] or 'i' in bx[2]:
        return True
    return False


def n_final(syllable):
    bx = parse_baxter(syllable)
    if bx[2].endswith('nH') or bx[2].endswith('n') or bx[2].endswith('nX'):
        return True
    return False


def has_t(syllable):
    bx = parse_baxter(syllable)
    if 't' in bx[2]:
        return True
    return False

def no_t_ng(syllable):
    bx = parse_baxter(syllable)
    if not 'ng' in bx[2] and not 't' in bx[2]:
        return True
    return False


def velars(syllable):
    bx = parse_baxter(syllable)
    if bx[0] in ['k', 'g', 'kh', 'x', 'h', 'ng']:
        return True
    return False


def glottals(syllable):
    bx = parse_baxter(syllable)
    if bx[0] in ["'", "y"]:
        return True
    return False


def lateral(syllable):
    bx = parse_baxter(syllable)
    if bx[0] in ['l']:
        return True
    return False


def qutone(syllable):
    bx = parse_baxter(syllable)
    if bx[-1] == 'H':
        return True
    return False


def final_p(syllable):
    bx = parse_baxter(syllable)
    if bx[2][-1] == 'p':
        return True
    return False


def final_t(syllable):
    bx = parse_baxter(syllable)
    if bx[2][-1] == 't':
        return True
    return False


def initial(syllable):
    bx = parse_baxter(syllable)
    return bx[0]
