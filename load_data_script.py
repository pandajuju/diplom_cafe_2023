import json
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist


def load_data():
    with open('data.json', 'r') as file:
        data = json.load(file)

        for app_name, items in data.items():
            for model_name, model_items in items.items():
                Model = apps.get_model(app_name, model_name)

                for item in model_items:
                    try:
                        obj = Model.objects.get(pk=item.get('id'))
                    except ObjectDoesNotExist:
                        obj = Model()

                    for field, value in item.items():
                        setattr(obj, field, value)

                    obj.save()


if __name__ == '__main__':
    load_data()
