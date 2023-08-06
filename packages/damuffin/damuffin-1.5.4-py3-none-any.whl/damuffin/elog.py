from . import hector
import os

INCOMPLETE = "incomplete"
INPROGRESS = "inprogress"
COMPLETE = "complete"

def _remove_whitespaces(text):
    return " ".join(text.split())

def _create_elog(dir: str, data: str, name: str=""):
    path = os.path.join(dir, name + ".elog")
    with open(path, "w") as elog:
        elog.write(data)
    return path

def _load_elog(incomplete: list, inprogress: list, complete: list):
    text = "[INCOMPLETE]\n"
    for i in incomplete:
        text += _remove_whitespaces(i) + "\n"
    
    text += ";[INPROGRESS]\n"
    for p in inprogress:
        text += _remove_whitespaces(p) + "\n"
    
    text += ";[COMPLETE]\n"
    for c in complete:
        text += _remove_whitespaces(c) + "\n"
    return text[:-1]

class FileParseError(Exception): pass
class FileFormatError(Exception): pass

class _elog_parser():
    def __init__(self, elogfile):
        self.elogfile = elogfile
        if not os.path.exists(elogfile):
            raise FileNotFoundError(f"Unable to find elog file with path: '{elogfile}'")
        self.__valid_states = ["incomplete", "inprogress", "complete"]

    def __find_missing_states(self, states):
        return [s for s in self.__valid_states if s not in states.keys()]

    def parse(self):
        def _(s, i):
            return [_remove_whitespaces(item) for item in s[i:].split("\n") if item != "" and item != "\n"]

        with open(self.elogfile, "r") as f:
            states = {}
            for s in f.read().split(";"):
                if "[INCOMPLETE]" in s:
                    states['incomplete'] = _(s, 12)
                    continue
                
                if "[INPROGRESS]" in s:
                    states['inprogress'] = _(s, 12)
                    continue
                
                if "[COMPLETE]" in s:
                    states["complete"] = _(s, 10)
                    continue

                raise FileParseError(f"Malformed elog file.")
            
            missing = self.__find_missing_states(states)
            if missing != []:
                raise FileParseError(f"Missing state(s): {missing}")
            
            return states

    def format(self, states):
        missing = self.__find_missing_states(states)
        if missing != []:
            raise FileFormatError(f"Missing state(s): {missing}")
        
        return states["incomplete"], states["inprogress"], states["complete"]

class elog():
    ALREADY_COMPLETED = "elog.AlreadyCompleted"

    def __init__(self, dir, incomplete=[], inprogress=[], complete=[], overwrite=False, encrypt=False):
        params = self.__verify_parameters({"incomplete": incomplete, "inprogress": inprogress, "complete": complete}, (list,))
        if params != []: raise ValueError(f"Expected paramter(s) {params} to be of type 'list'")

        path = os.path.join(dir, ".elog")
        self.__encrypt_elog_items = encrypt
        self.__elogfile = path

        match os.path.exists(path):
            case True:
                if self.__is_empty(path): self.__wipe()
                if not overwrite:
                    parser = _elog_parser(path)
                    incomplete, inprogress, complete = _elog_parser(path).format(parser.parse())
            case False: self.__elogfile = _create_elog(path, _load_elog(incomplete, inprogress, complete))

        self.incomplete = incomplete
        self.inprogress = inprogress
        self.complete = complete

        if overwrite: self.__write()
        self.__valid_states = ["incomplete", "inprogress", "complete"]

        print(incomplete, inprogress, complete)
    
    def __verify_parameters(self, objects: dict, types: tuple | list) -> bool:
        return [name for name, value in objects.items() if type(value) not in types]

    def __verify_state(self, state):
        if state not in self.__valid_states:
            raise ValueError("Expected 'state' parameter to be either, 'incomplete', 'inprogress", 'complete')
    
    def __find_item(self, item):
        for state in self.__valid_states:
            if item in self.__dict__[state]: return state
    
    def __verify_item(self, item):
        if self.__find_item(self.__encrypt(item)) is None:
            raise ValueError(f"Missing item: {item} from elog.")

    def __is_empty(self, path):
        with open(path, "r") as f:
            return f.read() == ""

    def __write(self, data=None):
        if data is None:
            data = _load_elog(self.incomplete, self.inprogress, self.complete)

        with open(self.__elogfile, "w") as elog:
            elog.write(data)

    def __wipe(self):
        self.__write(_load_elog([], [], []))
    
    def __encrypt(self, txt):
        if self.__encrypt_elog_items:
            return hector.sha3_256(txt)
        return txt

    def wipe(self):
        self.incomplete.clear()
        self.inprogress.clear()
        self.complete.clear()
        self.__write()

    def get(self, item):
        self.__verify_item(item)
        item = self.__encrypt(item)
        return self.__find_item(item)

    def update(self, item, ignore_completed=True) -> None | str:
        self.__verify_item(item)
        item = self.__encrypt(item)
        items_state = self.__find_item(item)

        if items_state == "completed" and ignore_completed: return self.ALREADY_COMPLETED
        next_state = self.__valid_states[(self.__valid_states.index(items_state) + 1) % 3]

        self.__dict__[items_state].remove(item)
        self.__dict__[next_state].append(item)
        self.__write()

    def set(self, item, state):
        self.__verify_state(state)
        item = self.__encrypt(item)
        self.__verify_item(item)

        items_state = self.__find_item(item)
        self.__dict__[items_state].remove(item)
        self.__dict__[state].append(item)
        self.__write()
    
    def add(self, item, state=INCOMPLETE):
        self.__verify_state(state)
        item = self.__encrypt(item)

        if item not in self.__dict__[state]:
            self.__dict__[state].append(item)
        self.__write()

    def remove(self, item):
        state = self.__find_item(item)
        item = self.__encrypt(item)

        if state is not None:
            self.__dict__[state].remove(item)
        self.__write()