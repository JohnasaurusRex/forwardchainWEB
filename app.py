from flask import Flask, render_template, request

class Rule:
    def __init__(self, conditions, result):
        self.conditions = conditions
        self.result = result

def forward_chain(rules, facts):
    facts = set(facts)
    while True:
        new_facts = set()
        for rule in rules:
            if all(condition in facts for condition in rule.conditions) and rule.result not in facts:
                new_facts.add(rule.result)
        if not new_facts:  # If no new facts were added, stop
            break
        facts.update(new_facts)  # Add the new facts to the known facts
    return list(facts)  # Convert facts back to a list

app = Flask(__name__)

# Initialize lists to store user inputs
facts = []
rules = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global facts, rules  # Use global to access the lists

    if request.method == 'POST':
        user_input = request.form['user_input']
        input_type = request.form['type_select']

        if 'undo' in request.form:  # Check if 'undo' button was clicked
            if input_type == 'fact' and facts:
                facts.pop()  # Remove the last fact
            elif input_type == 'rule' and rules:
                rules.pop()  # Remove the last rule

        elif input_type == 'rule':
            if 'if' in user_input and ', then' in user_input:
                parts = user_input.split('if')
                conditions = parts[1].split(', then')[0].strip().split(' and ')
                result = parts[1].split(', then')[1].strip()
                rules.append(Rule(conditions, result))
            else:
                return "Invalid rule format. Please use 'if condition1 and condition2, then result'."
        elif input_type == 'fact':
            facts.append(user_input)

    generated_facts = forward_chain(rules, facts)

    return render_template('index.html', generated_facts=generated_facts, facts=facts, rules=[f"if {' and '.join(rule.conditions)}, then {rule.result}" for rule in rules])

if __name__ == '__main__':
    app.run(debug=True)
