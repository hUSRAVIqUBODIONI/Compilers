%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>



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

TokenArray tokens = {NULL, 0, 0};
CommentArray comments = {NULL, 0, 0};
ErrorArray errors = {NULL, 0, 0};

char* string_buf = NULL;
size_t string_buf_len = 0;
size_t string_buf_cap = 0;

Position cur_pos = {1, 1, 0};
Position str_start;
Position comment_start;

void init_array(void** arr, int* count, int* capacity, size_t item_size, int initial_capacity) {
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

void add_token(int type, Fragment frag, int char_val, long num_val, char* str_val) {
    Token token = {
        .type = type,
        .coords = frag,
        .attr = {0}
    };
    
    switch(type) {
        case 3: token.attr.char_value = char_val; break;
        case 2: token.attr.number_value = num_val; break;
        case 1: token.attr.string_value = strdup(str_val); break;
        case 10: token.attr.string_value = strdup(str_val); break;
    }
    
    add_to_array((void**)&tokens.items, &tokens.count, &tokens.capacity, sizeof(Token), &token);
}

void add_comment(Fragment frag) {
    Comment comment = {
        .coords = frag
       
    };
    add_to_array((void**)&comments.items, &comments.count, &comments.capacity, sizeof(Comment), &comment);
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
    printf("\nTOKENS (%d):\n", tokens.count);
    for (int i = 0; i < tokens.count; i++) {
        print_frag(tokens.items[i].coords);
        switch(tokens.items[i].type) {
            case 1: printf(" IDENT %s\n", tokens.items[i].attr.string_value); break;
            case 2: printf(" NUMBER %ld\n", tokens.items[i].attr.number_value); break;
            case 3: printf(" CHAR %d\n", tokens.items[i].attr.char_value); break;
            case 4: printf(" LPAREN\n"); break;
            case 5: printf(" RPAREN\n"); break;
            case 6: printf(" PLUS\n"); break;
            case 7: printf(" MINUS\n"); break;
            case 8: printf(" MULTIPLY\n"); break;
            case 9: printf(" DIVIDE\n"); break;
            case 10: printf(" STRING %s\n", tokens.items[i].attr.string_value); break;
        }
    }
    
    printf("\nCOMMENTS (%d):\n", comments.count);
    for (int i = 0; i < comments.count; i++) {
        print_frag(comments.items[i].coords);
        printf("\n");
    }
    
    printf("\nERRORS (%d):\n", errors.count);
    for (int i = 0; i < errors.count; i++) {
        printf("Error (%d,%d): %s\n", errors.items[i].pos.line, errors.items[i].pos.pos, errors.items[i].message);
    }
}

void free_arrays() {
    for (int i = 0; i < tokens.count; i++) {
        if (tokens.items[i].type == 1 || tokens.items[i].type == 10) free(tokens.items[i].attr.string_value);
    }
    free(tokens.items);
    
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
    clear_string_buf();  // Очищаем буфер
    BEGIN(INITIAL);      // Возвращаемся в начальное состояние
    return 0;            // Завершаем лексический анализ
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
    add_token(10, frag, 0, 0, string_buf);
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
    clear_string_buf();  // Очищаем буфер
    BEGIN(INITIAL);      // Возвращаемся в начальное состояние
    return 0;            // Завершаем лексический анализ
}

<ESCAPE>{HEX}{2} {
    char hex[3] = {yytext[0], yytext[1], '\0'};
    char *endptr;
    errno = 0;
    int c = strtol(hex, &endptr, 16);
   
    if (endptr == hex || errno == ERANGE) {
        add_error(cur_pos, "Invalid hex escape");
    } else {
        
        char string[9]; 
        snprintf(string, sizeof(string), "%d", c); 
        for(int i=0; i< strlen(string);i++){
            append_to_string(string[i]);
        }
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
    add_token(6, frag, 0, 0, NULL);
    update_position(yytext, yyleng);
}

"-"         { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos++; frag.following.index++;
    add_token(7, frag, 0, 0, NULL);
    update_position(yytext, yyleng);
}

"*"         { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos++; frag.following.index++;
    add_token(8, frag, 0, 0, NULL);
    update_position(yytext, yyleng);
}

"/"         { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos++; frag.following.index++;
    add_token(9, frag, 0, 0, NULL);
    update_position(yytext, yyleng);
}

{NUMBER}    { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos += yyleng; frag.following.index += yyleng;
    long num = atol(yytext);
    add_token(2, frag, 0, num, NULL);
    update_position(yytext, yyleng);
}

{IDENT}     { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos += yyleng; frag.following.index += yyleng;
    add_token(1, frag, 0, 0, yytext);
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