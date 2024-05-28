<template>
    <div>
        <form @submit.prevent="loginUser">
            <h2>Login</h2>
            <p><input type="email" placeholder="Email" required v-model="email"></p>
            <p><input type="password" placeholder="Password" required v-model="password"></p>
            <button>Login</button>
            <p v-if="error" class="error-message">{{ error }}</p>
        </form>
    </div>
</template>

<script>
import { signInWithEmailAndPassword, signOut } from 'firebase/auth';
import { auth } from '../firebase/init.js';
export default {
    name: 'LoginForm',
    data() {
        return {
            email: '',
            password: '',
            error: ''
        }
    },
    methods: {
        loginUser() {
            signInWithEmailAndPassword(auth, this.email, this.password).then(() => {
                if (auth.currentUser.emailVerified) {
                    this.$emit('loggedIn')
                } else {
                    this.error = 'Please verify your email address'
                    signOut(auth);
                }
            })
                .catch((error) => {
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
        },
    },

}
</script>
<style scoped></style>