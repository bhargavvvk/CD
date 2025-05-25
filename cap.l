%{

#include <stdio.h>
#include <ctype.h>
int first_char=1;

%}


%%

^[a-zA-Z] { printf("%c",toupper(yytext[0])); first_char=0;}
[a-zA-Z]  { printf("%c",tolower(yytext[0]));}
.   { printf("%s",yytext);}
%%


int main(){
    printf("Enter the Input: ");
    yylex();
    return 0;
}

int yywrap(){
    return 1;
}