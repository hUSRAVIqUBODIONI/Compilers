# main.py
from lexer import Lexer
from parser import Parser
from ast import print_ast

def main():
    # Пример входного файла
    input_text = """
    %class SimpleImperativeLang

    %tokens NUMBER . PLUS MINUS STAR FRAC LBRAC RBRAC
    TRUE FALSE AND OR NOT LT GT LE GE NE EQ
    IF THEN ELSE END WHILE DO SEMICOLON
    VAR ASSIGN INPUT PRINT COMMA

    %types
      Expr, Term, Factor, NUMBER: ArithmExpr;
      PLUS, MINUS, STAR, FRAC: ArithmOp;
      BoolExpr, BoolTerm, BoolFactor, TRUE, FALSE: BoolExpr;
      LT, GT, LE, GE, NE, EQ: RelaOp;
      Program, Statement, StatementList, Program: Statement;
      VAR, STRING: String;
      PrintItem: PrintItem;

    %methods
      ArithmExpr neg_op(ArithmOp, ArithmExpr)
      ArithmExprChunk chunk(ArithmOp, ArithmExpr);
      ArithmExpr neg_op(ArithmOp, ArithmExpr);
      ArithmExprChunk chunk(ArithmOp, ArithmExpr);
      ArithmExpr bin_op(ArithmExpr, ArithmExprChunk[]);
      ArithmExpr deref(String);

      BoolExpr rela_op(ArithmExpr, RelaOp, ArithmExpr);
      BoolExpr disj_op(BoolExpr, BoolExpr[]);
      BoolExpr conj_op(BoolExpr, BoolExpr[]);
      BoolExpr not_op(BoolExpr);

      Statement assign_stmt(String, ArithmExpr);
      Statement append(Statement, Statement);
      Statement compound(Statement, Statement[]);
      Statement if_else_stmt(BoolExpr, Statement, Statement);
      Statement empty_stmt();
      Statement while_stmt(BoolExpr, Statement);
      Statement input_stmt(String, String[]);

      PrintItem print_value(ArithmExpr);
      PrintItem print_string(String);
      Statement print_stmt(PrintItem, PrintItem[]);

      %grammar
      Program = StatementList;

      StatementList = Statement %rep (SEMICOLON Statement) / compound;

      Statement =
          VAR ASSIGN Expr / assign_stmt
          $ Ветка else может отсутствовать
        | IF BoolExpr THEN StatementList (/ empty_stmt | ELSE StatementList) END
          / if_else_stmt
        | WHILE BoolExpr DO StatementList END / while_stmt
        | INPUT VAR %rep (COMMA VAR) / input_stmt
        | PRINT PrintItem (COMMA PrintItem) / print_stmt
        ;

      PrintItem = Expr / print_value | STRING / print_string;

      BoolExpr = BoolTerm %rep (OR BoolTerm) / disj_op;
      BoolTerm = BoolFactor %rep (AND BoolFactor) / conj_op;
      BoolFactor =
          TRUE | FALSE
        | Expr RelaOp Expr / rela_op
        | NOT BoolFactor / not_op
        | LBRAC BoolExpr RBRAC
        ;

      $ Первому терму в выражении может предшествовать знак минус
      Expr = (Term | MINUS Term / neg_op) %rep ((PLUS | MINUS) Term / chunk)
          / bin_op;
      Term = Factor %rep ((STAR | FRAC) Factor / chunk) / bin_op;
      Factor = NUMBER | VAR / deref | LBRAC Expr RBRAC;

      %axiom
      Program

      %end
      """

    # Токенизация
    lexer = Lexer(input_text)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()
    
    print_ast(ast)
    print("\n")
    for i in parser.errors:
        print(i,)


if __name__ == "__main__":
    main()