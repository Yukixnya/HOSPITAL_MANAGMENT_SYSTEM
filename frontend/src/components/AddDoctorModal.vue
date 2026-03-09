<script setup>
import { ref } from 'vue';
import { specializations } from '../utils/DoctorSpecialization';
import { addDoctor } from '../services/admin';
import { schedules } from '../utils/DoctorSchedule';

const props = defineProps({
    isOpen: Boolean
});

const emit = defineEmits(['close', 'submit']);
const loading = ref(false)

const showPassword = ref(false); 

const formData = ref({
    "name": "Dr. " + '',
    "email": '',
    "password": '',
    "gender": '',
    "mobile": '',
    "specialization": '',
    "experience": '',
    "schedule": ''
});

const closeModal = () => {
    formData.value = {
        "name": '',
        "email": '',
        "password": '',
        "gender": '',
        "mobile": '',
        "specialization": '',
        "experience": '',
        "schedule": ''
    }
    emit('close')
};

const generatePassword = () => {
    const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+";
    let retVal = "";
    for (let i = 0, n = charset.length; i < 12; ++i) {
        retVal += charset.charAt(Math.floor(Math.random() * n));
    }
    formData.value.password = retVal;
    showPassword.value = true;
};

const schedule = ref(schedules)

const docSpecialization = ref(specializations)

const handleSubmit = async() => {
    try {
        loading.value = true
        const res = await addDoctor(formData.value);
        emit('submit')
        closeModal()
    } catch (error) {
        alert(error.message)
        console.log("Unable to add doctor ", error)
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <div v-if="isOpen"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-md p-4 transition-opacity"
        @click.self="closeModal">
        <div class="bg-white w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden border border-slate-200">

            <div class="px-8 py-5 border-b border-slate-100 flex justify-between items-center bg-white">
                <div>
                    <h3 class="text-xl font-bold text-slate-900">Add New Doctor</h3>
                    <p class="text-sm text-slate-500">Create a new practitioner profile in the system.</p>
                </div>
                <button @click="closeModal"
                    class="p-2 rounded-full hover:bg-slate-100 text-slate-400 transition-colors">
                    <span class="text-2xl leading-none">&times;</span>
                </button>
            </div>

            <form @submit.prevent="handleSubmit" class="p-8 max-h-[85vh] overflow-y-auto">

                <div class="mb-8">
                    <h4 class="text-xs font-semibold text-blue-600 uppercase tracking-wider mb-4">Account Information
                    </h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div class="space-y-1">
                            <label class="block text-sm font-semibold text-slate-700">Full Name</label>
                            <input v-model="formData.name" type="text" placeholder="Dr. Sarah Smith"
                                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none transition-all placeholder:text-slate-400"
                                required />
                        </div>

                        <div class="space-y-1">
                            <label class="block text-sm font-semibold text-slate-700">Email Address</label>
                            <input v-model="formData.email" type="email" placeholder="sarah.s@hospital.com"
                                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none transition-all placeholder:text-slate-400"
                                required />
                        </div>

                        <div class="space-y-1 md:col-span-2">
                            <label class="block text-sm font-semibold text-slate-700">Password</label>
                            <div class="relative group">
                                <input v-model="formData.password" :type="showPassword ? 'text' : 'password'"
                                    placeholder="••••••••"
                                    class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none transition-all"
                                    required />
                                <button type="button" @click="generatePassword"
                                    class="absolute right-2 top-1.5 px-3 py-1 text-xs font-bold uppercase bg-white border border-slate-200 text-slate-600 rounded-lg hover:bg-blue-50 hover:text-blue-600 hover:border-blue-200 transition-all shadow-sm">
                                    Generate
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mb-4">
                    <h4 class="text-xs font-semibold text-blue-600 uppercase tracking-wider mb-4">Professional Details
                    </h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div class="space-y-1">
                            <label class="block text-sm font-semibold text-slate-700">Specialization</label>
                            <select v-model="formData.specialization"
                                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none transition-all">
                                <option value="" disabled>Select a Specialization</option>
                                <option v-for="s in docSpecialization" :key="s" :value="s">
                                    {{ s }}
                                </option>
                            </select>
                        </div>

                        <div class="space-y-1">
                            <label class="block text-sm font-semibold text-slate-700">Experience (Years)</label>
                            <input v-model="formData.experience" type="number"
                                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none transition-all" />
                        </div>

                        <div class="space-y-1">
                            <label class="block text-sm font-semibold text-slate-700">Mobile Number</label>
                            <input v-model="formData.mobile" type="tel"
                                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none transition-all" />
                        </div>

                        <div class="space-y-1">
                            <label class="block text-sm font-semibold text-slate-700">Gender</label>
                            <select v-model="formData.gender"
                                class="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none bg-white transition-all appearance-none">
                                <option value="">Select Gender</option>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                            </select>
                        </div>

                        <div class="space-y-1 md:col-span-2">
                            <label class="block text-sm font-semibold text-slate-700">Work Schedule</label>
                            <select v-model="formData.schedule"
                                class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 outline-none transition-all">
                                <option value="" disabled>Select a shift</option>
                                <option v-for="s in schedule" :key="s" :value="s">
                                    {{ s }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>

                <div class="mt-10 flex items-center justify-end gap-4 border-t border-slate-100 pt-6">
                    <button type="button" @click="closeModal"
                        class="px-5 py-2.5 text-sm font-bold text-slate-500 hover:text-slate-700 transition-colors">
                        Discard
                    </button>
                    <button type="submit"
                        class="px-8 py-2.5 text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-lg shadow-blue-200 transition-all active:scale-95">
                        {{ loading ? "Saving...." : "Save Profile"}}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>
