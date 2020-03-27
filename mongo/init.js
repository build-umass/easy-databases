db.auth('admin-user', 'admin')

//create database
db = db.getSiblingDB('dev_db')

//create user
db.createUser({
    user: 'dev_user',
    pwd: 'dev',
    roles: [{
        role: 'dbOwner',
        db: 'dev_db',
    }],
})