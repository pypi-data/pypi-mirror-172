import ast

from ezflake import create_violation, Plugin, Visitor


UNF001 = create_violation('UNF001', "Do not raise 'NotImplementedError'")


class UnfinishedVisitor(Visitor):
    def visit_Raise(self, node: ast.Raise):
        if isinstance(node.exc, ast.Name):
            name = node.exc.id
        elif isinstance(node.exc, ast.Call):
            if isinstance(node.exc.func, ast.Name):
                name = node.exc.func.id
            else:
                name = None
        else:
            raise ValueError
        if name == 'NotImplementedError':
            self.violate(UNF001, node)
        self.generic_visit(node)


class UnfinishedPlugin(Plugin):
    name = __name__
    visitors = [UnfinishedVisitor]
