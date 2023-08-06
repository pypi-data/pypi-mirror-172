class DataClayException(Exception):
    """Base class for exceptions in this module."""

    pass


###########
# Account #
###########


class AccountError(DataClayException):
    def __init__(self, username):
        self.username = username


class AccountDoesNotExistError(AccountError):
    def __str__(self):
        return f"Account {self.username} does not exist"


class AccountAlreadyExistError(AccountError):
    def __str__(self):
        return f"Account {self.username} already exist"


class AccountInvalidCredentialsError(AccountError):
    def __str__(self):
        return f"Account {self.username} invalid credentials"


###########
# Dataset #
###########


class DatasetError(DataClayException):
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name


class DatasetDoesNotExistError(DatasetError):
    def __str__(self):
        return f"Dataset {self.dataset_name} does not exist"


class DatasetAlreadyExistError(DatasetError):
    def __str__(self):
        return f"Dataset {self.dataset_name} already exist"


class DatasetIsNotAccessibleError(DatasetError):
    def __init__(self, dataset_name, username):
        self.dataset_name = dataset_name
        self.username = username

    def __str__(self):
        return f"Dataset {self.dataset_name} is not accessible by {self.username}"


###########
# Session #
###########


class SessionError(DataClayException):
    def __init__(self, session_id):
        self.session_id = session_id


class SessionDoesNotExistError(SessionError):
    def __str__(self):
        return f"Session {self.session_id} does not exist"


class SessionAlreadyExistError(SessionError):
    def __str__(self):
        return f"Session {self.session_id} already exist"


class SessionIsNotActiveError(SessionError):
    def __str__(self):
        return f"Session {self.session_id} is not active"


###########
# Alias #
###########


class AliasError(DataClayException):
    def __init__(self, alias_name, dataset_name):
        self.alias_name = alias_name
        self.dataset_name = dataset_name


class AliasDoesNotExistError(AliasError):
    def __str__(self):
        return f"Alias {self.dataset_name}/{self.alias_name} does not exist"


class AliasAlreadyExistError(AliasError):
    def __str__(self):
        return f"Alias {self.dataset_name}/{self.alias_name} already exist"


###########
# Object #
###########


class ObjectError(DataClayException):
    def __init__(self, object_id):
        self.object_id = object_id


class ObjectDoesNotExistError(ObjectError):
    def __str__(self):
        return f"Object {self.object_id} does not exist!"


class ObjectAlreadyExistError(ObjectError):
    def __str__(self):
        return f"Object {self.object_id} already exist!"


#########################
# Execution Environment #
#########################


class ExecutionEnvironmentError(DataClayException):
    def __init__(self, ee_id):
        self.ee_id = ee_id


class ExecutionEnvironmentDoesNotExistError(ExecutionEnvironmentError):
    def __str__(self):
        return f"ExecutionEnvironment {self.ee_id} does not exist!"


class ExecutionEnvironmentAlreadyExistError(ExecutionEnvironmentError):
    def __str__(self):
        return f"ExecutionEnvironment {self.ee_id} already exist!"


############
# Dataclay #
############


class DataclayError(DataClayException):
    def __init__(self, dataclay_id):
        self.dataclay_id = dataclay_id


class DataclayDoesNotExistError(DataclayError):
    def __str__(self):
        return f"Dataclay {self.dataclay_id} does not exist!"


class DataclayAlreadyExistError(DataclayError):
    def __str__(self):
        return f"Dataclay {self.dataclay_id} already exist!"


###################
# StorageLocation #
###################


class StorageLocationError(DataClayException):
    def __init__(self, sl_name):
        self.sl_name = sl_name


class StorageLocationDoesNotExistError(StorageLocationError):
    def __str__(self):
        return f"StorageLocation {self.sl_name} does not exist!"


class StorageLocationAlreadyExistError(StorageLocationError):
    def __str__(self):
        return f"Dataclay {self.sl_name} already exist!"


#############
# MetaClass #
#############


class MetaclassError(DataClayException):
    def __init__(self, metaclass_id):
        self.metaclass_id = metaclass_id


class MetaclassDoesNotExistError(MetaclassError):
    def __str__(self):
        return f"Metaclass {self.metaclass_id} does not exist!"


class MetaclassAlreadyExistError(MetaclassError):
    def __str__(self):
        return f"Dataclay {self.metaclass_id} already exist!"
