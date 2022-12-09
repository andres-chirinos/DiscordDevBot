from quart import Blueprint, render_template

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main.route('/')
async def home():
     return await render_template('index.html')