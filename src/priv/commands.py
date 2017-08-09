from app import manager, db
import yaml


from .models import Record


@manager.command
def export(output=None, book_id=None):
    "Export data"
    if book_id is None:
        query = Record.query
    else:
        query = Record.query.filter_by(book_id=book_id)
    records = query.all()
    export_data = {
        'version': "2.5.0",
    }
    export_data['records'] = [r.export() for r in records]

    print(yaml.dump(export_data, default_flow_style=False, allow_unicode=True))
    if output is not None:
        print("Save to \"%s\"" % (output))
        with open(output, "w") as outfile:
            yaml.dump(export_data, outfile, default_flow_style=False, allow_unicode=True)
        print("Saved to %s" % (output, ))


@manager.command
def import_yml(input=None):
    "Import data"
    if input is None:
        print("No data to import")
        return
    else:
        with open(input, 'r') as infile:
            try:
                print("Load from \"%s\"" % (input))
                data = yaml.load(infile)
                # print(data)
                version = data.get('version')
                if version == "2.5.0":
                    print(version)
                    records = data.get('records', [])
                    for r in records:
                        record_id = r.get('reg_id')
                        record = Record.query.filter_by(reg_id=record_id).first()
                        if record is None:
                            record = Record(reg_id=record_id)
                        record.import_yml(r)
                        print("%s:\t%s" % (r.get('reg_id'), r))
                        db.session.add(record)
                    db.session.commit()
                print("Loaded from \"%s\"" % (input))
            except yaml.YAMLError as exc:
                print(exc)
