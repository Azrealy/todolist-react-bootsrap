-- Drop tables and functions if exists
DROP TABLE IF EXISTS :schema.todo_list;

-- Create `todo_list` table
CREATE TABLE :schema.todo_list (
    id  int NOT NULL,
    context  text NOT NULL,
    completed boolean NOT NULL,
    PRIMARY KEY(id)
);

INSERT INTO todo_list VALUES
    (1, 'clothing', True),
    (2, 'aaa', True);