% "Лабораторная работа 3.2 «Форматтер исходных текстов»"
% 28 мая 2025 г.
% Шоди Шоимов, ИУ9-62Б

# Цель работы
Целью данной работы является приобретение навыков использования генератора 
синтаксических анализаторов bison.

# Индивидуальный вариант
Определения структур, объединений и перечислений языка Си. В инициализаторах перечислений 
допустимы знаки операций +, -, *, /, sizeof, операндами могут служить имена перечислимых 
значений и целые числа.

Числовые константы могут быть только целочисленными и десятичными.
```
struct Coords {
  int x, y;
};

enum Color {
  COLOR_RED = 1,
  COLOR_GREEN = 2,
  COLOR_BLUE = 4,
  COLOR_HIGHLIGHT = 8, // запятая после последнего необязательна
};

enum ScreenType {
  SCREEN_TYPE_TEXT,
  SCREEN_TYPE_GRAPHIC
} screen_type;  // ← объявили переменную

enum {
  HPIXELS = 480,
  WPIXELS = 640,
  HCHARS = 24,
  WCHARS = 80,
};

struct ScreenChar {
  char symbol;
  enum Color sym_color;
  enum Color back_color;
};

struct TextScreen {
  struct ScreenChar chars[HCHARS][WCHARS];
};

struct GrahpicScreen {
  enum Color pixels[HPIXELS][WPIXELS];
};

union Screen {
  struct TextScreen text;
  struct GraphicScreen graphic;
};

enum {
  BUFFER_SIZE = sizeof(union Screen),
  PAGE_SIZE = 4096,
  PAGES_FOR_BUFFER = (BUFFER_SIZE + PAGE_SIZE - 1) / PAGE_SIZE
};

/* допустимы и вложенные определения */
struct Token {
  struct Fragment {
    struct Pos {
      int line;
      int col;
    } starting, following;
  } fragment;

  enum { Ident, IntConst, FloatConst } type;

  union {
    char *name;
    int int_value;
    double float_value;
  } info;
};

struct List {
  struct Token value;
  struct List *next;
};
```


# Реализация
lexer.l
```
%{
#include "lexer.h"
#include "parser.tab.h"

#define YY_USER_ACTION \
  { \
    int i; \
    struct Extra *extra = yyextra; \
    if (! extra->continued ) { \
      yylloc->first_line = extra->cur_line; \
      yylloc->first_column = extra->cur_column; \
    } \
    extra->continued = false; \
    for (i = 0; i < yyleng; ++i) { \
      if (yytext[i] == '\n') { \
        extra->cur_line += 1; \
        extra->cur_column = 1; \
      } else { \
        extra->cur_column += 1; \
      } \
    } \
    yylloc->last_line = extra->cur_line; \
    yylloc->last_column = extra->cur_column; \
  }

void yyerror(YYLTYPE *loc, yyscan_t scanner, long env[26], int tab_count, const char *message) {
    printf("Error (%d,%d): %s\n", loc->first_line, loc->first_column, message);
}

%}

%option reentrant noyywrap bison-bridge bison-locations
%option extra-type="struct Extra *"
D   [0-9]
NZ  [1-9]
L   [a-zA-Z_]
A   [a-zA-Z_0-9]
WS  [ \t\v\n\f]

%%

"char"					{ return(CHAR); }
"double"				{ return(DOUBLE); }
"enum"					{ return(ENUM); }
"float"					{ return(FLOAT); }
"int"					{ return(INT); }
"long"					{ return(LONG); }
"short"					{ return(SHORT); }
"sizeof"				{ return(SIZEOF); }
"struct"				{ return(STRUCT); }
"union"					{ return(UNION); }
"void"					{ return(VOID); }

("{")				{ return '{'; }
("}")				{ return '}'; }

{L}{A}*					{ yylval->ident = strdup(yytext); return IDENTIFIER; }

{NZ}{D}*				{ yylval->number = atoi(yytext); return I_CONSTANT; }


\"[^"\n]*\"    { yylval->string = yytext; return STRING_LITERAL; }

";"					{ return ';'; }

","					{ return ','; }
":"					{ return ':'; }
"="					{ return '='; }
"("					{ return '('; }
")"					{ return ')'; }
("[")				{ return '['; }
("]")				{ return ']'; }
"-"					{ return '-'; }
"+"					{ return '+'; }
"*"					{ return '*'; }
"/"					{ return '/'; }
"%"					{ return '%'; }

{WS}+				
.			

%%

void init_scanner(FILE *input, yyscan_t *scanner, struct Extra *extra) {
    extra->continued = false;
    extra->cur_line = 1;
    extra->cur_column = 1;

    yylex_init(scanner);
    yylex_init_extra(extra, scanner);
    yyset_in(input, *scanner);
}

void destroy_scanner(yyscan_t scanner) {
    yylex_destroy(scanner);
}
```

