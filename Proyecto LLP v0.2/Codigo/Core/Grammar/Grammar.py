# -*- coding: utf-8 -*-

import re 

grammarFun = """

        ?start: exp+
        
        ?exp: "function" var "(" (var ","?)* ")" "{" argument* "}" 
            | var "("((var|number) ","?)* ")" ";"? 
            | "console" "." "log" "(" string "," exp ")" ";"   
            //| inicoment cualquieronda finalcoment  
            
            
        ?argument: var "=" (number|string|var) ";"    
            | "return" (number) ";" 
            | "return" (var) ";" 
            | "return" (string) ";"
            | "console" "." "error" "(" (var|number|string) ")" ";" 
            | "return" var operator var "(" var operator number ")" ";"   
            | "console" "." "log" "(" (number|string) ")" ";"   
            | "console" "." "log" "(" var ")" ";"   
            | "if" "(" var operation number ")" var number ";"  
            //| "if" "(" var operation number ")" var number ";"  
            | inicoment content* finalcoment 
            | inicoment content* 

        //?showfun: var "("((var|number) ","?)* ")" 
        //?ree:number
        ?string: /"[^"]*"/
            |  /̈́'[^']*'/
        
        ?operator:/\*/
                | /\+/
                | /\-/
                | /\//
        
        ?operation: /\==/
                | /\</
                | /\>/
                
       
        ?inicoment: "/*"
                | "//"

        ?finalcoment: "*/"

        ?content: /[a-z]\w*/
                | /.+/
                | /\d+(\.\d+)?/
                | /̈́'[^']*'/
                | /"[^"]*"/
                

        ?number: /\d+(\.\d+)?/

        ?var: /[a-z]\w*/

        %ignore /\s+/
        



"""


grammarBash1 =  """
    //Axioma inicial
    ?start: "#!/bin/bash" exp+
    //definicion de una expresion
    ?exp: var "=" aritmeticoperationatom ";"?
        | var "=" "$" aritmeticoperationatom ";"?
        | var "=" string ";"?
        | "echo" "\"" var "\"" ";"?
        | "echo"  var 
        | "echo" "\"" combinate "\"" ";"?
        | "echo" "\"" string+ "\"" ";"?
        | "echo" string* ";"?
        | "echo" "\"" arithmeticoperation* "\"" ";"?
 
    ?if: "if" "[[" condition "]]" ";"? "then" content "else" content "fi"
        | "if" "[[" condition "]]" ";"? "then" content "fi"
        | "if" "[[" condition "]]" ";"? "then" content "else" content "fi"
        | "if" "[[" condition "]]" ";"? "then" content elif "else" content "fi"
    
    ?logicoperation: arithmeticoperationatom "" arithmeticoperationatom
        //lesserequal
        | arithmeticoperationatom "-le" arithmeticoperationatom 
        //Greater
        | arithmeticoperationatom "-gt" arithmeticoperationatom 
        //Lesser
        | arithmeticoperationatom "-lt" arithmeticoperationatom 
          
        //Definir comparación 
    ?comparisonoperation: arithmeticoperationatom "-eq" arithmeticoperation 
        | arithmeticoperation "-eq" arithmeticoperationatom
        | arithmeticoperation "-ne" arithmeticoperationatom 
        | arithmeticoperationatom "-ne" arithmeticoperation 

    ?elif: "elif" content  
        | elif "elif" content 
    
    ?condition: conditionnum
        | conditionstr

    ?conditionnum:  arithmeticoperation

    ?conditionstr: string

    ?content: exp+

    ?combinate: string* var*
        | var* string

    ?boolean: "true" 
        |"false"

    ?exp2: if
        | "."
    //definicion de una variable
    ?var:  /[a-zA-Z]\w*/
        | "$" var
 
    //Definicion de una cadena
    ?string: /"[^"]*"/
        |  /̈́'[^']*'/
        | /[a-zA-Z][\w]+/
        | string " " string  

    //Definicion de un numero
    ?number: /\d+(\.\d+)?/
    //Definicion de operacion aritmetica
    ?arithmeticoperation: product
        //| cadenaoperation "$" cadenaoperationatom 
        | arithmeticoperation "+" product 
        | arithmeticoperation "-" product 
    //definicion de un atomo de operacion aritmetica
    ?product: arithmeticoperationatom
        | product "*" arithmeticoperationatom
        | product "/" arithmeticoperationatom   
        
    ?arithmeticoperationatom: var
        | number
        | "-" arithmeticoperationatom
        | "((" arithmeticoperation "))"
        
    ?concatenar: string 
        | concatenar "+" string 
        | concatenar "+" arithmeticoperationatom 
        | arithmeticoperationatom "+" concatenar 
    //Ignorar espacios,saltos de linea y tabulados
    %ignore /\s+/
    //Ignorar comentarios
    %ignore /\#\.+/
"""

