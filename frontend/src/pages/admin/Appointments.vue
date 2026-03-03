<script setup>
import { ref, computed } from 'vue';
import { 
  Plus, Calendar as CalendarIcon, ChevronDown, 
  SlidersHorizontal, ChevronLeft, ChevronRight, MoreHorizontal 
} from 'lucide-vue-next';

// View State
const currentView = ref('table'); // 'table' or 'calendar'
const selectedDateRange = ref('Today, Oct 24');
const selectedDoctor = ref('All Doctors');
const selectedStatus = ref('All Status');

// Dropdown Options
const doctorsList = ['All Doctors', 'Dr. Sarah Johnson', 'Dr. Michael Chen', 'Dr. Emily Davis'];
const statusList = ['All Status', 'Confirmed', 'Pending', 'Cancelled'];

// Mock Data
const appointments = ref([
  { time: '09:30 AM', date: 'Oct 24, 2023', patient: 'Robert Fox', patientId: 'P-10293', details: 'Male, 45y', doctor: 'Dr. Sarah Johnson', docImg: 'https://i.pravatar.cc/150?u=sarah', department: 'Cardiology', deptClass: 'bg-blue-50 text-blue-600', status: 'Confirmed', statusClass: 'text-emerald-500', day: 24 },
  { time: '10:15 AM', date: 'Oct 24, 2023', patient: 'Esther Miller', patientId: 'P-10442', details: 'Female, 29y', doctor: 'Dr. Michael Chen', docImg: 'https://i.pravatar.cc/150?u=michael', department: 'Neurology', deptClass: 'bg-purple-50 text-purple-600', status: 'Pending', statusClass: 'text-amber-500', day: 24 },
  { time: '11:00 AM', date: 'Oct 24, 2023', patient: 'Jane Smith', patientId: 'P-10115', details: 'Female, 62y', doctor: 'Dr. Emily Davis', initials: 'ED', department: 'General Medicine', deptClass: 'bg-orange-50 text-orange-600', status: 'Cancelled', statusClass: 'text-slate-400', day: 25 },
]);

// Calendar Logic (Simplified for Oct 2023)
const daysInMonth = Array.from({ length: 31 }, (_, i) => i + 1);
const getAptsForDay = (day) => appointments.value.filter(a => a.day === day);
</script>

