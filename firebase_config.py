import pyrebase

firebase_config = {
    "apiKey": "AIzaSyAKShsi8jwjKaUS-K9jTrWmnn_QglJJ9aU",
    "authDomain": "authentication-23c87.firebaseapp.com",
    "projectId": "authentication-23c87",
    "storageBucket": "authentication-23c87.firebasestorage.app",
    "messagingSenderId": "548400146237",
    "appId": "1:548400146237:web:23c1f1ad64da4c43724754",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
