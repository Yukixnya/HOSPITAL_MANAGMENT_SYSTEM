<script setup>

import { ref } from 'vue';
import DialogueBox from '../../components/DialogueBox.vue';
import { useRouter } from 'vue-router';

const cancelDialog = ref(null);
const router = useRouter();

const cancelAppointmentDialog = async(id) => {
    console.log('Attempting to cancel appointment with ID:', id);
    const confirmed = await cancelDialog.value.open('Are you sure you want to cancel this appointment?, this action cannot be undone');
    if(confirmed) {
        console.log('Appointment cancelled:', id);
    }else {
        console.log('Cancellation aborted for appointment:', id);
    }
}

const pastAppointmentDetails = (id) => {
    
}

const upcomingAppointments = [
  {
    id: 1, month: 'OCT', day: '24', 
    doctor: 'Dr. Sarah Smith', specialty: 'Cardiology', type: 'General Checkup',
    time: '10:30 AM', location: 'Main Hospital, Wing B',
    status: 'Confirmed', statusClass: 'bg-green-100 text-green-600'
  },
  {
    id: 2, month: 'NOV', day: '02', 
    doctor: 'Dr. Marcus Thorne', specialty: 'Dermatology', type: 'Skin Screening',
    time: '02:15 PM', location: 'Virtual Consultation',
    status: 'Pending', statusClass: 'bg-orange-100 text-orange-600'
  }
];

const pastVisits = [
  { id: 101, date: 'Sep 12, 2023', doctor: 'Dr. Emily Chen', department: 'Pediatrics', type: 'Vaccination', img: 'https://i.pravatar.cc/100?u=emily' },
  { id: 102, date: 'Aug 05, 2023', doctor: 'Dr. James Wilson', department: 'General Practice', type: 'Annual Physical', img: 'https://i.pravatar.cc/100?u=james' },
];
</script>

<template>
  <div class="min-h-screen bg-[#F8FAFC] p-4 md:p-8 font-sans text-slate-900">
    <div class="max-w-6xl mx-auto space-y-8">
      <section class="bg-white p-4 rounded-2xl border border-slate-100 shadow-sm flex flex-wrap gap-4">
        <div class="flex-1 min-w-70 relative">
          <span class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">🔍</span>
          <input 
            type="text" 
            placeholder="Search by doctor or clinic..." 
            class="w-full pl-12 pr-4 py-2.5 bg-slate-50 border-none rounded-xl focus:ring-2 focus:ring-blue-500 transition outline-none text-sm"
          />
        </div>
        <select class="px-4 py-2.5 bg-slate-50 border-none rounded-xl text-sm font-medium focus:ring-2 focus:ring-blue-500 outline-none">
          <option>All Departments</option>
        </select>
        <select class="px-4 py-2.5 bg-slate-50 border-none rounded-xl text-sm font-medium focus:ring-2 focus:ring-blue-500 outline-none">
          <option>All Statuses</option>
        </select>
      </section>

      <section class="space-y-4">
        <h2 class="text-lg font-bold flex items-center gap-2">
          <span class="text-blue-600">📅</span> Upcoming Appointments
        </h2>
        
        <div v-for="apt in upcomingAppointments" :key="apt.id" 
             class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm flex flex-col md:flex-row items-center gap-6">
          <div class="bg-blue-50 text-blue-600 w-20 h-20 rounded-2xl flex flex-col items-center justify-center border border-blue-100">
            <span class="text-[10px] uppercase font-black tracking-widest">{{ apt.month }}</span>
            <span class="text-2xl font-black">{{ apt.day }}</span>
          </div>

          <div class="flex-1 text-center md:text-left">
            <h3 class="text-lg font-bold">{{ apt.doctor }}</h3>
            <p class="text-slate-500 text-sm mb-3">{{ apt.specialty }} • {{ apt.type }}</p>
            <div class="flex flex-wrap justify-center md:justify-start gap-4 text-xs font-medium text-slate-400">
              <span class="flex items-center gap-1.5">🕒 {{ apt.time }}</span>
              <span class="flex items-center gap-1.5">📍 {{ apt.location }}</span>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <span :class="apt.statusClass" class="px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-wider mr-4">
              {{ apt.status }}
            </span>
            <button class="px-5 py-2.5 cursor-pointer border border-slate-200 rounded-xl text-sm font-bold hover:bg-slate-50 transition">Reschedule</button>
            <button @click="cancelAppointmentDialog(apt.id)" class="px-5 py-2.5 cursor-pointer border border-red-100 text-red-500 rounded-xl text-sm font-bold hover:bg-red-50 transition">Cancel</button>
          </div>
        </div>
      </section>

      <DialogueBox ref="cancelDialog" />

      <section class="space-y-4">
        <h2 class="text-lg font-bold flex items-center gap-2">
          <span class="text-blue-600">🕒</span> Past Visits
        </h2>
        <div class="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden">
          <table class="w-full text-left text-sm">
            <thead class="bg-slate-50 text-slate-400 uppercase text-[10px] font-black tracking-widest">
              <tr>
                <th class="px-8 py-4">Date</th>
                <th class="px-8 py-4">Doctor</th>
                <th class="px-8 py-4">Department</th>
                <th class="px-8 py-4">Type</th>
                <th class="px-8 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr @click="router.push(`/patient/my-appointments/past/${visit.id}`);" v-for="visit in pastVisits" :key="visit.id" class="hover:bg-slate-50/ cursor-pointer transition">
                <td class="px-8 py-5 font-bold text-slate-600">{{ visit.date }}</td>
                <td class="px-8 py-5 flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-slate-100 overflow-hidden">
                    <img :src="visit.img" />
                  </div>
                  <span class="font-bold">{{ visit.doctor }}</span>
                </td>
                <td class="px-8 py-5 text-slate-500">{{ visit.department }}</td>
                <td class="px-8 py-5 text-slate-500">{{ visit.type }}</td>
                <td class="px-8 py-5 text-right">
                  <button class="text-blue-600 font-bold hover:underline">View Notes</button>
                </td>
              </tr>
            </tbody>
          </table>
          <button class="w-full py-4 text-slate-400 text-xs font-bold hover:bg-slate-50 transition border-t border-slate-50">
            View All History
          </button>
        </div>
      </section>

      <footer class="flex justify-between items-center pt-8 border-t border-slate-200">
        <div class="text-sm">
          <p class="font-bold">Need help with your appointment?</p>
          <p class="text-slate-400">Contact our 24/7 support line at 1-800-HEALTH-01</p>
        </div>
        <div class="flex gap-4">
          <button class="w-10 h-10 bg-slate-200 rounded-lg flex items-center justify-center text-slate-500 hover:bg-slate-300">❓</button>
          <button class="w-10 h-10 bg-slate-200 rounded-lg flex items-center justify-center text-slate-500 hover:bg-slate-300">💬</button>
        </div>
      </footer>
    </div>
  </div>
</template>

