<template>
    <q-page>
        <!-- Kullanıcı bilgilerinin gösterildiği form -->
        <q-form @submit.prevent="updateProfile" :style="{ marginBottom: '20px' }" method="POST">
            <q-input filled label="Ad" v-model="userInfo.firstName" :readonly="!isEditing" />

            &nbsp;
            <q-input filled label="Soyad" v-model="userInfo.lastName" :readonly="!isEditing" />
            &nbsp;
            <q-input filled label="Kullanıcı Adı" v-model="userInfo.username" :readonly="!isEditing" />
            &nbsp;
            <q-input filled label="E-mail" v-model="userInfo.email" :readonly="!isEditing" />
            &nbsp;
            <q-input :style="{ marginBottom: '20px' }" filled label="Address" v-model="userInfo.address"
                :readonly="!isEditing" />
            <q-input :style="{ marginBottom: '20px' }" filled label="Phone" v-model="userInfo.phone"
                :readonly="!isEditing" />
            <q-btn class="mb-4" @click="changePasswordButton" color="blue-9" label="Change the Password"
                :style="{ width: '100%', marginBottom: '-8px' }" />
            <q-btn class="mb-4" v-if="isEditing" color="green-9" label="Save" type="submit"
                :style="{ width: '100%', marginTop: '18px' }" />
        </q-form>
        <q-btn v-if="!isEditing" @click="startEditing" color="blue-9" label="Edit" class="full-width-btn"
            :style="{ width: '100%' }" />
        <!-- Change Password Modal -->
        <q-dialog v-model="showChangePasswordModal" persistent>
            <q-card style="min-width: 400px; max-width: 90vw;">
                <q-card-section>
                    <div class="text-h6">Change Password</div>
                </q-card-section>
                <q-card-section>
                    <q-form @submit.prevent="verifyCurrentPassword">
                        <q-input v-model="currentPassword" label="Current Password" type="password"
                            :rules="[requiredRule]" dense required />
                        <q-btn flat label="No" color="negative" v-close-popup />
                        <q-btn flat label="Verify" color="positive" type="submit" />

                    </q-form>
                </q-card-section>
            </q-card>
        </q-dialog>
        <!-- New Password Modal -->
        <q-dialog v-model="showNewPasswordModal" persistent>
            <q-card style="min-width: 400px; max-width: 90vw;">
                <q-card-section>
                    <div class="text-h6">Enter New Password</div>
                </q-card-section>
                <q-card-section>
                    <q-form @submit.prevent="updatePassword">
                        <q-input v-model="newPassword" label="New Password" type="password" :rules="[requiredRule]"
                            dense required />
                        <q-input v-model="confirmNewPassword" label="Confirm New Password" type="password"
                            :rules="[requiredRule, passwordMatchRule]" dense required />
                        <q-btn flat label="No" color="negative" v-close-popup />
                        <q-btn flat label="Yes" color="positive" type="submit" />
                    </q-form>
                </q-card-section>
            </q-card>
        </q-dialog>

        <q-dialog v-model="showLogoutModal">
            <q-card>
                <q-card-section class="row items-center">
                    <q-spinner-dots size="40px" color="primary" />
                    <span class="q-ml-sm">Bilgileriniz güncellendi, Yeniden giriş yapmanız gerekiyor...</span>
                </q-card-section>
            </q-card>
        </q-dialog>

    </q-page>
</template>

<script>
    import axios from 'axios'
    export default {
        data() {
            return {
                userInfo: {
                    real_username: this.$route.params.username,
                    username: this.$route.params.username,
                    firstName: '',
                    lastName: '',
                    email: '',
                    address: '',
                    phone: ''
                },
                isEditing: false,
                showChangePasswordModal: false,
                showNewPasswordModal: false,
                showLogoutModal: false,
                currentPassword: '',
                newPassword: '',
                confirmNewPassword: ''
            };
        },
        created() {
            axios
                .post("http://127.0.0.1:5000/api/getTeacherData", this.userInfo)
                .then((response) => {
                    this.userInfo.firstName = response.data[0][6];
                    this.userInfo.lastName = response.data[0][7];
                    this.userInfo.username = response.data[0][1];
                    this.userInfo.email = response.data[0][4];
                    this.userInfo.address = response.data[0][5];
                    this.userInfo.phone = response.data[0][8]

                });
        },
        methods: {
            startEditing() {
                this.isEditing = true;
            },

            updateProfile() {
                if (!this.isEditing) return;
                axios
                    .post("http://127.0.0.1:5000/api/updateTeacherData", this.userInfo)
                    .then((response) => {
                        if (response.data.logout == true) {
                            this.showLogoutModal = true; // Modalı göster
                            setTimeout(() => {
                                window.location.href = '/';
                            }, 2000); // 5 saniye sonra yönlendirme yap
                        }

                    });
                this.isEditing = false;
            },
            changePasswordButton() {
                this.showChangePasswordModal = true;
            },
            verifyCurrentPassword() {
                axios.post("http://127.0.0.1:5000/api/verifyPassword", {
                    username: this.userInfo.username,
                    password: this.currentPassword
                }).then((response) => {
                    if (response.data.status) {
                        this.showChangePasswordModal = false;
                        this.showNewPasswordModal = true;
                    } else {
                        this.$q.notify({
                            color: 'negative',
                            message: 'Current password is incorrect',
                            position: 'top'
                        });
                    }
                }).catch((error) => {
                    console.error('Error verifying password:', error);
                });
            },
            updatePassword() {
                if (this.newPassword !== this.confirmNewPassword) {
                    this.$q.notify({
                        color: 'negative',
                        message: 'Passwords do not match',
                        position: 'top'
                    });
                    return;
                }
                axios.post("http://127.0.0.1:5000/api/changePassword", {
                    username: this.userInfo.username,
                    new_password: this.newPassword
                }).then((response) => {
                    if (response.data.status) {
                        this.$q.notify({
                            color: 'positive',
                            message: 'Password updated successfully',
                            position: 'top'
                        });
                        this.showNewPasswordModal = false;
                    } else {
                        this.$q.notify({
                            color: 'negative',
                            message: 'Error updating password',
                            position: 'top'
                        });
                    }
                }).catch((error) => {
                    this.$q.notify({
                        color: 'negative',
                        message: 'Error updating password',
                        position: 'top'
                    });
                });
            }
        },
        computed: {
            requiredRule() {
                return val => !!val || 'This field is required';
            },
            passwordMatchRule() {
                return val => val === this.newPassword || 'Passwords must match';
            }
        }
    };
</script>
