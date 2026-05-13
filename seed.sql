-- seed data for https://github.com/maria-caseiro/web-library
-- books from the public domain


-- admin password: admin

INSERT INTO admin (username, password_hash) VALUES
('admin', 'scrypt:32768:8:1$nvLBFezASwi4APi6$717c5f5c6c44a7f5725e46e55b9835b8d3077b9bdc7f38bc43c0a090e5438369a33f8d8bf8d71daa4ac69b09f3cf390563e17709cf11faaa5491fd1dea52ff71');


-- books

INSERT INTO books (title, author, isbn, category, year, publisher) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 'Fiction', 1925, 'Scribner'),
('To Kill a Mockingbird', 'Harper Lee', '9780061935466', 'Fiction', 1960, 'J. B. Lippincott'),
('1984', 'George Orwell', '9780451524935', 'Dystopia', 1949, 'Secker & Warburg'),
('Brave New World', 'Aldous Huxley', '9780060850524', 'Dystopia', 1932, 'Chatto & Windus'),
('The Old Man and the Sea', 'Ernest Hemingway', '9780684801223', 'Fiction', 1952, 'Scribner'),
('Crime and Punishment', 'Fyodor Dostoevsky', '9780143107637', 'Classic', 1866, 'The Russian Messenger'),
('Don Quixote', 'Miguel de Cervantes', '9780060934347', 'Classic', 1605, 'Francisco de Robles'),
('The Metamorphosis', 'Franz Kafka', '9780553213690', 'Fiction', 1915, 'Kurt Wolff Verlag');


-- copies

INSERT INTO copies (book_id, status, condition) VALUES
(1, 'available', 'good'),
(1, 'available', 'good'),
(2, 'available', 'good'),
(2, 'available', 'good'),
(3, 'available', 'good'),
(3, 'available', 'good'),
(3, 'available', 'good'),
(4, 'available', 'good'),
(5, 'available', 'good'),
(6, 'available', 'good'),
(6, 'available', 'good'),
(7, 'available', 'good'),
(8, 'available', 'good'),
(8, 'unavailable', 'damaged');


-- readers

INSERT INTO readers (name, email, phone, address, location) VALUES
('Maria Silva', 'maria@email.com', '912345678', 'Rua das Flores 10', 'Lisboa'),
('João Santos', 'joao@email.com', '923456789', 'Av. Central 25', 'Porto'),
('Ana Ferreira', 'ana@email.com', '934567890', 'Rua do Comércio 5', 'Coimbra'),
('Pedro Costa', 'pedro@email.com', '945678901', 'Rua Nova 18', 'Braga'),
('Sofia Rodrigues', 'sofia@email.com', '956789012', 'Praça do Município 3', 'Faro');


-- loans

INSERT INTO loans (copy_id, reader_id, loan_date, due_date, return_date) VALUES
(1, 1, '2026-03-01', '2026-03-31', '2026-03-28'),
(3, 2, '2026-04-01', '2026-05-01', '2026-04-25'),
(5, 3, '2026-03-15', '2026-04-14', NULL),
(7, 4, '2026-04-20', '2026-05-20', NULL),
(10, 5, '2026-05-01', '2026-05-31', NULL);


-- update status of loaned copies

UPDATE copies SET status = 'loaned' WHERE copy_id IN (5, 7, 10);
