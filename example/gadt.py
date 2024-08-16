# type _ value =
#   | Int : int -> int value
#   | Bool : bool -> bool value
#
# type _ expr =
#   | Value : 'a value -> 'a expr
#   | Eq : int expr * int expr -> bool expr
#   | Plus : int expr * int expr -> int expr
#   | If : bool expr * 'a expr * 'a expr -> 'a expr

