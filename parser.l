%{

#include "parser.tab.h"

%}

%%

a   { return A;}
b   { return B;}
\n  { return '\n'; }
.  { return 0; }

%%


int yywrap(){
    return 1;
}