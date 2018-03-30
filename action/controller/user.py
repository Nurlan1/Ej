from action.model.user import adduser
def addusercontroller(by):
    return adduser(by)

class usercontroller:
    def adduser(self, data):
        return  userdb.create_user(data)
    def get_byname(self,name):
        return userdb.getByname(name)
    def get_bypId(self,pId):
        return userdb.getBypId(pId)