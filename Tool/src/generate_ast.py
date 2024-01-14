from io import TextIOWrapper
from typing import Callable
import sys

astExpressionTypes = [
    "Binary : Expr left, Token operator, Expr right",
    "Grouping : Expr expression",
    "Literal : Object value",
    "Unary : Token operator, Expr right",
  ]

astStatementTypes = [
    "Expression : Expr expression",
    "Print : Expr expression",
]

def main():
  if len(sys.argv) != 2:
    print("Usage: python generate_ast <output_directory")
    sys.exit(64)
  
  outputDir = sys.argv[1]
  print(f"outputDir: {outputDir}")
  # defineAst(outputDir=outputDir, baseName="Expr", types=astExpressionTypes)
  defineAst(outputDir=outputDir, baseName="Stmt", types=astStatementTypes)

def createWriter(file: TextIOWrapper):
  def w(contents: str|None = ""):
    file.write(contents + "\n")
  return w

def defineAst(outputDir: str, baseName: str, types: list[str]):
  path = f"{outputDir}/{baseName}.java"
  with open(path, 'a') as file:
    writeln = createWriter(file)
    writeln("import java.util.List;")
    writeln(f"abstract class {baseName} {{")
    defineVisitor(writeln=writeln, baseName=baseName, types=types)

    # The AST classes
    for typ in types:
      className = typ.split(":")[0].strip()
      fields = typ.split(":")[1].strip()
      defineType(writeln=writeln, baseName=baseName, className=className, fieldList=fields)

    # The base accept() method.
    writeln("")
    writeln("  abstract<R> R accept(Visitor<R> visitor);")
    writeln("}")
    file.close()

def defineType(writeln: Callable[[str], None], baseName: str, className: str, fieldList: str):
  writeln(f"  static class {className} extends {baseName} {{")

  # Store parameters in fields
  fields = fieldList.split(", ")

  # Fields.
  for field in fields:
    writeln(f"  final {field};")

  # Constructor
  writeln(f"    {className} ({fieldList}) {{")

  for field in fields:
    name = field.split(" ")[1]
    writeln(f"    this.{name} = {name};")
  writeln("    }")

  # Visitor pattern
  writeln("  @Override")
  writeln("  <R> R accept(Visitor<R> visitor) {")
  writeln(f"    return visitor.visit{className}{baseName}(this);")
  writeln("  }")
  
  writeln("  }")

def defineVisitor(writeln: Callable[[str], None], baseName: str, types: list[str]):
  writeln("  interface Visitor<R> {")
  for typ in types:
    typeName = typ.split(":")[0].strip()
    writeln(f"    R visit{typeName}{baseName}({typeName} {baseName.lower()});")
  writeln("  }")

if __name__ == "__main__":
  main()