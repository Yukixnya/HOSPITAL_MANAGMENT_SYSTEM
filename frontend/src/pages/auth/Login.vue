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

const router = useRouter()

const selectedRole = ref('doctor')
const showPassword = ref(false)
const loading = ref(false)

const userDetails = reactive({
    email: '',
    password: '',
})

const handleLogin = async () => {
    try {
        loading.value = true
        const data = await loginAPI(userDetails, selectedRole.value)
        const token = data[0].token
        const role = data[1];

        localStorage.setItem("token", token)

        alert("Login Successful")

        if(role === 'admin') {
            router.push("/admin")
        } else if (role === 'doctor') {
            router.push("/doctor")
        } else if (role === 'patient') {
            router.push("/patient")
        }

    } catch (error) {
        console.error(error)
    } finally {
        loading.value = false
        userDetails.email = ''
        userDetails.password = ''
    }
}

</script>

<template>
    <div class="min-h-screen min-w-screen bg-slate-50 flex flex-col items-center justify-center p-6 font-sans">
        <div class="bg-white rounded-4xl shadow-xl shadow-slate-200/60 p-10 md:p-12">

            <header class="mb-8">
                <h1 class="text-3xl font-extrabold text-slate-900 mb-2">System Login</h1>
                <p class="text-slate-500 leading-relaxed">
                    Welcome back, please select your role and enter credentials.
                </p>
            </header>

            <div class="mb-8">
                <label class="block text-sm font-bold text-slate-700 mb-3">Select Role</label>
                <div class="flex p-1.5 bg-slate-100 rounded-2xl">
                    <button v-for="role in ['admin', 'doctor', 'patient']" :key="role" @click="selectedRole = role"
                        :class="[
                            'flex-1 py-2.5 text-sm font-bold rounded-xl transition-all',
                            selectedRole === role
                                ? 'bg-blue-600 text-white shadow-md'
                                : 'text-slate-500 hover:text-slate-700'
                        ]">
                        {{ role }}
                    </button>
                </div>
            </div>

            <form @submit.prevent="handleLogin" class="space-y-6">
                <div>
                    <label class="block text-sm font-bold text-slate-700 mb-2">Email Address</label>
                    <div class="relative">
                        <EnvelopeIcon class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                        <input type="email" v-model="userDetails.email" placeholder="name@hospital.com"
                            class="w-full pl-12 pr-4 py-3.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all placeholder:text-slate-400" />
                    </div>
                </div>

                <div>
                    <div class="flex justify-between mb-2">
                        <label class="text-sm font-bold text-slate-700">Password</label>
                        <a href="#"
                            class="text-xs font-bold text-blue-600 hover:text-blue-700 uppercase tracking-tight">Forgot
                            Password?</a>
                    </div>
                    <div class="relative">
                        <LockClosedIcon class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                        <input :type="showPassword ? 'text' : 'password'" placeholder="••••••••"
                            v-model="userDetails.password"
                            class="w-full pl-12 pr-12 py-3.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all placeholder:text-slate-400" />
                        <button type="button" @click="showPassword = !showPassword"
                            class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                            <EyeIcon v-if="!showPassword" class="w-5 h-5" />
                            <EyeSlashIcon v-else class="w-5 h-5" />
                        </button>
                    </div>
                </div>

                <button
                    class="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-2xl shadow-lg shadow-blue-200 flex items-center justify-center gap-2 transition-all active:scale-[0.98]">
                    {{ loading ? 'Logging in...' : 'Login' }}
                    <ArrowRightIcon class="w-5 h-5" />
                </button>
            </form>
            <p class="mt-4 text-center text-sm text-slate-500">
                Don't have an account?
                <router-link to="/auth/register" class="font-bold text-blue-600 hover:text-blue-700"> Sign Up</router-link>
            </p>


        </div>

        <footer class="mt-12 text-center space-y-2">
            <p class="text-slate-400 text-xs">© 2024 MedFlow Hospital Management Systems. All rights reserved.</p>
            <div class="flex justify-center gap-4 text-[11px] font-bold text-slate-400">
                <a href="#" class="hover:text-slate-600">Privacy Policy</a>
                <a href="#" class="hover:text-slate-600">Terms of Service</a>
                <a href="#" class="hover:text-slate-600">HIPAA Compliance</a>
            </div>
        </footer>
    </div>
</template>

