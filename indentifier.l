%%

if|else|return|int|main {printf("%s is the keyword\n",yytext);}

[a-zA-Z][a-zA-Z_0-9]* {printf("%s is a identifier\n",yytext);}

.   {printf("%s is invalid\n",yytext);}

%%

int main(){
    printf("enter the string");
    yylex();
    return 1;
}

int yywrap(){
    return 1;
}
