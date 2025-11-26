def test_index_and_spaces_routes(client):
    rv = client.get('/')
    assert rv.status_code == 200
    body = rv.data.decode('utf-8')
    assert 'Reserva Certa' in body

    # spaces list
    rv2 = client.get('/spaces')
    assert rv2.status_code == 200
    assert 'Espaços' in rv2.data.decode('utf-8')


def test_create_space_via_post(client):
    data = {
        'name': 'Nova Sala X',
        'capacity': '20',
        'equipments': 'Mesa',
        'price_per_hour': '0',
        'description': 'Criada pelo teste'
    }
    rv = client.post('/spaces/new', data=data, follow_redirects=True)
    assert rv.status_code == 200
    text = rv.data.decode('utf-8')
    assert 'Espaço criado com sucesso' in text or 'Espaço criado com sucesso!' in text
