from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ._0errors import *
from ._0imports import *


class Database:

    def __init__(self, database_name, vital=False, date_to_update='daily', force_update=False, ask_size=None):

        package_name = 'iraclis'
        info_file_name = '_0database.pickle'
        directory_name = 'database'
        last_update_file_name = 'database_last_update.txt'

        info_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), info_file_name)
        package_path = os.path.join(os.path.expanduser('~'), '.{0}'.format(package_name))
        if not os.path.isdir(package_path):
            os.mkdir(package_path)
        directory_path = os.path.join(package_path, '{0}_{1}'.format(database_name, directory_name))
        last_update_file_path = os.path.join(package_path, '{0}_{1}'.format(database_name, last_update_file_name))

        if date_to_update == 'daily':
            date_to_update = int(time.strftime('%y%m%d'))
        else:
            date_to_update = int(date_to_update)

        if os.path.isdir(directory_path):
            if force_update or len(glob.glob(os.path.join(directory_path, '*'))) == 0:
                shutil.rmtree(directory_path)
                os.mkdir(directory_path)
                update = True
            else:
                if not os.path.isfile(last_update_file_path):
                    update = True
                elif int(open(last_update_file_path).readlines()[0]) < date_to_update:
                    update = True
                else:
                    update = False
        else:
            os.mkdir(directory_path)
            update = True

        if update and ask_size:
            if input('Downloading {0} database (up to {1})... proceed with download now? (y/n): '.format(
                    database_name, ask_size)) == 'y':
                update = True
            else:
                update = False

        if update:
            # noinspection PyBroadException
            try:
                print('\nDownloading {0} database...'.format(database_name))

                dbx_files = pickle.load(open(info_file_path, 'rb'))
                dbx_files = dbx_files['{0}_{1}'.format(database_name, directory_name)]

                for i in glob.glob(os.path.join(directory_path, '*')):
                    if os.path.split(i)[1] not in dbx_files:
                        os.remove(i)

                for i in dbx_files:
                    if not os.path.isfile(os.path.join(package_path, dbx_files[i]['local_path'])):
                        print(i)
                        urlretrieve(dbx_files[i]['link'], os.path.join(package_path, dbx_files[i]['local_path']))

                if database_name == 'clablimb':
                    xx = pickle.load(open(glob.glob(os.path.join(directory_path, '*'))[0], 'rb'))
                    for i in xx:
                        w = open(os.path.join(directory_path, i), 'w')
                        w.write(xx[i])
                        w.close()

                w = open(last_update_file_path, 'w')
                w.write(time.strftime('%y%m%d'))
                w.close()

            except:
                print('\nDownloading {0} database failed. A download will be attempted next time.'.format(
                    database_name))
                pass

        if (not os.path.isdir(directory_path) or
                len(glob.glob(os.path.join(directory_path, '*'))) == 0):
            if vital:
                raise IraclisLibraryError('{0} database not available.'.format(database_name))
            else:
                print('\n{0} features cannot be used.'.format(database_name))
                self.path = False
        else:
            self.path = directory_path


class Databases:

    def __init__(self):

        self.wfc3 = Database('wfc3', vital=True, date_to_update='181212').path


databases = Databases()
