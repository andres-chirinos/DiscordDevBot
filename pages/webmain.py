from quart import Blueprint, render_template
webmain = Blueprint('webmain', __name__, static_folder='pages/static')

@webmain.route('/')
async def home():
     return await render_template('index.html')