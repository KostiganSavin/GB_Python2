import sqlite3
from collections import namedtuple


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


Terminal = namedtuple('Terminal', ('id_', 'configuration', 'title',
                                   'comment', 'pub_key'))
Partner = namedtuple('Partner', ('id_', 'title', 'comment'))
Debet = namedtuple('Debet', ('id_', 'agent_id', 'datetime', 'summ'))
Credit = namedtuple('Credit', ('id_', 'agent_id', 'datetime', 'summ'))
Payment = namedtuple('Payment', ('id_', 'datetime', 'terminal_id',
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
                                values(?, ?, ?, ?);''',
                                (terminal.configuration, terminal.title,
                                 terminal.comment,  terminal.pub_key))
            self.conn.commit()
        except:
            self.conn.rollback()

    def get_all_terminals(self):
        self.cursor.execute('''select * from `terminal`;''')
        result = self.cursor.fetchall()
        return result

    def get_terminal_by_id(self, id_):
        self.cursor.execute('''select * from `terminal` where id = ?;''',
                            (id_, ))
        result = self.cursor.fetchone()
        return result


class PartnerDb:
    def __init__(self):
        self.conn = db_connect()
        self.cursor = self.conn.cursor()

    def write_to_partner(self, partner):
        try:
            self.cursor.execute('''insert into `partner`
                                (`title`, `comment`)
                                values(?, ?);''', (partner.title,
                                partner.comment))
            self.conn.commit()
        except:
            self.conn.rollback()

    def get_all_partners(self):
        self.cursor.execute('''select * from `partner`;''')
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
                                (`datetime`,
                                 `terminal_id`,
                                 `transaction_id`,
                                 `partner_id`,
                                 `summ`)
                                values(?, ?, ?, ?, ?);''',
                                (payment.datetime,
                                 payment.terminal_id,
                                 payment.transaction_id,
                                 payment.partner_id,
                                 payment.summ))
            self.conn.commit()
        except:
            self.conn.rollback()

    def get_all_payments(self):
        self.cursor.execute('''select * from `payment`;''')
        result = self.cursor.fetchall()
        return result


class CreditDb:
    pass


class DebetDb:
    pass


class TerminalWorker:
    def __init__(self, repository):
        self.repository = repository

    def write_to_terminal(self, terminal):
        self.repository.write_to_terminal(terminal)

    def get_terminal_by_id(self, id_):
        return Terminal(*self.repository.get_terminal_by_id(id_))

    def get_all_terminals(self):
        return self.repository.get_all_terminals()

    def delete_terminal_by_id(self):
        pass


class PartnerWorker:
    def __init__(self, repository):
        self.repository = repository

    def write_to_partner(self):
        pass

    def get_all_partners(self):
        pass

    def get_partner_by_id(self):
        pass

    def delete_partner_by_id(self):
        pass


class PaymentWorker:
    def __init__(self, repository):
        self.repository = repository

    def write_to_payment(self):
        pass

    def get_all_payment(self):
        pass

    def get_payment_by_id(self):
        pass



def main():
    pass
    # make_db(clear=1)
    # t = Terminal("00", "{'key': 'Value''}", "Terminal1", "Term1", "KEY")
    # print(t)
    tr = TerminalDb()
    tw = TerminalWorker(tr)

    # for i in range(2, 20):
    #     t = Terminal("00", "{'key': 'Value''}", "Terminal{}".format(i), "Term{}".format(i), "KEY")
    #     print(t)
    #     tw.write_to_terminal(t)
    t = tw.get_all_terminals()
    print(t)


if __name__ == '__main__':
    main()
