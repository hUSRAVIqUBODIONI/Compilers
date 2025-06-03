% Лабораторная работа № 1.5 «Порождение лексического анализатора с помощью flex»
% 26 марта 2025 г.
% Шоди Шоимов, ИУ9-62Б

# Цель работы
Целью данной работы является изучение генератора лексических анализаторов flex.

# Индивидуальный вариант
Числа: последовательности десятичных цифр, могут начинаться с нуля.

Знаки операций: «+», «-», «*», «/», «(», «)».

Комментарии начинаются на «(*», заканчиваются на «*)», не могут быть вложенными.

Строки: ограничены фигурными скобками «{ … }», escape-последовательности «#{», «#}», «##», «#hh», означают,
соответственно «{», «}», «#» и символ с кодом hh, где h — шестнадцатеричное число, не могут 
пересекать границы строчек тeкста.

# Реализация

```lex
%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#define TAG_IDENT 1
#define TAG_NUMBER 2
#define TAG_CHAR 3
#define TAG_LPAREN 4
#define TAG_RPAREN 5
#define TAG_PLUS 6
#define TAG_MINUS 7
#define TAG_MULTIPLY 8
#define TAG_DIVIDE 9
#define TAG_STRING 10

char* tag_names[] = {
    "END_OF_PROGRAM", "IDENT", "NUMBER",
    "CHAR", "LPAREN", "RPAREN", "PLUS",
    "MINUS", "MULTIPLY", "DIVIDE", "STRING"
};

typedef struct {
    int line, pos, index;
} Position;

typedef struct {
    Position starting, following;
} Fragment;

typedef struct {
    int type;
    Fragment coords;
    union {
        int char_value;
        long number_value;
        char* string_value;
    } attr;
} Token;

typedef struct {
    Fragment coords;
    char* text;
} Comment;

typedef struct {
    Position pos;
    char* message;
} Error;

typedef struct {
    Token* items;
    int count;
    int capacity;
} TokenArray;

typedef struct {
    Comment* items;
    int count;
    int capacity;
} CommentArray;

typedef struct {
    Error* items;
    int count;
    int capacity;
} ErrorArray;

typedef struct {
    char** items;
    int count;
    int capacity;
} IdentTable;

TokenArray tokens = {NULL, 0, 0};
CommentArray comments = {NULL, 0, 0};
ErrorArray errors = {NULL, 0, 0};
IdentTable ident_table = {NULL, 0, 0};

char* string_buf = NULL;
size_t string_buf_len = 0;
size_t string_buf_cap = 0;

Position cur_pos = {1, 1, 0};
Position str_start;
Position comment_start;

void init_array(void** arr, int* count, 
int* capacity, size_t item_size, int initial_capacity) {
    *arr = malloc(item_size * initial_capacity);
    *count = 0;
    *capacity = initial_capacity;
}

void add_to_array(void** arr, int* count, int* capacity, size_t item_size, void* item) {
    if (*count >= *capacity) {
        *capacity *= 2;
        *arr = realloc(*arr, item_size * *capacity);
    }
    memcpy((char*)*arr + (*count * item_size), item, item_size);
    (*count)++;
}

int find_or_add_ident(const char* name) {
    for (int i = 0; i < ident_table.count; i++) {
        if (strcmp(ident_table.items[i], name) == 0) {
            return i + 1;
        }
    }
    
    if (ident_table.count >= ident_table.capacity) {
        ident_table.capacity = ident_table.capacity ? ident_table.capacity * 2 : 16;
        ident_table.items = realloc(ident_table.items, sizeof(char*) * ident_table.capacity);
    }
    
    ident_table.items[ident_table.count] = strdup(name);
    return ++ident_table.count;
}

void add_token(const char* type_name, Fragment frag, int char_val, long num_val, char* str_val) {
    Token token = {0};
    token.coords = frag;
    
    if (strcmp(type_name, "IDENT") == 0) {
        token.type = TAG_IDENT;
        token.attr.number_value = find_or_add_ident(str_val);
        free(str_val);
    }
    else if (strcmp(type_name, "NUMBER") == 0) {
        token.type = TAG_NUMBER;
        token.attr.number_value = num_val;
    }
    else if (strcmp(type_name, "CHAR") == 0) {
        token.type = TAG_CHAR;
        token.attr.char_value = char_val;
    }
    else if (strcmp(type_name, "LPAREN") == 0) {
        token.type = TAG_LPAREN;
    }
    else if (strcmp(type_name, "RPAREN") == 0) {
        token.type = TAG_RPAREN;
    }
    else if (strcmp(type_name, "PLUS") == 0) {
        token.type = TAG_PLUS;
    }
    else if (strcmp(type_name, "MINUS") == 0) {
        token.type = TAG_MINUS;
    }
    else if (strcmp(type_name, "MULTIPLY") == 0) {
        token.type = TAG_MULTIPLY;
    }
    else if (strcmp(type_name, "DIVIDE") == 0) {
        token.type = TAG_DIVIDE;
    }
    else if (strcmp(type_name, "STRING") == 0) {
        token.type = TAG_STRING;
        token.attr.string_value = strdup(str_val);
    }
    
    add_to_array((void**)&tokens.items, &tokens.count, &tokens.capacity, sizeof(Token), &token);
}

void add_comment(Fragment frag) {
    Comment comment = {
        .coords = frag
    };
    add_to_array((void**)&comments.items, &comments.count,
     &comments.capacity, sizeof(Comment), &comment);
}

void add_error(Position pos, char* message) {
    Error error = {
        .pos = pos,
        .message = strdup(message)
    };
    add_to_array((void**)&errors.items, &errors.count, &errors.capacity, sizeof(Error), &error);
}

void print_frag(Fragment f) {
    printf("(%d,%d)-(%d,%d)", f.starting.line, f.starting.pos, f.following.line, f.following.pos);
}

void print_all() {
    printf("\nIDENTIFIER TABLE (%d):\n", ident_table.count);
    for (int i = 0; i < ident_table.count; i++) {
        printf("%d: %s\n", i+1, ident_table.items[i]);
    }
    
    printf("\nTOKENS (%d):\n", tokens.count);
    for (int i = 0; i < tokens.count; i++) {
        print_frag(tokens.items[i].coords);
        printf(" %s", tag_names[tokens.items[i].type]);
        
        switch(tokens.items[i].type) {
            case TAG_IDENT:
                printf(" %ld (%s)\n", tokens.items[i].attr.number_value, 
                       ident_table.items[tokens.items[i].attr.number_value - 1]);
                break;
            case TAG_STRING:
                printf(" %s\n", tokens.items[i].attr.string_value);
                break;
            case TAG_NUMBER:
                printf(" %ld\n", tokens.items[i].attr.number_value);
                break;
            case TAG_CHAR:
                printf(" %d\n", tokens.items[i].attr.char_value);
                break;
            default:
                printf("\n");
                break;
        }
    }
    
    printf("\nCOMMENTS (%d):\n", comments.count);
    for (int i = 0; i < comments.count; i++) {
        print_frag(comments.items[i].coords);
        printf("\n");
    }
    
    printf("\nERRORS (%d):\n", errors.count);
    for (int i = 0; i < errors.count; i++) {
        printf("Error (%d,%d): %s\n", 
        errors.items[i].pos.line, errors.items[i].pos.pos, errors.items[i].message);
    }
}

void free_arrays() {
    for (int i = 0; i < tokens.count; i++) {
        if (tokens.items[i].type == TAG_STRING) {
            free(tokens.items[i].attr.string_value);
        }
    }
    free(tokens.items);
    
    for (int i = 0; i < ident_table.count; i++) {
        free(ident_table.items[i]);
    }
    free(ident_table.items);
    
    for (int i = 0; i < comments.count; i++) {
        free(comments.items[i].text);
    }
    free(comments.items);
    
    for (int i = 0; i < errors.count; i++) {
        free(errors.items[i].message);
    }
    free(errors.items);
    
    if (string_buf) free(string_buf);
}

void update_position(const char* text, int len) {
    for (int i = 0; i < len; i++) {
        if (text[i] == '\n') {
            cur_pos.line++;
            cur_pos.pos = 1;
        } else {
            cur_pos.pos++;
        }
        cur_pos.index++;
    }
}

void clear_string_buf() {
    if (string_buf) free(string_buf);
    string_buf = NULL;
    string_buf_len = 0;
    string_buf_cap = 0;
}

void append_to_string(char c) {
    if (string_buf_len >= string_buf_cap) {
        string_buf_cap = string_buf_cap ? string_buf_cap * 2 : 16;
        string_buf = realloc(string_buf, string_buf_cap);
    }
    string_buf[string_buf_len++] = c;
}
%}

%option noyywrap nounput noinput

LETTER      [a-zA-Z]
DIGIT       [0-9]
IDENT       {LETTER}({LETTER}|{DIGIT})*
NUMBER      {DIGIT}+
WS          [ \t]+
HEX         [0-9a-fA-F]

%x COMMENT 
%x STRING ESCAPE

%%

{WS}        { update_position(yytext, yyleng); }

"(*"        { 
    comment_start = cur_pos;
    update_position(yytext, yyleng);
    BEGIN(COMMENT);
}

<COMMENT>"*)" {
    Fragment comment_frag = {comment_start, cur_pos};
    comment_frag.following.pos += yyleng;
    comment_frag.following.index += yyleng;
    add_comment(comment_frag);
    update_position(yytext, yyleng);
    BEGIN(INITIAL);
}

<COMMENT>[^*\n]+      { update_position(yytext, yyleng); }
<COMMENT>\*[^*)\n]*   { update_position(yytext, yyleng); }
<COMMENT>\n          { update_position(yytext, yyleng); }
<COMMENT><<EOF>> {
    add_error(comment_start, "Find end of programm expected *)");
    clear_string_buf();
    BEGIN(INITIAL);
    return 0;
}

"{"         { 
    str_start = cur_pos;
    clear_string_buf();
    BEGIN(STRING);
    update_position(yytext, yyleng);
}

<STRING>"}" {
    Fragment frag = {str_start, cur_pos};
    frag.following.pos++; 
    frag.following.index++;
    append_to_string('\0');
    add_token("STRING", frag, 0, 0, string_buf);
    clear_string_buf();
    update_position(yytext, yyleng);
    BEGIN(INITIAL);
}

<STRING>"#{" {
    append_to_string('{');
    update_position(yytext, yyleng);
}

<STRING>"#}" {
    append_to_string('}');
    update_position(yytext, yyleng);
}

<STRING>"##" {
    append_to_string('#');
    update_position(yytext, yyleng);
}

<STRING>"#" {
    update_position(yytext, yyleng);
    BEGIN(ESCAPE);
}

<STRING>\n  {
    add_error(cur_pos, "Newline in string");
    update_position(yytext, yyleng);
}

<STRING>.   {
    append_to_string(yytext[0]);
    update_position(yytext, yyleng);
}
<STRING><<EOF>> {
    add_error(str_start, "Unclosed string, expected '}'");
    clear_string_buf();
    BEGIN(INITIAL);
    return 0;
}

<ESCAPE>{HEX}{2} {
    char hex[3] = {yytext[0], yytext[1], '\0'};
    char *endptr;
    errno = 0;
    int c = strtol(hex, &endptr, 16);
   
    if (endptr == hex || errno == ERANGE) {
        add_error(cur_pos, "Invalid hex escape");
    } else {
        char ch = (char)c;
        append_to_string(ch);
    }
    
    update_position(yytext, yyleng);
    BEGIN(STRING);
}

<ESCAPE>.   {
    add_error(cur_pos, "Invalid escape sequence");
    update_position(yytext, yyleng);
    BEGIN(STRING);
}

"+"         { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos++; frag.following.index++;
    add_token("PLUS", frag, 0, 0, NULL);
    update_position(yytext, yyleng);
}

"-"         { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos++; frag.following.index++;
    add_token("MINUS", frag, 0, 0, NULL);
    update_position(yytext, yyleng);
}

"*"         { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos++; frag.following.index++;
    add_token("MULTIPLY", frag, 0, 0, NULL);
    update_position(yytext, yyleng);
}

"/"         { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos++; frag.following.index++;
    add_token("DIVIDE", frag, 0, 0, NULL);
    update_position(yytext, yyleng);
}

{NUMBER}    { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos += yyleng; frag.following.index += yyleng;
    long long num = atol(yytext);
    add_token("NUMBER", frag, 0, num, NULL);
    update_position(yytext, yyleng);
}

{IDENT}     { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos += yyleng; frag.following.index += yyleng;
    add_token("IDENT", frag, 0, 0, strdup(yytext));
    update_position(yytext, yyleng);
}

\n          { cur_pos.line++; cur_pos.pos = 1; cur_pos.index++; }

<<EOF>>     { return 0; }
.           { 
    add_error(cur_pos, "Invalid character");
    cur_pos.pos++; cur_pos.index++; 
}

%%

int main(int argc, char **argv) {
    init_array((void**)&tokens.items, &tokens.count, &tokens.capacity, sizeof(Token), 100);
    init_array((void**)&comments.items, &comments.count, &comments.capacity, sizeof(Comment), 50);
    init_array((void**)&errors.items, &errors.count, &errors.capacity, sizeof(Error), 50);

    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            perror(argv[1]);
            return 1;
        }
    }
    yylex();
    print_all();
    free_arrays();

    if (yyin != stdin) fclose(yyin);
    return 0;
}
```

