class TextEditor:
    def __init__(self):
        self.text_buffer = []      
        self.undo_stack = []
        self.redo_stack = []

    def write(self, text):
        self.undo_stack.append(self.text_buffer.copy())
        self.redo_stack.clear()

        words = text.split()
        self.text_buffer.extend(words)
        print(f"Written: '{text}'")

    def undo(self):
        if not self.undo_stack:
            print("Nothing to undo.")
            return

        self.redo_stack.append(self.text_buffer.copy())
        self.text_buffer = self.undo_stack.pop()
        print("Undid last action.")

    def redo(self):
        if not self.redo_stack:
            print("Nothing to redo.")
            return

        self.undo_stack.append(self.text_buffer.copy())
        self.text_buffer = self.redo_stack.pop()
        print("Redid last action.")

    def display(self):
        print("Current Text:", " ".join(self.text_buffer))

def main():
    editor = TextEditor()
    print("Welcome to Simple CLI Text Editor!")
    print("Commands: write <text>, undo, redo, show, exit")

    while True:
        try:
            command_input = input(">> ").strip()
            if not command_input:
                continue

            parts = command_input.split(" ", 1)
            command = parts[0].lower()

            if command == "exit":
                print("Exiting Editor.")
                break
            
            elif command == "write":
                if len(parts) < 2:
                    print("Usage: write <text>")
                else:
                    editor.write(parts[1])
            
            elif command == "undo":
                editor.undo()
            
            elif command == "redo":
                editor.redo()
            
            elif command == "show":
                editor.display()
            
            else:
                print("Unknown command. Available: write, undo, redo, show, exit")

        except KeyboardInterrupt:
            print("\nExiting Editor.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()