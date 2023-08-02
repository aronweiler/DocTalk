import os
import clang.cindex

class CSplitter:
    def get_chunk_text(self, cpp_code, extent):
        start = extent.start.offset
        end = extent.end.offset

        return cpp_code[start:end]

    def parse_cpp_file(self, file_path):
        # Initialize libclang
        # TODO: Do this better
        os.environ['LIBCLANG_LIBRARY_PATH'] = "C:\\Repos\\DocTalk\\doctalk_venv\\Lib\\site-packages\\clang"

        index = clang.cindex.Index.create()
        translation_unit = index.parse(file_path)

        with open(file_path, 'r') as file:
            cpp_code = file.read()

        chunk_strings = []
        for cursor in translation_unit.cursor.walk_preorder():
            print(f"Found: {cursor.kind}, {cursor.spelling} - {cursor.location.line}")
            if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL or cursor.kind == clang.cindex.CursorKind.CXX_METHOD:
                function_text = self.get_chunk_text(cpp_code, cursor.extent)
                chunk_strings.append(function_text.strip())

        return chunk_strings

# Testing
if __name__ == "__main__":
    splitter = CSplitter()
    file_path = 'C:\\Repos\\sample_docs\\Work\\Fpga Code\\Bug\\fpga.cc'
    chunks = splitter.parse_cpp_file(file_path)
    for chunk in chunks:
        print(chunk)