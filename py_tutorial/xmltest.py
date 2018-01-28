#!/usr/bin/python

import xmltodict

mydict = {
     'domain': {
         "@type": 'kvm',
         'name':'testvm',
         'uuid':'1234567',
         'memory':'1024000',
         'vcpu':'1',
         'os': {
             'type': {
                '@arch': 'x86_64',
                '#text': 'hvm'
             }
         },
         'devices': {
            'emulator': '/usr/libexec/qemu-kvm',
            'disk': {
                '@type': 'file',
                '@device': 'disk',
                'driver':{
                        '@name': 'qemu',
                        '@type': 'raw',
                        'target': {
                            '@dev': 'hda'
                        },
                        'source': {
                            '@file': '/opt/vm_images/centos-68.img'
                        }
                        
                }
            },
            'interface': {
                '@type': 'network',
                        'source': {
                            '@network': 'mgmt-dmz'
                        },
                        'mac': {
                            '@address': '24:42:54:21:52:45'
                        }
            },
            'graphics': {
                '@type': 'vnc',
                '@port': '-1',
                '@keymap': 'en-us'
            }

         }
     }
}
print(xmltodict.unparse(mydict, pretty=True))
