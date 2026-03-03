<script setup>
import { ref } from 'vue';
import {
    Trash2,         
    History,
    Stethoscope,
    Search,
    User
} from 'lucide-vue-next';
import AddmedicationModal from '../../components/AddmedicationModal.vue';

const vitals = [
    { label: 'Blood Pressure', value: '120/80', unit: 'mmHg' },
    { label: 'Temperature', value: '98.6', unit: '°F' },
    { label: 'Weight', value: '72', unit: 'kg' },
    { label: 'Heart Rate', value: '72', unit: 'bpm' }
];

const isOpen = ref(false);

const patient = { id: '9842', name: 'John Doe', age: 34, gender: 'Male' };
</script>

<template>
    <div class="p-8 bg-slate-50 min-h-screen font-sans text-slate-600">
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 mb-6 flex justify-between items-center">
            <div class="flex items-center gap-6">
                <img :src="`https://i.pravatar.cc/150?u=${patient.id}`"
                    class="w-16 h-16 rounded-full border-2 border-slate-50" />
                <div>
                    <div class="flex items-center gap-3">
                        <h1 class="text-2xl font-bold text-slate-800">{{ patient.name }}</h1>
                        <span class="bg-blue-50 text-blue-600 text-[10px] font-bold px-2 py-0.5 rounded uppercase">
                            ID: #{{ patient.id }}
                        </span>
                    </div>
                    <p class="text-slate-400 text-sm font-medium mt-1">
                        {{ patient.age }} years • {{ patient.gender }} • 10:30 AM - 11:00 AM
                    </p>
                </div>
            </div>
            <div class="flex gap-3">
                <button
                    class="px-5 py-2 text-slate-600 font-bold text-sm hover:bg-slate-50 rounded-xl transition-all flex items-center gap-2">
                    <History class="w-4 h-4" /> View History
                </button>
                <button
                    class="px-6 py-2 bg-blue-600 text-white font-bold text-sm rounded-xl shadow-lg shadow-blue-200 hover:bg-blue-700 transition-all">
                    Contact
                </button>
            </div>
        </div>

        <div class="grid grid-cols-12 gap-6">
            <div class="col-span-12 lg:col-span-8 space-y-6">
                <div class="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm">
                    <h2
                        class="text-sm font-black text-slate-400 uppercase tracking-widest mb-6 flex items-center gap-2">
                        <Stethoscope class="w-4 h-4 text-blue-500" /> Diagnosis & Symptoms
                    </h2>
                    <div class="space-y-4">
                        <div>
                            <label class="text-[11px] font-bold text-slate-500 uppercase mb-2 block">Primary
                                Diagnosis</label>
                            <div class="relative">
                                <Search class="absolute left-4 top-3 w-4 h-4 text-slate-300" />
                                <input type="text" placeholder="Type to search codes..."
                                    class="w-full pl-11 pr-4 py-3 bg-slate-50 rounded-xl border-transparent focus:bg-white focus:ring-2 focus:ring-blue-100 transition-all outline-none" />
                            </div>
                        </div>
                        <textarea placeholder="Describe symptoms..."
                            class="w-full p-4 bg-slate-50 rounded-xl border-transparent h-32 focus:bg-white transition-all outline-none"></textarea>
                    </div>
                </div>

                <div class="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-sm font-black text-slate-400 uppercase tracking-widest">Prescription</h2>
                        <button @click="isOpen = true" class="text-blue-600 text-xs font-bold hover:underline">+ Add
                            Medication</button>
                    </div>
                    <table class="w-full text-left">
                        <thead>
                            <tr class="text-[10px] font-black uppercase text-slate-300 border-b border-slate-50">
                                <th class="pb-3">Medication Name</th>
                                <th class="pb-3">Dosage</th>
                                <th class="pb-3 text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="group hover:bg-slate-50 transition-colors">
                                <td class="py-4 text-sm font-bold text-slate-700">Amlodipine</td>
                                <td class="py-4 text-sm text-slate-500">5mg - Once daily</td>
                                <td class="py-4 text-right">
                                    <button
                                        class="p-2 text-slate-300 cursor-pointer hover:text-red-500 transition-colors">
                                        <Trash2 class="w-4 h-4" />
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="col-span-12 lg:col-span-4 space-y-6">
                <div class="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm">
                    <h2 class="text-sm font-black text-slate-400 uppercase tracking-widest mb-6">Patient Vitals</h2>
                    <div class="grid grid-cols-2 gap-4">
                        <div v-for="v in vitals" :key="v.label"
                            class="p-4 bg-slate-50 rounded-2xl border border-slate-100">
                            <p class="text-[9px] font-black text-slate-400 uppercase mb-1">{{ v.label }}</p>
                            <p class="text-lg font-bold text-slate-800">{{ v.value }} <span
                                    class="text-xs text-slate-400">{{ v.unit }}</span></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="mt-12">
            <button
                class="w-full px-4 py-3 bg-blue-600 text-white font-bold text-sm rounded-xl shadow-lg shadow-blue-200 hover:bg-blue-700 transition-all">
                Save Changes
            </button>
        </div>
    </div>

    <AddmedicationModal :isOpen="isOpen" @close="isOpen = false"
        @add="(med) => console.log('Adding medication:', med)" />
</template>