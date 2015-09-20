from flask import Flask, render_template, request
import keywords
import json

# creates the application
app = Flask(__name__)
#app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def starting_page():
	return render_template('index.html')

@app.route('/handled', methods=['POST'])
def handle_text():
	text = request.form['jobInput']
	if text:
		scores = masc_or_fem(text)
		new_female_text = replace_words(scores[2], text, keywords.masculine)
		new_male_text = replace_words(scores[3], text, keywords.feminine)
		new_male_scores = masc_or_fem(new_female_text);
		new_fem_scores = masc_or_fem(new_male_text);
		data = [scores[0], scores[1]];
	else:
		print("enter stuff")
	return render_template('handled.html',
		male_score = str(scores[0]), fem_score = str(scores[1]),
		job_description = text,
		new_female_text = new_female_text, new_male_text = new_male_text,
		new_male_score = new_male_scores[0], new_fem_score = new_male_scores[1],
		new_male_score2 = new_fem_scores[0], new_fem_score2 = new_fem_scores[1])
def replace_words(words_list, text, dict):
	new_text = text
	for word in words_list:
		word = word.strip(',').strip('.').strip('?')
		if word in new_text:
			if dict[word] != '':
				if dict[word] not in new_text:
					new_text = new_text.replace(word, dict[word])
	return new_text

def masc_or_fem(text):
    word_list = text.split()
    numWords = len(word_list)
    male_words = []
    fem_words = []
    male_count = 0
    fem_count = 0
    for i in range(0, numWords):
        word = word_list[i].strip(',').strip('.').strip('?')
        if word in keywords.masculine:
            male_count+=1
            male_words.append(word)
        elif word in keywords.feminine:
            fem_count+=1
            fem_words.append(word)
    male_score = round(male_count*100/numWords)
    fem_score = round(fem_count*100/numWords)
    scores = [male_score, fem_score, male_words, fem_words]
    return scores



if __name__ == '__main__':
    app.run(debug=True)
    app.run()
