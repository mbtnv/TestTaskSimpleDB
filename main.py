import sys
from collections import Counter


db = {}
transaction_log = []


def set_value(key, value):
    db[key] = value


def unset_value(key):
    try:
        db.pop(key)
    except:
        pass


def command_set(key, value):
    if len(transaction_log) == 0:
        set_value(key, value)
    else:
        transaction_log.append(f'{key}:{command_get(key)}')
        set_value(key, value)


def command_get(key):
    return db.get(key, 'NULL')


def command_unset(key):
    if len(transaction_log) == 0:
        unset_value(key)
    else:
        transaction_log.append(f'{key}:{command_get(key)}')
        unset_value(key)


def command_counts(key):
    c = Counter(db.values())
    count = c[key]
    return count


def command_end():
    sys.exit()


def command_begin():
    transaction_log.append('BEGIN')


def command_rollback():
    if len(transaction_log) > 0:
        while True:
            tr_lr = transaction_log.pop()
            if tr_lr == 'BEGIN':
                break
            else:
                key = tr_lr.split(':')[0]
                value = tr_lr.split(':')[1]
                if value == 'NULL':
                    unset_value(key)
                else:
                    set_value(key, value)


def command_commit():
    transaction_log.clear()


def command_parser(str):
    command = None
    key = None
    value = None
    try:
        command = str.split()[0]
        key = str.split()[1]
        value = str.split()[2]
    except:
        pass
    return command, key, value


def command_executer(command, key, value):
    if command == 'END':
        command_end()
    elif command == 'SET':
        if key is not None and value is not None:
            command_set(key, value)
    elif command == 'GET':
        if key is not None:
            print(command_get(key))
    elif command == 'UNSET':
        if key is not None:
            command_unset(key)
    elif command == 'COUNTS':
        if key is not None:
            print(command_counts(key))
    elif command == 'BEGIN':
        command_begin()
    elif command == 'ROLLBACK':
        command_rollback()
    elif command == 'COMMIT':
        command_commit()


def main():
    while True:
        try:
            command, key, value = command_parser(input())
            command_executer(command, key, value)
        except EOFError:
            command_end()


if __name__ == "__main__":
    main()
