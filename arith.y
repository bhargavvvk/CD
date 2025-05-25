%{
#include <stdio.h>
#include <stdlib.h>

void yyerror(char *msg);
int yylex();
%}

%token NUMBER
%left '+' '-'
%left '*' '/' '%'

%%

input: expr '\n' { printf("Valid expression\n"); return 0; }
  ;

expr:
    expr '+' expr
  | expr '-' expr
  | expr '*' expr
  | expr '/' expr
  | expr '%' expr
  | '(' expr ')'
  | NUMBER
  ;

%%

void yyerror(char *msg) {
    printf("error\n");
}

int main() {
    printf("enter the expression: ");
    yyparse();
    return 0;
}
