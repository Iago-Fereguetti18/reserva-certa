from persistence.space_repository import SpaceRepository
from persistence.user_repository import UserRepository
from persistence.reservation_repository import ReservationRepository


def test_space_create_and_get(test_db):
    repo = SpaceRepository()
    sid = 'st_test'
    repo.create(sid, 'Sala Teste', 5, 'Quadro', 10.0, 'Sala para teste')
    s = repo.get(sid)
    assert s is not None
    assert s['name'] == 'Sala Teste'
    all_spaces = repo.list_all()
    assert any(x['id'] == sid for x in all_spaces)


def test_user_list_and_get(test_db):
    repo = UserRepository()
    # existing user from insert_data.sql
    u = repo.get('u1')
    assert u is not None
    assert u['name'] == 'Lucas'
    # create a new user and retrieve
    uid = 'u_test'
    repo.create(uid, 'Teste', 'teste@example.com', False, '2025-11-13T00:00:00Z')
    ut = repo.get(uid)
    assert ut['email'] == 'teste@example.com'


def test_reservation_create_list_update(test_db):
    repo = ReservationRepository()
    rid = 'rt_test'
    repo.create(rid, 'u1', 's1', '2025-12-01T10:00:00Z', '2025-12-01T11:00:00Z', 'CONFIRMED', '', '2025-11-13T00:00:00Z')
    by_user = repo.list_by_user('u1')
    assert any(r['id'] == rid for r in by_user)
    # update status
    repo.update(rid, status='CANCELED')
    r = repo.get(rid)
    assert r['status'] == 'CANCELED'
