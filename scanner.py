from token import Token

keyword_map = {

    '%alias': 'ALIAS',
    '%and': 'AND',
    '%array': 'ARRAY',
    '%begin': 'BEGIN',
    '%byte': 'BYTE',
    '%c': 'C',
    '%comment': 'COMMENT',
    '%const': 'CONST',
    '%constant': 'CONSTANT',
    '%continue': 'CONTINUE',
    '%cycle': 'CYCLE',
    '%dynamic': 'DYNAMIC',
    '%end': 'END',
    '%event': 'EVENT',
    '%exit': 'EXIT',
    '%external': 'EXTERNAL',
    '%file': 'FILE',
    '%finish': 'FINISH',
    '%fn': 'FN',
    '%for': 'FOR',
    '%format': 'FORMAT',
    '%function': 'FUNCTION',
    '%half': 'HALF',
    '%if': 'IF_KEYWORD',
    '%include': 'INCLUDE',
    '%integer': 'INTEGER',
    '%list': 'LIST',
    '%long': 'LONG',
    '%map': 'MAP',
    '%monitor': 'MONITOR',
    '%name': 'NAME',
    '%not': 'NOT',
    '%on': 'ON',
    '%of': 'OF',
    '%or': 'OR',
    '%own': 'OWN',
    '%program': 'PROGRAM',
    '%real': 'REAL',
    '%record': 'RECORD',
    '%repeat': 'REPEAT',
    '%result': 'RESULT',
    '%return': 'RETURN_KEYWORD',
    '%routine': 'ROUTINE',
    '%short': 'SHORT',
    '%signal': 'SIGNAL',
    '%spec': 'SPEC',
    '%start': 'START',
    '%stop': 'STOP',
    '%string': 'STRING',
    '%switch': 'SWITCH',
    '%system': 'SYSTEM',
    '%then': 'THEN',
    '%unless': 'UNLESS',
    '%until': 'UNTIL',
    '%while': 'WHILE',
    '%short%integer': 'SHORT_INTEGER',
    '%long%integer': 'LONG_INTEGER',
    '%long%real': 'LONG_REAL',
    '%integer%array': 'INTEGER_ARRAY',
    '%real%array': 'REAL_ARRAY',
    '%end%of%program': 'END_OF_PROGRAM',
    '%integer%function': 'INTEGER_FUNCTION',
    '%cycle%repeat': 'CYCLE_REPEAT'
}



