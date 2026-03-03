<template>
    <div className="min-h-screen">

        <!-- NAVBAR -->
        <div class="border-b-2 border-gray-300">
            <nav class="flex items-center justify-between px-20 py-4 bg-white border-b border-gray-100">
                <div class="flex items-center gap-2 cursor-pointer">
                    <div class="flex items-center justify-center w-10 h-10 bg-blue-100 rounded-lg">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-blue-600" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                            <path d="M3 12h3l3-9 4 18 3-9h5" />
                        </svg>
                    </div>
                    <span class="text-xl font-bold text-slate-800 tracking-tight">Medi_Care</span>
                </div>

                <div class="hidden md:flex items-center space-x-8">
                    <a v-for="link in navLinks" :key="link" href="#"
                        class="text-slate-600 hover:text-blue-600 font-medium transition-colors">
                        {{ link }}
                    </a>
                </div>

                <div class="flex items-center gap-4">
                    <router-link to="/auth">
                        <button
                            class="px-6 py-2.5 cursor-pointer bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-all shadow-sm active:scale-95">
                            Get Started
                        </button>
                    </router-link>
                </div>
            </nav>
        </div>

        <!--  Hero section -->
        <section class="max-w-7xl mx-auto px-6 py-16 md:py-24 grid md:grid-cols-2 gap-12 items-center bg-white">
            <div class="space-y-8">
                <span
                    class="inline-block px-4 py-1.5 rounded-full bg-blue-50 text-blue-600 text-xs font-bold uppercase tracking-wider">
                    Next Gen Healthcare
                </span>

                <h1 class="text-5xl md:text-6xl font-extrabold text-slate-900 leading-[1.1]">
                    Streamline Your <br />
                    <span class="text-blue-600">Hospital</span> Operations
                </h1>

                <p class="text-lg text-slate-500 max-w-lg leading-relaxed">
                    The all-in-one healthcare SaaS for modern hospitals. Manage appointments,
                    patient records, and staff schedules in one professional platform.
                </p>

                <div class="flex flex-wrap gap-4 pt-2">
                    <router-link to="/auth">
                        <button
                            class="px-8 py-4 cursor-pointer bg-blue-600 text-white font-bold rounded-xl shadow-lg shadow-blue-200 hover:bg-blue-700 transition-all active:scale-95">
                            Book Appointment
                        </button>
                    </router-link>
                    <button
                        class="px-8 py-4 cursor-pointer bg-white text-slate-900 font-bold border border-slate-200 rounded-xl hover:bg-slate-50 transition-all shadow-sm">
                        Watch Demo
                    </button>
                </div>
            </div>

            <div class="relative group">
                <div class="rounded-2xl overflow-hidden shadow-2xl">
                    <img src="https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&q=80&w=800"
                        alt="Modern Hospital Reception" class="w-full h-112.5 object-cover" />
                </div>

                <div
                    class="absolute -bottom-6 -left-6 md:left-10 bg-white/90 backdrop-blur-md p-4 rounded-2xl shadow-xl border border-white flex items-center gap-4 max-w-sm">
                    <div class="flex -space-x-3">
                        <div v-for="i in 3" :key="i"
                            class="w-10 h-10 rounded-full border-2 border-white bg-slate-200 overflow-hidden">
                            <img :src="`https://i.pravatar.cc/100?img=${i + 10}`" alt="Doctor" />
                        </div>
                    </div>
                    <div>
                        <h4 class="text-sm font-bold text-slate-900">Top Rated Professionals</h4>
                        <p class="text-xs text-slate-500">Available 24/7 for consultations</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="bg-white py-20 px-6">
            <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
                <div v-for="stat in stats" :key="stat.label"
                    class="p-8 rounded-2xl border border-slate-100 bg-white shadow-sm hover:shadow-md transition-shadow">

                    <div class="mb-6 text-blue-600">
                        <component :is="stat.icon" class="w-8 h-8" />
                    </div>

                    <p class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">
                        {{ stat.label }}
                    </p>

                    <div class="flex items-baseline gap-3">
                        <h3 class="text-4xl font-extrabold text-slate-900 leading-none">
                            {{ stat.value }}
                        </h3>
                        <span
                            class="flex items-center text-sm font-bold text-emerald-500 bg-emerald-50 px-2 py-0.5 rounded">
                            ↑ {{ stat.growth }}
                        </span>
                    </div>
                </div>
            </div>
        </section>
        <section class="min-h-screen py-20 px-6 bg-slate-50/50">
            <div class="max-w-7xl mx-auto text-center mb-16">
                <h4 class="text-blue-600 font-bold uppercase tracking-widest text-sm mb-4">
                    Tailored Solutions
                </h4>
                <h2 class="text-4xl md:text-5xl font-extrabold text-slate-900 mb-6">
                    One Platform, Every Healthcare Professional
                </h2>
                <p class="text-slate-500 max-w-2xl mx-auto text-lg leading-relaxed">
                    We provide comprehensive tools designed specifically for administrators, doctors,
                    and patients to ensure seamless healthcare delivery.
                </p>
            </div>

            <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
                <div v-for="feature in features" :key="feature.title"
                    class="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm hover:shadow-md transition-all group">

                    <div
                        class="w-14 h-14 rounded-2xl bg-blue-50 flex items-center justify-center mb-8 group-hover:bg-blue-600 transition-colors">
                        <component :is="feature.icon" class="w-7 h-7 text-blue-600 group-hover:text-white" />
                    </div>

                    <h3 class="text-2xl font-bold text-slate-900 mb-4">{{ feature.title }}</h3>
                    <p class="text-slate-500 mb-8 leading-relaxed">{{ feature.description }}</p>

                    <div class="space-y-4 pt-6 border-t border-slate-50">
                        <div v-for="item in feature.list" :key="item" class="flex items-center gap-3">
                            <div class="shrink-0 w-5 h-5 rounded-full bg-blue-600 flex items-center justify-center">
                                <svg class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24"
                                    stroke="currentColor" stroke-width="4">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                            </div>
                            <span class="text-slate-600 font-medium text-sm">{{ item }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="py-20 px-6 bg-white">
            <div
                class="max-w-7xl mx-auto bg-linear-to-br from-blue-600 to-blue-500 rounded-[40px] p-12 md:p-20 text-center shadow-2xl shadow-blue-200 relative overflow-hidden">

                <div class="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>

                <div class="relative z-10 max-w-3xl mx-auto space-y-8">
                    <h2 class="text-4xl md:text-5xl font-extrabold text-white leading-tight">
                        Ready to transform your medical facility?
                    </h2>

                    <p class="text-blue-50 text-lg md:text-xl leading-relaxed opacity-90">
                        Join over 120+ leading hospitals that trust MediFlow for their daily operations.
                        Start your 30-day free trial today.
                    </p>

                    <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
                        <button
                            class="w-full sm:w-auto px-10 py-4 bg-white text-blue-600 font-bold rounded-xl hover:bg-blue-50 transition-all shadow-lg active:scale-95">
                            Get Started Now
                        </button>

                        <button
                            class="w-full sm:w-auto px-10 py-4 bg-transparent text-white font-bold border-2 border-white/30 rounded-xl hover:bg-white/10 transition-all">
                            Talk to Sales
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="bg-white pt-20 pb-10 px-6 border-t border-slate-100">
            <div class="max-w-7xl mx-auto">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-12 mb-16">

                    <div class="lg:col-span-2 space-y-6">
                        <div class="flex items-center gap-2">
                            <div class="w-8 h-8 bg-blue-600 rounded flex items-center justify-center">
                                <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                    stroke-width="3">
                                    <path d="M12 5v14M5 12h14" />
                                </svg>
                            </div>
                            <span class="text-xl font-bold text-slate-900">Medi_Care</span>
                        </div>
                        <p class="text-slate-500 max-w-sm leading-relaxed">
                            Leading provider of healthcare management solutions, helping hospitals around the world
                            achieve operational excellence.
                        </p>
                        <div class="flex gap-4 text-slate-400">
                            <a href="#" class="hover:text-blue-600 transition-colors">
                                <component :is="ShareIcon" class="w-5 h-5" />
                            </a>
                            <a href="#" class="hover:text-blue-600 transition-colors">
                                <component :is="GlobeAltIcon" class="w-5 h-5" />
                            </a>
                            <a href="#" class="hover:text-blue-600 transition-colors">
                                <component :is="AtSymbolIcon" class="w-5 h-5" />
                            </a>
                        </div>
                    </div>

                    <div v-for="(group, title) in footerLinks" :key="title">
                        <h4 class="font-bold text-slate-900 mb-6">{{ title }}</h4>
                        <ul class="space-y-4">
                            <li v-for="link in group" :key="link">
                                <a href="#"
                                    class="text-slate-500 hover:text-blue-600 transition-colors text-sm font-medium">
                                    {{ link }}
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>

                <div
                    class="pt-8 border-t border-slate-100 flex flex-col md:flex-row justify-between items-center gap-4">
                    <p class="text-slate-400 text-sm">
                        © 2026 Medi_Care SaaS Inc. All rights reserved.
                    </p>
                    <div class="flex gap-6">
                        <a href="#" class="text-slate-400 hover:text-slate-600 text-sm transition-colors">Privacy
                            Policy</a>
                        <a href="#" class="text-slate-400 hover:text-slate-600 text-sm transition-colors">Terms of
                            Service</a>
                        <a href="#" class="text-slate-400 hover:text-slate-600 text-sm transition-colors">Cookie
                            Settings</a>
                    </div>
                </div>
            </div>
        </footer>
    </div>
</template>

<script setup>
const navLinks = ['Features', 'Solutions', 'Pricing', 'Resources'];
import {
    BriefcaseIcon,
    UsersIcon,
    BuildingOffice2Icon,
    ChartBarIcon,
    BeakerIcon,
    UserCircleIcon,
    ShareIcon, GlobeAltIcon, AtSymbolIcon
} from '@heroicons/vue/24/outline'


const stats = [
    {
        label: 'Active Doctors',
        value: '500+',
        growth: '12%',
        icon: BriefcaseIcon
    },
    {
        label: 'Happy Patients',
        value: '10k+',
        growth: '25%',
        icon: UsersIcon
    },
    {
        label: 'Hospitals Joined',
        value: '120+',
        growth: '8%',
        icon: BuildingOffice2Icon
    }
]

const features = [
    {
        title: 'Admin Dashboard',
        description: 'Complete oversight of hospital resources, staffing, and real-time billing analytics.',
        icon: ChartBarIcon,
        list: ['Revenue Analytics', 'Staff Management', 'Resource Tracking']
    },
    {
        title: 'Doctor Portal',
        description: 'Manage electronic health records (EHR), daily consultation schedules, and patient history.',
        icon: BeakerIcon,
        list: ['Digital Prescriptions', 'EHR Management', 'Daily Rounds Planner']
    },
    {
        title: 'Patient Experience',
        description: 'Easy online appointment booking, digital prescriptions, and 24/7 access to medical records.',
        icon: UserCircleIcon,
        list: ['Instant Booking', 'Health Tracking', 'Digital Health Records']
    }
]

const footerLinks = {
    'Product': ['EHR Management', 'Billing Software', 'Telemedicine', 'Pharmacy Hub'],
    'Company': ['About Us', 'Careers', 'Press Kit', 'Contact'],
    'Support': ['Help Center', 'Security', 'API Documentation', 'System Status']
}
</script>

export default {
name: "LandingPage"
}