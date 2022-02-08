from django.db import migrations
from api.user.models import CoustomUser


class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CoustomUser(name="balaji",
                           email="balajikotni4@gmail.com",
                           is_staff=True,
                           is_superuser=True,
                           phone="7032874146",
                           )
        user.set_password("balaji1656")
        user.save()
    dependencies = []

    operations = [migrations.RunPython(seed_data)]
