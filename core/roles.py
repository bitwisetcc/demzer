from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    available_permissions = {"create_user": True, "see_alerts": True}


class Coordinator(AbstractUserRole):
    available_permissions = {"see_alerts": True}


class Secretary(AbstractUserRole):
    available_permissions = {"create_user": True}


class Staff(AbstractUserRole):
    available_permissions = {}


class Teacher(AbstractUserRole):
    available_permissions = {"create_assessment": True, "crate_attendance": True}


class Student(AbstractUserRole):
    available_permissions = {}
