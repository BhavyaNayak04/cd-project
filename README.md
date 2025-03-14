# cd-project
To design a Compiler for the following hypothetical language:

```plaintext
X: integer ;

Procedure foo( b : integer ) 
b := 13; 
If x = 12 and b = 13 then 
    printf( "by copy-in copy-out" ); 
elseif x = 13 and b = 13 then 
    printf( "by address" ); 
else 
    printf( "A mystery" ); 
end if; 
end foo
