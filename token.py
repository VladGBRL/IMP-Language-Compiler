class Token:
    def __init__(self, _type=None, _lexeme=None, _value=None):
        self.type = _type
        self.lexeme = _lexeme
        self.value = _value

    def print_screen(self):
        if self.type is None:
            print("()")
        else:
            if self.value is not None:
                # INTCONST DECCONST carry numeric values
                if self.type == "INTCONST"  or self.type == "DECCONST":
                    print("(" + self.type + ", " + self.lexeme + ", " + str(self.value) + ")")
                else:
                    print("(" + self.type + ", " + self.lexeme + ", " + self.value + ")")
            else:
                print("(" + self.type + ", " + self.lexeme + ")")

    def print_file(self, f):
        if self.type is None:
            f.write("()\n")
        else:
            if self.value is not None:
                # INTCONST and DECCONST carry numeric values
                if self.type == "INTCONST" or self.type == "DECCONST":
                    f.write("(" + self.type + ", " + self.lexeme + ", " + str(self.value) + ")\n")
                else:
                    f.write("(" + self.type + ", " + self.lexeme + ", " + self.value + ")\n")
            else:
                f.write("(" + self.type + ", " + self.lexeme + ")\n")

    def print_token(self, f=None):
        if f is None:
            self.print_screen()
        else:
            self.print_file(f)

    def get_type(self):
        return self.type


if __name__ == "__main__":
    print("token module")
