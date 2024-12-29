import nltk

nltk.download('punkt')

nltk.download('averaged_perceptron_tagger')



from nltk.tokenize import word_tokenize

from nltk import pos_tag

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash

knowledge_base = {

"delhi": {

"info": "Delhi, the capital city of India, is known for its rich history and vibrant culture.",

"places_to_visit": ["Red Fort", "India Gate", "Qutub Minar", "Lotus Temple"],

"transport": "The Delhi Metro is an efficient way to navigate the city. Auto-rickshaws and taxis are also available.",

"hotels": ["The Oberoi", "Taj Mahal Hotel", "Leela Palace"],

"restaurants": ["Karim's", "Bukhara", "Indian Accent"]

},

"jaipur": {

"info": "Jaipur, also known as the Pink City, is famous for its palaces and forts.",

"places_to_visit": ["Hawa Mahal", "Amber Fort", "City Palace", "Jantar Mantar"],

"transport": "Local transport includes auto-rickshaws, taxis, and city buses.",

"hotels": ["Rambagh Palace", "Samode Haveli", "ITC Rajputana"],

"restaurants": ["Chokhi Dhani", "Suwadik Rajasthani Restaurant", "Spice Court"]

},

"goa": {

"info": "Goa is known for its beautiful beaches, nightlife, and Portuguese heritage.",

"places_to_visit": ["Baga Beach", "Anjuna Beach", "Fort Aguada", "Dudhsagar Falls"],

"transport": "Renting a scooter or bike is popular. Taxis are also available.",

"hotels": ["Taj Exotica", "W Goa", "Leela Goa"],

"restaurants": ["Fisherman's Wharf", "Vinayak Family Restaurant", "Martin's Corner"]

},

"mumbai": {

"info": "Mumbai, the financial capital of India, is known for its Bollywood film industry.",

"places_to_visit": ["Gateway of India", "Marine Drive", "Chhatrapati Shivaji Terminus", "Elephanta Caves"],

"transport": "Local trains are the fastest way to travel. Taxis and auto-rickshaws are also available.",

"hotels": ["The Taj Mahal Palace", "Oberoi Mumbai", "Four Seasons"],

"restaurants": ["Leopold Cafe", "Bademiya", "The Table"]

},

"varanasi": {

"info": "Varanasi, one of the oldest cities in the world, is famous for its ghats along the Ganges River.",

"places_to_visit": ["Dashashwamedh Ghat", "Kashi Vishwanath Temple", "Sarnath", "Manikarnika Ghat"],

"transport": "Auto-rickshaws and cycle rickshaws are common. You can also hire a taxi.",

"hotels": ["BrijRama Palace", "Taj Ganges", "Suryauday Haveli"],

"restaurants": ["Kashi Chat Bhandar", "The Kashi Cafe", "Open Hand Cafe"]

},

"kerala": {

"info": "Kerala, known as 'God's Own Country', is famous for its backwaters and houseboats.",

"places_to_visit": ["Alleppey", "Munnar", "Kochi", "Thekkady"],

"transport": "Houseboats, taxis, and local buses are common for getting around.",

"hotels": ["Kumarakom Lake Resort", "Spice Tree Munnar", "The Zuri Kumarakom"],

"restaurants": ["Saravanaa Bhavan", "Malabar Kitchen", "The Rice Boat"]

},

"chennai": {

"info": "Chennai is known for its cultural heritage and beautiful beaches.",

"places_to_visit": ["Marina Beach", "Kapaleeshwarar Temple", "Fort St. George", "San Thome Basilica"],

"transport": "The Chennai Metro is an efficient way to navigate the city.",

"hotels": ["The Leela Palace", "ITC Grand Chola", "Taj Connemara"],

"restaurants": ["Murugan Idli Shop", "Saravana Bhavan", "The Flying Elephant"]

},

"madurai": {

"info": "Madurai is famous for its Meenakshi Temple and rich history.",

"places_to_visit": ["Meenakshi Amman Temple", "Thirumalai Nayakkar Palace", "Gandhi Museum"],

"transport": "Local transport includes auto-rickshaws and taxis.",

"hotels": ["Heritage Madurai", "Sangam Hotel", "Taj Garden Retreat"],

"restaurants": ["Kumar Mess", "Sree Sabarees"]

},

"coimbatore": {

"info": "Coimbatore is known for its textile industry and proximity to hill stations.",

"places_to_visit": ["Marudamalai Temple", "Nilgiri Biosphere", "VOC Park"],

"transport": "Taxis and local buses are available for getting around.",

"hotels": ["The Residency", "Vivanta Coimbatore", "Le Meridien"],

"restaurants": ["Anandhas", "Sree Krishna"]

},

"hi": "Hello! How can I help you today?",

"hello": "Hi there! What can I do for you?",

"flight": "You can book flights through various online platforms like Expedia, Kayak, or directly through airlines.",

"hotel": "I recommend checking out Booking.com or Airbnb for hotel accommodations.",

"attraction": "What city are you visiting? I can suggest some attractions!",

"food": "You can explore local cuisines using Yelp or TripAdvisor.",

"visa": "Visa requirements vary by country. Please specify your nationality and destination.",

"weather": "You can check the weather on websites like Weather.com or use weather apps on your phone.",

"transportation": "Depending on the city, you can use public transport, taxis, or rideshare services like Uber or Lyft.",

"activities": "Popular activities include sightseeing, hiking, food tours, and cultural experiences. What are you interested in?",

"local customs": "It's important to respect local customs and traditions. Researching before you go can enhance your experience.",

"safety tips": "Always stay aware of your surroundings, keep your belongings secure, and avoid risky areas, especially at night.",

"currency exchange": "You can exchange currency at airports, banks, or local exchange bureaus. Credit cards are widely accepted too.",

# Expanded knowledge base



"hi": "Hello! How can I help you today?",

"hello": "Hi there! What can I do for you?",

"flight": "You can book flights through various online platforms like Expedia, Kayak, or directly through airlines.",

"hotel": "I recommend checking out Booking.com or Airbnb for hotel accommodations.",

"attraction": "What city are you visiting? I can suggest some attractions!",

"food": "You can explore local cuisines using Yelp or TripAdvisor.",

"visa": "Visa requirements vary by country. Please specify your nationality and destination.",

"weather": "You can check the weather on websites like Weather.com or use weather apps on your phone.",

"transportation": "Depending on the city, you can use public transport, taxis, or rideshare services like Uber or Lyft.",

"activities": "Popular activities include sightseeing, hiking, food tours, and cultural experiences. What are you interested in?",

"local customs": "It's important to respect local customs and traditions. Researching before you go can enhance your experience.",

"safety tips": "Always stay aware of your surroundings, keep your belongings secure, and avoid risky areas, especially at night.",

"currency exchange": "You can exchange currency at airports, banks, or local exchange bureaus. Credit cards are widely accepted too.",

}

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)

