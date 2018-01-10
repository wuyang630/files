## Prepare:
```bash
$ pip install peewee
```

## Export:
```bash
$ python tool.py --l debug export --sqlite db.sqlite3 --output data --date 2017-12-30 --hour 8
```

## Import:
```bash
$ python tool.py --l debug import --sqlite db.sqlite3 --input data
```

## Help:
```bash
$ python tool.py -h
usage: tool.py [-h] [-l level] COMMAND ...

Help you manage django managed database.

positional arguments:
  COMMAND               Actions
    import              Import csv to databse.
    export              Export reports in databse to csv

optional arguments:
  -h, --help            show this help message and exit
  -l level, --log level
                        Log level


$ python tool.py export -h
usage: tool.py export [-h] [-o path] -d DATE [-t HOUR] [--sqlite database]

optional arguments:
  -h, --help            show this help message and exit
  -o path, --output path
                        Path to output csv files
  -d DATE, --date DATE  Date to export.
  -t HOUR, --hour HOUR  Optional. Hour to export.
  --sqlite database     Path to sqlite database. Default is db.sqlite3



$ python tool.py import -h
usage: tool.py import [-h] [-i path] [-b number] [--sqlite database]

optional arguments:
  -h, --help            show this help message and exit
  -i path, --input path
                        Path to import csv files
  -b number, --bulk number
                        Bulk number to insert data.
  --sqlite database     Path to sqlite database. Default is db.sqlite3


```