class Scanner:
    def __init__(self, input_file):
        self.file_name = input_file
        self.curr_position = 0
        self.switch_dict = {
   
            '+': self.case_plus,
            '-': self.case_minus,
            '*': self.case_times,
            '/': self.case_div,
            '\\': self.case_backslash,
            '!': self.case_exmark,
            ',': self.case_comma,
            ';': self.case_semicolon,
            ':': self.case_colon,
            '(': self.case_lparen,
            ')': self.case_rparen,
            '{': self.case_lbrace,
            '}': self.case_rbrace,
            '=': self.case_equal,
            '<': self.case_lt,
            '>': self.case_gt,
            '#': self.case_hashtag,
            '_': self.case_underscore,
            '.': self.case_dot,
            '\n': self.case_newline,
            ' ': self.case_space,
            '@': self.case_at,
            '~': self.case_tilde,
            '&': self.case_ampersand,
            "'": self.case_single_quote,
            '"': self.case_double_quote
        }


    def case_plus(self, f, c):
        # If a plus is followed by digits, treat as signed INTCONST/DECCONST
        c1 = f.read(1)
        # rewind so default_case can read the digit itself
        f.seek(f.tell() - 1)
        if c1 and c1.isdigit():
            return self.default_case(f, '+')
        # not a signed number -> regular PLUS
        self.curr_position = f.tell()
        return Token('PLUS', '+')
    
    def case_minus(self, f, c):
        # If a minus is followed by digits, treat as signed INTCONST/DECCONST
        c1 = f.read(1)
        if c1 == '>':
            self.curr_position = f.tell()
            return Token('ASSIGMENT', '->')
        # rewind so default_case can read the digit itself
        else:
            f.seek(f.tell() - 1)
            if c1 and c1.isdigit():
                return self.default_case(f, '-')
            self.curr_position = f.tell()
            return Token('MINUS', '-')
    
    def case_div(self, f, c):
        c1 = f.read(1)
        if c1 == '/':
            self.curr_position = f.tell()
            return Token('IDIV', '//')
        else:
            self.curr_position = f.tell() - 1
            return Token('DIV', '/')
        
    def case_backslash(self, f, c):
        c1 = f.read(1)
        if c1 == '\\':                # IEXP
            self.curr_position = f.tell()
            return Token('IEXP', '\\\\')
        elif c1 == '=':               # \=
            self.curr_position = f.tell()
            return Token('NEQ', '\\=')
        else:                         # EXP
            self.curr_position = f.tell() - 1
            return Token('EXP', '\\')
        
    def case_exmark(self, f, c):
        c1 = f.read(1)
        if c1 == '!':                 # !!
            self.curr_position = f.tell()
            return Token('DEXMARK', '!!')
        else:
            self.curr_position = f.tell() - 1
            return Token('EXMARK', '!')

    def case_times(self, f, c):
        t = Token('TIMES', '*')
        self.curr_position = f.tell()
        return t

    def case_comma(self, f, c):
        t = Token('COMMA', ',')
        self.curr_position = f.tell()
        return t

    def case_semicolon(self, f, c):
        t = Token('SEMICOLON', ';')
        self.curr_position = f.tell()
        return t
    def case_colon(self, f, c):
        self.curr_position = f.tell()
        return Token('COLON', ':')
    def case_lparen(self, f, c):
        t = Token('LPAREN', '(')
        self.curr_position = f.tell()
        return t

    def case_rparen(self, f, c):
        t = Token('RPAREN', ')')
        self.curr_position = f.tell()
        return t

    def case_lbrace(self, f, c):
        t = Token('LBRACE', '{')
        self.curr_position = f.tell()
        return t

    def case_rbrace(self, f, c):
        t = Token('RBRACE', '}')
        self.curr_position = f.tell()
        return t
    def case_equal(self, f, c):
        c1 = f.read(1)
        if c1 == '=':
            t = Token('EQID', '==')
            self.curr_position = f.tell()
            return t
        else:
            self.curr_position = f.tell() - 1
            return Token('EQ', '=')
    def case_not(self, f, c):
        c1 = f.read(1)
        if c1 != '=':
            raise ValueError("Illegal character after !")
        t = Token('NEQ', '!=')
        self.curr_position = f.tell()
        return t

    def case_ass(self, f, c):
        c1 = f.read(1)
        if c1 == '=':
            t = Token('EQ', '==')
            self.curr_position = f.tell()
            return t
        else:
            self.curr_position = f.tell() - 1
            return Token('ASSIGN', '=')

    def case_lt(self, f, c):
        c1 = f.read(1)
        if c1 == '=':
            t = Token('LE', '<=')
            self.curr_position = f.tell()
            return t
        elif c1 == '-':
            t = Token('RCOPY', '<-')
            self.curr_position = f.tell()
            return t
        elif c1 == '<':
            t = Token('SHL', '<<')
            self.curr_position = f.tell()
            return t
        else:
            self.curr_position = f.tell() - 1
            return Token('LT', '<')

    def case_gt(self, f, c):
        c1 = f.read(1)
        if c1 == '=':
            t = Token('GE', '>=')
            self.curr_position = f.tell()
            return t
        elif c1 == '>':
            t = Token('SHR', '>>')
            self.curr_position = f.tell()
            return t
        else:
            self.curr_position = f.tell() - 1
            return Token('GT', '>')
        
    def case_hashtag(self, f, c):
        c1 = f.read(1)
        if c1 == '#':
            t = Token('DHASH', '##')
            self.curr_position = f.tell()
            return t
        else:         
            t = Token('HASH', '#')
            self.curr_position = f.tell() -1
            return t
        
    def case_underscore(self, f, c):
        t = Token('UNDERSCORE', '_')
        self.curr_position = f.tell()
        return t
    
    def case_newline(self, f, c):
        t = Token('NEWLINE', '\\n')
        self.curr_position = f.tell()
        return t
    
    def case_space(self, f, c):
        t = Token('SPACE', ' ')
        self.curr_position = f.tell()
        return t
    
    def case_dot(self, f, c):
        c1 = f.read(1)

        # .<digits>  → FRAC
        if c1.isdigit():
            lex, frac_val = self.fractional_part(f, c1)
            self.curr_position = f.tell()
            return Token('FRAC', '.' + lex)

        # .  (epsilon) → FRAC
        self.curr_position = f.tell() - 1
        return Token('FRAC', '.')
   
    def case_at(self, f, c):
        c1 = f.read(1)
        # @ can be followed by optional +/- and then digits
        if c1 in ['+', '-']:
            sign = c1
            c2 = f.read(1)
            if c2 and c2.isdigit():
                lex, val = self.decimal_part(f, c2)
                self.curr_position = f.tell()
                return Token('DECCONST', '@' + sign + lex)
            else:
                raise ValueError("Illegal '@' format: sign not followed by digit")
        elif c1 and c1.isdigit():
            lex, val = self.decimal_part(f, c1)
            self.curr_position = f.tell()
            return Token('DECCONST', '@' + lex)
        raise ValueError("Illegal '@' format")
    
    def case_tilde(self, f, c):
        self.curr_position = f.tell()
        return Token('NOT', '~')
    
    def case_ampersand(self, f, c):
        self.curr_position = f.tell()
        return Token('AND', '&')
    
    def case_single_quote(self, f, c):
        ch = f.read(1)
        closing = f.read(1)
        if closing != "'":
            raise ValueError("Invalid CHARCONST")
        lex = "'" + ch + "'"
        self.curr_position = f.tell()
        return Token('CHARCONST', lex)
    
    def case_double_quote(self, f, c):
        lexeme = ''
        while True:
            c1 = f.read(1)
            if c1 == '"':
                break
            if not c1:
                raise ValueError("Unterminated STRINGCONST")
            lexeme += c1
        lex = '"' + lexeme + '"'
        self.curr_position = f.tell()
        return Token('STRCONST', lex)
    
    def case_zero(self, f, c):
        c1 = f.read(1)
        if c1.isdigit():
            raise ValueError("A decimal constant must start with 1-9")
        elif c1 == '.':
            c2 = f.read(1)
            if c2.isdigit():
                lexeme, x_val = self.fractional_part(f, c2)
                token = Token('REALCONST', '0.' + lexeme, x_val)
                self.curr_position = f.tell() - 1
                return token
        self.curr_position = f.tell() - 1
        return Token('INTCONST', '0', 0)

    def default_case(self, f, c):
       
        # Signed numbers: called from case_plus/case_minus which peeked next char
        if c in ['+', '-']:
            sign = c
            first_digit = f.read(1)
            if not first_digit or not first_digit.isdigit():
                raise ValueError("Illegal signed number format")
            # parse integer part
            lex, int_val = self.decimal_part(f, first_digit)
            # inspect next char
            f.seek(self.curr_position)
            c1 = f.read(1)
            if not c1 or c1 not in ['.', '@']:
                self.curr_position = f.tell() - 1
                value = int_val if sign == '+' else -int_val
                return Token('INTCONST', sign + lex, value)

            if c1 == '.':
                c2 = f.read(1)
                if c2 and c2.isdigit():
                    lex2, frac_part = self.fractional_part(f, c2)
                    lexeme = sign + lex + '.' + lex2
                    x_val = int_val + frac_part
                    if sign == '-':
                        x_val = -x_val
                    self.curr_position = f.tell() - 1
                    return Token('DECCONST', lexeme, x_val)
                if c2 == '@':
                    c3 = f.read(1)
                    if c3 in ['+', '-']:
                        sign2 = c3
                        c4 = f.read(1)
                        if c4 and c4.isdigit():
                            lex3, _ = self.decimal_part(f, c4)
                            lexeme = sign + lex + '.' + '@' + sign2 + lex3
                            self.curr_position = f.tell() - 1
                            return Token('DECCONST', lexeme)
                        else:
                            raise ValueError("Illegal '@' format: sign not followed by digit")
                    elif c3 and c3.isdigit():
                        lex3, _ = self.decimal_part(f, c3)
                        lexeme = sign + lex + '.' + '@' + lex3
                        self.curr_position = f.tell() - 1
                        return Token('DECCONST', lexeme)
                    else:
                        raise ValueError("Illegal '@' format after decimal point")
                # '.' followed by non-digit/non-'@'
                self.curr_position = f.tell() - 1
                x_val = float(int_val)
                if sign == '-':
                    x_val = -x_val
                return Token('DECCONST', sign + lex + '.', x_val)

            # c1 == '@'
            if c1 == '@':
                c2 = f.read(1)
                if not c2 or not c2.isdigit():
                    raise ValueError("Illegal '@' format")
                lex2, _ = self.decimal_part(f, c2)
                self.curr_position = f.tell() - 1
                lexeme = sign + lex + '@' + lex2
                return Token('DECCONST', lexeme)

        # Unsigned numbers and names
        if c.isdigit():
            lex, int_val = self.decimal_part(f, c)
            f.seek(self.curr_position)
            c1 = f.read(1)
            if c1 not in ['.', '@']:
                self.curr_position = f.tell() - 1
                return Token('INTCONST', lex)

            # integer followed by fractional part
            if c1 == '.':
                frac_val = f.read(1)
                if frac_val.isdigit():
                    lex2, frac_part = self.fractional_part(f, frac_val)
                    # after fractional_part, check for optional @<int>
                    f.seek(self.curr_position)
                    c_at = f.read(1)
                    if c_at == '@':
                        c_after = f.read(1)
                        if not c_after or not c_after.isdigit():
                            raise ValueError("Illegal '@' format after decimal point")
                        lex3, _ = self.decimal_part(f, c_after)
                        self.curr_position = f.tell() - 1
                        return Token('DECCONST', lex + '.' + lex2 + '@' + lex3)
                    # no @ -> regular DECCONST with numeric value
                    x_val = int_val + frac_part
                    self.curr_position = f.tell() - 1
                    return Token('DECCONST', lex + '.' + lex2, x_val)
                else:
                    # '.' followed by non-digit -> illegal
                    raise ValueError("Illegal character after decimal point")

            # integer followed by @ -> int@int -> DECCONST (int can be signed)
            if c1 == '@':
                c2 = f.read(1)
                if c2 in ['+', '-']:
                    sign = c2
                    c3 = f.read(1)
                    if c3 and c3.isdigit():
                        lex2, _ = self.decimal_part(f, c3)
                        self.curr_position = f.tell() - 1
                        return Token('DECCONST', lex + '@' + sign + lex2)
                    else:
                        raise ValueError("Illegal '@' format: sign not followed by digit")
                elif c2 and c2.isdigit():
                    lex2, _ = self.decimal_part(f, c2)
                    self.curr_position = f.tell() - 1
                    return Token('DECCONST', lex + '@' + lex2)
                else:
                    raise ValueError("Illegal '@' format")

        elif c.isalpha():
            # NAME: starts with letter, continues with letters/digits
            lexeme = c
            while True:
                c1 = f.read(1)
                if not c1 or not (c1.isalnum()):
                    break
                lexeme += c1
            self.curr_position = f.tell() - 1
            return Token('NAME', lexeme)
        
        elif c == '%':
            # KEYWORD: starts with %, continues with alphanumeric or %
            lexeme = c
            while True:
                c1 = f.read(1)
                if not c1 or not (c1.isalnum() or c1 == '%'):
                    break
                lexeme += c1
            self.curr_position = f.tell() - 1
            if lexeme in keyword_map:
                return Token(keyword_map[lexeme], lexeme)
            else:
                raise ValueError(f"Unknown keyword: {lexeme}")

        else:
            raise ValueError("Unknown character")

    def decimal_part(self, f, c):
        lexeme = c
        i_val = int(c)
        while True:
            c1 = f.read(1)
            if not c1 or not c1.isdigit():
                break
            lexeme += c1
            i_val = i_val * 10 + int(c1)
        self.curr_position = f.tell() - 1
        return lexeme, i_val

    # _parse_signed_number has been merged into default_case

    def fractional_part(self, f, c):
        lexeme = c
        y = 0.1
        f_val = (int(c) * y)
        while True:
            c1 = f.read(1)
            if not c1 or not c1.isdigit():
                break
            lexeme += c1
            y /= 10
            f_val += int(c1) * y
        self.curr_position = f.tell() - 1
        return lexeme, f_val

    def execute_case(self, val, f, c):
        return self.switch_dict.get(val, self.default_case)(f, c)

    def next_token(self):
        with open(self.file_name) as f:
            f.seek(self.curr_position)
            while True:
                c = f.read(1)
                if not c:
                    return Token('END_OF_PROGRAM', '')
                if c == '\n':
                    return self.case_newline(f, c)
                if c == ' ':
                    return self.case_space(f, c)
                if c.isspace():
                    while True:
                        c1 = f.read(1)
                        if not c1.isspace():
                            c=c1
                            break
                return self.execute_case(c, f, c)


if __name__ == "__main__":
    print("module scanner")
