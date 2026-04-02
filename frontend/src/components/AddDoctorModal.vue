<script setup>
import { ref } from 'vue';
import { XIcon, SparklesIcon, Loader2Icon } from 'lucide-vue-next';
import { specializations } from '../utils/DoctorSpecialization';
import { addDoctor } from '../services/admin';
import { schedules } from '../utils/DoctorSchedule';

const props = defineProps({
    isOpen: Boolean
});

const emit = defineEmits(['close', 'submit']);
const loading = ref(false);
const showPassword = ref(false); 

const formData = ref({
    name: "Dr. ",
    email: '',
    password: '',
    gender: '',
    mobile: '',
    specialization: '',
    experience: '',
    schedule: ''
});

const closeModal = () => {
    formData.value = {
        name: "Dr. ", email: '', password: '', gender: '',
        mobile: '', specialization: '', experience: '', schedule: ''
    }
    emit('close')
};

const generatePassword = () => {
    const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%";
    let retVal = "";
    for (let i = 0; i < 12; ++i) {
        retVal += charset.charAt(Math.floor(Math.random() * charset.length));
    }
    formData.value.password = retVal;
    showPassword.value = true;
};

const handleSubmit = async() => {
    try {
        loading.value = true
        await addDoctor(formData.value);
        emit('submit')
        closeModal()
    } catch (error) {
        alert(error.message)
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <Teleport to="body">
        <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
            <div class="modal-card">
                
                <header class="modal-header">
                    <div class="header-text">
                        <h3 class="modal-title">Add New Doctor</h3>
                        <p class="modal-subtitle">Create a new practitioner profile in the system.</p>
                    </div>
                    <button @click="closeModal" class="close-btn">
                        <XIcon :size="20" />
                    </button>
                </header>

                <form @submit.prevent="handleSubmit" class="modal-form scrollbar-hide">
                    
                    <div class="form-section">
                        <h4 class="section-divider">Account Information</h4>
                        <div class="form-grid">
                            <div class="form-group">
                                <label class="label-text">Full Name</label>
                                <input v-model="formData.name" type="text" placeholder="Dr. Sarah Smith" class="styled-input" required />
                            </div>

                            <div class="form-group">
                                <label class="label-text">Email Address</label>
                                <input v-model="formData.email" type="email" placeholder="sarah.s@hospital.com" class="styled-input" required />
                            </div>

                            <div class="form-group span-2">
                                <label class="label-text">Password</label>
                                <div class="relative-input">
                                    <input v-model="formData.password" :type="showPassword ? 'text' : 'password'" placeholder="••••••••" class="styled-input pr-24" required />
                                    <button type="button" @click="generatePassword" class="btn-inline-action">
                                        <SparklesIcon :size="12" />
                                        Generate
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="form-section">
                        <h4 class="section-divider">Professional Details</h4>
                        <div class="form-grid">
                            <div class="form-group">
                                <label class="label-text">Specialization</label>
                                <select v-model="formData.specialization" class="styled-input" required>
                                    <option value="" disabled>Select specialization</option>
                                    <option v-for="s in specializations" :key="s" :value="s">{{ s }}</option>
                                </select>
                            </div>

                            <div class="form-group">
                                <label class="label-text">Experience (Years)</label>
                                <input v-model="formData.experience" type="number" class="styled-input" placeholder="0" />
                            </div>

                            <div class="form-group">
                                <label class="label-text">Mobile Number</label>
                                <input v-model="formData.mobile" type="tel" placeholder="+1..." class="styled-input" />
                            </div>

                            <div class="form-group">
                                <label class="label-text">Gender</label>
                                <select v-model="formData.gender" class="styled-input">
                                    <option value="">Select Gender</option>
                                    <option value="male">Male</option>
                                    <option value="female">Female</option>
                                    <option value="other">Other</option>
                                </select>
                            </div>

                            <div class="form-group span-2">
                                <label class="label-text">Work Schedule</label>
                                <select v-model="formData.schedule" class="styled-input" required>
                                    <option value="" disabled>Select a shift</option>
                                    <option v-for="s in schedules" :key="s" :value="s">{{ s }}</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <footer class="modal-footer">
                        <button type="button" @click="closeModal" class="btn-ghost">Discard</button>
                        <button type="submit" :disabled="loading" class="btn-primary-md">
                            <Loader2Icon v-if="loading" class="spinner" :size="18" />
                            <span>{{ loading ? "Saving..." : "Save Profile" }}</span>
                        </button>
                    </footer>
                </form>
            </div>
        </div>
    </Teleport>
</template>
<style src="./styles/doctorModal.css" scoped></style>