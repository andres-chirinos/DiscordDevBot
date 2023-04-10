from quart import Blueprint, render_template
import os

webmain = Blueprint('webmain', __name__, static_folder='static')

@webmain.route('/')
async def home():
     return await render_template('index.html')