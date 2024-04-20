import mariadb


class sqlDB:

    def __init__(self, host_name: str, user_name: str, user_password: str, db_name:str):
        self.__host_name = host_name
        self.__user_name = user_name
        self.__user_password = user_password
        self.__db_name = db_name
        self.__connection = self.create_db_connection()
    def __str__(self):
        return f"An object of sqlDB type with (host_name = {self.host_name}, user_name = {self.user_name},user_password = {self.user_password}, db_name = {self.db_name})"

    @property
    def host_name(self) -> str:
        return self.__host_name
    @host_name.setter
    def host_name(self, value:str) -> None:
        self.__host_name = value

    @property
    def user_name(self) -> str:
        return self.__user_name
    @user_name.setter
    def user_name(self, value: str) -> None:
        self.__user_name = value

    @property
    def user_password(self):
        """The user_password property."""
        return self.__user_password
    @user_password.setter
    def user_password(self, value):
        self.__user_password = value
    
    @property
    def db_name(self):
        return self.__db_name
    @db_name.setter
    def db_name(self, value):
        self.__db_name = value

    @property
    def connection(self): 
        return self.__connection
    @connection.setter
    def connection(self, value):
        self.__connection = value



    def create_server_connection(self):
        connection = None
        try:
            connection = mariadb.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.user_password
            )
            print("Database connection successful")
        except mariadb.Error as err:
            print(f"Error: '{err}'")
    
        return connection

    def create_db_connection(self): 
        connection = None
        try:
            connection = mariadb.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.user_password,
                database=self.db_name
            )
            print("MySQL Database connection successful to the {} ".format(self.db_name))
        except mariadb.Error as err:
            print(f"Error: '{err}'") 
        return connection
    
    def return_connection(self):
        return self.connection

    def execute_query(self , query:str):
        if self.connection == None:
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query successful")
        except mariadb.Error as err:
            print(f"Error: '{err}' COULDNT EXECUTE QUERY")
    
    
    def read_query(self, query:str):

        if self.connection == None:
            return

        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")