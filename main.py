import argparse
import json
import os

class NoteManager:
    def __init__(self, filename="notable_notes.json"):
        self.filename = filename

    def _read_data(self):
        if not os.path.exists(self.filename): return []
        with open(self.filename, "r") as f:
            try: return json.load(f)
            except json.JSONDecodeError: return []

    def _write_data(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def add(self, title, content):
        notes = self._read_data()
        new_id = max([n["id"] for n in notes], default=0) + 1
        notes.append({"id": new_id, "title": title, "content": content})
        self._write_data(notes)

    def read(self):
        return self._read_data()

    def find_by_title(self, title):
        return [n for n in self._read_data() if n["title"].lower() == title.lower()]

    def delete(self, note_id):
        notes = [n for n in self._read_data() if n["id"] != note_id]
        self._write_data(notes)

    def edit(self, note_id, new_content):
        notes = self._read_data()
        for n in notes:
            if n["id"] == note_id:
                n["content"] = new_content
        self._write_data(notes)

def main():
    parser = argparse.ArgumentParser(prog="notable")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # read
    subparsers.add_parser("read")
    # add "title" "desc"
    add = subparsers.add_parser("add")
    add.add_argument("title"); add.add_argument("desc")
    # del "title"
    dele = subparsers.add_parser("del")
    dele.add_argument("title")
    # edit "title" "new_desc"
    edit = subparsers.add_parser("edit")
    edit.add_argument("title"); edit.add_argument("desc")

    args = parser.parse_args()
    mgr = NoteManager()

    if args.command == "read":
        for n in mgr.read(): print(f"[{n['id']}] {n['title']}: {n['content']}")

    elif args.command == "add":
        mgr.add(args.title, args.desc)
        print(f"Added: {args.title}")

    elif args.command == "del":
        matches = mgr.find_by_title(args.title)
        if not matches: print("Not found."); return
        idx = 0 if len(matches) == 1 else int(input(f"Pick item (1-{len(matches)}): ")) - 1
        mgr.delete(matches[idx]["id"])
        print("Deleted.")

    elif args.command == "edit":
        matches = mgr.find_by_title(args.title)
        if not matches: print("Not found."); return
        idx = 0 if len(matches) == 1 else int(input(f"Pick item (1-{len(matches)}): ")) - 1
        mgr.edit(matches[idx]["id"], args.desc)
        print("Updated.")

if __name__ == "__main__":
    main()
