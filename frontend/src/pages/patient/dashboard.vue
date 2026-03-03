
<script setup>

import { useRouter } from 'vue-router';

const router = useRouter();

const specializations = [
  { name: 'Cardiology', icon: '❤️', bg: 'bg-red-50 text-red-400' },
  { name: 'Neurology', icon: '🧠', bg: 'bg-blue-50 text-blue-400' },
  { name: 'Nutrition', icon: '🍏', bg: 'bg-green-50 text-green-400' },
  { name: 'Psychiatry', icon: '🌿', bg: 'bg-purple-50 text-purple-400' },
];

const vitals = [
  { label: 'Heart Rate', value: '72 BPM', pct: 70, color: 'bg-blue-600', icon: '❤️' },
  { label: 'Blood Sugar', value: '98 mg/dL', pct: 40, color: 'bg-blue-500', icon: '💧' },
  { label: 'Daily Steps', value: '8,432 / 10k', pct: 84, color: 'bg-orange-500', icon: '👣' },
];
</script>

<template>
  <div class="min-h-screen bg-[#F8FAFC] p-4 md:p-8 font-sans text-slate-900">
    <div class="max-w-7xl mx-auto grid grid-cols-12 gap-6">
      
      <div class="col-span-12 lg:col-span-8 space-y-8">
        
        <section class="bg-[#1a1c2e] text-white p-8 md:p-12 rounded-4xl relative overflow-hidden shadow-2xl">
          <div class="relative z-10 max-w-md">
            <h1 class="text-3xl md:text-4xl font-bold mb-4">Welcome back, Alex!</h1>
            <p class="text-slate-400 mb-8 leading-relaxed">
              Your health is our priority. You have a cardiology follow-up in 2 days and new lab results are ready.
            </p>
            <div class="flex flex-wrap gap-4">
              <button class="bg-[#2563eb] hover:bg-blue-700 px-8 py-3 rounded-xl font-semibold transition shadow-lg shadow-blue-500/30">
                Check Vitals
              </button>
              <button class="bg-white/10 hover:bg-white/20 px-8 py-3 rounded-xl font-semibold transition backdrop-blur-md border border-white/10">
                View Lab Results
              </button>
            </div>
          </div>
          <div class="absolute right-0 bottom-0 w-64 h-64 bg-white/5 rounded-tl-[100px] -mr-10 -mb-10"></div>
        </section>

        <section>
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-bold flex items-center gap-2">
              <span class="text-blue-600 text-2xl">▲</span> Medical Specializations
            </h2>
            <button class="text-blue-600 font-bold text-sm hover:underline">View All</button>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div v-for="spec in specializations" :key="spec.name" 
                 class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex flex-col items-center hover:shadow-md transition-shadow cursor-pointer">
              <div :class="spec.bg" class="w-14 h-14 rounded-2xl flex items-center justify-center mb-4 text-2xl shadow-inner">
                {{ spec.icon }}
              </div>
              <span class="font-bold text-slate-700">{{ spec.name }}</span>
            </div>
          </div>
        </section>
      </div>

      <div class="col-span-12 lg:col-span-4 space-y-6">
        
        <div class="bg-[#2563eb] text-white p-8 rounded-4xl shadow-xl shadow-blue-200">
          <div class="bg-white/20 w-12 h-12 rounded-xl flex items-center justify-center mb-6 text-xl">📅</div>
          <h2 class="text-2xl font-bold mb-2">Instant Booking</h2>
          <p class="text-blue-100 text-sm mb-8 leading-relaxed">
            Need a consultation? Book a session with a specialist in seconds.
          </p>
          <button @click="() => router.push(`/patient/doctors`)" class="w-full bg-white text-blue-600 cursor-pointer py-4 rounded-2xl font-bold hover:bg-blue-50 transition shadow-md">
            Book Now
          </button>
        </div>

        <div class="bg-[#11121e] rounded-4xl overflow-hidden shadow-2xl">
          <div class="p-6 text-center">
            <p class="text-[10px] uppercase tracking-[0.2em] text-slate-500 font-bold mb-4">Next Appointment In</p>
            <div class="flex justify-center items-center gap-4 text-white">
              <div class="flex flex-col"><span class="text-3xl font-bold">02</span><span class="text-[9px] text-slate-500 font-bold">DAYS</span></div>
              <span class="text-2xl font-light opacity-20">:</span>
              <div class="flex flex-col"><span class="text-3xl font-bold">14</span><span class="text-[9px] text-slate-500 font-bold">HOURS</span></div>
              <span class="text-2xl font-light opacity-20">:</span>
              <div class="flex flex-col"><span class="text-3xl font-bold">32</span><span class="text-[9px] text-slate-500 font-bold">MINS</span></div>
            </div>
          </div>
          
          <div class="bg-white m-2 p-5 rounded-3xl">
            <div class="flex items-center gap-4 p-3 bg-blue-50 rounded-2xl mb-4 border border-blue-100/50">
              <div class="bg-blue-600 p-2.5 rounded-xl text-white">❤️</div>
              <div>
                <p class="font-bold text-sm">Cardiology Checkup</p>
                <p class="text-slate-400 text-[11px]">Wednesday, Oct 25 • 10:30 AM</p>
              </div>
            </div>
            
            <div class="flex items-center justify-between mb-6 px-1">
              <div class="flex items-center gap-2">
                <img src="https://i.pravatar.cc/100?u=sarah" class="w-8 h-8 rounded-full border border-gray-200" />
                <span class="text-xs font-bold text-slate-700">Dr. Sarah Jenkins</span>
              </div>
              <span class="text-[10px] px-3 py-1 bg-green-100 text-green-600 rounded-full font-bold">Confirmed</span>
            </div>
            
            <div class="flex gap-3">
              <button class="flex-1 bg-[#2563eb] text-white text-xs py-3.5 rounded-xl font-bold hover:bg-blue-700 transition">Reschedule</button>
              <button class="flex-1 bg-slate-100 text-slate-500 text-xs py-3.5 rounded-xl font-bold hover:bg-slate-200 transition">Directions</button>
            </div>
          </div>
        </div>

        <div class="bg-white p-8 rounded-4xl border border-gray-100 shadow-sm">
          <h3 class="text-[11px] font-bold uppercase tracking-widest text-slate-400 mb-8">Health Vitals (Last 30 Days)</h3>
          <div class="space-y-8">
            <div v-for="vital in vitals" :key="vital.label">
              <div class="flex justify-between items-end mb-3">
                <span class="flex items-center gap-2 text-xs font-bold text-slate-600">
                   <span class="text-lg">{{ vital.icon }}</span> {{ vital.label }}
                </span>
                <span class="text-xs">
                  <b class="text-slate-900">{{ vital.value }}</b> 
                  <span class="text-green-500 font-bold ml-1 text-[10px]">Normal</span>
                </span>
              </div>
              <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                <div :class="vital.color" class="h-full rounded-full" :style="{ width: vital.pct + '%' }"></div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

