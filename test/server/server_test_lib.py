# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# Copyright (c) 2014, Arista Networks, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
#   Neither the name of Arista Networks nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import os
import shutil

WORKINGDIR = '/tmp/ztpserver'
FILESTORE = os.path.join(WORKINGDIR, 'filestore')
ZTPSCONF = os.path.join(WORKINGDIR, 'ztpserver.conf')

FOLDERS = ['bootstrap', 'actions', 'definitions', 'nodes',
           'packages', 'files']

NODES = {
    '001c73111111': [ 'definition', 'pattern' , 'topology'],
    '001c73222222': [ 'startup-config' ],
    '001c73333333': [ 'definition', 'startup-config' ]
}

class FileStore(object):

    @classmethod
    def create(cls):
        fs = cls()
        fs.filestore()
        fs.neighbordb()
        fs.actions
        fs.bootstrap()
        fs.nodes()
        fs.definitions()
        return fs

    def write_file(self, filename, contents):
        fp = os.path.join(FILESTORE, filename)
        open(fp, 'w').write(contents)

    def neighbordb(self):
        data = """
            variables:
              foo: bar
            patterns:
              - name: test pattern 1
                definition: test
                node: 001c73aabbcc
                interfaces:
                  - Ethernet1: any:any
                  - Ethernet2: none
              - name: test pattern 2
                definition: test
                interfaces:
                  - Ethernet1: any:any
                  - Ethernet2: none
        """
        self.write_file('neighbordb', data)

    def bootstrap(self):
        data = """
            #!/usr/bin/python
            print "Hello World!"
        """
        self.write_file('bootstrap/default', data)

    def actions(self):
        data = """
            #!/usr/bin/python
            print "Hello World!"
        """
        self.write_file('actions/test', data)

    def definitions(self):
        data = """
            actions:
              - name: test action
                action: test_action
        """
        self.write_file('definitions/test', data)

    def nodes(self):
        contents = {
            "startup-config": """
                ! startup-config
                hostname test
            """,
            "definition": """
                actions:
                  - name: test action
                    action: test_action
            """,
            "pattern": """
                "name": "test pattern",
                "definition": "test",
                "variables": { "foo": "bar" },
                "interfaces": [
                    { "Ethernet1": "any" },
                    { "Ethernet2": "none" }
                ]
            """,
            "topology": """
                {"Ethernet1": [{ "device": "test", "port": "test"}],
                 "Ethernet2": [{ "device": "test", "port": "test"}]}
            """
        }
        try:
            for node, files in NODES.items():
                fp = os.path.join(FILESTORE, 'nodes/%s' % node)
                os.makedirs(fp)
                for item in files:
                    fp = 'nodes/%s/%s' % (node, item)
                    self.write_file(fp, contents[item])
        except os.error:
            pass

    def filestore(self, **kwargs):
        try:
            os.makedirs(FILESTORE)
            for fldr in FOLDERS:
                fldr = os.path.join(FILESTORE, fldr)
                os.makedirs(fldr)
        except os.error:
            pass

def ztpserver_conf():
    with open(ZTPSCONF, 'w') as conf:
        conf.write('[default]\n')
        conf.write('data_root = %s\n' % FILESTORE)
    return ZTPSCONF

def create_filestore():
    FileStore.create()

def delete_filestore():
    try:
        fp = os.path.join(WORKINGDIR, FILESTORE)
        shutil.rmtree(fp)
    except shutil.Error as exc:
        print exc

def remove_all():
    shutil.rmtree(WORKINGDIR)



