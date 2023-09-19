from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


GROUPS = {
    "Admins":{
        "user" : ["add","delete","change","view"],
        "group": ["add","delete","change","view"],
        "log entry": ["add","delete","change","view"],
        "trashed questions": ["add","delete","change","view"],
        "user_logs": ["add","delete","change","view"],
        "answers": ["add","delete","change","view"],
        "company": ["add","delete","change","view"],
        "context": ["add","delete","change","view"],
        "conversation": ["add","delete","change","view"],
        "document": ["add","delete","change","view"],
        "frequency": ["add","delete","change","view"],
        "rating": ["add","delete","change","view"],
        "tag": ["add","delete","change","view"],
        "untagged questions": ["add","delete","change","view"],
        },
    "Maintenance":{
        "user" : ["view"],
        "group": ["view"],
        "log entry": ["add","delete","change","view"],
        "trashed questions": ["add","delete","change","view"],
        "user_logs": ["add","delete","change","view"],
        "answers": ["add","delete","change","view"],
        "company": ["add","delete","change","view"],
        "context": ["add","delete","change","view"],
        "conversation": ["add","delete","change","view"],
        "document": ["add","delete","change","view"],
        "frequency": ["add","delete","change","view"],
        "rating": ["add","delete","change","view"],
        "tag": ["add","delete","change","view"],
        "untagged questions": ["add","delete","change","view"],
        }
}

class Command(BaseCommand):
    help = "Create groups"

    def handle(self, *args, **options):
        for group_name in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group_name)

            for app_model in GROUPS[group_name]:
                for permission_name in GROUPS[group_name][app_model]:
                    name = "Can {} {}".format(permission_name, app_model)

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        continue

                    new_group.permissions.add(model_add_perm)

                    self.stdout.write("Adding {} to {}".format(model_add_perm,new_group))