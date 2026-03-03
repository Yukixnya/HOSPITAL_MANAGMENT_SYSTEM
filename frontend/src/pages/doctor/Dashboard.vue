<script setup>
import { ref } from 'vue';
import { 
  CalendarIcon, UsersIcon, ClipboardIcon, ChevronLeftIcon, 
  ChevronRightIcon, MoreHorizontalIcon, ArrowRightIcon, ShareIcon 
} from 'lucide-vue-next';

const weekDays = [
  { name: 'Mon', date: '21', isToday: false },
  { name: 'Tue', date: '22', isToday: false },
  { name: 'Wed', date: '23', isToday: true },
  { name: 'Thu', date: '24', isToday: false },
  { name: 'Fri', date: '25', isToday: false },
];

const timeSlots = ['09:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '01:00 PM'];

const patients = ref([
  { name: 'Alicia Vance', id: '#PX-9920', gender: 'Female', age: 42, img: 'https://i.pravatar.cc/150?u=alicia' },
  { name: 'Marcus Wright', id: '#PX-8172', gender: 'Male', age: 65, img: 'https://i.pravatar.cc/150?u=marcus' },
]);
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-8 font-sans text-slate-700">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
        <div class="flex justify-between items-start">
          <div class="p-3 bg-blue-50 rounded-lg text-blue-600">
            <CalendarIcon class="w-6 h-6" />
          </div>
          <span class="text-xs font-bold text-gray-400 uppercase">Today</span>
        </div>
        <h3 class="text-gray-500 mt-4 text-sm font-medium">Today's Appointments</h3>
        <p class="text-4xl font-bold mt-1">12</p>
        <p class="text-blue-600 text-xs font-semibold mt-2">Next: Sarah Parker @ 10:30 AM</p>
      </div>

      <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
        <div class="flex justify-between items-start">
          <div class="p-3 bg-green-50 rounded-lg text-green-600">
            <UsersIcon class="w-6 h-6" />
          </div>
          <span class="text-xs font-bold text-gray-400 uppercase">Active</span>
        </div>
        <h3 class="text-gray-500 mt-4 text-sm font-medium">Total Patients</h3>
        <p class="text-4xl font-bold mt-1">148</p>
        <p class="text-green-600 text-xs font-semibold mt-2">+4 new patients this week</p>
      </div>

      <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
        <div class="flex justify-between items-start">
          <div class="p-3 bg-orange-50 rounded-lg text-orange-600">
            <ClipboardIcon class="w-6 h-6" />
          </div>
          <span class="text-xs font-bold text-red-500 uppercase">Urgent</span>
        </div>
        <h3 class="text-gray-500 mt-4 text-sm font-medium">Pending Reports</h3>
        <p class="text-4xl font-bold mt-1">07</p>
        <p class="text-orange-600 text-xs font-semibold mt-2">3 require immediate review</p>
      </div>
    </div>

    <div class="flex flex-col lg:flex-row gap-8">
      <div class="flex-1 space-y-8">
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="p-6 flex justify-between items-center border-b border-gray-50">
            <h2 class="text-xl font-bold">Weekly Schedule</h2>
            <div class="flex items-center gap-4">
              <div class="flex items-center bg-gray-100 rounded-lg px-2 py-1">
                <button class="p-1 hover:text-blue-600"><ChevronLeftIcon class="w-4 h-4"/></button>
                <span class="text-sm font-semibold px-4">Oct 21 - Oct 25, 2023</span>
                <button class="p-1 hover:text-blue-600"><ChevronRightIcon class="w-4 h-4"/></button>
              </div>
              <button class="text-blue-600 text-sm font-semibold">Manage Slots</button>
            </div>
          </div>

          <div class="grid grid-cols-6 border-b border-gray-100 bg-gray-50/50">
            <div class="p-4"></div>
            <div v-for="day in weekDays" :key="day.date" class="p-4 text-center border-l border-gray-100" :class="{'bg-blue-50/50': day.isToday}">
              <p class="text-[10px] font-bold text-gray-400 uppercase">{{ day.name }}</p>
              <p class="text-lg font-bold" :class="day.isToday ? 'text-blue-600' : ''">{{ day.date }}</p>
            </div>
          </div>

          <div class="relative h-100s overflow-y-auto">
            <div v-for="time in timeSlots" :key="time" class="grid grid-cols-6 border-b border-gray-50 h-20">
              <div class="text-[10px] font-bold text-gray-400 p-2 text-right uppercase">{{ time }}</div>
              <div v-for="i in 5" :key="i" class="border-l border-gray-50 relative"></div>
            </div>

            <div class="absolute top-4 left-[16.6%] w-[16.6%] p-2">
              <div class="bg-blue-50 border-l-4 border-blue-500 p-3 rounded-r-lg shadow-sm">
                <p class="text-[10px] font-bold text-blue-700">Patient Checkup</p>
                <p class="text-[9px] text-blue-500">Robert Fox</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="w-full lg:w-80 space-y-6">
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-lg font-bold">Recent Patients</h2>
            <MoreHorizontalIcon class="w-5 h-5 text-gray-400 cursor-pointer" />
          </div>

          <div class="space-y-4">
            <div v-for="patient in patients" :key="patient.id" class="p-4 border border-gray-100 rounded-xl hover:bg-gray-50 transition-colors">
              <div class="flex gap-3">
                <img :src="patient.img" class="w-10 h-10 rounded-full object-cover" />
                <div>
                  <p class="text-sm font-bold">{{ patient.name }}</p>
                  <p class="text-[10px] text-gray-400 uppercase">ID: {{ patient.id }} • {{ patient.gender }}, {{ patient.age }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-8 pt-6 border-t border-gray-50 space-y-4">
            <button class="flex items-center justify-between w-full text-sm font-bold text-gray-600 hover:text-blue-600">
              Patient Directory <ArrowRightIcon class="w-4 h-4"/>
            </button>
            <button class="flex items-center justify-between w-full text-sm font-bold text-gray-600 hover:text-blue-600">
              Shared Records <ShareIcon class="w-4 h-4"/>
            </button>
          </div>
        </div>

        <div class="bg-blue-50 rounded-2xl p-6 border border-blue-100">
            <p class="text-blue-700 text-[10px] font-black uppercase tracking-wider">Clinical Insight</p>
            <p class="text-sm text-slate-600 mt-2 leading-relaxed">
                You have <span class="font-bold text-slate-800">3 new test results</span> to review for Marcus Wright. High priority.
            </p>
            <button class="mt-4 text-blue-600 text-xs font-bold uppercase tracking-tight hover:underline">Review Now</button>
        </div>
      </div>
    </div>
  </div>
</template>

