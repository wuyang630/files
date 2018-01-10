#!/usr/bin/env python3
import csv
import logging
import argparse
import json
import os
import errno
import datetime
from peewee import SqliteDatabase
from models import database_proxy, HeatmapHeatvalue, HeatmapStayvalue, FlowFlow, PeoplePerson

log = logging


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)


def _export_csv(file, model, fields, date, hour=None):
    """

    Args:
        file:
        model:
        fields:
        date:
        hour:

    Returns:

    """
    log.info('start export from {0}. filter date {1} hour {2}'.format(model.__name__, date.date(), hour))
    if hour is None:
        query = model.select().where((model.time.year == date.year) &
                                     (model.time.month == date.month) &
                                     (model.time.day == date.day)).dicts()
    else:
        query = model.select().where((model.time.year == date.year) &
                                     (model.time.month == date.month) &
                                     (model.time.day == date.day) &
                                     (model.time.hour == hour)).dicts()

    log.info('generating {0}'.format(file))

    with open(file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        count = 0
        for record in query:
            count += 1
            if count % 1000 == 1:
                log.debug('{}: {}'.format(count, json.dumps(record, cls=DateTimeEncoder)[0:120]))
            writer.writerow(record)
    log.info('{} exported. Total {} records in the table'.format(count, model.select().count()))


def _export_heat_map(file, date, hour=None):
    fieldnames = ['id', 'rect', 'x', 'y', 'time', 'hot', 'created', 'updated', 'is_deleted', 'deleted_time']
    _export_csv(file, HeatmapHeatvalue, fieldnames, date, hour=hour)


def _export_stay_map(file, date, hour=None):
    fieldnames = ['id', 'rect', 'x', 'y', 'time', 'stay', 'created', 'updated', 'is_deleted', 'deleted_time']
    _export_csv(file, HeatmapStayvalue, fieldnames, date, hour=hour)


def _export_flow(file, date, hour=None):
    # FlowFlow
    fieldnames = ['id', 'area', 'time', 'flow_in', 'flow_out', 'created', 'updated', 'is_deleted', 'deleted_time']
    _export_csv(file, FlowFlow, fieldnames, date, hour=hour)


def _export_people(file, date, hour=None):
    fieldnames = ['id', 'area', 'time', 'age', 'gender', 'created', 'updated', 'is_deleted', 'deleted_time']
    _export_csv(file, PeoplePerson, fieldnames, date, hour=hour)


def _export(directory, date, hour=None):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    _export_heat_map(os.path.join(directory, 'heatmap.csv'), date, hour)
    _export_stay_map(os.path.join(directory, 'staymap.csv'), date, hour)
    _export_flow(os.path.join(directory, 'flow.csv'), date, hour)
    _export_people(os.path.join(directory, 'people.csv'), date, hour)


def _import_csv(file, model, bulk_number=100, typed_fileds=None):
    log.info('reading {}'.format(file))
    rows = []
    with open(file, newline='') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            count += 1
            for key in ['time', 'updated', 'created', 'deleted_time']:
                date_string = row.get(key, '')
                try:
                    if date_string is None or len(date_string) == 0:
                        row[key] = None
                    else:
                        dt = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")
                        row[key] = dt
                except ValueError:
                    row[key] = None
            for key in ['is_deleted']:
                b_string = row.get(key, None)
                if b_string is not None:
                    row[key] = (b_string == 'True')
            if typed_fileds is not None:
                for t, fields in typed_fileds.items():
                    for key in fields:
                        s = row.get(key, None)
                        if s is not None:
                            row[key] = t(s)

            if count % 1000 == 1:
                log.debug('{}: {} {}'.format(count, row['id'], row['time']))
            rows.append(row)

    with database_proxy.atomic():
        for idx in range(0, len(rows), bulk_number):
            model.insert_many(rows[idx:idx + bulk_number]).execute()

    log.info('{} done'.format(count))


def _import_heat_map(file, bulk_number=100):
    _import_csv(file, HeatmapHeatvalue, bulk_number, typed_fileds={int: {'x', 'y', 'hot'}})


def _import_stay_map(file, bulk_number=100):
    _import_csv(file, HeatmapStayvalue, bulk_number, typed_fileds={int: {'x', 'y', 'stay'}})


def _import_flow(file, bulk_number=100):
    _import_csv(file, FlowFlow, bulk_number, typed_fileds={int: {'flow_in', 'flow_out'}})


def _import_people(file, bulk_number=100):
    _import_csv(file, PeoplePerson, bulk_number, typed_fileds={int: {'age', 'gender'}})


def _import(folder, bulk_number=100):
    _import_heat_map(os.path.join(folder, 'heatmap.csv'), bulk_number)
    _import_stay_map(os.path.join(folder, 'staymap.csv'), bulk_number)
    _import_flow(os.path.join(folder, 'flow.csv'), bulk_number)
    _import_people(os.path.join(folder, 'people.csv'), bulk_number)


if __name__ == '__main__':

    for n in ['peewee', 'PIL', 'Django']:
        logging.getLogger(n).setLevel(logging.WARN)

    CMDS = ['export', 'import']
    DEFAULT_SQLITE_FILE = 'db.sqlite3'
    parser = argparse.ArgumentParser(description='Help you manage django managed database.')
    parser.add_argument('-l', '--log', help='Log level', metavar='level')

    subparsers = parser.add_subparsers(help='Actions', dest='cmd', metavar='COMMAND')
    parser_in = subparsers.add_parser('import', help='Import csv to databse.')
    parser_ex = subparsers.add_parser('export', help='Export reports in databse to csv')

    parser_ex.add_argument('-o', '--output', help='Path to output csv files', metavar='path', default='.')
    parser_ex.add_argument('-d', '--date', help='Date to export.', required=True)
    parser_ex.add_argument('-t', '--hour', help='Optional. Hour to export.', type=int)
    parser_ex.add_argument('--sqlite', help='Path to sqlite database. Default is db.sqlite3', metavar='database')

    parser_in.add_argument('-i', '--input', help='Path to import csv files', metavar='path', default='.')
    parser_in.add_argument('-b', '--bulk', help='Bulk number to insert data.', metavar='number')
    parser_in.add_argument('--sqlite', help='Path to sqlite database. Default is db.sqlite3', metavar='database')

    args = parser.parse_args()
    _level = logging.INFO
    if args.log is not None:
        _level = logging.getLevelName(args.log.upper())

    logging.basicConfig(level=_level,
                        format='[%(asctime)s %(levelname)s %(relativeCreated)d %(module)s:%(lineno)d]: %(message)s')

    if args.cmd == CMDS[0]:

        if args.date is not None and args.output is not None:
            database = SqliteDatabase(args.sqlite or DEFAULT_SQLITE_FILE, **{})
            log.info('{} from {}'.format(args.cmd, args.sqlite))
            database_proxy.initialize(database)
            if args.hour is not None:
                d = datetime.datetime.strptime('{0} {1}'.format(args.date, args.hour), '%Y-%m-%d %H')
                _export(args.output, d, args.hour)
            else:
                d = datetime.datetime.strptime(args.date, '%Y-%m-%d')
                _export(args.output, d)
        else:
            parser.print_help()
    elif args.cmd == CMDS[1]:
        if args.input is not None:
            database = SqliteDatabase(args.sqlite or DEFAULT_SQLITE_FILE, **{})
            log.info('{} to {}'.format(args.cmd, args.sqlite))
            database_proxy.initialize(database)
            _import(args.input)
        else:
            parser.print_help()
    else:
        parser.print_help()
