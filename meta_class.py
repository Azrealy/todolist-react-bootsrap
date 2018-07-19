# -*- coding: utf-8 -*-


class Field(object):

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return "<%s %s %s>" % (self.__class__.__name__, self.name, self.column_type)

class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, "int")


class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, "varchar(255)")


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return type.__new__(cls, name, bases, attrs)

        print("Fond Model: %s" % name)


        mappings = {}
        for k, v in attrs.items():
            if isinstance(v, Field):
                print("Fond Field: %s => %s" % (k, v))
                mappings[k] = v


        for k in mappings.keys():
            attrs.pop(k)

        attrs["__mappings__"] = mappings  
        attrs["__table__"] = name   
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            params.append("?")
            args.append(getattr(self, k, None))
        sql = "insert into %s (%s) VALUES (%s)" % (
            self.__table__, ",".join(fields), ",".join(params))
        print("sql: %s" % sql)
        print("args: %s" % args)


class User(Model):
    id = IntegerField("id")
    name = StringField("name")
    email = StringField("email")
    password = StringField("password")


if __name__ == '__main__':

    user = User(id=1, name="Tom", email="12345@qq.com", password="123456")

    user.save()

    print(user.name)
    print(user["name"])
    user.name = "jack"
    print(user.name)