# Тестирование

Входные данные

```
shodi bobob aaaa shodi
12334  {HELLO## #{aaa#} #4F}
bbbbbb
```

Вывод на `stdout`

```

IDENTIFIER TABLE (4):
1: shodi
2: bobob
3: aaaa
4: bbbbbb

TOKENS (7):
(1,1)-(1,6) IDENT 1 (shodi)
(1,7)-(1,12) IDENT 2 (bobob)
(1,13)-(1,17) IDENT 3 (aaaa)
(1,18)-(1,23) IDENT 1 (shodi)
(2,1)-(2,6) NUMBER 12334
(2,8)-(2,29) STRING HELLO# {aaa} O
(3,1)-(3,7) IDENT 4 (bbbbbb)

COMMENTS (0):

ERRORS (0):
```

# Вывод
абота с flex оказалась неожиданно приятным возвращением в мир Си.

Генератор лексеров, оказывается, не просто разматывает регулярки в switch-case, а требует чёткого понимания,
как состояния (%x), контексты (yymore(), yyless()) и буферизация влияют на разбор. Пришлось вспомнить, что
yytext — это не просто строка, а подвижное окно в буфере, а unput() может спасти при переполнении lookahead.

Особенно занятно было настраивать обработку ошибок: flex по умолчанию просто проглатывает невалидные символы,
но вставка %option nodefault заставила его явно ругаться на пропущенные правила. А ещё — неочевидная магия 
YY_USER_ACTION для подсчёта позиций в файле без тормозов.