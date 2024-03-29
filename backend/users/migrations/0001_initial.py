# Generated by Django 3.2 on 2023-06-06 16:34

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.password_validation
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import django.utils.timezone
import users.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(db_index=True, error_messages={'unique': 'Это имя уже занято!'}, help_text='Введите логин', max_length=150, unique=True, validators=[users.validators.validate_non_reserved, users.validators.validate_username_allowed_chars], verbose_name='Логин')),
                ('email', models.EmailField(db_index=True, error_messages={'unique': 'Этот email уже зарегистрирован!'}, help_text='введите адрес электронной почты', max_length=254, unique=True, verbose_name='адрес электронной почты')),
                ('first_name', models.CharField(blank=True, help_text='Введите имя', max_length=150, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, help_text='Введите фамилию', max_length=150, verbose_name='Фамилия')),
                ('password', models.CharField(help_text='Введите пароль. Обязательно. Не более 150 символов', max_length=150, validators=[django.contrib.auth.password_validation.validate_password], verbose_name='Пароль')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('created',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта, на которого подписываются')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик на автора рецепта')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
                'ordering': ('-author_id',),
            },
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_follow'),
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, user=django.db.models.expressions.F('author')), name='users_subscription_prevent_self_follow'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('email', 'username'), name='unique_user'),
        ),
    ]
