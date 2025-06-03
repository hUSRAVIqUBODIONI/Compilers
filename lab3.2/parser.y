%{
#include <stdio.h>
#include "lexer.h"
%}

%define api.pure
%locations
%lex-param {yyscan_t scanner}  /* параметр для yylex() */
/* параметры для yyparse() */
%parse-param {yyscan_t scanner}
%parse-param {int tab_count}

%union {
    long number;
    char* string;
    char* ident;
    char char_cnst;
    bool bool_cnst;
}

%token  SIZEOF
%token	ENUMERATION_CONSTANT

%token	BOOL CHAR SHORT INT LONG FLOAT DOUBLE VOID
%token	STRUCT UNION ENUM

%token <ident> IDENTIFIER
%token <string> STRING_LITERAL
%token <number> I_CONSTANT


%start translation_unit

%{
int yylex(YYSTYPE *yylval_param, YYLTYPE *yylloc_param, yyscan_t scanner);
void yyerror(YYLTYPE *loc, yyscan_t scanner, int tab_count, const char *message);
%}

%{
void tabulate(int tab_count) {
    for(int i = 0; i < tab_count; i++) {
        printf("  ");
    }
}


%}

%%

print_l_paren
    : { printf("("); }
    ;

print_r_paren
    : { printf(")"); }
    ;

print_l_sq_bracket
    : { printf("["); }
    ;

print_r_sq_bracket
    : { printf("]"); }
    ;

print_l_cr_bracket
    : {  printf("{\n"); tab_count +=1;}
    ;

print_r_cr_bracket
    : {printf("\n"); tab_count -=1; tabulate(tab_count); printf("}"); }
    ;

print_tab
	: {tabulate(tab_count);}
	;

print_star
	: {printf("*");}
	;

primary_expression
	: IDENTIFIER { printf("%s", $1); }
	| constant
	| '(' print_l_paren expression ')' print_r_paren
	;

constant
	: I_CONSTANT { printf("%li", $1); }
	;

enumeration_constant
	: IDENTIFIER { printf(" %s", $1); }
	;


unary_expression
	: primary_expression
	| unary_operator unary_expression
	| SIZEOF {printf("sizeof");} '(' print_l_paren type_specifier ')' print_r_paren
	;

unary_operator
	: '+' {printf("+");}
	| '-' {printf("-");}
	;


multiplicative_expression
	: unary_expression
	| multiplicative_expression '*' {printf(" * ");} unary_expression
	| multiplicative_expression '/' {printf(" / ");} unary_expression
	| multiplicative_expression '%' {printf(" %% ");} unary_expression
	;

additive_expression
	: multiplicative_expression
	| additive_expression '+' {printf(" + ");} multiplicative_expression
	| additive_expression '-' {printf(" - ");} multiplicative_expression
	;


assignment_expression
	: additive_expression
	| unary_expression assignment_operator assignment_expression
	;

assignment_operator
	: '=' { printf(" = "); }
	;

expression
	: assignment_expression
	| expression ',' { printf(", "); } assignment_expression
	;

declaration
	: type_specifier ';' { printf(";\n\n"); }
	| type_specifier declarator ';' { printf(";\n\n"); }
	;


type_specifier
	: VOID { printf("void "); }
	| CHAR { printf("char "); }
	| SHORT { printf("short "); }
	| INT { printf("int "); }
	| LONG { printf("long "); }
	| FLOAT { printf("float "); }
	| DOUBLE { printf("double "); }
	| BOOL { printf("bool "); }
	| struct_or_union_specifier
	| enum_specifier
	;

struct_or_union_specifier
	: struct_or_union '{' print_l_cr_bracket struct_declaration_list '}' print_r_cr_bracket
	| struct_or_union IDENTIFIER { printf("%s ", $2); } '{'  print_l_cr_bracket struct_declaration_list '}'  print_r_cr_bracket 
	| struct_or_union IDENTIFIER { printf("%s ", $2); }
	;

struct_or_union
	: STRUCT {printf("struct ");}
	| UNION {printf("union ");}
	;

struct_declaration_list
	: print_tab struct_declaration
	| struct_declaration_list {printf("\n"); tabulate(tab_count);}struct_declaration
	;

struct_declaration
    : type_specifier ';'
    | type_specifier struct_declarator_list ';' { printf(";"); }
    ;

struct_declarator_list
	: struct_declarator
	| struct_declarator_list ',' { printf(", "); } struct_declarator
	;

struct_declarator
	: ':' { printf(":"); }
	| declarator ':' { printf(":"); } additive_expression
	| declarator
	;

enum_name
	: ENUM {printf("enum ");}
	;

ident_print
	: IDENTIFIER { printf("%s", $1); }
	;

enum_specifier
	: enum_name '{' print_l_cr_bracket enumerator_list '}' print_r_cr_bracket
	| enum_name '{' print_l_cr_bracket enumerator_list ',' { printf(", "); } '}' print_r_cr_bracket
	| enum_name ident_print '{' print_l_cr_bracket enumerator_list '}' print_r_cr_bracket
	| enum_name ident_print '{' print_l_cr_bracket enumerator_list ',' { printf(","); } '}' print_r_cr_bracket
	| enum_name ident_print 
	;

enumerator_list
	: {tabulate(tab_count);} enumerator
	| enumerator_list ',' { printf(",\n"); tabulate(tab_count);} enumerator
	;

enumerator	
	: enumeration_constant '=' { printf(" = "); } additive_expression
	| enumeration_constant
	;


declarator
	: pointer direct_declarator
	| direct_declarator
	;

direct_declarator
	: IDENTIFIER { printf("%s", $1); }
	| direct_declarator '[' print_l_sq_bracket assignment_expression ']' print_r_sq_bracket
	;

pointer
	: '*' print_star pointer
	| '*' print_star
	;


translation_unit
	: declaration
	| translation_unit declaration
	;
%%



int main(int argc, char *argv[]) {
    FILE *input = 0;
    int tab_count = 0;
    bool user_tab = false;
    yyscan_t scanner;
    struct Extra extra;

    if (argc > 1) {
        printf("Read file %s\n", argv[1]);
        input = fopen(argv[1], "r");
    } else {
        printf("No file in command line, use stdin\n");
        input = stdin;
    }

    init_scanner(input, &scanner, &extra);
    yyparse(scanner, tab_count);
    destroy_scanner(scanner);

    if (input != stdin) {
        fclose(input);
    }

    return 0;
}