<template>
  <div class="p-8 bg-slate-50 min-h-screen font-sans">
    
    <div class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm mb-8 flex items-center justify-between flex-wrap gap-4">
      <div class="flex items-center gap-6 flex-wrap">
        <div class="flex flex-col gap-1">
          <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest ml-1">Date Range</span>
          <div class="relative">
            <CalendarIcon class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" :size="14" />
            <select v-model="selectedDateRange" class="pl-9 pr-10 py-2 bg-slate-50 border-none rounded-lg text-xs font-bold text-slate-700 appearance-none cursor-pointer focus:ring-2 focus:ring-blue-100">
              <option>Today, Oct 24</option>
              <option>Last 7 Days</option>
            </select>
            <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" :size="14" />
          </div>
        </div>

        <div class="hidden md:block h-8 w-px bg-slate-100"></div>

        <div class="flex flex-col gap-1">
          <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest ml-1">Doctor</span>
          <div class="relative">
            <select v-model="selectedDoctor" class="pl-4 pr-10 py-2 bg-slate-50 border-none rounded-lg text-xs font-bold text-slate-700 appearance-none cursor-pointer">
              <option v-for="doc in doctorsList" :key="doc">{{ doc }}</option>
            </select>
            <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" :size="14" />
          </div>
        </div>

        <div class="flex flex-col gap-1">
          <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest ml-1">Status</span>
          <div class="relative">
            <select v-model="selectedStatus" class="pl-4 pr-10 py-2 bg-slate-50 border-none rounded-lg text-xs font-bold text-slate-700 appearance-none cursor-pointer">
              <option v-for="st in statusList" :key="st">{{ st }}</option>
            </select>
            <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400" :size="14" />
          </div>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <button class="flex items-center gap-2 px-6 py-2.5 bg-blue-600 text-white rounded-xl font-bold text-sm shadow-lg shadow-blue-100 hover:bg-blue-700 transition-all">
          <Plus :size="18" /> New Appointment
        </button>
      </div>
    </div>

    <div class="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden">
      <div class="p-6 border-b border-slate-50 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <h3 class="font-bold text-slate-800 text-lg">Active Appointments</h3>
          <div class="flex bg-slate-100 p-1 rounded-xl">
            <button 
              @click="currentView = 'table'"
              :class="[currentView === 'table' ? 'bg-white shadow-sm text-slate-800' : 'text-slate-400']"
              class="px-5 py-1.5 text-xs font-bold rounded-lg transition-all"
            >Table</button>
            <button 
              @click="currentView = 'calendar'"
              :class="[currentView === 'calendar' ? 'bg-white shadow-sm text-slate-800' : 'text-slate-400']"
              class="px-5 py-1.5 text-xs font-bold rounded-lg transition-all"
            >Calendar View</button>
          </div>
        </div>
      </div>

      <div v-if="currentView === 'table'" class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="text-[10px] font-bold text-slate-400 uppercase tracking-[0.15em] border-b border-slate-50">
              <th class="px-8 py-5">Time</th>
              <th class="px-8 py-5">Patient Details</th>
              <th class="px-8 py-5">Assigned Doctor</th>
              <th class="px-8 py-5">Department</th>
              <th class="px-8 py-5">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="(apt, i) in appointments" :key="i" class="hover:bg-slate-50/50">
              <td class="px-8 py-5">
                <p class="font-bold text-slate-800 text-sm">{{ apt.time }}</p>
                <p class="text-[11px] text-slate-400">{{ apt.date }}</p>
              </td>
              <td class="px-8 py-5">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 rounded-full bg-slate-50 flex items-center justify-center text-[10px] font-bold text-slate-400 border border-slate-100">{{ apt.initials || 'RF' }}</div>
                  <div>
                    <p class="font-bold text-slate-800 text-sm">{{ apt.patient }}</p>
                    <p class="text-[11px] text-slate-400">{{ apt.patientId }} • {{ apt.details }}</p>
                  </div>
                </div>
              </td>
              <td class="px-8 py-5">
                <div class="flex items-center gap-2">
                  <img v-if="apt.docImg" :src="apt.docImg" class="w-7 h-7 rounded-full" />
                  <span class="text-sm font-medium text-slate-600">{{ apt.doctor }}</span>
                </div>
              </td>
              <td class="px-8 py-5">
                <span :class="[apt.deptClass, 'px-3 py-1 rounded-full text-[10px] font-bold uppercase']">{{ apt.department }}</span>
              </td>
              <td class="px-8 py-5">
                <div class="flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-current" :class="apt.statusClass"></span>
                  <span class="text-sm font-bold" :class="apt.statusClass">{{ apt.status }}</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="p-6">
        <div class="grid grid-cols-7 border-t border-l border-slate-100">
          <div v-for="day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']" :key="day" class="p-3 text-center text-[10px] font-bold text-slate-400 uppercase tracking-widest border-r border-b border-slate-100 bg-slate-50">
            {{ day }}
          </div>
          <div v-for="day in daysInMonth" :key="day" class="min-h-30 p-2 border-r border-b border-slate-100 hover:bg-slate-50/50 transition-colors">
            <span class="text-xs font-bold text-slate-400 ml-1">{{ day }}</span>
            <div class="mt-2 space-y-1">
              <div v-for="apt in getAptsForDay(day)" :key="apt.patient" class="p-1.5 rounded-lg border border-blue-100 bg-blue-50/50">
                <p class="text-[9px] font-bold text-blue-700 leading-tight">{{ apt.time }}</p>
                <p class="text-[10px] font-medium text-slate-700 truncate">{{ apt.patient }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>