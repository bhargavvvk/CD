%{
#include "arith.tab.h"
#include <stdlib.h>
%}

%%

[0-9]+        { yylval = atoi(yytext); return NUMBER; }
[+\-*/()%]    { return yytext[0]; }
[ \t]+        ;             // Skip only space and tabs
\n            { return '\n'; }  // Return newline as token
.             { printf("Invalid character: %s\n", yytext); }

%%

int yywrap() {
    return 1;
}

