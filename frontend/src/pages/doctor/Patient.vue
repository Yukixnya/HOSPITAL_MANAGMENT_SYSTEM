<script setup>
import { ref, computed } from 'vue';
import { FilterIcon, DownloadIcon, EyeIcon, MoreVerticalIcon } from 'lucide-vue-next';

const activeTab = ref('All Patients');

const patients = ref([
    {
        name: 'Alicia Vance',
        id: '#PX-9920',
        gender: 'Female',
        age: 42,
        img: 'https://i.pravatar.cc/150?u=alicia',
        lastVisit: 'Oct 18,',
        lastVisitYear: '2023',
        condition: 'Hypertension',
        treatment: 'ACE Inhibitors daily, Low-sodium diet...',
        status: 'CHRONIC CARE'
    },
    {
        name: 'Marcus Wright',
        id: '#PX-8172',
        gender: 'Male',
        age: 65,
        img: 'https://i.pravatar.cc/150?u=marcus',
        lastVisit: 'Oct 15,',
        lastVisitYear: '2023',
        condition: 'Coronary Artery Disease',
        treatment: 'Statin therapy, Cardiac rehab phase...',
        status: 'REGULAR'
    },
    {
        name: 'Sarah Parker',
        id: '#PX-4412',
        gender: 'Female',
        age: 29,
        initials: 'SP',
        lastVisit: 'Oct 21,',
        lastVisitYear: '2023',
        condition: 'Post-Op Recovery',
        treatment: 'Wound care management, Pain medication...',
        status: 'RECENT SURGERY'
    },
    {
        name: 'Robert Johnson',
        id: '#PX-1109',
        gender: 'Male',
        age: 54,
        initials: 'RJ',
        lastVisit: 'Sept 30,',
        lastVisitYear: '2023',
        condition: 'Type 2 Diabetes',
        treatment: 'Insulin titration, Quarterly A1C monitoring...',
        status: 'CHRONIC CARE'
    }
]);

// Styling Helpers
const conditionStyles = (cond) => {
    const map = {
        'Hypertension': 'bg-purple-50 text-purple-600',
        'Coronary Artery Disease': 'bg-orange-50 text-orange-600',
        'Post-Op Recovery': 'bg-green-50 text-green-600',
        'Type 2 Diabetes': 'bg-red-50 text-red-600'
    };
    return map[cond] || 'bg-gray-50 text-gray-600';
};

const statusStyles = (status) => {
    const map = {
        'CHRONIC CARE': 'text-blue-500 bg-blue-50/50 px-2 py-0.5 rounded',
        'REGULAR': 'text-slate-400',
        'RECENT SURGERY': 'text-purple-500 bg-purple-50/50 px-2 py-0.5 rounded'
    };
    return map[status] || 'text-slate-400';
};

// Filtering Logic
const filteredPatients = computed(() => {
    if (activeTab.value === 'All Patients') return patients.value;
    return patients.value.filter(p => p.status.toLowerCase() === activeTab.value.toLowerCase());
});
</script>

