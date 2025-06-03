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

