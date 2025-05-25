%{

#include <stdio.h>
#include "math.h"

extern int yylex();
extern int yyparse();
extern void yyerror(const char *s);

extern FILE* yyin;

%}

%token NUM

%start USER_INPUT
%left '+' '-'
%left '*' '/'
%left '^'


%%

EXPR : EXPR '+' EXPR { $$ = $1 + $3; }
     | EXPR '-' EXPR { $$ = $1 - $3; }
     | EXPR '*' EXPR { $$ = $1 * $3; }
     | EXPR '/' EXPR { $$ = $1 / $3; }
     | EXPR '^' EXPR { $$ = (int)pow($1, $3); }
     | '(' EXPR ')' { $$ = $2; }
     | NUM { $$ = $1; }
     ;

USER_INPUT : EXPR { printf("%d\n", $1); }
           ;
%%

int main()
{
    yyin = fopen("input.txt", "r");

    if (!yyin) {
        printf("File not found\n");
        return 1;
    }
    yyparse();
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "%s\n", s);
}

int yywrap() {
  return 1;
}

/*
Command:
lex calc.l
yacc -d calc.y
gcc lex.yy.c y.tab.c -o calc -lm
./calc
 */ 