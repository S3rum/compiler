startRule
: def_main_part
;

def_main_part
: ( def_main_function )+
;

def_main_function
: ’#def’ 'main'
  declarations
  ( def_function )*  #TODO
  statements
;

def_function
: ’def’ ID ’(’ id_list ’)’ ’:’
  ’#{’
  declarations
  ( def_function )*     #TODO
  statements
  ’#}’
;

declarations
: ( declaration_line )*
;

declaration_line
: ’#int’ id_list
;

statement
: simple_statement
| structured_statement
;

statements
: statement+
;

simple_statement
: assignment_stat
| print_stat
| return_stat
;

structured_statement
: if_stat
| while_stat
;

assignment_stat
: ID ’=’
( expression ’;’        #TODO
| ’int’ ’(’ ’input’ ’(’ ’)’ ’)’ ’;’
)
;

print_stat
: ’print’ ’(’ expression ’)’ #TODO
;

return_stat
: ’return’ ’(’ expression ’)’ ’;’ #TODO
;

if_stat
: ’if’ ’(’ condition ’)’ ’:’  #TODO
( statement
| ’#{’ statements ’#}’
)
( ’else’ ’:’
( statement
| ’#{’ statements ’#}’
)
)?
;

while_stat
: ’while’ ’(’ condition ’)’ ’:’  #TODO
( statement
| ’#{’ statements ’#}’
)
;

id_list
: ID ( ’,’ ID )*
|
;

expression
: optional_sign term
( ADD_OP term )*    #TODO
;

term
: factor
( MUL_OP factor )*
;

factor
: INTEGER
| ’(’ expression ’)’
| ID idtail
;

idtail
: ’(’ actual_par_list ’)’
|
;

actual_par_list
: expression ( ’,’ expression )*
|
;

optional_sign
: ADD_OP
|
;

condition
: bool_term ( ’or’ bool_term )*
;

bool_term
: bool_factor ( ’and’ bool_factor )*
;

bool_factor
: ’not’ condition
| condition                        #TODO
| expression REL_OP expression



