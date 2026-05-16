from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import re
from aspToEnglish import aspToEnglish
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import clingo
import pytz
import logging

base_dir = os.path.dirname(__file__)

app = Flask(__name__)
CORS(app)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
#model = "gpt-4.1"
model = "gpt-5.5"

app.logger.setLevel(logging.INFO)
defaultEventDuration = 90 # In minutes

program = open(os.path.join(base_dir, "asp_code", "course_info.lp"), "r", encoding="utf-8").read()
program += '\n' + open(os.path.join(base_dir, "asp_code", "classes.lp"), "r", encoding="utf-8").read()
program += '\n' + open(os.path.join(base_dir, "asp_code", "exams.lp"), "r", encoding="utf-8").read()
program += '\n' + open(os.path.join(base_dir, "asp_code", "days.lp"), "r", encoding="utf-8").read()
program += '\n' + open(os.path.join(base_dir, "asp_code", "time_info.lp"), "r", encoding="utf-8").read()

promptPath = os.path.join(base_dir, "prompts", "prompt.txt")
prompt = open(promptPath, "r", encoding="utf-8").read()

prompt2Path = os.path.join(base_dir, "prompts", "prompt2.txt")
prompt2 = open(prompt2Path, "r", encoding="utf-8").read()

promptICSPath = os.path.join(base_dir, "prompts", "promptICS.txt")
promptICS = open(promptICSPath, "r", encoding="utf-8").read()

slots = {}
for line in program.splitlines():
    if line.startswith("slot_time"):
        values = re.search(r'slot_time\((.*)\)', line).group(1).split(',')
        slots[values[0].strip()] = (values[1].strip().strip('"'), values[2].strip().strip('"'))

def getModelResponse(input_text):
    response = client.responses.create(
        model=model,
        input=input_text
    )
    return response.output_text

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('message', '')

    response = getModelResponse(prompt.replace("<question>", question))

    print("Response from model:", response)
    return jsonify({"response": response})

@app.route('/getQuery', methods=['POST'])
def getQuery():
    data = request.get_json()
    question = data.get('message', '')
    genICS = data.get('genICS', False)

    today = datetime.today().strftime("%A, %d-%m-%Y")

    response = getModelResponse(promptICS.replace("<date>", today).replace("<question>", question) if genICS else prompt.replace("<date>", today).replace("<question>", question))
    
    block_match = re.search(r'query\(.*?\.\s*(?:query\(.*?\.\s*)*', response, re.DOTALL)

    queries = []
    if block_match:
        block = block_match.group(0)
        queries = re.findall(r'query\(.*?\.', block, re.DOTALL)
    
    firstHead = queries[0].split(":-")[0].strip()
    head_match = re.match(r"query\((.*)\)", firstHead)
    if head_match.group(1) not in ["yes", "no"]:
        queries = [q for q in queries if not re.match(r"query\((.*)\)", q.split(":-")[0].strip()).group(1) in ["yes", "no"]]

    pseudo_queries = [aspToEnglish(q) for q in queries]
    app.logger.info(f"User question: {question}")
    app.logger.info(f"Queries extracted: {queries}")

    return jsonify({"queries": queries, "pseudo_queries": pseudo_queries})

@app.route('/getResponse', methods=['POST'])
def getResponse():
    data = request.get_json()
    query = data.get('query', '')
    question = data.get('question', '')

    match = re.search(r'^query\((.*?)\)\s*:-', query, re.MULTILINE)
    numValues = len(re.split(r',(?![^()]*\))', match.group(1)))
    aspCode = program + '\n'+ query + '\n#show query/' + str(numValues) + '.'

    try:
        ctl = clingo.Control()
        ctl.add("base", [], aspCode)
        ctl.ground([("base", [])])

        with ctl.solve(yield_=True) as handle:
            for m in handle:
                values = [str(a) for a in m.symbols(shown=True)]
    except Exception as e:
        return jsonify({"out": "Error in ASP code execution: " + str(e)})

    today = datetime.today().strftime("%A, %d-%m-%Y")
    response = getModelResponse(prompt2.replace("<date>", today).replace("<question>", question).replace("<output>", ' '.join(values)))
    app.logger.info(f"User question: {question}")
    app.logger.info(f"Model response: {response}")

    return jsonify({"out": values, "response": response})

@app.route('/generateICS', methods=['POST'])
def generateICS():
    tz = pytz.timezone('Europe/Madrid')

    def createDate(slot, day, month, year):
        dateStr = f"{day} {month} {year}"

        startTime, endTime = slots[slot]

        startDate = datetime.strptime(f"{dateStr} {startTime}", "%d %m %Y %H:%M")

        if endTime == "undefined":
            endDate = startDate + timedelta(minutes=defaultEventDuration)
        else:
            endDate = datetime.strptime(f"{dateStr} {endTime}", "%d %m %Y %H:%M")

        startDate = tz.localize(startDate_naive)
        endDate = tz.localize(endDate_naive)

        return startDate, endDate

    def addEvent(cal, name, description, start, end):
        event = Event()
        event.add('summary', name)
        event.add('description', description)
        event.add('dtstart', start)
        event.add('dtend', end)
        event.add('dtstamp', datetime.now(pytz.utc))

        cal.add_component(event)
    
    cal = Calendar()
    cal.add('version', '2.0') 
    cal.add('prodid', '-//MyApp//')    
    
    data = request.get_json()
    query = data.get('query', '')
    aspCode = program + '\n'+ query + '\n#show query/7.'
    
    try:
        ctl = clingo.Control()
        ctl.add("base", [], aspCode)
        ctl.ground([("base", [])])

        with ctl.solve(yield_=True) as handle:
            for m in handle:
                classes = [str(a) for a in m.symbols(shown=True)]
    except Exception as e:
        return jsonify({"out": "Error in ASP code execution: " + str(e)})

    for c in classes:
        inside = re.search(r'\((.*)\)', c).group(1)
        values = re.split(r',(?![^()]*\))', inside)
        startDate, endDate = createDate(values[0].strip(), values[1].strip(), values[2].strip(), values[3].strip())
        addEvent(
            cal = cal,
            name=values[5].strip('"'),
            description=values[6].strip('"'),
            start=startDate,
            end=endDate,
        )
    return jsonify({"calendar": cal.to_ical().decode('utf-8')})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
