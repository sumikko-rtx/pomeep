#!/usr/bin/env python3
import sys
from simple_argparse import simple_argparse
import os
from constants import DEFAULT_RSNAPSHOT_CONFIG_FILE


#/* Note: this is a temporary implementation and will be replaced in future version of ycspomeep */

#/* get parameter: backup from a rsnapconfig config file */
def rsnapconfig_getparam_backup(config_file=DEFAULT_RSNAPSHOT_CONFIG_FILE):

    #
    # syntax
    #
    # (1) backup   /etc/        localhost/
    # (2) backup   /usr/local/  localhost/
    # (3) backup   root@example.com:/etc/       example.com/
    # (4) backup   example.com:/etc/       example.com/
    # (5) backup   root@example.com:/usr/local/ example.com/
    # (6) backup   rsync://example.com/pub/      example.com/pub/
    # (7) backup   /var/     localhost/   one_fs=1
    # (8) backup   lvm://vg0/home/path2/       lvm-vg0/
    #

    result = []

    with open(config_file, 'r') as f:

        #/* https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list */
        content_lines = f.readlines()

        #/* you may also want to remove whitespace characters like `\n` at the end of each line */
        content_lines = [x.strip() for x in content_lines]

        #/* look for lockfile */
        for x in content_lines:

            if x.startswith('backup'):

                #/* rsnapconfig paremeters are split by TAB */
                tmp = x.split('\t')
                #print(tmp)

                #/* minimum required paremeters num, including tmp[0]="backup": 3 */
                if len(tmp) >= 3:

                    #/* source and dest directory */
                    srcdir = tmp[1]
                    destdir = tmp[2]



                    #/* identify for source filetype */
                    #/* (6) starting with rsync:// */
                    if srcdir.lower().startswith('rsync://'):
                        type_ = 'rsync'

                    #/* (8) starting with lvm:// */
                    elif srcdir.lower().startswith('lvm://'):
                        type_ = 'lvm'

                    #/* (3), (4), (5) contais : */
                    elif ':' in srcdir:
                        type_ = 'ssh'

                    #/* otherwise, local is used */
                    else:
                        type_ = 'local'



                    #/* TODO extra rsync parameters */
                    rsync_extra_params = None
                    #if len(tmp) >= 4:
                    #    pass

                    result.append((type_, srcdir, destdir, rsync_extra_params))

    return result


if __name__ == '__main__':
    print(simple_argparse(rsnapconfig_getparam_backup, sys.argv[1:]))
