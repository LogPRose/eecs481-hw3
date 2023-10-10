# This "Starter Code" for EECS 481 HW3 shows how to use a visitor
# pattern to replace nodes in an abstract syntax tree. 
# 
# Note well:
# (1) It does not show you how to read input from a file. 
# (2) It does not show you how to write your resulting source
#       code to a file.
# (3) It does not show you how to "count up" how many of 
#       instances of various node types exist.
# (4) It does not show you how to use random numbers. 
# (5) It does not show you how to only apply a transformation
#       "once" or "some of the time" based on a condition.
# (6) It does not show you how to copy the AST so that each
#       mutant starts from scratch. 
# (7) It does show you how to execute modified code, which is
#       not relevant for this assignment.
#
# ... and so on. It's starter code, not finished code. :-) 
# 
# But it does highlight how to "check" if a node has a particular type, 
# and how to "change" a node to be different. 

from _ast import BinOp
import ast
from typing import Any
import astor
import sys
import random

class MyVisitor(ast.NodeTransformer):
    """Notes all Numbers and all Strings. Replaces all numbers with 481 and
    strings with 'SE'."""

    # Note how we never say "if node.type == Number" or anything like that.
    # The Visitor Pattern hides that information from us. Instead, we use
    # these visit_Num() functions and the like, which are called
    # automatically for us by the library. 
    def visit_Num(self, node, generatedNum, num_mutants):
        print("Visitor sees a number: ", ast.dump(node), " aka ", astor.to_source(node))
        # Note how we never say "node.contents = 481" or anything like
        # that. We do not directly assign to nodes. Intead, the Visitor
        # Pattern hides that information from us. We use the return value
        # of this function and the new node we return is put in place by
        # the library. 
        # Note: some students may want: return ast.Num(n=481)
        if (generatedNum % 2 == 1):
            return node
        return ast.Num(value=481, kind=None)

    def visit_Str(self, node, generatedNum, num_mutants):
        print("Visitor sees a string: ", ast.dump(node), " aka ", astor.to_source(node))
        # Note: some students may want: return ast.Str(s=481)
        if (generatedNum % 2 == 2):
            return node
        return ast.Str(value="SE", kind=None)
    def visit_Compare(self, node, generatedNum, num_mutants):
        if (generatedNum % 4 == 3):
            return node
        return ast.Compare(left=node.left, ops=[ast.Lt()],comparators=[node.comparators[0]], kind=None)
    def visit_BinOp(self, node, generatedNum, num_mutants):
        if (generatedNum % 5 == 0):
            return node
        if (type(node.op) == ast.Add):
            new_op = ast.Sub()
        elif (type(node.op) == ast.Sub):
            new_op = ast.Add()
        elif (type(node.op) == ast.Mult):
            new_op = ast.Div()
        else:
            new_op = ast.Mult()
        return ast.BinOp(left=node.left, op=new_op, right=node.right, kind=None)
    def visit_Assign(self, node, generatedNum):
        if (generatedNum % 6 == 0):
            return node
        return ""
# Instead of reading from a file, the starter code always processes in 
# a small Python expression literally written in this string below:
args = sys.argv
print("args", args)
code = ""
random.seed(0)
with open (f"{args[1]}", "r") as source:
    code = source.read() 

# As a sanity check, we'll make sure we're reading the code
# correctly before we do any processing. 
print("Before any AST transformation")
print("Code is: ", code)
print("Code's output is:") 
exec(code)      # not needed for HW3
print()
num_mutatnts = int(args[2])


for i in range(num_mutatnts):
    print(i)


# Now we will apply our transformation. 
print("Applying AST transformation")
tree = ast.parse(code)
tree = MyVisitor().visit(tree, random.random(0, 100))
# Add lineno & col_offset to the nodes we created
ast.fix_missing_locations(tree)
print("Transformed code is: ", astor.to_source(tree))
co = compile(tree, "", "exec")
print("Transformed code's output is:") 
exec(co)        # not needed for HW3