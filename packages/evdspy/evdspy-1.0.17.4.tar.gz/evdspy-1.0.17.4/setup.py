# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evdspy',
 'evdspy.EVDSlocal',
 'evdspy.EVDSlocal.common',
 'evdspy.EVDSlocal.components',
 'evdspy.EVDSlocal.config',
 'evdspy.EVDSlocal.console',
 'evdspy.EVDSlocal.examples',
 'evdspy.EVDSlocal.helper',
 'evdspy.EVDSlocal.initial',
 'evdspy.EVDSlocal.initial_setup',
 'evdspy.EVDSlocal.log_classes',
 'evdspy.EVDSlocal.manual_requests',
 'evdspy.EVDSlocal.messages',
 'evdspy.EVDSlocal.requests_',
 'evdspy.EVDSlocal.series_format',
 'evdspy.EVDSlocal.series_format.stats',
 'evdspy.EVDSlocal.session',
 'evdspy.EVDSlocal.setup_project',
 'evdspy.EVDSlocal.state',
 'evdspy.EVDSlocal.stats',
 'evdspy.EVDSlocal.tests',
 'evdspy.EVDSlocal.utils']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.5.1,<13.0.0']

setup_kwargs = {
    'name': 'evdspy',
    'version': '1.0.17.4',
    'description': 'Get data from EVDS API and organize your local work environment with systematical approach. Using caching facility, this package makes less request from the server.',
    'long_description': '\n[![Python package](https://github.com/SermetPekin/evdspy/actions/workflows/python-package.yml/badge.svg)](https://github.com/SermetPekin/evdspy/actions/workflows/python-package.yml)\n[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)\n[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)\n[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)\n\n\n## evdspy\n\n### installation\n\n    pip install evdspy\n\n### importing\n\n    from evdspy import *  \n    check()\n    get()\n    help_evds()\n\nor\n\n    import evdspy as ev \n    ev.check()\n    ev.get()\n    ev.help_evds()\n\n### menu\n\n    from evdspy import *\n    menu()\n\nor\n\n    import evdspy as ev\n    ev.menu()\n\n    Menu function will display a friendly menu to setup project, creating output folders and some setup files to\n    create some set of series to make a request and download from EVDS server save your api key to get data from EVDS.\n    Than it will convert this data to a pandas dataframe and create some folders on your local area.\n\n\n### menu()\n\n**************************************************\n\n                    M E N U\n\n**************************************************\n\n               1. check setup\n               2. setup\n               3. create user options file\n               4. create series file\n               5. add new series group\n               6. get data\n               7. help\n               8. show api key\n               9. save api key to file\n               10. console\n                                  Selection ?\n\n#### FROM THE CONSOLE\n### cache choice (default:daily)\n\n    # hourly :  no new request within an hour with same URL combination\n    # nocache: new request upon each call without checking cache results\n    # daily : program will use local data requested earlier if data was saved same day.    \n\n    create_series_file()\n\nor\n\n    csf()\n\nor from selection menu choose create series file (config_series.cfg) option.\n\nWith this command program will create file similar to below. You may later add new series info\nor modify this file or delete and create a new on from menu or console using commands summarized in this file.\n\n#### config_series.cfg content example\n\n    #Series_config_file    \n    E V D S P Y  _  C O N F I G  _  F I L E  ---------------------------------------------\n    #\n    # This file will be used by evdspy package (python) in order to help updating \n    # your series. \n    # Script will be adding this file when you setup a new project.\n    # Deleting or modifying its content may require to setup configuration from the beginning\n    # ----------------------------------------------------------------------------------------\n    #\n    #About alternative params \n    # ----------------------------------------------------------------------------------------\n    \n    \n              Frequencies\n              -----------------\n    \n              Daily: 1\n              Business: 2\n              Weekly(Friday): 3\n              Twicemonthly: 4\n              Monthly: 5\n              Quarterly: 6\n              Semiannual: 7\n              Annual: 8\n    \n    \n              `Formulas`s\n              -----------------\n    \n              Level: 0\n              Percentage change: 1\n              Difference: 2\n              Year-to-year Percent Change: 3\n              Year-to-year Differences: 4\n              Percentage Change Compared to End-of-Previous Year: 5\n              Difference Compared to End-of-Previous Year : 6\n              Moving Average: 7\n              Moving Sum: 8\n    \n              Aggregate types\n              -----------------\n    \n              Average: avg,\n              Minimum: min,\n              Maximum: max\n              Beginning: first,\n              End: last,\n              Cumulative: sum\n    \n    \n    #Begin_series\n    \n    ---Series---------------------------------\n    foldername : visitors\\annual\n    abs_path : visitors\\annual \n    subject  : visitors\n    prefix   : EVPY_\n    frequency : 8 # annually\n    formulas : 0 # Level\n    aggregateType : avg\n    ------------SERIES CODES------------------\n    TP.ODEMGZS.BDTTOPLAM\n    TP.ODEMGZS.ABD\n    TP.ODEMGZS.ARJANTIN\n    TP.ODEMGZS.BREZILYA\n    TP.ODEMGZS.KANADA\n    TP.ODEMGZS.KOLOMBIYA\n    TP.ODEMGZS.MEKSIKA\n    TP.ODEMGZS.SILI\n    ------------/SERIES CODES------------------\n    ---/Series---------------------------------\n    --++--\n    \n    ---Series---------------------------------\n    foldername : visitors\\monthly\n    abs_path : C:\\Users\\User\\SeriesData\\visitors\\monthly \n    subject  : visitors\n    prefix   : EVPY_\n    frequency : 5 # Monthly\n    formulas : 0 # Level\n    aggregateType : avg\n    ------------SERIES CODES------------------\n    TP.ODEMGZS.BDTTOPLAM\n    TP.ODEMGZS.ABD\n    TP.ODEMGZS.ARJANTIN\n    TP.ODEMGZS.BREZILYA\n    TP.ODEMGZS.KANADA\n    TP.ODEMGZS.KOLOMBIYA\n    TP.ODEMGZS.MEKSIKA\n    TP.ODEMGZS.SILI\n    ------------/SERIES CODES------------------\n    ---/Series---------------------------------\n    --++--\n\n### initial commands\n\n    from evdspy.main import * \n\n#### help_evds():\n\n    see a list of popular commands of this package to create setup folder and files, and request data.\n    \n\n#### check():\n    check setup and create required folders and see current installation status.\n\n#### setup_now()   :\n\n    creates folders and files\n    ____Folders_______________\n            `pickles` \n                will be used to store some request results to ovoid redundant requests from the EVDS api \n    \n            `SeriesData` \n                to save results of requests or caches to an excel file using information on user option files\n    ____Files_______________\n            `options.cfg`\n                a text file consisting global user options such as start date, end date and caching period.\n\n        \n            `config_series.cfg`\n                this file consists information regarding individual sets of series. From the menu user can add\n            new series that will be requesting from the server. Program will produce on for example and this file\n            can be modified and new sets of series can be added following the example format.\n            \n    from evdspy.main import *\n    setup_now()\n\n\n#### get():\n\n    # this will check for your current series.txt file\n    # if proper data series codes are given it will either download them\n    # or use the latest cache from your local environment\n    # to provide other cache options such as nocache / daily / hourly you may change your\n    # defaults or give arguments such as\n\n        get()\n\n\n#### save( key = "xxxxyyy"):\n\n    Program will store your api key in your environment in a safe folder\n    called APIKEY_FOLDER\n    and only use it when you run a new request which was not requested \n    recently depending on your cache preference.\n\n.\n\n       save_apikey("MyApiKey")\n\n#### save()\n\n        When you call it with not argument program will ask for your key and do the same \n    above \n\n#### create_series_file()  or csf() :\n\n--------------------------------\n\n    # creates example `config_series.cfg` file on your work environment. evdspy input file (EIF) formatted \n    # you may modify it according to your preferences.  \n\n--------------------------------\n\n    create_series_file()\n    # or\n    csf()\n\n# MENU\n### menu()\n\n**************************************************\n\n                    M E N U\n\n**************************************************\n\n               1. check setup\n               2. setup\n               3. create user options file\n               4. create series file\n               5. add new series group\n               6. get data\n               7. help\n               8. show api key\n               9. save api key to file\n               10. exit (from menu to console)\n    ......................... Selection ?',
    'author': 'Sermet Pekin',
    'author_email': 'sermet.pekin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/SermetPekin/evdspy-repo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
