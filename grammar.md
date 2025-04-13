ProgramStart       → Program

Program            → Declarations Procedure

Declarations       → Identifier : Type ;

Type               → integer

Procedure          → procedure Identifier ( Parameter ) StatementBlock end Identifier

Parameter          → Identifier : Type

StatementBlock     → Statement
                   | StatementBlock Statement

Statement          → Assignment ;
                   | IfStatement ;
                   | PrintStatement ;

Assignment         → Identifier := Number

IfStatement        → if Condition then StatementBlock  
                   | elsif Condition then StatementBlock  
                   | else StatementBlock  
                   | end if

Condition          → Comparison and Comparison

Comparison         → Identifier = Number

PrintStatement     → printf ( String )
