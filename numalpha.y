%token NUMBER LETTER

%%
input : sequence '\n' { printf("Valid\n"); return 0; }
      ;

sequence : NUMBER NUMBER
         | NUMBER LETTER
         ;
%%