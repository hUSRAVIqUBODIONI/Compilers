%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

 
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

Position cur_pos = {1, 1, 0};
Position char_start;

 
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
    }
    
    add_to_array((void**)&tokens.items, &tokens.count, &tokens.capacity, sizeof(Token), &token);
}

void add_comment(Fragment frag, char* text) {
    Comment comment = {
        .coords = frag,
        .text = strdup(text)
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
        }
    }
    
    printf("\nCOMMENTS (%d):\n", comments.count);
    for (int i = 0; i < comments.count; i++) {
        print_frag(comments.items[i].coords);
        printf(" %s\n", comments.items[i].text);
    }
    
    printf("\nERRORS (%d):\n", errors.count);
    for (int i = 0; i < errors.count; i++) {
        printf("Error (%d,%d): %s\n", errors.items[i].pos.line, errors.items[i].pos.pos, errors.items[i].message);
    }
}

void free_arrays() {
    for (int i = 0; i < tokens.count; i++) {
        if (tokens.items[i].type == 1) free(tokens.items[i].attr.string_value);
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
}
%}

%option noyywrap nounput noinput

LETTER      [a-zA-Z]
DIGIT       [0-9]
IDENT       {LETTER}({LETTER}|{DIGIT})*
NUMBER      {DIGIT}+
WS          [ \t]+

%x COMMENT CHAR

%%



{WS}        { cur_pos.pos += yyleng; cur_pos.index += yyleng; }

"(*"        { 
    Fragment comment_frag;
    comment_frag.starting = cur_pos;
    cur_pos.pos += 2; cur_pos.index += 2;
    BEGIN(COMMENT); 
}

<COMMENT>[^*)\n]*      { cur_pos.pos += yyleng; cur_pos.index += yyleng; }
<COMMENT>\*+[^*)\n]*   { cur_pos.pos += yyleng; cur_pos.index += yyleng; }
<COMMENT>\*+")"        { 
    Fragment comment_frag;
    comment_frag.starting = cur_pos;
    comment_frag.following.line = cur_pos.line;
    comment_frag.following.pos = cur_pos.pos + yyleng;
    comment_frag.following.index = cur_pos.index + yyleng;
    
    char* text = strndup(yytext, yyleng-2);
    add_comment(comment_frag, text);
    free(text);
    
    cur_pos.pos += yyleng; cur_pos.index += yyleng;
    BEGIN(INITIAL); 
}
<COMMENT><<EOF>>       { 
    add_error(cur_pos, "Unclosed comment");
    return 0; 
}

"'"        { 
    char_start = cur_pos;
    cur_pos.pos++; cur_pos.index++;
    BEGIN(CHAR); 
}

<CHAR>[^'\n\\]+  { 
    Fragment frag = {char_start, cur_pos};
    frag.following.pos += yyleng;
    frag.following.index += yyleng;
    add_token(3, frag, yytext[0], 0, NULL);
    cur_pos.pos += yyleng; cur_pos.index += yyleng;
    BEGIN(INITIAL);
}

<CHAR>\\n   { 
    Fragment frag = {char_start, cur_pos};
    frag.following.pos += 2;
    frag.following.index += 2;
    add_token(3, frag, '\n', 0, NULL);
    cur_pos.pos += 2; cur_pos.index += 2;
    BEGIN(INITIAL);
}

"("         { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos++; frag.following.index++;
    add_token(4, frag, 0, 0, NULL);
    cur_pos.pos++; cur_pos.index++;
}

")"         { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos++; frag.following.index++;
    add_token(5, frag, 0, 0, NULL);
    cur_pos.pos++; cur_pos.index++;
}

"+"         { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos++; frag.following.index++;
    add_token(6, frag, 0, 0, NULL);
    cur_pos.pos++; cur_pos.index++;
}

"-"         { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos++; frag.following.index++;
    add_token(7, frag, 0, 0, NULL);
    cur_pos.pos++; cur_pos.index++;
}

"*"         { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos++; frag.following.index++;
    add_token(8, frag, 0, 0, NULL);
    cur_pos.pos++; cur_pos.index++;
}

"/"         { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos++; frag.following.index++;
    add_token(9, frag, 0, 0, NULL);
    cur_pos.pos++; cur_pos.index++;
}

{NUMBER}    { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos += yyleng; frag.following.index += yyleng;
    long num = atol(yytext);
    add_token(2, frag, 0, num, NULL);
    cur_pos.pos += yyleng; cur_pos.index += yyleng;
}

{IDENT}     { 
    Fragment frag = {cur_pos, cur_pos};
    frag.following.pos += yyleng; frag.following.index += yyleng;
    add_token(1, frag, 0, 0, yytext);
    cur_pos.pos += yyleng; cur_pos.index += yyleng;
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