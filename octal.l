%{


#include <stdio.h>

%}

digit [0-7]
octal {digit}+

hexp 0[xX]

hexs [A-Fa-f0-9]

hex {hexp}{hexs}+

%%

{octal} {printf("it is octal %s\n",yytext);}
{hex}   {printf("it is hexdecimal %s\n",yytext);}
.   {printf("it is invalid %s\n",yytext);}


%%


int main(){
    printf("enter the number :");
    yylex();
    return 1;
}

int yywrap(){
    return 1;
}