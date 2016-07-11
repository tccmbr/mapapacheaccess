#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MapAccess


class Application:

    def __init__(self):
        print 30*'='
        print 5*' '+'MAP APACHE2 ACCESS'
        print 30 * '='
        self.ip = raw_input('IP = ')
        self.palavra_chave = raw_input('Palavra chave = ')

        self.map_access_usuario = MapAccess.MapAccess(self.ip, self.palavra_chave)
        self.__init__()

if __name__ == '__main__':
    app = Application()
