%{
#include "y.tab.h"
%}

%%
[0-9]+    return NUMBER;
[a-zA-Z]  return LETTER;
\n        return '\n';
.         return 0;  // Invalid character
%%