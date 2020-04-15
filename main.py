from dbremote import db_session


def main():
    db_session.global_init("db/data.sqlite")
    return 0


if __name__ == "__main__":
    main()
