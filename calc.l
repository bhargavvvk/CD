%{

#include <stdio.h>
#include "y.tab.h"

%}


%%
[1-9][0-9]* {
  /* 
    Found an integer
    Its value will be stored in yylval (we will see this in parser too)
 */
  yylval = atoi(yytext);
  return NUM;
}

[()-+*/^] {
  /* Found an operator */
  return *yytext;
}

[ \t] {/* ignore whitespace */}

