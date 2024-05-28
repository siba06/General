<template>
    <div>
        <div class="container">
            <input class='container-input' type="radio" id="tab1" ref="tab1" name="tab" checked>
            <label class='container-label' for="tab1" @click="currentTab = 'c1'"><i class="fa fa-code"></i> Account
                Details</label>
            <input class='container-input' type="radio" id="tab2" name="tab">
            <label class='container-label' for="tab2" @click="currentTab = 'c2'"><i class="fa fa-history"></i> Change
                Password</label>

            <div class="line"></div>
            <div class="content-container">
                <div v-if="currentTab == 'c1'" class="content" id="c1">
                    <div class="content-body">
                        <form @submit.prevent="detailsChanged" ref="details_form">
                            <p>
                                <label for="username">Name</label><input type="text" name="username"
                                    v-model="user_name">
                            </p>

                            <p><label for="email">Email</label><input type="text" name="email" v-model="user_email"
                                    disabled="true"></p>
                            <p><button>Save Changes</button></p>
                            <p>{{ changes_code }}</p>
                        </form>
                    </div>
                </div>
                <div v-if="currentTab == 'c2'" class="content" id="c2">
                    <div class="content-body">
                        <form @submit.prevent="passwordChanged" class="pass-form" ref="pass_form">
                            <input type="password" name="current_pass" placeholder="Current Password" required="">

                            <p> <input type="password" name="new_pass" placeholder="New Password" required=""></p>
                            <p><button>Change Password</button></p>
                            <p v-if="error_code" style="color: red;">{{ error_code }}</p>
                        </form>
                    </div>
                </div>
                <div class="content" id="c3">
                    <h3>Reviews</h3>
                    <p>Amazing product. I don't know how it works.</p>
                    <i>- Anonymous</i>
                </div>
                <div class="content" id="c4">
                    <h3>Share</h3>
                    <p>This product is currently not shareable.</p>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { auth } from '../firebase/init.js';
import { updateProfile, updatePassword, signInWithEmailAndPassword } from 'firebase/auth';

export default {
    data() {
        return {
            user_name: auth.currentUser.displayName,
            user_email: auth.currentUser.email,
            currentTab: 'c1',
            error_code: '',
            changes_code: '',
        }
    },
    methods: {
        async detailsChanged(submitEvent) {
            const username = submitEvent.target.username.value;
            await updateProfile(auth.currentUser, {
                displayName: username,
            }).then(() => {
                this.changes_code = 'Changes saved successfully';
            }).catch((error) => {
                console.log(error);
                this.changes_code = 'An error occurred';
            });
        },
        async passwordChanged(submitEvent) {
            const current_pass = submitEvent.target.current_pass.value;

            const new_pass = submitEvent.target.new_pass.value;

            await signInWithEmailAndPassword(auth, auth.currentUser.email, current_pass).then(() => {
                updatePassword(auth.currentUser, new_pass).then(() => {
                    this.error_code = 'Password changed successfully';
                    this.$refs.pass_form.reset();
                }).catch((error) => {
                    if (error.code == 'auth/weak-password') {
                        this.error_code = 'Password needs to be longer than 6 characters';
                    } else {
                        this.error_code = 'An error occurred';
                    }
                })

            }).catch((error) => {
                if (error.code == 'auth/invalid-login-credentials') {
                    this.error_code = 'Wrong password';

                } else {
                    this.error_code = 'An error occurred';
                }
            })


        },
    },

}
</script>
<style lang="scss">
.pass-form {
    z-index: 100;
}

.container {

    width: 80%;
    height: 80%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 0;
    box-shadow: 0 0 100px RGBa(0, 0, 0, 0.5);
    border-radius: 3px;
    overflow: hidden;
    background: #f4f4f4;


    .container-input {
        display: none;

        &:checked+label {
            background: #eee;
        }

        @for $i from 1 through 2 {
            &#tab#{$i}:checked {
                ~.line {
                    left: #{($i) * 25%};
                }

                ~.content-container #c#{$i} {
                    opacity: 1;
                }
            }
        }
    }

    .container-label {
        display: inline-block;
        font-size: 16px;
        height: 36px;
        line-height: 36px;
        width: 25%;
        text-align: center;
        background: #f4f4f4;
        color: #555;
        position: relative;
        transition: 0.25s background ease;
        cursor: pointer;

        &::after {
            content: "";
            height: 2px;
            width: 100%;
            position: absolute;
            display: block;
            background: #ccc;
            bottom: 0;
            opacity: 0;
            left: 0;
            transition: 0.25s ease;
        }

        &:hover::after {
            opacity: 1;
        }
    }

    .line {
        position: absolute;
        height: 2px;
        background: #1E88E5;
        width: 25%;
        top: 34px;
        left: 0;
        transition: 0.25s ease;
    }

    .content-container {
        background: #eee;
        position: relative;
        width: 100%;
        height: 100%;
        font-size: 16px;


        .content {
            //position: absolute;
            position: relative;
            padding: 0px;
            height: 100%;
            width: 100%;
            margin: auto auto;
            opacity: 0;
            transition: 0.25s ease;
            color: #333;
            display: flex;
            align-items: center;
            justify-content: center;


            h3 {
                font-weight: 200;
                margin: 10px 0;
            }

            p {
                margin: 10px 0;
            }

            p,
            i {
                font-size: 13px;
            }

            input {
                border: 1px solid #ccc;
                width: 400px;
                height: 30px;
                margin: 20px;
            }

            button {
                margin: 20px;
            }
        }
    }
}
</style>