parser.y
```
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
	| struct_or_union IDENTIFIER { printf("%s ", $2); } '{'  print_l_cr_bracket struct_declaration_list '}'
      print_r_cr_bracket 
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
	| enum_name ident_print '{' print_l_cr_bracket enumerator_list ',' { printf(","); } '}
    ' print_r_cr_bracket
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

```

# Тестирование

Входные данные

```
struct Coords {
  int x, y;
};

enum Color {
  COLOR_RED = -1,
  COLOR_GREEN = 2,
  COLOR_BLUE = 4,
  COLOR_HIGHLIGHT = 8, 
};

enum ScreenType {
  SCREEN_TYPE_TEXT,
  SCREEN_TYPE_GRAPHIC
} screen_type;

struct ScreenChar {
  char symbol;
  enum Color sym_color;
  enum Color back_color;
};

struct TextScreen {
  struct ScreenChar chars[HCHARS][WCHARS];
};

struct GrahpicScreen {
  enum Color pixels[HPIXELS][WPIXELS];
};

union Screen {
  struct TextScreen text;
  struct GraphicScreen graphic;
};

enum {
  BUFFER_SIZE = sizeof(union Screen),
  PAGE_SIZE = 4096,
  PAGES_FOR_BUFFER = (BUFFER_SIZE + PAGE_SIZE - 1) / PAGE_SIZE
};

struct Token {
  struct Fragment {
    struct Pos {
      int line;
      int col;
    } starting, following;
  } fragment;

  enum { Ident, IntConst, FloatConst } type;

  union {
    char *name;
    int int_value;
    double float_value;
  } info;
};

struct List {
struct Token value;struct List *next;
};
```

Вывод на `stdout`

```
struct Coords {
  int x, y;
};

enum Color {
  COLOR_RED = -1,
  COLOR_GREEN = 2,
  COLOR_BLUE = 4,
  COLOR_HIGHLIGHT = 8, 
};

enum ScreenType {
  SCREEN_TYPE_TEXT,
  SCREEN_TYPE_GRAPHIC
} screen_type;

struct ScreenChar {
  char symbol;
  enum Color sym_color;
  enum Color back_color;
};

struct TextScreen {
  struct ScreenChar chars[HCHARS][WCHARS];
};

struct GrahpicScreen {
  enum Color pixels[HPIXELS][WPIXELS];
};

union Screen {
  struct TextScreen text;
  struct GraphicScreen graphic;
};

enum {
  BUFFER_SIZE = sizeof(union Screen),
  PAGE_SIZE = 4096,
  PAGES_FOR_BUFFER = (BUFFER_SIZE + PAGE_SIZE - 1) / PAGE_SIZE
};

struct Token {
  struct Fragment {
    struct Pos {
      int line;
      int col;
    } starting, following;
  } fragment;

  enum { Ident, IntConst, FloatConst } type;

  union {
    char *name;
    int int_value;
    double float_value;
  } info;
};

struct List {
    struct Token value;
    struct List *next;
};
```

# Вывод
В ходе работы я освоил использование библиотеки Bison для построения синтаксического анализатора. 
Главным преимуществом стало то, что у меня уже был опыт работы с Flex для лексического анализа, что 
значительно упростило процесс.

Bison оказался удобным инструментом для описания грамматики: он автоматически разрешает конфликты и 
генерирует готовый парсер на основе заданных правил. Однако при выполнении лабораторной работы столкнулся
с неочевидной проблемой: при добавлении printf() в правила грамматики анализатор неожиданно ломался. 
Методом тыка мне удалось добиться работоспособности, но причину бага с printf так и не понял.

В итоге мы получаем мощный инструмент для форматирования исходного кода.