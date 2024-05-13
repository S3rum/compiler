Compiler in Python for C like code

Grammar:

startRule
: def_main_part
;

def_main_part
: ( def_main_function )+
;

def_main_function
: ’#def’ 'main'
  declarations
  ( def_function )*
  statements
;

def_function
: ’def’ ID ’(’ id_list ’)’ ’:’
  ’#{’
  declarations
  ( def_function )*
  statements
  ’#}’
;

declarations
: ( ’#int’ id_list )*
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
( expression ’;’
| ’int’ ’(’ ’input’ ’(’ ’)’ ’)’ ’;’
)
;

print_stat
: ’print’ ’(’ expression ’)’
;

return_stat
: ’return’ ’(’ expression ’)’ ’;’
;

if_stat
: ’if’ ’(’ condition ’)’ ’:’
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
: ’while’ ’(’ condition ’)’ ’:’
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
( ADD_OP term )*
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
| condition
| expression REL_OP expression



