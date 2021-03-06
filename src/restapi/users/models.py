from django import forms
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.forms import SimpleArrayField
from django.contrib.postgres.fields import ArrayField

import uuid
import datetime


def jwt_get_secret_key(user_model):
	return user_model.jwt_secret


class UserManager(BaseUserManager):
	def create_user(self, username, full_name, email, password=None):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not username:
			raise ValueError('Username must be present.')

		user = self.model(
			username=username,
			full_name=full_name,
			email=email
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, full_name, email, password):
		"""
		Creates and saves a superuser with the given email and
		password.
		"""
		user = self.create_user(
			username,
			password=password,
			full_name=full_name,
			email=email
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser, PermissionsMixin):
	bio = models.CharField(max_length=255, null=True)
	birth_date = models.DateField(null=True)
	email = models.EmailField(
			max_length=255, unique=True, blank=True, null=True)
	full_name = models.CharField(max_length=30, blank=True, null=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	location = models.CharField(max_length=15, null=True)
	profile_pic = models.URLField(default='/assets/user.png')
	social_links = ArrayField(models.CharField(max_length=100, blank=True, null=True), default=list)
	technologies = ArrayField(models.CharField(max_length=20, blank=True, null=True), default=list)
	username = models.CharField(
		verbose_name='Username', max_length=35, unique=True)
	website = models.URLField(null=True)
	jwt_secret = models.UUIDField(default=uuid.uuid4)
	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['full_name', 'email']

	def __str__(self):
		return self.username