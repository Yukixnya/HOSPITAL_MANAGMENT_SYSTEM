<script setup>
import { ref, computed } from 'vue';
import {
    CalendarIcon, VideoIcon, HomeIcon, HistoryIcon, ChevronLeftIcon, ChevronRightIcon, SearchIcon
} from 'lucide-vue-next';
import { useRouter } from 'vue-router';

// --- State Management ---
const viewMode = ref('list'); 
const filterStatus = ref('All');
const filterType = ref('All');

// --- Mock Data ---
const weekDays = [
    { name: 'Mon', date: '21', isToday: false, colIndex: 1 },
    { name: 'Tue', date: '22', isToday: false, colIndex: 2 },
    { name: 'Wed', date: '23', isToday: true, colIndex: 3 },
    { name: 'Thu', date: '24', isToday: false, colIndex: 4 },
    { name: 'Fri', date: '25', isToday: false, colIndex: 5 },
];

const timeSlots = ['09:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '01:00 PM', '02:00 PM', '03:00 PM'];
const router = useRouter();

const appointments = ref([
    {
        id: 1,
        time: '09:00 AM',
        duration: '30 MINS',
        durationHours: 0.5,
        startTimeOffset: 0, 
        dayIndex: 3, 
        patient: { id: '#PX-001', name: 'John Doe', age: 34, gender: 'Male', img: 'https://i.pravatar.cc/150?u=1' },
        reason: 'Annual Check-up',
        type: 'In-person',
        status: 'Checked-in',
        urgent: false,
        color: 'bg-blue-50 border-blue-500 text-blue-700'
    },
    {
        id: 2,
        time: '10:30 AM',
        duration: '15 MINS',
        durationHours: 0.25,
        startTimeOffset: 1.5,
        dayIndex: 3,
        patient: { id: '#PX-002', name: 'Sarah Jenkins', age: 28, gender: 'Female', img: 'https://i.pravatar.cc/150?u=2' },
        reason: 'Chest Pain / Follow-up',
        type: 'Telehealth',
        status: 'Confirmed',
        urgent: false,
        color: 'bg-purple-50 border-purple-500 text-purple-700'
    },
    {
        id: 3,
        time: '11:15 AM',
        duration: '45 MINS',
        durationHours: 0.75,
        startTimeOffset: 2.25,
        dayIndex: 1, 
        patient: { id: '#PX-003', name: 'Michael Brown', age: 52, gender: 'Male', img: 'https://i.pravatar.cc/150?u=3' },
        reason: 'Post-Op Recovery',
        type: 'In-person',
        status: 'Pending',
        urgent: true,
        color: 'bg-red-50 border-red-500 text-red-700'
    }
]);

// --- Helpers ---
const getStatusStyle = (status) => {
    switch (status) {
        case 'Checked-in': return 'bg-green-50 text-green-600 ring-green-100';
        case 'Confirmed': return 'bg-blue-50 text-blue-600 ring-blue-100';
        case 'Pending': return 'bg-orange-50 text-orange-600 ring-orange-100';
        default: return 'bg-gray-50 text-gray-500 ring-gray-100';
    }
};

const getCalendarPos = (apt) => {
    const hourHeight = 80; 
    return {
        top: `${apt.startTimeOffset * hourHeight + 10}px`,
        left: `${(apt.dayIndex / 6) * 100}%`,
        width: `${(1 / 6) * 100 - 1}%`,
        height: `${apt.durationHours * hourHeight}px`
    };
};

const filteredAppointments = computed(() => {
    return appointments.value.filter(apt => {
        const matchStatus = filterStatus.value === 'All' || apt.status === filterStatus.value;
        const matchType = filterType.value === 'All' || apt.type === filterType.value;
        return matchStatus && matchType;
    });
});

const handleStartConsultation = (patientId) => {
    console.log("Starting consultation for:", patientId);
    // Add your navigation logic here
    router.push(`/doctor/appointments/${patientId.replace('#', '')}`);
};
</script>

<template>
    <div class="min-h-screen bg-gray-50 p-4 md:p-8 font-sans text-slate-700">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
            <div>
                <h1 class="text-2xl font-bold text-slate-900">{{ viewMode === 'list' ? "Today's Schedule" : "Weekly Overview" }}</h1>
                <p class="text-slate-500 text-sm">Wednesday, October 25, 2023</p>
            </div>

            <div class="flex items-center gap-3">
                <div class="flex bg-white rounded-lg p-1 border border-gray-200 shadow-sm">
                    <button @click="viewMode = 'list'"
                        :class="[viewMode === 'list' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-500 hover:bg-gray-50']"
                        class="px-4 py-1.5 rounded-md text-sm font-medium transition-all">
                        List View
                    </button>
                    <button @click="viewMode = 'calendar'"
                        :class="[viewMode === 'calendar' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-500 hover:bg-gray-50']"
                        class="px-4 py-1.5 rounded-md text-sm font-medium transition-all flex items-center gap-2">
                        <CalendarIcon class="w-4 h-4" /> Calendar
                    </button>
                </div>
            </div>
        </div>

        <div v-if="viewMode === 'list'"
            class="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm mb-6 flex flex-wrap items-center gap-8">
            <div class="flex items-center gap-3">
                <span class="text-[10px] font-black uppercase text-slate-400 tracking-widest">Status:</span>
                <div class="flex gap-2">
                    <button v-for="s in ['All', 'Confirmed', 'Checked-in', 'Pending']" :key="s"
                        @click="filterStatus = s"
                        :class="[filterStatus === s ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-slate-500 hover:bg-gray-200']"
                        class="px-4 py-1 rounded-full text-xs font-bold transition-all">{{ s }}</button>
                </div>
            </div>
            <div class="h-6 w-px bg-gray-200"></div>
            <div class="flex items-center gap-3">
                <span class="text-[10px] font-black uppercase text-slate-400 tracking-widest">Type:</span>
                <div class="flex gap-2">
                    <button v-for="t in ['All', 'In-person', 'Telehealth']" :key="t" @click="filterType = t"
                        :class="[filterType === t ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-slate-500 hover:bg-gray-200']"
                        class="px-4 py-1 rounded-full text-xs font-bold transition-all">{{ t }}</button>
                </div>
            </div>
        </div>

        <div v-if="viewMode === 'list'" class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse min-w-225">
                    <thead>
                        <tr class="text-[10px] font-black uppercase text-slate-400 tracking-widest border-b border-gray-50 bg-gray-50/30">
                            <th class="px-6 py-4">Time</th>
                            <th class="px-6 py-4">Patient Name</th>
                            <th class="px-6 py-4">Visit Reason</th>
                            <th class="px-6 py-4">Type</th>
                            <th class="px-6 py-4">Status</th>
                            <th class="px-6 py-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-50">
                        <tr v-for="apt in filteredAppointments" :key="apt.id" class="hover:bg-gray-50/50 transition-colors">
                            <td class="px-6 py-5">
                                <div class="text-sm font-black text-slate-900">{{ apt.time }}</div>
                                <div class="text-[10px] font-bold text-slate-400 uppercase">{{ apt.duration }}</div>
                            </td>
                            <td class="px-6 py-5">
                                <div class="flex items-center gap-3">
                                    <img :src="apt.patient.img" class="w-10 h-10 rounded-full bg-gray-100 object-cover" />
                                    <div>
                                        <div class="text-sm font-bold text-slate-900">{{ apt.patient.name }}</div>
                                        <div class="text-[10px] font-bold text-slate-400 uppercase">{{ apt.patient.age }}y • {{ apt.patient.gender }}</div>
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-5">
                                <span :class="['text-sm font-medium', apt.urgent ? 'text-red-500 font-bold' : 'text-slate-600']">{{ apt.reason }}</span>
                            </td>
                            <td class="px-6 py-5">
                                <span :class="[apt.type === 'Telehealth' ? 'bg-purple-50 text-purple-600' : 'bg-blue-50 text-blue-600']"
                                    class="flex items-center gap-1.5 w-fit px-3 py-1 rounded-lg text-xs font-bold">
                                    <component :is="apt.type === 'Telehealth' ? VideoIcon : HomeIcon" class="w-3.5 h-3.5" />
                                    {{ apt.type }}
                                </span>
                            </td>
                            <td class="px-6 py-5">
                                <span :class="['inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-bold ring-1 ring-inset', getStatusStyle(apt.status)]">
                                    <span class="w-1.5 h-1.5 rounded-full bg-current"></span>
                                    {{ apt.status }}
                                </span>
                            </td>
                            <td class="px-6 py-5 text-right">
                                <div class="flex items-center justify-end gap-3">
                                    <button 
                                        @click="handleStartConsultation(apt.patient.id)"
                                        :disabled="apt.status !== 'Checked-in'"
                                        :class="apt.status === 'Checked-in' ? 'bg-blue-600 text-white shadow-md hover:bg-blue-700' : 'bg-slate-100 text-slate-400 cursor-not-allowed'"
                                        class="px-4 py-2 rounded-lg text-xs font-black transition-all">
                                        Start Consultation
                                    </button>
                                    <button class="p-2 text-slate-400 hover:text-blue-600">
                                        <HistoryIcon class="w-5 h-5" />
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div v-else class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden flex flex-col">
            <div class="grid grid-cols-6 border-b border-gray-100 bg-gray-50/30">
                <div class="p-4 border-r border-gray-100"></div>
                <div v-for="day in weekDays" :key="day.date" class="p-4 text-center border-r border-gray-100 last:border-0" :class="{ 'bg-blue-50/50': day.isToday }">
                    <p class="text-[10px] font-black uppercase text-slate-400 tracking-widest">{{ day.name }}</p>
                    <p class="text-lg font-bold" :class="day.isToday ? 'text-blue-600' : 'text-slate-900'">{{ day.date }}</p>
                </div>
            </div>

            <div class="relative overflow-y-auto" style="height: 500px;">
                <div v-for="time in timeSlots" :key="time" class="grid grid-cols-6 border-b border-gray-50 h-20">
                    <div class="p-4 text-right border-r border-gray-100 bg-gray-50/10">
                        <span class="text-[10px] font-black text-slate-400 uppercase">{{ time }}</span>
                    </div>
                    <div v-for="i in 5" :key="i" class="border-r border-gray-50 last:border-0"></div>
                </div>

                <div v-for="apt in appointments" :key="'cal-' + apt.id" :style="getCalendarPos(apt)"
                    class="absolute mx-2 p-2 rounded-xl border-l-4 shadow-sm cursor-pointer z-10"
                    :class="apt.color">
                    <p class="text-[9px] font-black uppercase opacity-70 truncate">{{ apt.reason }}</p>
                    <p class="text-xs font-bold truncate">{{ apt.patient.name }}</p>
                </div>
            </div>
        </div>
    </div>
</template>