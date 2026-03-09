<script setup>
import API from '../../services/api'
import { ref } from 'vue'
import {useRouter} from 'vue-router'
import { registerAPI } from '../../services/auth'

import {
    UserIcon, CalendarIcon, PhoneIcon, EnvelopeIcon,
    LockClosedIcon, EyeIcon, EyeSlashIcon, UserPlusIcon
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
    password: ''
})


const handleSubmit = async () => {

    if (!formData.value.name || !formData.value.gender || !formData.value.mobile || !formData.value.email || !formData.value.password) {
        alert('Please fill in all required fields.')
        return
    }

    if (!isChecked.value) {
        alert('You must agree to the Terms of Service and Privacy Policy to register.')
        return
    }
    try{
        loading.value = true
        const data = await registerAPI(formData.value);
        alert("Registration Successful")
        router.push("/auth/login")
    }catch(error){
        alert(error.message);
        console.error(error)
    }finally{
        loading.value = false
        formData.value = {
            name: '',
            gender: '',
            mobile: '',
            email: '',
            password: ''    
        }
    }
    
    console.log('Form submitted:', formData.value)
}
</script>

<template>
    <div class="min-h-screen min-w-screen bg-slate-50 flex flex-col items-center justify-center p-6 font-sans">
        <div class=" bg-white rounded-4xl shadow-2xl shadow-slate-200/50 p-8 md:p-12">

            <header class="text-center mb-10">
                <h1 class="text-3xl font-extrabold text-slate-900 mb-2">Patient Registration</h1>
                <p class="text-slate-500 text-sm">Create your secure medical account to access digital healthcare
                    services.</p>
            </header>

            <form @submit.prevent="handleSubmit" class="space-y-6">

                <div class="space-y-2">
                    <label class="block text-sm font-bold text-slate-700">Full Legal Name</label>
                    <div class="relative">
                        <UserIcon class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                        <input v-model="formData.name" type="text" placeholder="Johnathan Doe"
                            class="w-full pl-12 pr-4 py-3.5 bg-slate-50 border border-slate-100 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all" />
                    </div>
                </div>

                <div class="grid grid-cols-1 col-span-2 md:grid-cols-1 gap-6">
                    <div class="space-y-2">
                        <label class="block text-sm font-bold text-slate-700">Gender</label>
                        <select v-model="formData.gender"
                            class="w-full px-4 py-3.5 bg-slate-50 border border-slate-100 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none appearance-none">
                            <option value="" disabled>Select Gender</option>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="space-y-2">
                        <label class="block text-sm font-bold text-slate-700">Phone Number</label>
                        <div class="relative">
                            <PhoneIcon class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                            <input v-model="formData.mobile" type="tel" placeholder="XXX-XXX-XXXX"
                                class="w-full pl-12 pr-4 py-3.5 bg-slate-50 border border-slate-100 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none" />
                        </div>
                    </div>
                    <div class="space-y-2">
                        <label class="block text-sm font-bold text-slate-700">Email Address</label>
                        <div class="relative">
                            <EnvelopeIcon class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                            <input v-model="formData.email" type="email" placeholder="john@example.com"
                                class="w-full pl-12 pr-4 py-3.5 bg-slate-50 border border-slate-100 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none" />
                        </div>
                    </div>
                </div>

                <div class="space-y-2">
                    <label class="block text-sm font-bold text-slate-700">Create Password</label>
                    <div class="relative">
                        <LockClosedIcon class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                        <input v-model="formData.password" :type="showPassword ? 'text' : 'password'"
                            placeholder="At least 8 characters"
                            class="w-full pl-12 pr-12 py-3.5 bg-slate-50 border border-slate-100 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none" />
                        <button type="button" @click="showPassword = !showPassword"
                            class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400">
                            <EyeIcon v-if="!showPassword" class="w-5 h-5" />
                            <EyeSlashIcon v-else class="w-5 h-5" />
                        </button>
                    </div>
                </div>

                <label class="flex items-start gap-3 cursor-pointer group py-2">
                    <input type="checkbox" v-model="isChecked"
                        class="mt-1 w-5 h-5 rounded border-slate-200 text-blue-600 focus:ring-blue-500 cursor-pointer" />
                    <span class="text-xs text-slate-500 leading-relaxed group-hover:text-slate-700">
                        I agree to the <a href="#" class="text-blue-600 font-bold">Terms of Service</a> and <a href="#"
                            class="text-blue-600 font-bold">Privacy Policy</a>, including HIPAA data handling protocols.
                    </span>
                </label>

                <button
                    class="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-2xl shadow-xl shadow-blue-200 flex items-center justify-center gap-2 transition-all active:scale-[0.98]">
                    {{ loading ? 'Registering...' : 'Create Account' }}
                    <UserPlusIcon class="w-5 h-5" />
                </button>
            </form>

            <p class="text-center mt-8 text-sm font-medium text-slate-500">
                Already have an account? <router-link to="/auth" class="text-blue-600 font-bold">Sign in here</router-link>
            </p>
        </div>
    </div>
</template>

