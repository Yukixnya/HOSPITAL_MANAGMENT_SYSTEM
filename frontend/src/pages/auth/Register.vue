<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { registerAPI } from '../../services/auth'
import {
    UserIcon, PhoneIcon, EnvelopeIcon,
    LockClosedIcon, EyeIcon, EyeSlashIcon, UserPlusIcon, ChevronDownIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const isChecked = ref(false)
const showPassword = ref(false)
const loading = ref(false)

const formData = ref({
    name: '',
    gender: '',
    mobile: '',
    email: '',
    password: '',
    age: '',
    role: 'Patient'
})

const handleSubmit = async () => {
    // Basic validation
    const { name, gender, mobile, email, password } = formData.value;
    if (!name || !gender || !mobile || !email || !password) {
        alert('Please fill in all required fields.')
        return
    }
    if (!isChecked.value) {
        alert('You must agree to the Terms of Service to register.')
        return
    }

    try {
        loading.value = true
        await registerAPI(formData.value);
        alert("Registration Successful")
        router.push("/auth")
    } catch (error) {
        alert(error.message || "Registration failed");
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="auth-wrapper">
        <div class="auth-card register-wide">
            <header class="auth-header">
                <h1 class="auth-title">Patient Registration</h1>
                <p class="auth-subtitle">Create your secure medical account to access digital healthcare services.</p>
            </header>

            <form @submit.prevent="handleSubmit" class="auth-form">
                <div class="form-group">
                    <label class="label-text">Full Legal Name</label>
                    <div class="relative-input">
                        <UserIcon class="input-icon-left" />
                        <input v-model="formData.name" type="text" placeholder="Johnathan Doe" class="auth-input" />
                    </div>
                </div>

                <div class="auth-input-grid">
                    <div class="form-group">
                        <label class="label-text">Gender</label>
                        <div class="relative-input">
                            <select v-model="formData.gender" class="auth-input select-custom">
                                <option value="" disabled>Select Gender</option>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                            </select>
                            <ChevronDownIcon class="input-icon-right pointer-events-none" />
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="label-text">Age</label>
                        <div class="relative-input">
                            <input v-model="formData.age" type="number" min="0" placeholder="e.g. 30"
                                class="auth-input" />
                        </div>
                    </div>
                </div>

                <div class="auth-input-grid">
                    <div class="form-group">
                        <label class="label-text">Phone Number</label>
                        <div class="relative-input">
                            <PhoneIcon class="input-icon-left" />
                            <input v-model="formData.mobile" type="tel" placeholder="XXX-XXX-XXXX" class="auth-input" />
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="label-text">Email Address</label>
                        <div class="relative-input">
                            <EnvelopeIcon class="input-icon-left" />
                            <input v-model="formData.email" type="email" placeholder="john@example.com"
                                class="auth-input" />
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label class="label-text">Create Password</label>
                    <div class="relative-input">
                        <LockClosedIcon class="input-icon-left" />
                        <input v-model="formData.password" :type="showPassword ? 'text' : 'password'"
                            placeholder="At least 8 characters" class="auth-input password-input" />
                        <button type="button" @click="showPassword = !showPassword" class="password-toggle">
                            <EyeIcon v-if="!showPassword" class="icon-sm" />
                            <EyeSlashIcon v-else class="icon-sm" />
                        </button>
                    </div>
                </div>

                <label class="consent-container">
                    <input type="checkbox" v-model="isChecked" class="hidden-checkbox" />
                    <div class="custom-checkbox" :class="{ checked: isChecked }"></div>
                    <span class="consent-text">
                        I agree to the <a href="#" class="auth-link">Terms of Service</a> and
                        <a href="#" class="auth-link">Privacy Policy</a>, including HIPAA data handling.
                    </span>
                </label>

                <button type="submit" class="btn-primary-lg" :disabled="loading">
                    <span>{{ loading ? 'Registering...' : 'Create Account' }}</span>
                    <UserPlusIcon v-if="!loading" class="icon-sm" />
                </button>
            </form>

            <p class="auth-footer-text">
                Already have an account?
                <router-link to="/auth" class="auth-link">Sign in here</router-link>
            </p>
        </div>
    </div>
</template>

<style src="../../styles/auth.css" scoped></style>