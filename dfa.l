%{

#include <stdio.h>
#include <string.h>
int step=1;


const char *keywords[]={
    "if",
    "else",
    "while",
    "return",
    "int",
    "float",
    "void",
};

#define NUM sizeof(keywords)/sizeof(keywords[0])
int is_keyword(const char *lexeme){
    for(int i=0;i<NUM-1;i++){
        if(strcmp(lexeme,keywords[i])==0){
            return 1;
        }
    }
    return 0;
}


void print_transition(const char* char_read,const char *current_state,const char *action){
    printf(" %2d | %5s | %15s | %35s\n",step++,char_read, current_state, action);
}

%}

%option noyywrap

%%

[ \t\n]+ { }
[0-9]+(\.[0-9]+)? {
    int i;
    char state[20]="q0-->q1";
    char char_read[2];
    for(int i=0;i<yyleng;i++){
        sprintf(char_read,"%c",yytext[i]);
        print_transition(char_read,state,(i==0) ? "Start Number" : "continue Number");
        strcpy(state,"q1");
    }
    print_transition("(end)","q1-->NUM","Number");
}

[a-zA-Z_][a-zA-Z0-9_]* {
    int i;
    char state[20]="q0-->q2";
    char char_read[2];
    for(int i=0;i<yyleng;i++){
        sprintf(char_read,"%c",yytext[i]);
        print_transition(char_read,state,(i==0) ? "Start Identifier" : "Conitnue Identifyer");
        strcpy(state,"q2");
    }
    if(is_keyword(yytext)){
        print_transition("(end)","q2-->KW","KEYWORD");
    }
    else{
        print_transition("(end)","q2-->ID","Identifier");
    }
}

[+\-*/=<>!]+ {
    print_transition(yytext,"q0-->q3"," Recognize Operator");
    print_transition("(end)","q3-->OP","Operator");
}

. { }

%%

int main(){
    printf("Step | char read | current state | action\n");
    printf("-----|-----------|----------------|-------------------------------\n"); 
    yylex();
    return 0;
}