import sqlite3


def make_db(clear=None):
    with sqlite3.connect('company.db3') as conn:
        cursor = conn.cursor()
        if clear is not None:
            cursor.execute('drop table if exists terminal;')
            cursor.execute('drop table if exists debit;')
            cursor.execute('drop table if exists credit;')
            cursor.execute('drop table if exists partner;')
            cursor.execute('drop table if exists payment;')
        
        cursor.execute('''create table if not exists terminal (
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            configuration TEXT,
                            title TEXT,
                            comment TEXT,
                            pub_key TEXT);
                       ''')

        cursor.execute('''create table if not exists partner (
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            title TEXT,
                            comment TEXT);
                       ''')

        cursor.execute('''create table if not exists debit (
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            agent_id INT,
                            datetime TEXT,
                            summ INT,
                            FOREIGN KEY (agent_id) REFERENCES partner(id));
                       ''')

        cursor.execute('''create table if not exists credit (
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            agent_id INT,
                            datetime TEXT,
                            summ INT,
                            FOREIGN KEY (agent_id) REFERENCES partner(id));
                       ''')
       
        cursor.execute('''create table if not exists payment (
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            datetime TEXT,
                            terminal_id INT,
                            transaction_id INT,
                            partner_id INT,
                            summ INT,
                            FOREIGN KEY (terminal_id) REFERENCES terminal(id),
                            FOREIGN KEY (partner_id) REFERENCES partner(id));
                       ''')


class DbWrite:

    def write_to_terminal():
        with sqlite3.connect('company.db3') as conn:
            cursor = conn.cursor()
            cursor.execute('''insert into terminal
                            (`configuration`, `title`, `comment`, `pub_key`)
                            values(?, ?, ?, ?);'''())



def main():
    pass
    # make_db(clear=1)


if __name__ == '__main__':
    main()