login_manager.login_view = 'login'

class User(db.Model, UserMixin):

id = db.Column(db.Integer, primary_key=True)

username = db.Column(db.String(150), unique=True, nullable=False)

password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader

def load_user(user_id):

return User.query.get(int(user_id))

@app.route('/')

def home():

return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])

def register():

if request.method == 'POST':

username = request.form['username']

password = request.form['password']

hashed_password = generate_password_hash(password)



new_user = User(username=username, password=hashed_password)

db.session.add(new_user)

db.session.commit()

flash('Registration successful! Please log in.')

return redirect(url_for('login'))

return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])

def login():

if request.method == 'POST':

username = request.form['username']

password = request.form['password']

user = User.query.filter_by(username=username).first()

if user and check_password_hash(user.password, password):

login_user(user)

return redirect(url_for('chat'))

else:

flash('Login Unsuccessful. Please check your credentials.')

return render_template('login.html')



@app.route('/chat')

@login_required

def chat():

return render_template('chat.html', username=current_user.username)



@app.route('/ask', methods=['POST'])

@login_required

def ask():

user_input = request.form['user_input']

response = get_response(user_input)

return jsonify({'response': response})



def get_response(user_input):

tokens = word_tokenize(user_input)

tagged = pos_tag(tokens)

for word, tag in tagged:

word_lower = word.lower()

if word_lower in knowledge_base:

place_info = knowledge_base[word_lower]

# Check if place_info is a dictionary

if isinstance(place_info, dict):

response = f"{place_info['info']}\n\nPlaces to Visit:\n" + "\n".join(place_info['places_to_visit']) + \

f"\n\nTransport: {place_info['transport']}\n\nHotels:\n" + \

"\n".join(place_info['hotels']) + f"\n\nRestaurants:\n" + \

"\n".join(place_info['restaurants'])

return response

else:

return place_info  # This handles the case where it's a string

return "I'm sorry, I don't understand. Can you ask about something specific?"

@app.route('/logout')

@login_required

def logout():

logout_user()

return redirect(url_for('login'))

if __name__ == '__main__':

with app.app_context():

db.create_all()  # Create database tables

app.run(debug=True)

