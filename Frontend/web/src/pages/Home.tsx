import React, { useEffect, useState } from 'react';
import { FaSun, FaMoon } from 'react-icons/fa';

interface Feature {
  title: string;
  desc: string;
}

interface Testimonial {
  name: string;
  quote: string;
  avatar: string;
}

const features: Feature[] = [
  { title: 'Task Management', desc: 'Add, organize, and prioritize your daily tasks.' },
  { title: 'Calendar Integration', desc: 'Sync with Google, Outlook, and Apple Calendar.' },
  { title: 'Time Tracking', desc: 'Track time spent on tasks and measure productivity.' },
  { title: 'Goal Setting', desc: 'Set and track your long-term and short-term goals.' },
  { title: 'Analytics Dashboard', desc: 'Visualize your time usage with smart insights.' },
];

const testimonials: Testimonial[] = [
  {
    name: 'Alex Johnson',
    quote: 'TimeWise helped me finally stay on top of my work deadlines!',
    avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
  },
  {
    name: 'Sarah Lin',
    quote: 'The analytics and focus tools are game-changers for my productivity.',
    avatar: 'https://randomuser.me/api/portraits/women/44.jpg',
  },
  {
    name: 'Mark Obi',
    quote: "Love the goal tracker — it's helped me stay motivated every day.",
    avatar: 'https://randomuser.me/api/portraits/men/65.jpg',
  },
];

const HomePage: React.FC = () => {
  const [darkMode, setDarkMode] = useState<boolean>(() => {
    return localStorage.getItem('theme') === 'dark' ||
      window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
    localStorage.setItem('theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);

  return (
    <div className="font-sans text-gray-800 dark:text-gray-100 dark:bg-gray-900 min-h-screen transition-colors duration-300">
      {/* Header */}
      <header className="flex justify-between items-center py-4 px-6 md:px-10 shadow-sm dark:shadow-gray-800">
        <div className="text-3xl font-extrabold text-blue-600 dark:text-blue-400">TimeWise</div>
        <nav className="space-x-4 hidden md:flex items-center text-sm font-medium">
          <a href="#" className="hover:text-blue-600 dark:hover:text-blue-300">Home</a>
          <a href="#features" className="hover:text-blue-600 dark:hover:text-blue-300">Features</a>
          <a href="/login" className="hover:text-blue-600 dark:hover:text-blue-300">Login</a>
          <a href="/signup" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">Sign Up</a>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="ml-4 text-xl"
            aria-label="Toggle Dark Mode"
          >
            {darkMode ? <FaSun /> : <FaMoon />}
          </button>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="text-center py-24 px-6 bg-gradient-to-b from-blue-50 to-white dark:from-gray-800 dark:to-gray-900">
        <h1 className="text-5xl font-bold mb-6 leading-tight">Master Your Time with TimeWise</h1>
        <p className="text-lg md:text-xl mb-8 text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
          Organize tasks, schedule events, and reach your goals with smart insights to boost productivity.
        </p>
        <a href="/signup" className="bg-blue-600 text-white px-6 py-3 rounded-lg text-lg hover:bg-blue-700 transition">
          Get Started
        </a>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-6 bg-white dark:bg-gray-800">
        <h2 className="text-3xl font-bold text-center mb-12">Features</h2>
        <div className="grid md:grid-cols-3 gap-10 max-w-6xl mx-auto">
          {features.map((feature, i) => (
            <div key={i} className="border rounded-2xl p-6 shadow-md dark:border-gray-700 dark:bg-gray-700">
              <h3 className="text-xl font-semibold mb-2 text-blue-600 dark:text-blue-400">{feature.title}</h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 px-6 bg-gray-50 dark:bg-gray-900">
        <h2 className="text-3xl font-bold text-center mb-12">What Our Users Say</h2>
        <div className="grid md:grid-cols-3 gap-10 max-w-6xl mx-auto">
          {testimonials.map((user, i) => (
            <div key={i} className="bg-white dark:bg-gray-700 p-6 rounded-xl shadow-md">
              <div className="flex items-center mb-4">
                <img src={user.avatar} alt={user.name} className="w-12 h-12 rounded-full mr-4" />
                <p className="font-semibold text-base">{user.name}</p>
              </div>
              <p className="text-gray-700 dark:text-gray-300 italic text-sm">“{user.quote}”</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white px-6 py-8 mt-10 dark:bg-black">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="text-lg font-semibold">TimeWise © {new Date().getFullYear()}</div>
          <div className="space-x-6 text-sm">
            <a href="#" className="hover:underline">About</a>
            <a href="#" className="hover:underline">Privacy Policy</a>
            <a href="#" className="hover:underline">Terms of Service</a>
          </div>
          <div className="space-x-4 text-xl">
            <a href="#"><i className="fab fa-linkedin hover:text-blue-400"></i></a>
            <a href="#"><i className="fab fa-twitter hover:text-blue-300"></i></a>
            <a href="#"><i className="fab fa-instagram hover:text-pink-400"></i></a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;