<template>
    <div class="min-h-screen bg-gray-50 p-8 font-sans text-slate-700">
        <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-8 gap-4">
            <div class="flex items-center gap-2">
                <div class="flex bg-white rounded-xl p-1 border border-gray-200 shadow-sm">
                    <button v-for="tab in ['All Patients', 'Chronic Care', 'Recent Surgery', 'High Risk']" :key="tab"
                        @click="activeTab = tab" :class="[
                            'px-4 py-2 rounded-lg text-sm font-bold transition-all',
                            activeTab === tab ? 'bg-blue-600 text-white shadow-md' : 'text-slate-500 hover:bg-gray-50'
                        ]">
                        {{ tab }}
                    </button>
                </div>
            </div>

            <div class="flex items-center gap-3 w-full lg:w-auto">
                <button
                    class="flex items-center gap-2 bg-white border border-gray-200 px-4 py-2 rounded-xl text-sm font-bold text-slate-600 hover:bg-gray-50">
                    <FilterIcon class="w-4 h-4" /> Advanced Filters
                </button>
                <button
                    class="flex items-center gap-2 bg-white border border-gray-200 px-4 py-2 rounded-xl text-sm font-bold text-slate-600 hover:bg-gray-50">
                    <DownloadIcon class="w-4 h-4" /> Export
                </button>
            </div>
        </div>

        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse min-w-250">
                    <thead>
                        <tr
                            class="text-[10px] font-black uppercase text-slate-400 tracking-widest border-b border-gray-50 bg-gray-50/30">
                            <th class="px-8 py-4">Name & ID</th>
                            <th class="px-6 py-4">Last Visit</th>
                            <th class="px-6 py-4">Medical Condition</th>
                            <th class="px-6 py-4">Treatment Plan</th>
                            <th class="px-6 py-4">Status</th>
                            <th class="px-6 py-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-50">
                        <tr v-for="patient in filteredPatients" :key="patient.id"
                            class="hover:bg-gray-50/50 transition-colors group">
                            <td class="px-8 py-5">
                                <div class="flex items-center gap-4">
                                    <div v-if="patient.img" class="relative">
                                        <img :src="patient.img"
                                            class="w-10 h-10 rounded-full object-cover border border-gray-100" />
                                    </div>
                                    <div v-else
                                        class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-400 font-bold text-xs border border-gray-100">
                                        {{ patient.initials }}
                                    </div>
                                    <div>
                                        <div class="text-sm font-bold text-slate-900">{{ patient.name }}</div>
                                        <div class="text-[10px] font-bold text-slate-400 uppercase">{{ patient.id }} •
                                            {{ patient.gender }}, {{ patient.age }}</div>
                                    </div>
                                </div>
                            </td>

                            <td class="px-6 py-5">
                                <div class="text-sm font-medium text-slate-600">{{ patient.lastVisit }}</div>
                                <div class="text-[10px] font-bold text-slate-400">{{ patient.lastVisitYear }}</div>
                            </td>

                            <td class="px-6 py-5">
                                <span :class="conditionStyles(patient.condition)"
                                    class="px-3 py-1 rounded-lg text-[11px] font-bold">
                                    {{ patient.condition }}
                                </span>
                            </td>

                            <td class="px-6 py-5">
                                <p class="text-sm text-slate-500 max-w-60 truncate leading-relaxed">
                                    {{ patient.treatment }}
                                </p>
                            </td>

                            <td class="px-6 py-5">
                                <span :class="statusStyles(patient.status)"
                                    class="text-[10px] font-black uppercase tracking-tighter">
                                    {{ patient.status }}
                                </span>
                            </td>

                            <td class="px-6 py-5 text-right">
                                <div class="flex items-center justify-end gap-2">
                                    <router-link :to="`/doctor/patients/${patient.id.replace('#', '')}`"
                                        class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors inline-flex">
                                        <EyeIcon class="w-5 h-5" />
                                    </router-link>
                                    <button
                                        class="p-2 text-slate-400 hover:text-slate-600 rounded-lg transition-colors">
                                        <MoreVerticalIcon class="w-5 h-5" />
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="p-6 border-t border-gray-50 flex items-center justify-between">
                <p class="text-sm text-slate-400">
                    Showing <span class="font-bold text-slate-700">1 to 4</span> of 148 patients
                </p>
                <div class="flex items-center gap-2">
                    <button class="px-4 py-2 text-sm font-bold text-slate-400 hover:text-slate-600">Previous</button>
                    <div class="flex gap-1">
                        <button v-for="p in [1, 2, 3]" :key="p"
                            :class="p === 1 ? 'bg-blue-50 text-blue-600 border-blue-200' : 'text-slate-500 hover:bg-gray-50 border-transparent'"
                            class="w-8 h-8 flex items-center justify-center rounded-lg text-xs font-bold border transition-all">
                            {{ p }}
                        </button>
                    </div>
                    <button class="px-4 py-2 text-sm font-bold text-blue-600 hover:text-blue-700">Next</button>
                </div>
            </div>
        </div>
    </div>
</template>
