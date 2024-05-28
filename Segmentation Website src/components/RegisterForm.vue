<template>
  <form @submit.prevent="checkPermission">
    <h2>Sign Up</h2>
    <p><input type="text" placeholder="First name" required v-model="firstname"></p>
    <p><input type="text" placeholder="Last name" required v-model="lastname"></p>
    <p><input type="email" placeholder="Email" required v-model="email"></p>
    <p><input type="password" placeholder="Password" required v-model="password"></p>
    <button>Sign Up</button>
    <p v-if="error" class="error-message">{{ error }}</p>
  </form>
</template>

<script>

import { createUserWithEmailAndPassword, updateProfile, sendEmailVerification, signOut } from 'firebase/auth';
import { auth, db } from '../firebase/init.js';
import { where, query, collection, getDocs } from 'firebase/firestore';

export default {
  name: 'RegisterForm',
  data() {
    return {
      email: '',
      password: '',
      firstname: '',
      lastname: '',
      isRegistering: null,
      error: null,
    };
  },
  methods: {
    async checkPermission() {
      const q = query(collection(db, "Users"), where("email", "==", this.email));
      const querySnapshot = await getDocs(q);
      if (querySnapshot.size === 0) {
        this.error = 'This email has not been verified for an account'
      } else if (querySnapshot.size > 0) {
        this.registerUser();
      }

    },
    async registerUser() {
      this.isRegistering = true;
      this.error = null;

      await createUserWithEmailAndPassword(auth, this.email, this.password).then(() => {
        updateProfile(auth.currentUser, {
          displayName: this.firstname + ' ' + this.lastname,
        })

          .then(() => {
            sendEmailVerification(auth.currentUser);
            signOut(auth);
            this.$emit('registered');
          })

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
  },
};
</script>

<style scoped>
input:invalid {
  background-color: #ffdddd;
}

.error-message {
  color: red;
}
</style>