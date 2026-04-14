from flask import Blueprint, render_template, session

dash_board = Blueprint('dash_board', __name__)

@dash_board.route('/dash_board_test')

def dash_board_test():
    return render_template('test.html', name='lvs', user_email=session.get("user_gmail", "User"))