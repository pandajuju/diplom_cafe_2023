import json
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist


def load_data():
    with open('data.json', 'r') as file:
        data = json.load(file)

        for app_data in data:
            app_name = app_data.get("app_name")
            if not app_name:
                continue

            for model_name, model_items in app_data.get("items", {}).items():
                if app_name == "coffee":
                    Model = apps.get_model("coffee", model_name)
                elif app_name == "main_app":
                    Model = apps.get_model("main_app", model_name)

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
