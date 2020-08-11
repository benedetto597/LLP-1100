 /*
    Color Rules
    @author Edgar Benedetto
    @date 2020/07/30
    @version 0.1
*/

%Hechos
color(rojo).
color(azul).
color(verde).
color(amarillo).
color('Cian semisaturado').

%En la consola solo se debe poner color(X). y se mostraran todos los valores de X

%Regla
colorPrimario(X) :- X == rojo ; X == verde; X == azul.
%En la consola colorPrimario('Cian semisaturado'). o colorPrimario(rojo).

%Regla para poder pasar a X como incognita
colorPrimario(rojo).
colorPrimario(azul).
colorPrimario(verde).
%En la consola colorPrimario(X).



