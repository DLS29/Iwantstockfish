# Fishscrript
file that contains docs for script called fishscript  
  
## doc
### defalt behaviour
with empty row and if difficulty or and depth not specified bot will play on stockfish level depth 15  by defalt  
difficulty and depth can be change  
  
### fishscript trivi    
every move stockfish runs script that you wrote in script entry  
every script must return move  
every new instruction must be seperated by ;  
values that have a limited automaticly will be rounded to maximum or minimum of possible  

# Flags:  
players ; flag that used to access variables from player side  
stockfishs ; flag that used to access variables from stockfish side  
whites ; flag that used to access variables from white side  
blacks ; flag that used to access variables from black side  
board ; flag that used to access variables from board side  

# Variables:  
n ; contains number of current move starts from 0 n does not support flags
diffc ; current difficulty 1 is min 3000 is max  
depth ; current depth 1 is min 20 is max  
mov ; list of all accesable moves ranked from best to worst access them write mov[] supports possitive and negative numbers 
evalt ; returns evaluation of current board position from stockfish  
movev ; returns evaluation of current move
movrank ; returns rank of current move by stockfish  

# Instructions:  
if ; executes instructions in {} if instruction in () is equals to true  
else ; executes instructions in {} if  if fails  
return ; returns move to make from list of moves and stops execution of script for a move  
random ; returns integer from a to b
function ; creates funcion with arguments


# Operators:
+,-,*,/ ; are supported  
= ; sets variable to value after it  
== ; works with if value a equals to value b  
!= ; not equals  
<,>,<=,>= ; are supported too  
&,|,^,!,!&,!|,!^ ; and,or,xor,not,nand,nor,xnor are supported

# Examples:  
defines: (
    define player p
    define stockfish s
    define movrank ifmov
)
functions: (
    function set_elo(depth_2,diffc_2){
        depth = depth_2,diffc = diffc_2
    };
);
script: (
    if(p.evalt < -5){set_elo(10,diffc =  - (n + s.evalt) * 5)};

    if(p.evalt < 0){set_elo(15,diffc  - n * 5)};

    if(p.evalt < 5){set_elo(20,3000)}

    if(p.ifmov == 0){return(s.mov[-1])};

    else{return(s.mov[0])}
    );  
# Explanation:  
firstly if possition for player is weak we change depth and we change difficulty by subtracting
we check if players last move was the best by checking if move rank was 0  
then if it's true stockfish makes the worst possible move if not play the best move
; at the end and space between different instructions not required but recommended for consistency reason and readability