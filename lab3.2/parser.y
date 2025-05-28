%{
#include <stdio.h>
#include "lexer.h"
%}

%define api.pure
%locations
%lex-param {yyscan_t scanner}  /* параметр для yylex() */
/* параметры для yyparse() */
%parse-param {yyscan_t scanner}
%parse-param {long env[26]}
%parse-param {int tab_count}

%union {
    long number;
    char* string;
    char* ident;
    char char_cnst;
    bool bool_cnst;
}

%token  F_CONSTANT FUNC_NAME SIZEOF
%token	PTR_OP INC_OP DEC_OP LEFT_OP RIGHT_OP LE_OP GE_OP EQ_OP NE_OP
%token	AND_OP OR_OP MUL_ASSIGN DIV_ASSIGN MOD_ASSIGN ADD_ASSIGN
%token	SUB_ASSIGN LEFT_ASSIGN RIGHT_ASSIGN AND_ASSIGN
%token	XOR_ASSIGN OR_ASSIGN
%token	TYPEDEF_NAME ENUMERATION_CONSTANT

%token	TYPEDEF EXTERN STATIC AUTO REGISTER INLINE
%token	CONST RESTRICT VOLATILE
%token	BOOL CHAR SHORT INT LONG SIGNED UNSIGNED FLOAT DOUBLE VOID
%token	COMPLEX IMAGINARY
%token	STRUCT UNION ENUM ELLIPSIS

%token	CASE DEFAULT IF ELSE SWITCH WHILE DO FOR GOTO CONTINUE BREAK RETURN

%token	ALIGNAS ALIGNOF ATOMIC GENERIC NORETURN STATIC_ASSERT THREAD_LOCAL

%token <ident> IDENTIFIER
%token <string> STRING_LITERAL
%token <number> I_CONSTANT


%start translation_unit

