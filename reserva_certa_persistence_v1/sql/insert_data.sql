-- insert_data.sql
PRAGMA foreign_keys = ON;

INSERT OR IGNORE INTO users (id, name, email, is_admin, created_at) VALUES
  ('u1', 'Lucas', 'lucas@example.com', 0, '2025-09-11T12:00:00Z'),
  ('u2', 'Maria', 'maria@example.com', 1, '2025-09-11T12:05:00Z');

INSERT OR IGNORE INTO spaces (id, name, capacity, equipments, price_per_hour, description) VALUES
  ('s1', 'Sala Reunião A', 10, 'Projetor,Mesa', 50.0, 'Sala pequena para reuniões'),
  ('s2', 'Auditório', 100, 'PA,Microfone', 200.0, 'Auditório grande');

INSERT OR IGNORE INTO reservations (id, user_id, space_id, start, end, status, notes, created_at) VALUES
  ('r1', 'u1', 's1', '2025-09-11T16:00:00Z', '2025-09-11T18:00:00Z', 'CONFIRMED', '', '2025-09-11T13:00:00Z'),
  ('r3', 'u2', 's2', '2025-09-11T17:00:00Z', '2025-09-11T19:00:00Z', 'CONFIRMED', '', '2025-09-11T13:05:00Z');
