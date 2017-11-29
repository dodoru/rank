import json

import config
from model import init_db
from user import User
from utility import (
    log_dict,
    log,
)

from api import API


def main():
    init_db()

    users = User.all()

    s = set([])
    for u in users:
        l = len(u.repositories)
        s.add(l)
        log('user stat <{}> <{}> <{}>'.format(l, u.name, u.url))
    log('repo count', s)

    for i, u in enumerate(users):
        log('第{}个用户'.format(i, u.login))
        u.add_contribution()

    wrong_contribution = []
    cs = []
    for u in users:
        log('contribution', len(u.contribution))
        log(json.dumps(u.contribution, indent=4))
        for c in u.contribution:
            cs.append(c)
            if c[0] == 0 or c[1] is None or c[2] == 0:
                wrong_contribution.append(c)

    for u in users:
        u.calculate_star()

    us = sorted(users, key=lambda u: u.star, reverse=True)
    for i, u in enumerate(us):
        log('user star: <{}> <{}> <{}>'.format(i, u.login, u.star))

    log('wrong_contribution', wrong_contribution)


def test():
    r = API.get_v3('/users/octocat', True)
    log_dict(r)


if __name__ == '__main__':
    main()
    # test()
