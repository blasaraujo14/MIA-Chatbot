import re

COURSE_NAMES = {
    "aif": "AI Fundamentals",
    "de": "Data Engineering",
    "rp": "Reasoning and Planning",
    "nlu": "Natural Language Understanding",
    "ml1": "Machine Learning 1",
    "cv1": "Computer Vision 1",
    "ir1": "Information Retrieval 1",
    "txai": "Trustable and Explainable AI",
    "mas": "Multi-Agent Systems",
    "kru": "Knowledge Representation with Uncertainty",
    "lm": "Language Modelling",
    "wist": "Web Intelligence and Semantic Technologies",
    "dl": "Deep Learning",
    "ml2": "Machine Learning 2",
    "ec": "Evolutionary Computation",
    "cv2": "Computer Vision 2",
    "ir2": "Information Retrieval 2",
    "aipm": "AI Project Management",
    "pm": "Process Mining",
    "irts": "Intelligent Real Time Systems"
}

WEEK_DAYS = {
    "mon": "Monday",
    "tue": "Tuesday",
    "wed": "Wednesday",
    "thu": "Thursday",
    "fri": "Friday",
    "sat": "Saturday",
    "sun": "Sunday"
}

PERIODS = {
    "q(1,a)": "first bimester",
    "q(1,b)": "second bimester",
    "q(2,a)": "third bimester",
    "q(2,b)": "fourth bimester",
    "q(1,a);q(1,b)": "first quadrimester",
    "(q(1,a);q(1,b))": "first quadrimester",
    "q(1,_)": "first quadrimester",
    "q(2,a);q(2,b)": "second quadrimester",
    "(q(2,a);q(2,b))": "second quadrimester",
    "q(2,_)": "second quadrimester",
}

# Split by commas outside of parentheses
def splitAtoms(body):
    atoms = []
    current = ""
    depth = 0

    for c in body:
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        if c == "," and depth == 0:
            atoms.append(current.strip())
            current = ""
        else:
            current += c
    if current:
        atoms.append(current.strip())
    return atoms

def translateQuery(args):
    return f"the answer is {args[0]}"

def translateClass(args):
    slot, dd, mm, yyyy, period, course, typ = args
    conditions = []

    if slot != "_":
        conditions.append(f"in slot {slot}")
    if dd != "_" and mm != "_" and yyyy != "_":
        conditions.append(f"on {dd}/{mm}/{yyyy}")
    elif dd != "_" and mm != "_":
        conditions.append(f"on {dd}/{mm}")
    if course != "_":
        name = COURSE_NAMES.get(course, course)
        conditions.append(f"for {name}")
    if typ != "_":
        conditions.append(f"({typ})")

    return "there exists a class " + " ".join(conditions)

def translateCourse(args):
    courseid, req, period, credits = args
    conditions = []
    if courseid != "_":
        name = COURSE_NAMES.get(courseid, courseid)
        conditions.append(f"named {name}")
    if req != "_":
        conditions.append(f"which is {req}")
    if period != "_":
        if PERIODS.get(period, None):
            message = f"in the {PERIODS.get(period, period)}"
        else:
            message = f"in period {period}"
        conditions.append(message)
    if credits != "_":
        conditions.append(f"worth {credits} credits")
        
    return "there is a course " + ", ".join(conditions)

def translateExam(args):
    slot, dd, mm, yyyy, course, opportunity = args
    conditions = []
    
    if course != "_":
        name = COURSE_NAMES.get(course, course)
        conditions.append(f"for {name}")
    if dd != "_" and mm != "_" and yyyy != "_":
        conditions.append(f"on {dd}/{mm}/{yyyy}")
    if slot != "_":
        conditions.append(f"in slot {slot}")
    if opportunity != "_":
        conditions.append(f"for opportunity {opportunity}")
        
    return "there is an exam " + " ".join(conditions)

def translateHoliday(args):
    dd, mm, yyyy = args
    return f"{dd}/{mm}/{yyyy} is a holiday"

def translateName(args):
    code, name_str = args
    return f"the name of {code} is {name_str}"

def translateDay(args):
    week_day, dd, mm, yyyy = args
    if week_day in WEEK_DAYS:
        return f"{dd}/{mm}/{yyyy} is a {WEEK_DAYS[week_day]}"
    else:
        return ""

def translateSlotId(args):
    slot_id = args[0]
    return f"slot {slot_id} is a valid slot"

def translateSlotTime(args):
    slot, h_start, h_end = args
    return f"slot {slot} runs from {h_start} to {h_end}"

def translateBimesterStart(args):
    period, dd, mm, yyyy = args
    return f"bimester {period} starts on {dd}/{mm}/{yyyy}"

def translateBimesterEnd(args):
    period, dd, mm, yyyy = args
    return f"bimester {period} ends on {dd}/{mm}/{yyyy}"

def translateAtom(atom):
    atom = atom.strip()

    if atom.startswith("not "):
        return "it is not true that " + translateAtom(atom[4:])

    match = re.match(r"(\w+)\((.*)\)", atom)
    if not match:
        return atom

    pred = match.group(1)
    args = splitAtoms(match.group(2))

    if pred == "query":
        return translateQuery(args)
    elif pred == "class":
        return translateClass(args)
    elif pred == "course":
        return translateCourse(args)
    elif pred == "exam":
        return translateExam(args)
    elif pred == "holiday":
        return translateHoliday(args)
    elif pred == "name":
        return translateName(args)
    elif pred == "day":
        return translateDay(args)
    elif pred == "slot_id":
        return translateSlotId(args)
    elif pred == "slot_time":
        return translateSlotTime(args)
    elif pred == "bimester_start":
        return translateBimesterStart(args)
    elif pred == "bimester_end":
        return translateBimesterEnd(args)

    return atom

def aspToEnglish(rule):
    rule = rule.strip().rstrip(".")

    if ":-" not in rule:
        head_match = re.match(r"query\((.*)\)", rule)
        return f"The answer is {head_match.group(1)}."

    if rule == "query(no) :- not query(yes)":
        return "The answer is no if the previous statement is false."

    head, body = rule.split(":-")
    head = head.strip()
    body = body.strip()

    body_atoms = splitAtoms(body)

    head_match = re.match(r"query\((.*)\)", head)
    if not head_match:
        return "Rule does not define query/1"

    head_content = head_match.group(1)

    translated_body = [translateAtom(atom) for atom in body_atoms if translateAtom(atom)]
    body_text = " and ".join(translated_body)

    return f"The answer is {head_content} if {body_text}."


# ======================
# Example
# ======================

if __name__ == "__main__":
    asp_rule = input("Enter ASP rule:\n")
    print("\nPseudo-natural language:")
    print(aspToEnglish(asp_rule))