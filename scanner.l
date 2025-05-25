%{

#include "stdio.h"
#include "string.h"

int line_number = 1;
const char *keywords[]={
    "if",
    "else",
    "while",
    "return",
    "int",
    "float",
    "void",
    NULL
};

#define NUM_KEYWORDS (sizeof(keywords)/sizeof(keywords[0]))

int is_keyword(const char *lexeme){
    for(int i = 0; i < NUM_KEYWORDS - 1; i++){
        if(strcmp(lexeme, keywords[i]) == 0){
            return 1;
        }
    }
    return 0;
}


void print_table_header(){
    printf("----------------------------------- \n");
    printf("  line No.  | Lexeme    | Token Type\n");
    printf("----------------------------------- \n");
}

void print_table_row(int line,const char * lexeme,const char *token){
    printf("%-8d|%-13s|%-12s\n",line,lexeme,token);
}

%}

%option noyywrap

%%

[0-9]+(\.[0-9]+)? { print_table_row(line_number, yytext, "NUMBER"); }
\"([^'\\]|\\.)*\" { print_table_row(line_number, yytext, "STRING"); }
[a-zA-Z_][a-zA-Z0-9_]* {
    if(is_keyword(yytext)){
        print_table_row(line_number,yytext,"KEYWORD");
    }
    else{
        print_table_row(line_number,yytext,"IDENTIFIER");
    }
}
\n { line_number++; }
[(){};,] { print_table_row(line_number, yytext, "SPECIAL CHARACTER"); }
[+\-*/=<>!]+ { print_table_row(line_number, yytext, "OPERATOR"); }
[ \t]+ { /* ignore whitespace */ }
. { print_table_row(line_number, yytext, "UNKNOWN"); }


%%


int main(int argc,char *argv[]){
    print_table_header();
    if(argc>1){
        yyin=fopen(argv[1],"r");
    }
    yylex();
     printf("----------------------------------- \n");
    return 0;
}