from quart import Blueprint, render_template, redirect

webmain = Blueprint('webmain', __name__, template_folder='templates', static_folder='static')#, root_path='/')

@webmain.route('/')
async def home():
     return await render_template('index.html')