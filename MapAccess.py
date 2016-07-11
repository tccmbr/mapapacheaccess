#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os


class MapAccess:

    diretorio_log = 'logs/'

    def __init__(self, ip, palavra_chave):
        self.ip = ip
        self.palavra_chave = palavra_chave

        try:
            self.valida_ip()
        except ValueError as e:
            print e
        else:
            try:
                if not os.path.exists(self.diretorio_log):
                    os.mkdir(self.diretorio_log, 0775)

                print "\n"
                print 'processando...'
                self.process()
                print "\n"
                print 25*'='
                print 5*' '+'RESULTADO'
                print 25 * '='
                self.search()
                print "\n"
            except IOError as e:
                print e

    def valida_ip(self):
        ip = self.ip.split('.')

        if len(ip) != 4:
            raise ValueError('Ip inválido!')

        for n in ip:
            if len(n) == 0 or re.search('[\D]', n):
                raise ValueError('Ip inválido!')

    def search(self):
        log = open(self.diretorio_log+'log_access_'+self.ip+'.log', 'r')
        result_file = open(self.diretorio_log+'result_'+self.ip+'.txt', 'a')

        for l in log.readlines():
            result = re.search(self.palavra_chave, l)
            if result:
                result = self.filter_url(l)
                if result:
                    # captura a url
                    url = result.group()

                    result = self.filter_data_hora(l)
                    data_hora = result.group()

                    if data_hora:
                        result = "%s %s" % (data_hora, url)
                        print result
                        result_file.write(result+"\n")

        result_file.close()
        log.close()

    def process(self):
        log_access = open('/var/log/apache2/access.log', 'r')
        log = open(self.diretorio_log+'log_access_'+self.ip+'.log', 'w')

        for l in log_access.readlines():
            result = self.filter_ip(l)
            if result:
                result = self.filter_url(l)
                if result:
                    # captura a url
                    url = result.group()
                    # captura a data e hora
                    result = self.filter_data_hora(l)
                    data_hora = result.group()

                    if data_hora:
                        log.write("%s %s\n" % (data_hora, url))

        log.close()
        log_access.close()

    def filter_ip(self, l):
        return re.search(self.ip, l)

    @staticmethod
    def filter_url(l):
        return re.search('(GET|POST)+\s[\w/?@&%=.-]+', l)

    @staticmethod
    def filter_data_hora(l):
        return re.search('[\d]+/[a-zA-Z]+/[\d]+:[\d]+:[\d]+:[\d]+', l)
