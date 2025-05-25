%{

#include <stdio.h>
#include <stdlib.h>

int yylex();

void yyerror(char *msg);


%}

%token A B

%%

start: S '\n'   { printf("Accepted"); return 0;}
S    : A S B
     | ;
     
%%

void yyerror(char *msg){
    printf("Rejected\n");
    exit(1);
}

int main(){
    printf("enter the string");
    yyparse();
}