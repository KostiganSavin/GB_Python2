import sqlite3
from collections import namedtupple


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


Terminal = namedtupple('Terminal', ('id_', 'configuration', 'title',
                                    'comment', 'pub_key'))
Partner = namedtupple('Partner', ('id_', 'title', 'comment'))
Debet = namedtupple('Debet', ('id_', 'agent_id', 'datetime', 'summ'))
Credit = namedtupple('Credit', ('id_', 'agent_id', 'datetime', 'summ'))
Payment = namedtupple('Payment', ('id_', 'datetime', 'terminal_id',
                                  'transaction_id', 'partner_id', 'summ'))


def db_connect():
    conn = sqlite3.connect('company.db3')
    return conn


class TerminalDb:
    def __init__(self):
        self.conn = db_connect()
        self.cursor = self.conn.cursor()

    def write_to_terminal(self, terminal):
        try:
            self.cursor.execute('''insert into `terminal` (`configuration`,
                                `title`, `comment`, `pub_key`)
                                values(?, ?, ?, ?);'''())
            self.conn.commit()
        except:
            self.conn.rollback()

    def get_all_terminals(self):
        self.cursor.execute('''select * from `terminal`''')
        result = self.cursor.fetchall()
        return result

    def get_terminal_by_id(self, id_):
        pass



class PartnerDb:
    def __init__(self):
        self.conn = db_connect()
        self.cursor = self.conn.cursor()

    def write_to_partner(self, partner):
        try:
            self.cursor.execute('''insert into `partner`
                               (`title`, `comment`)
                               values(?, ?);'''())
            self.conn.commit()
        except:
            self.conn.rollback()

    def get_all_partners(self):
        self.cursor.execute('''select * from `partner`''')
        result = self.cursor.fetchall()
        return result

    def get_partner_by_id(self, id_):
        pass


class PaymentDb:
    def __init__(self):
        self.conn = db_connect()
        self.cursor = self.conn.cursor()

    def write_to_payment(self, payment):
        try:
            self.cursor.execute('''insert into `payment`
                                (`datetime`, `terminal_id`, `transaction_id`,
                                `partner_id`, `summ`)
                                values(?, ?, ?, ?, ?);'''(payment.datetime,
                                payment.terminal_id, payment.transaction_id,
                                payment.partner_id, payment.summ))
            self.conn.commit()
        except:
            self.conn.rollback()

    def get_all_payments(self):
        self.cursor.execute('''select * from `payment`''')
        result = self.cursor.fetchall()
        return result


class CreditDb:
    pass


class DebetDb:
    pass


class TerminalWorker:
    def __init__(self, repository):
        self.repository = repository

    def writetopayment(self, payment):
        self.repository.write_to_payment(payment)


class PartnerWorker:
    def __init__(self, repository):
        self.repository = repository


class PaymentWorker:
    def __init__(self, repository):
        self.repository = repository


def main():
    pass
    # make_db(clear=1)


if __name__ == '__main__':
    main()
