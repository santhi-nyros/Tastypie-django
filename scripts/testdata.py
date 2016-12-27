#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially casted so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones inteact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# ./manage.py dumpscript api.Post
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script
import os, sys
from django.db import transaction

class BasicImportHelper(object):

    def pre_import(self):
        pass

    @transaction.atomic
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(self, original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = { pk_name: pk_value }
        the_obj = the_class.objects.get(**search_data)
        #print(the_obj)
        return the_obj


    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print(the_obj.__class__)
            print(" ")
            print(the_obj.__dict__)
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    import import_helper
    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type("DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper ) , {} )()
except ImportError as e:
    # From Python 3.3 we can check e.name - string match is for backward compatibility.
    if 'import_helper' in str(e):
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)

def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()

def import_data():
    # Initial Imports

    # Processing model: api.models.Post

    from api.models import Post

    api_post_1 = Post()
    api_post_1.text = u'Good Morning....all'
    api_post_1.image = u'static/posts/baby_kQNfSKT.jpeg'
    api_post_1.video = u'undefined'
    api_post_1.created = dateutil.parser.parse("2016-11-23T02:58:47.002719+00:00")
    api_post_1 = importer.save_or_locate(api_post_1)

    api_post_2 = Post()
    api_post_2.text = u'Hello world'
    api_post_2.image = u'static/posts/silde5.jpg'
    api_post_2.video = u'undefined'
    api_post_2.created = dateutil.parser.parse("2016-11-23T02:59:22.787073+00:00")
    api_post_2 = importer.save_or_locate(api_post_2)

    api_post_3 = Post()
    api_post_3.text = u'hi friends'
    api_post_3.image = u'static/posts/true_Jqj4Fvb.jpg'
    api_post_3.video = u'undefined'
    api_post_3.created = dateutil.parser.parse("2016-11-23T02:59:39.696062+00:00")
    api_post_3 = importer.save_or_locate(api_post_3)

    api_post_4 = Post()
    api_post_4.text = u'Be happy'
    api_post_4.image = u'static/posts/jpg_OCcQaIn.jpg'
    api_post_4.video = u'undefined'
    api_post_4.created = dateutil.parser.parse("2016-11-23T03:00:02.075318+00:00")
    api_post_4 = importer.save_or_locate(api_post_4)

    api_post_5 = Post()
    api_post_5.text = u''
    api_post_5.image = u'static/posts/image3_PJhlvpb.jpeg'
    api_post_5.video = u'undefined'
    api_post_5.created = dateutil.parser.parse("2016-11-23T03:00:08.232111+00:00")
    api_post_5 = importer.save_or_locate(api_post_5)

    api_post_6 = Post()
    api_post_6.text = u''
    api_post_6.image = u'static/posts/jpg_2.jpg'
    api_post_6.video = u'undefined'
    api_post_6.created = dateutil.parser.parse("2016-11-23T03:00:15.139267+00:00")
    api_post_6 = importer.save_or_locate(api_post_6)

    api_post_7 = Post()
    api_post_7.text = u''
    api_post_7.image = u'static/posts/jpg_4_HkyMv8n.jpg'
    api_post_7.video = u'undefined'
    api_post_7.created = dateutil.parser.parse("2016-11-23T03:00:20.395528+00:00")
    api_post_7 = importer.save_or_locate(api_post_7)

    api_post_8 = Post()
    api_post_8.text = u''
    api_post_8.image = u'static/posts/jpg_3.jpg'
    api_post_8.video = u'undefined'
    api_post_8.created = dateutil.parser.parse("2016-11-23T03:00:26.072965+00:00")
    api_post_8 = importer.save_or_locate(api_post_8)

    api_post_9 = Post()
    api_post_9.text = u''
    api_post_9.image = u'static/posts/jpg_5_QFamYh9.jpg'
    api_post_9.video = u'undefined'
    api_post_9.created = dateutil.parser.parse("2016-11-23T03:00:32.480778+00:00")
    api_post_9 = importer.save_or_locate(api_post_9)

    api_post_10 = Post()
    api_post_10.text = u''
    api_post_10.image = u'static/posts/n3_AitVGDW.jpeg'
    api_post_10.video = u'undefined'
    api_post_10.created = dateutil.parser.parse("2016-11-23T03:00:41.105164+00:00")
    api_post_10 = importer.save_or_locate(api_post_10)

    api_post_11 = Post()
    api_post_11.text = u''
    api_post_11.image = u'static/posts/t4_mgmO9Ke.jpeg'
    api_post_11.video = u'undefined'
    api_post_11.created = dateutil.parser.parse("2016-11-23T03:00:50.375267+00:00")
    api_post_11 = importer.save_or_locate(api_post_11)

    api_post_12 = Post()
    api_post_12.text = u''
    api_post_12.image = u'static/posts/t2.jpeg'
    api_post_12.video = u'undefined'
    api_post_12.created = dateutil.parser.parse("2016-11-23T03:00:57.704855+00:00")
    api_post_12 = importer.save_or_locate(api_post_12)

    api_post_13 = Post()
    api_post_13.text = u''
    api_post_13.image = u'static/posts/roses_meQwCuv.jpg'
    api_post_13.video = u'undefined'
    api_post_13.created = dateutil.parser.parse("2016-11-23T03:01:06.036182+00:00")
    api_post_13 = importer.save_or_locate(api_post_13)

    api_post_14 = Post()
    api_post_14.text = u'undefined'
    api_post_14.image = u'static/posts/index_OOnIY7n.jpeg'
    api_post_14.video = u'undefined'
    api_post_14.created = dateutil.parser.parse("2016-11-23T03:18:15.427418+00:00")
    api_post_14 = importer.save_or_locate(api_post_14)

    api_post_15 = Post()
    api_post_15.text = u'undefined'
    api_post_15.image = u'static/posts/jpg_6.jpg'
    api_post_15.video = u'undefined'
    api_post_15.created = dateutil.parser.parse("2016-11-23T04:04:05.008619+00:00")
    api_post_15 = importer.save_or_locate(api_post_15)

    api_post_16 = Post()
    api_post_16.text = u'undefined'
    api_post_16.image = u'undefined'
    api_post_16.video = u'static/videos/34343_4wVMezl.mp4'
    api_post_16.created = dateutil.parser.parse("2016-11-23T04:05:45.527933+00:00")
    api_post_16 = importer.save_or_locate(api_post_16)

    api_post_17 = Post()
    api_post_17.text = u'undefined'
    api_post_17.image = u'static/posts/y1_kcWYR1y.jpeg'
    api_post_17.video = u'undefined'
    api_post_17.created = dateutil.parser.parse("2016-11-23T04:07:31.583524+00:00")
    api_post_17 = importer.save_or_locate(api_post_17)

    api_post_18 = Post()
    api_post_18.text = u'undefined'
    api_post_18.image = u'undefined'
    api_post_18.video = u'static/videos/333.mp4'
    api_post_18.created = dateutil.parser.parse("2016-11-23T04:13:21.787995+00:00")
    api_post_18 = importer.save_or_locate(api_post_18)

    api_post_19 = Post()
    api_post_19.text = u'Good Evening...'
    api_post_19.image = u'static/posts/y3_CUqaofm.jpeg'
    api_post_19.video = u'undefined'
    api_post_19.created = dateutil.parser.parse("2016-11-24T09:50:09.296224+00:00")
    api_post_19 = importer.save_or_locate(api_post_19)

    api_post_20 = Post()
    api_post_20.text = u'Good Morning'
    api_post_20.image = u'static/posts/jpg_6_t7bR2ZH.jpg'
    api_post_20.video = u'undefined'
    api_post_20.created = dateutil.parser.parse("2016-11-28T03:07:40.940745+00:00")
    api_post_20 = importer.save_or_locate(api_post_20)

    api_post_21 = Post()
    api_post_21.text = u'Have a nice day'
    api_post_21.image = u'static/posts/n5_y2hyn8F.jpeg'
    api_post_21.video = u'undefined'
    api_post_21.created = dateutil.parser.parse("2016-11-28T04:53:39.516626+00:00")
    api_post_21 = importer.save_or_locate(api_post_21)

    api_post_22 = Post()
    api_post_22.text = u'dsfsfs'
    api_post_22.image = u'undefined'
    api_post_22.video = u'undefined'
    api_post_22.created = dateutil.parser.parse("2016-11-29T11:50:59.071518+00:00")
    api_post_22 = importer.save_or_locate(api_post_22)

    api_post_23 = Post()
    api_post_23.text = u'My Dog'
    api_post_23.image = u'static/posts/images.jpeg'
    api_post_23.video = u'undefined'
    api_post_23.created = dateutil.parser.parse("2016-11-30T10:32:58.170744+00:00")
    api_post_23 = importer.save_or_locate(api_post_23)

