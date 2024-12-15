STA /B
LDA ?1
STA /C
LDA @C
LOOP123: ADD /A
    STA /A
    LDA /C
    INC /C
    STA /C
    LDA /B
    INC /B
    STA /B
    CMP ?0
    LDA @C
JZ LOOP123
LDA /A
OUT