import os

from tree_sitter import Language, Parser
import tree_sitter_go

from brief_generator import generate_func_brief

GO_LANGUAGE = Language(tree_sitter_go.language())

parser = Parser()
parser.language = GO_LANGUAGE

root_dir = "/home/rynko/Projects/ndnd2"

def main():
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".go"):
                path = os.path.join(dirpath, filename)
                with open(path, "rb") as f:
                    code = f.read()
                with open(path, "r") as f:
                    contents = f.readlines()
                
                process_file(code, path, contents)

                with open(path, "w") as f:
                    f.writelines(contents)


def process_file(code: bytes, path: str, contents: list):
    tree = parser.parse(code)
    cursor = tree.walk()
    offset = 0

    def get_node_text(node):
        name_node = node.child_by_field_name('name')
        if name_node:
            name = code[name_node.start_byte:name_node.end_byte].decode()
            return name
        else:
            return None

    def get_class(node):
        try:
            receiver_node = node.child_by_field_name("receiver")
            if not receiver_node:
               return None

            param_list = receiver_node.child(1)
            if not param_list:
                return None

            type_node = param_list.child(1)
            if type_node is None:
                return None

            # Handle pointer receiver
            if type_node.type == "pointer_type":
                type_node = type_node.child(1)

            if type_node is None:
                return None

            return code[type_node.start_byte:type_node.end_byte].decode()
        except:
            return None

    def process_function(node):
        nonlocal offset
        func_code = code[node.start_byte:node.end_byte].decode()

        brief = generate_func_brief(func_code) + '\n'
        brief = "(AI GENERATED DESCRIPTION): " + brief

        # insert the generated brief into the file
        contents.insert(node.start_point.row + offset, "// " + brief)

        offset += 1

    # def process_class(node):
    #     nonlocal offset
    #     class_code = code[node.start_byte:node.end_byte].decode()

    #     brief = generate_class_brief(class_code) + '\n'

    #     # insert the generated brief into the file
    #     contents.insert(node.start_point.row + offset, brief)

    #     offset += 1

    def visit(cursor):
        while True:
            node = cursor.node
            print(node.type)
            if node.type == 'function_declaration' or node.type == 'method_declaration':
                process_function(node)

#             if node.type == 

            if cursor.goto_first_child():
                visit(cursor)
                
                cursor.goto_parent()
            
            if not cursor.goto_next_sibling():
                break

    return visit(cursor)


def set_root_dir(dir_path):
    root_dir = dir_path

if __name__ == "__main__":
    main()
