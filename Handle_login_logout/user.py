class User:
    def __init__(self,  username, password, email, phone, address, role, created_at, updated_at):

        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.address = address
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at


    def update_info(self, password=None, email=None, phone=None, address=None):
        if password is not None:
            self.password = password
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if address is not None:
            self.address = address


