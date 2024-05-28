<template>
    <div class="main center">
        <input type="checkbox" id="chk" aria-hidden="true">

        <div class="signup">
            <form @submit.prevent="checkRegistrationPermission" ref="registrationform">
                <label for="chk" aria-hidden="true" @click="error = ''">Register</label>
                <input type="text" name="fname" placeholder="Firstname" required="">
                <input type="text" name="lname" placeholder="Lastname" required="">
                <input type="email" name="email" placeholder="Email" required="">
                <input type="password" name="pswd" placeholder="Password" required="">
                <button>Sign up</button>
                <p v-if="error" style="color: white;">{{ error }}</p>

            </form>
        </div>

        <div class="login">
            <form @submit.prevent="userLoggedIn">
                <label for="chk" aria-hidden="true" @click="error = ''">Login</label>
                <input type="email" name="email" placeholder="Email" required="">
                <input type="password" name="pswd" placeholder="Password" required="">
                <button>Login</button>
                <p v-if="error" class="error-message">{{ error }}</p>
            </form>
        </div>
    </div>
</template>

<script>

import { createUserWithEmailAndPassword, updateProfile, sendEmailVerification, signOut, signInWithEmailAndPassword } from 'firebase/auth';
import { auth, db } from '../firebase/init.js';
import { where, query, collection, getDocs, updateDoc, doc } from 'firebase/firestore';

import { setPersistence, inMemoryPersistence } from '@firebase/auth';

export default {
    name: 'LoginView',
    data() {
        return {
            error: '',
        }
    },
    methods: {
        async checkRegistrationPermission(submitEvent) {
            const firstname = submitEvent.target.fname.value;
            const lastname = submitEvent.target.lname.value;
            const email = submitEvent.target.email.value;
            const password = submitEvent.target.pswd.value;

            const q = query(collection(db, "Users"), where("email", "==", email));
            const querySnapshot = await getDocs(q);
            if (querySnapshot.size === 0) {
                this.error = 'This email has not been verified for an account'
            } else if (querySnapshot.size > 0) {
                this.registerUser(firstname, lastname, email, password).then(() => {
                    querySnapshot.forEach(async (userdoc) => {
                        // Update 'status' field in the document
                        const docRef = doc(db, "Users", userdoc.id);
                        await updateDoc(docRef, {
                            ['status']: "registered"
                        }).then(() => {
                            signOut(auth);
                            this.$refs.registrationform.reset();
                            this.error = 'A verification link has been sent to your email';
                        }).catch((error) => {
                            console.error("Error updating document: ", error);
                        })
                    });

                });
            }
        },

        async registerUser(firstname, lastname, email, password) {
            this.isRegistering = true;
            this.error = null;

            await createUserWithEmailAndPassword(auth, email, password).then(() => {
                updateProfile(auth.currentUser, {
                    displayName: firstname + ' ' + lastname,
                })
                sendEmailVerification(auth.currentUser);
            })
                .catch((error) => {
                    switch (error.code) {
                        case 'auth/invalid-email':
                            this.error = 'Invalid email address.';
                            break;
                        case 'auth/weak-password':
                            this.error = 'Password must be at least 6 characters.';
                            break;
                        case 'auth/email-already-in-use':
                            this.error = 'Email already in use.';
                            break;
                        default:
                            this.error = 'An error occurred. Please try again.';
                    }
                });
        },

        userLoggedIn(submitEvent) {
            const email = submitEvent.target.email.value;
            const password = submitEvent.target.pswd.value;
            signInWithEmailAndPassword(auth, email, password).then(async () => {
                if (auth.currentUser.emailVerified) {
                    this.$router.push({ name: 'PendingApproval' });
                } else {
                    this.error = 'Please verify your email address';
                    signOut(auth);
                }
            }).catch((error) => {
                switch (error.code) {
                    case 'auth/invalid-email':
                        this.error = 'Invalid email address.';
                        break;
                    case 'auth/invalid-login-credentials':
                        this.error = "Invalid email or password";
                        break;
                    case 'auth/wrong-password':
                        this.error = 'Invalid email or password.';
                        break;
                    default:
                        this.error = 'An error occurred. Please try again.';
                }
            });
        }

    },
    created() {
        document.title = "Login";

    },
    mounted() {
        setPersistence(auth, inMemoryPersistence);
        const chk = document.getElementById('chk');
        chk.checked = true;
        if (auth.currentUser) {
            signOut(auth);
        }
    },

}
</script>
<style scoped>
/* #68246D */
body {
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    /* min-height: 100vh; */
}

.main {
    width: 350px;
    height: 500px;
    background: #1F497D;
    overflow: hidden;
    border-radius: 10px;
    box-shadow: 0px 0px 60px 10px#1f497d61;
    font-family: Arial;

}

#chk {
    display: none;
}

.signup {
    position: relative;
    width: 100%;
    height: 100%;

}

label {
    color: #fff;
    font-size: 2.3em;
    justify-content: center;
    display: flex;
    margin: 35px;
    font-weight: bold;
    cursor: pointer;
    transition: .5s ease-in-out;
}

input {
    width: 60%;
    height: 15px;
    background: #e0dede;
    justify-content: center;
    display: flex;
    margin: 20px auto;
    padding: 10px;
    border: none;
    outline: none;
    border-radius: 5px;
}

button {
    width: 60%;
    height: 40px;
    margin: 10px auto;
    justify-content: center;
    display: block;
    color: #fff;
    background: #1F497D;
    font-size: 1em;
    font-weight: bold;
    margin-top: 20px;
    outline: none;
    border: none;
    border-radius: 5px;
    transition: .2s ease-in;
    cursor: pointer;
}

button:hover {
    background: #345782;
}

.login {
    height: 460px;
    background: #eee;
    border-radius: 60% / 10%;
    transform: translateY(-130px);
    transition: .8s ease-in-out;
}

.login label {
    color: #1F497D;
    transform: scale(.6);
}

#chk:checked~.login {
    transform: translateY(-500px);
}

#chk:checked~.login label {
    transform: scale(1);
}

#chk:checked~.signup label {
    transform: scale(.6);
}
</style>