from flask import Flask, render_template, request, redirect, url_for, flash, session
from persistence.user_repository import UserRepository
from persistence.space_repository import SpaceRepository
from persistence.reservation_repository import ReservationRepository
from datetime import datetime, timezone
import uuid, os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev_secret')

# repositories
user_repo = UserRepository()
space_repo = SpaceRepository()
reservation_repo = ReservationRepository()

@app.route('/')
def index():
    spaces = space_repo.list_all()
    for s in spaces:
        s['equipments_list'] = s['equipments'].split(',') if s.get('equipments') else []
    uid = session.get('user_id', 'u1')
    user = user_repo.get(uid)
    my_reservations = reservation_repo.list_by_user(uid)
    return render_template('index.html', spaces=spaces, my_reservations=my_reservations, user=user)

@app.route('/reservar/<space_id>', methods=['GET','POST'])
def reservar(space_id):
    space = space_repo.get(space_id)
    if request.method == 'POST':
        user_id = request.form.get('user_id') or session.get('user_id', 'u1')
        start = request.form.get('start')
        end = request.form.get('end')
        start_iso = start + ':00Z' if len(start)==16 else start
        end_iso = end + ':00Z' if len(end)==16 else end
        rid = str(uuid.uuid4())[:8]
        reservation_repo.create(rid, user_id, space_id, start_iso, end_iso, 'CONFIRMED', '', datetime.now(timezone.utc).isoformat())
        flash('Reserva criada com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('reserve.html', space=space)


def _current_user():
    uid = session.get('user_id')
    return user_repo.get(uid) if uid else None


def _require_admin():
    u = _current_user()
    if not u or not u.get('is_admin'):
        flash('Acesso negado: administrador apenas.', 'danger')
        return False
    return True


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        uid = request.form.get('user_id')
        user = user_repo.get(uid)
        if user:
            session['user_id'] = uid
            flash(f'Logado como {user.get("name")}', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário não encontrado.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Desconectado.', 'info')
    return redirect(url_for('index'))


@app.route('/spaces')
def spaces_list():
    spaces = space_repo.list_all()
    return render_template('spaces_list.html', spaces=spaces)


@app.route('/spaces/new', methods=['GET','POST'])
def spaces_new():
    if request.method == 'POST':
        name = request.form.get('name')
        capacity = int(request.form.get('capacity') or 0)
        equipments = request.form.get('equipments') or ''
        try:
            price_per_hour = float(request.form.get('price_per_hour') or 0)
        except ValueError:
            price_per_hour = 0.0
        description = request.form.get('description')
        sid = 's' + str(uuid.uuid4())[:8]
        space_repo.create(sid, name, capacity, equipments, price_per_hour, description)
        flash('Espaço criado com sucesso!', 'success')
        return redirect(url_for('spaces_list'))
    return render_template('spaces_new.html')


@app.route('/users')
def users_list():
    users = user_repo.list_all()
    return render_template('users_list.html', users=users)


@app.route('/admin/reservations')
def admin_reservations():
    reservations = reservation_repo.list_all()
    return render_template('admin_reservations.html', reservations=reservations)


@app.route('/agenda')
def daily_agenda():
    # build agenda for today (UTC date)
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).date().isoformat()
    reservations = reservation_repo.list_all()
    agenda = {}
    for r in reservations:
        start = r.get('start') or ''
        if len(start) >= 10 and start[:10] == today:
            sid = r.get('space_id') or 'unknown'
            # fetch space name if possible
            sp = space_repo.get(sid)
            space_name = sp['name'] if sp else sid
            agenda.setdefault(space_name, []).append(r)
    return render_template('agenda_day.html', agenda=agenda, date=today)


@app.route('/reports')
def reports():
    reservations = reservation_repo.list_all()
    total = len(reservations)
    by_space = {}
    by_status = {}
    for r in reservations:
        sid = r.get('space_id') or 'unknown'
        sp = space_repo.get(sid)
        space_name = sp['name'] if sp else sid
        by_space[space_name] = by_space.get(space_name, 0) + 1
        status = r.get('status') or 'UNKNOWN'
        by_status[status] = by_status.get(status, 0) + 1
    return render_template('reports.html', total=total, by_space=by_space, by_status=by_status)

@app.route('/cancelar/<reservation_id>', methods=['POST'])
def cancelar(reservation_id):
    reservation_repo.update(reservation_id, status='CANCELED')
    flash('Reserva cancelada.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    from pathlib import Path
    BASE = Path(__file__).resolve().parents[0]
    DB = BASE / 'reserva_certa.db'
    SQL_DIR = BASE / 'sql'
    if not DB.exists():
        import sqlite3
        conn = sqlite3.connect(DB)
        with open(SQL_DIR / 'create_tables.sql','r',encoding='utf-8') as f:
            conn.executescript(f.read())
        with open(SQL_DIR / 'insert_data.sql','r',encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.close()
    app.run(debug=True)
