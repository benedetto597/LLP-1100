#!/bin/bash

#initialize factorial
factorial=1
 
#for loop
for ((i=1;i<=num;i++))
do
    factorial=$(($factorial*$i))
done
 
echo "Factorial of $num is $factorial"