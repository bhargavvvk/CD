%{

#include <stdio.h>
int countv=0;
int countc=0;


%}

%%
[aeiouAEIOU] {countv++;}
[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ] {countc++;}

%%

int main(){
    printf("enter the string\n");
    yylex();
    printf("number of vowels: %d\n",countv);
    printf("number of consonants: %d\n",countc);
    return 1;
}

int yywrap(){
    return 1;
}