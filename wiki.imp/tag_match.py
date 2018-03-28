
def tag_match(text, op="{{", cl="}}"):
    open = 0
    n = len(op)
    final_pos = 0
    for idx, _ in enumerate(text):
        slc = text[idx:idx + n]

        if slc == op:
            open += 1
        elif slc == cl:
            open -= 1

        if open == 0:
            final_pos = idx + 2
            break

    return text[0:final_pos]


if __name__ == "__main__":
    print(tag_match("{{ ASD REF:{{ QWE }} ZXC {{ asd 123}} {{ qwe {{ asd 123}} {{ qwe qwe}} qwe}} }} {{ Xasd 123}} {{ XXqwe qwe}}"))
