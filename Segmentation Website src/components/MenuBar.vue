<template>
    <div>
        <confirm-modal v-if="showSignout" @close="showSignout = false" @confirm="signOutUser">
            <template v-slot:header>
                <h1>Sign Out</h1>
            </template>
            <template v-slot:body>
                <p>Are you sure you want to sign out?</p>
            </template>
        </confirm-modal>
    </div>

    <div class="nav" id="navdiv">
        <input type="checkbox" id="menucheckbox" v-model="navOn">
        <span></span>
        <span></span>
        <div class="menu">
            <li><a href="#"><router-link to="/pending" @click="navOn = false">Pending</router-link></a></li>
            <li><a href="#" class="disabled"><router-link to="/completed"
                        @click="navOn = false">Completed</router-link></a>
            </li>
            <li><a href="#"><router-link to="/about" @click="navOn = false">About</router-link></a></li>
            <li></li>
            <li><a href="#"><router-link to="/settings" @click="navOn = false">Settings</router-link></a></li>
            <li><a href="#" @click="showSignout = true">Sign Out</a></li>
        </div>
    </div>
</template>


<script>
import ConfirmModal from './ConfirmModal.vue';


export default {
    data() {
        return {
            navOn: false,
            showModal: false,
            showSignout: false,
        };
    },
    watch: {
        navOn() {
            const navdiv = document.getElementById("navdiv");
            if (this.navOn) {
                navdiv.style.transform = "scale(1)";
            }
            else {
                setTimeout(() => {
                    navdiv.style.transform = "scale(0.5)";
                }, 500);
            }
        }
    },
    components: {
        ConfirmModal,
    },
    methods: {
        signOutUser() {
            this.showSignout = false;
            this.$router.push({ name: 'Login' });
        }
    }
}
</script>
<style scoped>
.disabled {
    pointer-events: none;
    cursor: default;
    color: #666666;
    opacity: 0.2;

}

.nav,
.menu {
    display: flex;
    justify-content: center;
    align-items: center;
}

.nav {
    position: fixed;
    z-index: 100;
    top: 10px;
    left: 10px;
    background-color: #fff;
    padding: 20px;
    transition: 0.5s;
    border-radius: 50px;
    overflow: hidden;
    box-shadow: 0 8px 15px rgba(0, 0, 0, .2);
    transform: scale(0.5);
}

.nav:hover {
    transform: scale(1) !important;
}

.menu {
    margin: 0;
    padding: 0;
    width: 0;
    overflow: hidden;
    transition: 0.5s;
}

.nav input:checked~.menu {
    width: 750px;
}

.menu li {
    list-style: none;
    margin: 0 30px;
}

.menu li a {
    text-decoration: none;
    color: #666;
    text-transform: uppercase;
    font-weight: 600;
    transition: 0.5s;
}

.menu li a:hover {
    color: #161919;
}

.nav input {
    width: 40px;
    height: 40px;
    cursor: pointer;
    opacity: 0;
}

.nav span {
    position: absolute;
    left: 30px;
    width: 30px;
    height: 4px;
    border-radius: 50px;
    background-color: #666;
    pointer-events: none;
    transition: 0.5s;

}

.nav input:checked~span {
    background-color: #f974a1;
}

.nav span:nth-child(2) {
    transform: translateY(-8px);
}

.nav input:checked~span:nth-child(2) {
    transform: translateY(0) rotate(-45deg);
}

.nav span:nth-child(3) {
    transform: translateY(8px);
}

.nav input:checked~span:nth-child(3) {
    transform: translateY(0) rotate(45deg);
}
</style>