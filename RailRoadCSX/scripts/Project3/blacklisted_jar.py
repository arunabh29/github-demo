#!/usr/bin/python

class BlacklistedJar(object):

    def __init__(self, blacklisted_jar_name, expected_md5_checksum, suggested_jar_name):
        self.__blacklisted_jar_name = blacklisted_jar_name
        self.__expected_md5_checksum = expected_md5_checksum
        self.__suggested_jar_name = suggested_jar_name
        
    def get_blacklisted_jar_name(self):
        return self.__blacklisted_jar_name
        
    def set_blacklisted_jar_name(self, blacklisted_jar_name):
        self.__blacklisted_jar_name = blacklisted_jar_name
        
    def get_expected_md5_checksum(self):
        return self.__expected_md5_checksum
        
    def set_expected_md5_checksum(self, expected_md5_checksum):
        self.__expected_md5_checksum = expected_md5_checksum
        
    def get_suggested_jar_name(self):
        return self.__suggested_jar_name
        
    def set_suggested_jar_name(self, suggested_jar_name):
        self.__suggested_jar_name = suggested_jar_name
    
    def __contains__(self, key):
        return key == self.get_blacklisted_jar_name() \
            or key == self.get_expected_md5_checksum()
