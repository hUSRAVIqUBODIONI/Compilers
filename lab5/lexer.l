%{
#include <iostream>
using namespace std;

void process_token(const char* token, int line, int start, int finish);

int temp = 0;
int yycolumn = 1;
%}

%option yylineno
%option noyywrap

DIGIT    [0-9]
LETTER   [a-zA-Z]
START_COMM \(\*
END_COMM   \*\)
WHITE_SPACE [\t\n]+
ID       {LETTER}({LETTER}|{DIGIT})*
COMMENT  {START_COMM}(.*|{WHITE_SPACE})*{END_COMM}
NUMBER   {DIGIT}+

%%

{NUMBER}   {
    temp = yycolumn + yyleng;
    process_token("NUMBER", yylineno, yycolumn, temp);
    yycolumn = temp;
}
{ID}       {
    temp = yycolumn + yyleng;
    process_token("IDENTIFIER", yylineno, yycolumn, temp);
    yycolumn = temp;
}
{COMMENT}  {
    int start = yycolumn;  
    char* text = yytext;   
    int finish = start;          
    while (*text) {
        if (*text == '\n') {    
            yycolumn = 1;      
            finish = 1;        
        } else {
            yycolumn++;        
            finish++;          
        }
        text++;                
    }

    process_token("COMMENT", yylineno, start, finish);
}
[ \t]+    {
    yycolumn += yyleng; 
}
\n        {
   
    yycolumn = 1; 
}
.         {
    temp = yycolumn + yyleng;
    process_token("UNKNOWN", yylineno, yycolumn, temp);
    cout << "Line: " << yylineno << ", Column: " << yycolumn << ", Value: " << yytext << endl;
    yycolumn = temp;
}

%%

void process_token(const char* token, int line, int start, int finish) {
    cout << "Found token: " << token << " (" << yytext << ")"
         << " at line " << line << ", columns " << start << "-" << finish << endl;
}

int main(int argc, char** argv) {
    if (argc > 1) {
        FILE* file = fopen(argv[1], "r");
        if (!file) {
            cerr << "Error opening file: " << argv[1] << endl;
            return 1;
        }
        yyin = file;
    }

    yycolumn = 1; 

    yylex();

    if (argc > 1) {
        fclose(yyin);
    }

    return 0;
}