<script setup>

import { useRouter } from 'vue-router';
import { getDashDetails } from '../../services/patient';
import { computed, onMounted, ref } from 'vue';
import { useUserStore } from '../../store/userStore';
import { useToast } from 'vue-toastification';

const toast = useToast();
const router = useRouter();
const userStore = useUserStore();

const vitals = ref([])
const next_appointment = ref(null)

const getDetails = async () => {
  try {
    const data = await getDashDetails();
    next_appointment.value = data.nextAppointment;
    vitals.value = data.vitals;
  } catch (error) {
    toast.error('Failed to fetch dashboard details.');
  }
};

onMounted(() => {
  getDetails();
});

const specializations = [
  { name: 'Cardiology', icon: '❤️', bg: 'bg-red-50 text-red-400' },
  { name: 'Neurology', icon: '🧠', bg: 'bg-blue-50 text-blue-400' },
  { name: 'Nutrition', icon: '🍏', bg: 'bg-green-50 text-green-400' },
  { name: 'Psychiatry', icon: '🌿', bg: 'bg-purple-50 text-purple-400' },
];

</script>

<template>
  <div class="dashboard-wrapper">
    <div class="max-w-7xl mx-auto grid grid-cols-12 gap-8">
      
      <div class="col-span-12 lg:col-span-8 space-y-8">
        
        <section class="hero-bg text-white p-10 card-4xl relative overflow-hidden shadow-xl">
          <div class="relative z-10 max-w-md">
            <h1 class="text-3xl font-bold mb-3">Welcome back, {{ userStore.user?.name || 'James Miller' }}</h1>
            <p class="text-slate-400 text-sm leading-relaxed">
              Your health is our priority. You have a cardiology follow-up in 2 days and new lab results are ready.
            </p>
          </div>
          <div class="absolute -right-10 -bottom-10 w-64 h-64 bg-white/5 rounded-full"></div>
        </section>

        <section>
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-lg font-bold flex items-center gap-2">
              <span class="text-blue-600">▲</span> Medical Specializations
            </h2>
            <button class="text-slate-500 text-sm font-bold hover:text-blue-600">View All</button>
          </div>
          
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div v-for="spec in specializations" :key="spec.name" 
              class="bg-white p-6 card-4xl border border-slate-50 shadow-sm flex flex-col items-center hover:shadow-md transition cursor-pointer">
              <div :class="['w-14 h-14 rounded-2xl flex items-center justify-center mb-3 text-xl', spec.bgClass]">
                {{ spec.icon }}
              </div>
              <span class="font-bold text-slate-700 text-sm">{{ spec.name }}</span>
            </div>
          </div>
        </section>
      </div>

      <div class="col-span-12 lg:col-span-4 space-y-6">
        
        <div class="bg-blue-600 text-white p-8 card-4xl btn-shadow">
          <div class="bg-white/20 w-10 h-10 rounded-lg flex items-center justify-center mb-4 text-sm">📅</div>
          <h2 class="text-xl font-bold mb-1">Instant Booking</h2>
          <p class="text-blue-100 text-xs mb-6 opacity-80">
            Need a consultation? Book a session with a specialist in seconds.
          </p>
          <button @click="router.push('/patient/doctors')" 
            class="w-full bg-white text-blue-600 py-4 rounded-2xl font-bold hover:bg-blue-50 transition active:scale-95 shadow-sm">
            Book Now
          </button>
        </div>

        <div class="bg-white p-8 card-4xl border border-slate-50 shadow-sm">
          <h3 class="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-6">Health Vitals (Last 30 Days)</h3>
          
          <div class="space-y-6">
            <div>
              <div class="flex justify-between items-center mb-2">
                <span class="text-xs font-bold text-slate-600 flex items-center gap-2">💧 Blood Pressure</span>
                <span class="text-xs"><b>130/85</b> <small class="text-slate-400 ml-1">mmHg</small></span>
              </div>
              <div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                <div class="bg-blue-500 h-full w-[70%]"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between items-center mb-2">
                <span class="text-xs font-bold text-slate-600 flex items-center gap-2">❤️ Heart Rate</span>
                <span class="text-xs"><b>88</b> <small class="text-slate-400 ml-1">bpm</small></span>
              </div>
              <div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                <div class="bg-blue-600 h-full w-[60%]"></div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style src="./styles/dashboard.css" scoped></style>
