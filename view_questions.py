import sqlite3
import json

def view_questions():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, user_id, question, timestamp FROM questions')
    rows = cursor.fetchall()
    conn.close()
    return rows

def questions_to_json(questions):
    questions_list = []
    for question in questions:
        question_dict = {
            'id': question[0],
            'user_id': question[1],
            'question': question[2],
            'timestamp': question[3]
        }
        questions_list.append(question_dict)
    return json.dumps(questions_list, indent=4, ensure_ascii=False)

def save_to_json_file(data, filename='questions.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)

if __name__ == '__main__':
    questions = view_questions()
    questions_json = questions_to_json(questions)
    save_to_json_file(questions_json)
    print(f"Data has been saved to questions.json")