%{
int yylex(YYSTYPE *yylval_param, YYLTYPE *yylloc_param, yyscan_t scanner);
void yyerror(YYLTYPE *loc, yyscan_t scanner, long env[26], int tab_count, const char *message);
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
    : {printf("\n"); tabulate(tab_count); printf("}\n"); }
    ;

print_r_cr_bracket_aux
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
	| string
	| '(' print_l_paren expression ')' print_r_paren
	| generic_selection
	;

constant
	: I_CONSTANT { printf("%li", $1); }
	| F_CONSTANT
	| ENUMERATION_CONSTANT	/* after it has been defined as such */
	;

enumeration_constant		/* before it has been defined as such */
	: IDENTIFIER { printf(" %s", $1); }
	;

string
	: STRING_LITERAL
	| FUNC_NAME
	;

generic_selection
	: GENERIC '(' print_l_paren assignment_expression ',' { printf(", "); } generic_assoc_list ')' print_r_paren
	;

generic_assoc_list
	: generic_association
	| generic_assoc_list ',' { printf(", "); } generic_association
	;

generic_association
	: type_name ':' { printf(":"); } assignment_expression
	| DEFAULT ':' { printf(":"); } assignment_expression
	;

postfix_expression
	: primary_expression
	| postfix_expression '[' print_l_sq_bracket expression ']' print_r_sq_bracket
	| postfix_expression '(' print_l_paren ')' print_r_paren
	| postfix_expression '(' print_l_paren argument_expression_list ')' print_r_paren
	| postfix_expression '.' { printf("."); }  IDENTIFIER { printf(" %s", $4); }
	| postfix_expression PTR_OP IDENTIFIER
	| postfix_expression INC_OP
	| postfix_expression DEC_OP
	| '(' print_l_paren type_name ')' print_r_paren '{' print_l_cr_bracket initializer_list '}' print_r_cr_bracket
	| '(' print_l_paren type_name ')' print_r_paren '{' print_l_cr_bracket initializer_list ',' { printf(", "); } '}' print_r_cr_bracket
	;

argument_expression_list
	: assignment_expression
	| argument_expression_list ',' { printf(", "); } assignment_expression
	;

unary_expression
	: postfix_expression
	| INC_OP unary_expression
	| DEC_OP unary_expression
	| unary_operator cast_expression
	| SIZEOF {printf("sizeof");} '(' print_l_paren type_name ')' print_r_paren
	| ALIGNOF '(' print_l_paren type_name ')' print_r_paren
	;

unary_operator
	: '&' {printf("&");}
	| '*' {printf("*");}
	| '+' {printf("+");}
	| '-' {printf("-");}
	| '~' {printf("~");}
	| '!' {printf("!");}
	;

cast_expression
	: unary_expression
	| '(' print_l_paren type_name ')' print_r_paren cast_expression
	;

multiplicative_expression
	: cast_expression
	| multiplicative_expression '*' {printf(" * ");} cast_expression
	| multiplicative_expression '/' {printf(" / ");} cast_expression
	| multiplicative_expression '%' {printf(" % ");} cast_expression
	;

additive_expression
	: multiplicative_expression
	| additive_expression '+' {printf(" + ");} multiplicative_expression
	| additive_expression '-' {printf(" - ");} multiplicative_expression
	;

shift_expression
	: additive_expression
	| shift_expression LEFT_OP additive_expression
	| shift_expression RIGHT_OP additive_expression
	;

relational_expression
	: shift_expression
	| relational_expression '<' { printf(" < ");} shift_expression
	| relational_expression '>' { printf(" > ");} shift_expression
	| relational_expression LE_OP shift_expression
	| relational_expression GE_OP shift_expression
	;

equality_expression
	: relational_expression
	| equality_expression EQ_OP relational_expression
	| equality_expression NE_OP relational_expression
	;

and_expression
	: equality_expression
	| and_expression '&' equality_expression
	;

exclusive_or_expression
	: and_expression
	| exclusive_or_expression '^' and_expression
	;

inclusive_or_expression
	: exclusive_or_expression
	| inclusive_or_expression '|' exclusive_or_expression
	;

logical_and_expression
	: inclusive_or_expression
	| logical_and_expression AND_OP inclusive_or_expression
	;

logical_or_expression
	: logical_and_expression
	| logical_or_expression OR_OP logical_and_expression
	;

conditional_expression
	: logical_or_expression
	| logical_or_expression '?' { printf("? "); } expression ':' { printf(":"); } conditional_expression
	;

assignment_expression
	: conditional_expression
	| unary_expression assignment_operator assignment_expression
	;

assignment_operator
	: '=' { printf(" = "); }
	| MUL_ASSIGN
	| DIV_ASSIGN
	| MOD_ASSIGN
	| ADD_ASSIGN
	| SUB_ASSIGN
	| LEFT_ASSIGN
	| RIGHT_ASSIGN
	| AND_ASSIGN
	| XOR_ASSIGN
	| OR_ASSIGN
	;

expression
	: assignment_expression
	| expression ',' { printf(", "); } assignment_expression
	;

constant_expression
	: conditional_expression	/* with constraints */
	;

declaration
	: declaration_specifiers ';' { printf(";\n\n"); }
	| declaration_specifiers init_declarator_list ';' { printf(";\n\n"); }
	| static_assert_declaration
	;

declaration_specifiers
	: storage_class_specifier declaration_specifiers
	| storage_class_specifier
	| type_specifier  declaration_specifiers
	| type_specifier
	| type_qualifier declaration_specifiers
	| type_qualifier
	| function_specifier declaration_specifiers
	| function_specifier
	| alignment_specifier declaration_specifiers
	| alignment_specifier
	;

init_declarator_list
	: init_declarator
	| init_declarator_list ',' { printf(", "); } init_declarator
	;

init_declarator
	: declarator '=' { printf(" = "); } initializer
	| declarator
	;

storage_class_specifier
	: TYPEDEF	/* identifiers must be flagged as TYPEDEF_NAME */
	| EXTERN
	| STATIC
	| THREAD_LOCAL
	| AUTO
	| REGISTER
	;

type_specifier
	: VOID { printf("void "); }
	| CHAR { printf("char "); }
	| SHORT { printf("short "); }
	| INT { printf("int "); }
	| LONG { printf("long "); }
	| FLOAT { printf("float "); }
	| DOUBLE { printf("double "); }
	| SIGNED
	| UNSIGNED
	| BOOL { printf("bool "); }
	| COMPLEX
	| IMAGINARY	  	/* non-mandated extension */
	| struct_or_union_specifier
	| enum_specifier
	| TYPEDEF_NAME		/* after it has been defined as such */
	;

struct_or_union_specifier
	: struct_or_union '{' print_l_cr_bracket struct_declaration_list '}' print_r_cr_bracket_aux
	| struct_or_union IDENTIFIER { printf("%s ", $2); } '{'  print_l_cr_bracket struct_declaration_list '}'  print_r_cr_bracket_aux
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
    : specifier_qualifier_list ';'
    | specifier_qualifier_list struct_declarator_list ';' { printf(";"); }
    | static_assert_declaration
    ;

specifier_qualifier_list
	: type_specifier specifier_qualifier_list
	| type_specifier
	| type_qualifier specifier_qualifier_list
	| type_qualifier
	;

struct_declarator_list
	: struct_declarator
	| struct_declarator_list ',' { printf(", "); } struct_declarator
	;

struct_declarator
	: ':' { printf(":"); } constant_expression
	| declarator ':' { printf(":"); } constant_expression
	| declarator
	;

enum_name
	: ENUM {printf("enum ");}
	;

ident_print
	: IDENTIFIER { printf("%s ", $1); }
	;

enum_specifier
	: enum_name '{' print_l_cr_bracket enumerator_list '}' print_r_cr_bracket_aux
	| enum_name '{' print_l_cr_bracket enumerator_list ',' { printf(", "); } '}' print_r_cr_bracket_aux
	| enum_name ident_print '{' print_l_cr_bracket enumerator_list '}' print_r_cr_bracket_aux
	| enum_name ident_print '{' print_l_cr_bracket enumerator_list ',' { printf(","); } '}' print_r_cr_bracket_aux
	| enum_name ident_print
	;

enumerator_list
	: {tabulate(tab_count);} enumerator
	| enumerator_list ',' { printf(",\n"); tabulate(tab_count);} enumerator
	;

enumerator	/* identifiers must be flagged as ENUMERATION_CONSTANT */
	: enumeration_constant '=' { printf(" = "); } constant_expression
	| enumeration_constant
	;

type_qualifier
	: CONST
	| RESTRICT
	| VOLATILE
	| ATOMIC
	;

function_specifier
	: INLINE
	| NORETURN
	;

alignment_specifier
	: ALIGNAS '(' print_l_paren type_name ')' print_r_paren
	| ALIGNAS '(' print_l_paren constant_expression ')' print_r_paren
	;

declarator
	: pointer direct_declarator
	| direct_declarator
	;

direct_declarator
	: IDENTIFIER { printf("%s", $1); }
	| '(' print_l_paren declarator ')' print_r_paren
	| direct_declarator '[' print_l_sq_bracket ']' print_r_sq_bracket
	| direct_declarator '[' print_l_sq_bracket '*' ']' print_r_sq_bracket
	| direct_declarator '[' print_l_sq_bracket  STATIC type_qualifier_list assignment_expression ']' print_r_sq_bracket
	| direct_declarator '[' print_l_sq_bracket  STATIC assignment_expression ']' print_r_sq_bracket
	| direct_declarator '[' print_l_sq_bracket  type_qualifier_list '*' ']' print_r_sq_bracket
	| direct_declarator '[' print_l_sq_bracket  type_qualifier_list STATIC assignment_expression ']' print_r_sq_bracket
	| direct_declarator '[' print_l_sq_bracket type_qualifier_list assignment_expression ']' print_r_sq_bracket
	| direct_declarator '[' print_l_sq_bracket  type_qualifier_list ']' print_r_sq_bracket
	| direct_declarator '[' print_l_sq_bracket assignment_expression ']' print_r_sq_bracket
	| direct_declarator '(' print_l_paren  parameter_type_list ')' print_r_paren
	| direct_declarator '(' print_l_paren  ')' print_r_paren
	| direct_declarator '(' print_l_paren  identifier_list ')' print_r_paren
	;

pointer
	: '*' print_star type_qualifier_list pointer
	| '*' print_star type_qualifier_list
	| '*' print_star pointer
	| '*' print_star
	;

type_qualifier_list
	: type_qualifier
	| type_qualifier_list type_qualifier
	;


parameter_type_list
	: parameter_list ',' { printf(", "); } ELLIPSIS
	| parameter_list
	;

parameter_list
	: parameter_declaration
	| parameter_list ',' { printf(", "); } parameter_declaration
	;

parameter_declaration
	: declaration_specifiers declarator
	| declaration_specifiers abstract_declarator
	| declaration_specifiers
	;

identifier_list
	: IDENTIFIER
	| identifier_list ',' { printf(", "); } IDENTIFIER
	;

type_name
	: specifier_qualifier_list abstract_declarator
	| specifier_qualifier_list
	;

abstract_declarator
	: pointer direct_abstract_declarator
	| pointer
	| direct_abstract_declarator
	;

direct_abstract_declarator
	: '(' print_l_paren abstract_declarator ')' print_r_paren
	| '[' print_l_sq_bracket ']' print_r_sq_bracket
	| '[' print_l_sq_bracket '*' ']' print_r_sq_bracket
	| '[' print_l_sq_bracket STATIC type_qualifier_list assignment_expression ']' print_r_sq_bracket
	| '[' print_l_sq_bracket STATIC assignment_expression ']' print_r_sq_bracket
	| '[' print_l_sq_bracket type_qualifier_list STATIC assignment_expression ']' print_r_sq_bracket
	| '[' print_l_sq_bracket type_qualifier_list assignment_expression ']' print_r_sq_bracket
	| '[' print_l_sq_bracket type_qualifier_list ']' print_r_sq_bracket
	| '[' print_l_sq_bracket assignment_expression ']' print_r_sq_bracket
	| direct_abstract_declarator '[' print_l_sq_bracket ']' print_r_sq_bracket
	| direct_abstract_declarator '[' print_l_sq_bracket '*' ']' print_r_sq_bracket
	| direct_abstract_declarator '[' print_l_sq_bracket STATIC type_qualifier_list assignment_expression ']' print_r_sq_bracket
	| direct_abstract_declarator '[' print_l_sq_bracket STATIC assignment_expression ']' print_r_sq_bracket
	| direct_abstract_declarator '[' print_l_sq_bracket type_qualifier_list assignment_expression ']' print_r_sq_bracket
	| direct_abstract_declarator '[' print_l_sq_bracket type_qualifier_list STATIC assignment_expression ']' print_r_sq_bracket
	| direct_abstract_declarator '[' print_l_sq_bracket type_qualifier_list ']' print_r_sq_bracket
	| direct_abstract_declarator '[' print_l_sq_bracket assignment_expression ']' print_r_sq_bracket
	| '(' print_l_paren ')' print_r_paren
	| '(' print_l_paren parameter_type_list ')' print_r_paren
	| direct_abstract_declarator '(' print_l_paren ')' print_r_paren
	| direct_abstract_declarator '(' print_l_paren parameter_type_list ')' print_r_paren
	;

initializer
	: '{' print_l_cr_bracket initializer_list '}' print_r_cr_bracket
	| '{' print_l_cr_bracket initializer_list ',' { printf(", "); } '}' print_r_cr_bracket
	| assignment_expression
	;

initializer_list
	: designation initializer
	| initializer
	| initializer_list ',' { printf(", "); } designation initializer
	| initializer_list ',' { printf(", "); } initializer
	;

designation
	: designator_list '=' { printf(" = "); }
	;

designator_list
	: designator
	| designator_list designator
	;

designator
	: '[' print_l_sq_bracket constant_expression ']' print_r_sq_bracket
	| '.' IDENTIFIER
	;

static_assert_declaration
	: STATIC_ASSERT '(' print_l_paren constant_expression ',' { printf(", "); } STRING_LITERAL ')' print_r_paren ';' { printf(";\n"); }
	;

statement
	: labeled_statement
	| compound_statement
	| expression_statement
	| selection_statement
	| iteration_statement
	| jump_statement
	;

labeled_statement
	: IDENTIFIER ':' { printf(":"); } statement
	| CASE constant_expression ':' { printf(":"); } statement
	| DEFAULT ':' { printf(":"); } statement
	;

compound_statement
	: '{' '}' { printf("{}"); }
	| '{' print_l_cr_bracket {tab_count +=1;} block_item_list '}' { tabulate(tab_count); tab_count -=1; } print_r_cr_bracket
	;

block_item_list
	: block_item
	| block_item_list block_item
	;

block_item
	: { tabulate(tab_count);} declaration
	| { tabulate(tab_count);} statement
	;

expression_statement
	: ';' { printf(";"); }
	| expression ';' { printf("; "); }
	;

selection_statement
	: IF '(' print_l_paren expression ')' print_r_paren statement ELSE statement
	| SWITCH '(' print_l_paren expression ')' print_r_paren statement
	;

iteration_statement
	: WHILE '(' print_l_paren expression ')' print_r_paren statement
	| DO statement WHILE '(' print_l_paren expression ')' print_r_paren ';' { printf(";"); }
	| FOR { printf("for"); } '(' print_l_paren expression_statement expression_statement expression ')' print_r_paren statement
	;

jump_statement
	: GOTO IDENTIFIER ';' { printf(";"); }
	| CONTINUE ';' { printf(";"); }
	| BREAK ';' { printf(";"); }
	| RETURN ';' { printf("return;"); }
	| RETURN { printf("return "); } expression ';' { printf(";"); }
	;

translation_unit
	: external_declaration
	| translation_unit external_declaration
	;

external_declaration
	: function_definition
	| declaration
	;

function_definition
	: declaration_specifiers declarator declaration_list compound_statement
	| declaration_specifiers declarator compound_statement
	;

declaration_list
	: declaration
	| declaration_list declaration
	;
%%



int main(int argc, char *argv[]) {
    FILE *input = 0;
    long env[26] = { 0 };
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
    yyparse(scanner, env, tab_count);
    destroy_scanner(scanner);

    if (input != stdin) {
        fclose(input);
    }

    return 0;
}

