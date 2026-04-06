<script setup>
import { useRouter } from 'vue-router'
import { reactive, ref } from 'vue'
import {
    EnvelopeIcon,
    LockClosedIcon,
    EyeIcon,
    EyeSlashIcon,
    ArrowRightIcon
} from '@heroicons/vue/24/outline'
import { loginAPI } from '../../services/auth'
import { useUserStore } from '../../store/userStore'
import { useToast } from "vue-toastification";

const toast = useToast()

const router = useRouter()
const userStore = useUserStore()

const showPassword = ref(false)
const loading = ref(false)

const userDetails = reactive({
    email: '',
    password: '',
    role: 'Doctor'
})

const handleLogin = async () => {
    try {
        loading.value = true
        const data = await loginAPI(userDetails)

        userStore.setUser(data.user, data.token)
        const role = data.user.role.toLowerCase(); 
        toast.success(`Welcome back, ${data.user.name}!`)
        router.push(`/${role}`);
    } catch (error) {
        toast.error("Login failed. Please check your credentials.")
        console.error(error)
    } finally {
        loading.value = false
        userDetails.password = ''
    }
}
</script>

<template>
    <div class="auth-wrapper">
        <div class="auth-card">
            <header class="auth-header">
                <h1 class="auth-title">System Login</h1>
                <p class="auth-subtitle">
                    Welcome back, please select your role and enter credentials.
                </p>
            </header>

            <div class="role-selector-container">
                <label class="label-text">Select Role</label>
                <div class="role-toggle-bg">
                    <button v-for="role in ['Admin', 'Doctor', 'Patient']" :key="role" @click="userDetails.role = role"
                        :class="['role-btn', { active: userDetails.role === role }]">
                        {{ role }}
                    </button>
                </div>
            </div>

            <form @submit.prevent="handleLogin" class="auth-form">
                <div class="form-group">
                    <label class="label-text">Email Address</label>
                    <div class="relative-input">
                        <EnvelopeIcon class="input-icon-left" />
                        <input type="email" v-model="userDetails.email" placeholder="name@hospital.com" required
                            class="styled-input auth-input" />
                    </div>
                </div>

                <div class="form-group">
                    <div class="label-row">
                        <label class="label-text">Password</label>
                        <a href="#" class="forgot-link">Forgot Password?</a>
                    </div>
                    <div class="relative-input">
                        <LockClosedIcon class="input-icon-left" />
                        <input :type="showPassword ? 'text' : 'password'" placeholder="••••••••" required
                            v-model="userDetails.password" class="styled-input auth-input password-input" />
                        <button type="button" @click="showPassword = !showPassword" class="password-toggle">
                            <EyeIcon v-if="!showPassword" class="icon-sm" />
                            <EyeSlashIcon v-else class="icon-sm" />
                        </button>
                    </div>
                </div>

                <button type="submit" :disabled="loading" class="btn-primary-lg">
                    <span>{{ loading ? 'Logging in...' : 'Login' }}</span>
                    <ArrowRightIcon v-if="!loading" class="icon-sm" />
                </button>
            </form>

            <p class="auth-footer-text">
                Don't have an account?
                <router-link to="/auth/register" class="auth-link"> Sign Up</router-link>
            </p>
        </div>

        <footer class="legal-footer">
            <p>© 2024 MedFlow Hospital Systems. All rights reserved.</p>
            <div class="legal-links">
                <a href="#">Privacy Policy</a>
                <a href="#">Terms of Service</a>
                <a href="#">HIPAA Compliance</a>
            </div>
        </footer>
    </div>
</template>

<style src="../../styles/auth.css" scoped></style>