grammarBash =  """
    //Axioma inicial
    ?start: exp+
    //definicion de una expresion
    ?exp: "echo" combination  ";"?
        | var "=" string ";"?
        | var "=" arithmeticoperation ";"?
        | "if" "[" "["? condition "]"? "]" ";"? "then" command ";"? "fi"
        | "if" "[" "["? condition "]"? "]" ";"? "then" command ";"? "else" command ";"? "fi"
        | "if" "[" "["? condition "]"? "]" ";"? "then" command ";"? ["elif" "[" "["? condition "]"? "]" ";"? "then" command ";"? ]* "else" command ";"? "fi"
        | "for" "((" ";" ";" "))" ";"? "do" exp+ ";"? "done"
        | "for" var "in" number+ ";"? "do" exp+ ";"? "done"
        | "for" var "in" stringoption+ ";"? "do" exp+ ";"? "done"
        | "for" var "in" var+ ";"? "do" exp+ ";"? "done"
        | "for" var "in" "{" arithmeticoperationatom "." "." arithmeticoperationatom "}" ";"? "do" exp+ ";"? "done"
        | "for" "((" ";" ";" "))" ";"? "do" exp+ ";"?  "done"
        | "for" "((" var "=" [number+|var] ";" var foroperation [number+|var] ";" var ["++" | "--"]"))" ";"? "do" exp+ ";"? "done"
        | "while" ":" ";"? "do" exp+ ";"? "done"
        | "while" "[" "["? condition "]"? "]" ";"? "do" exp+ actioncount? ";"? "done"
    
    ?actioncount: "((" var ["++"|"--"] "))"
        
    //Definicion de operaciones aritmeticas admitidas en el for
    ?foroperation: "<"
        | "<="
        | ">"
        | ">="

    //Definicion de opciones en forma de cadena para el bucle for
    ?stringoption: /[a-zA-Z]+/

    //Definir contenido de las sentencias
    ?command: "continue" 
        | "break" 
        | exp+

    //Definicion de combinacion de variables y cadenas
    ?combination: string
        | var string*
    

    //Definicion de operacion aritmetica
    ?arithmeticoperation: product
        | arithmeticoperation "+" product 
        | arithmeticoperation "-" product 
        | arithmeticoperation "%" product 

    //definicion de un atomo de operacion aritmetica
    ?product: arithmeticoperationatom
        | product "*" arithmeticoperationatom
        | product "/" arithmeticoperationatom   
        
    //Definir atomo aritmetico
    ?arithmeticoperationatom: var
        | number
        | "-" arithmeticoperationatom
        | "$((" arithmeticoperation "))"

    //Definir operacion logica
    ?logicoperation: arithmeticoperationatom "-ge" arithmeticoperationatom
        //lesserequal
        | arithmeticoperationatom "-le" arithmeticoperationatom 
        //Greater
        | arithmeticoperationatom "-gt" arithmeticoperationatom 
        //Lesser
        | arithmeticoperationatom "-lt" arithmeticoperationatom 
          
    //Definir comparación igual y distinta
    ?comparisonoperation: arithmeticoperationatom "-eq" arithmeticoperation 
        | arithmeticoperation "-eq" arithmeticoperationatom
        | arithmeticoperation "-ne" arithmeticoperationatom 
        | arithmeticoperationatom "-ne" arithmeticoperation 

    //Definicion de operaciones con cadenas
    ?stringoperation: "-n" [string | var]
        | "-z" [string | var]
        | [string | var] "=" [string | var]
        | [string | var] "==" [string | var]
        | [string | var] "!=" [string | var]
        | [string | var] "\<" [string | var]
        | [string | var] "\>" [string | var]

    //Definicion de condiciones para la sentencia if
    ?condition: logicoperation
        | comparisonoperation
        | stringoperation
        | arithmeticoperation

    //Definicion de una variable
    ?var:  /[a-zA-Z]\w*/
        | "$" var
 
    //Definicion de una cadena
    ?string: /[\"].+[\"]/
        | /[\'].+[\']/

    //Definicion de un numero
    ?number: /\d+(\.\d+)?/

    //Ignorar comentarios
    %ignore /[\#].+/
    %ignore /\s+/

"""
       