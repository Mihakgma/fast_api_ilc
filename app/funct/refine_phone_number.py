def refine_phone_number(txt: str) -> str:
    if type(txt) is not str:
        raise TypeError
    out = ""
    for s in txt:
        if s.isdigit() or s == "+":
            out += s
    if out.startswith("+"):
        out = "".join(["+", out[1:].replace("+", "")])
    else:
        out = out.replace("+", "")
    return out


if __name__ == '__main__':
    print(refine_phone_number("+123 +456 789"))