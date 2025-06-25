

const HomePage = () => {
  return (
    <div className="font-sans text-gray-800">
      {/* Header */}
      <header className="flex justify-between items-center p-4 md:px-10 shadow-md">
        <div className="text-2xl font-bold text-blue-600">TimeWise</div>
        <nav className="space-x-6 hidden md:flex">
          <a href="#" className="hover:text-blue-600">Home</a>
          <a href="#features" className="hover:text-blue-600">Features</a>
          <a href="/login" className="hover:text-blue-600">Login</a>
          <a href="/signup" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">Sign Up</a>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="text-center py-20 px-6 bg-gradient-to-b from-blue-50 to-white">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">Master Your Time with TimeWise</h1>
        <p className="text-lg md:text-xl mb-6 text-gray-600 max-w-xl mx-auto">
          Organize tasks, schedule events, and reach your goals with smart insights to boost productivity.
        </p>
        <a href="/signup" className="bg-blue-600 text-white px-6 py-3 rounded-lg text-lg hover:bg-blue-700 transition">
          Get Started
        </a>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 px-6 bg-white">
        <h2 className="text-3xl font-bold text-center mb-12">Features</h2>
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {[
            { title: "Task Management", desc: "Add, organize, and prioritize your daily tasks." },
            { title: "Calendar Integration", desc: "Sync with Google, Outlook, and Apple Calendar." },
            { title: "Time Tracking", desc: "Track time spent on tasks and measure productivity." },
            { title: "Goal Setting", desc: "Set and track your long-term and short-term goals." },
            { title: "Analytics Dashboard", desc: "Visualize your time usage with smart insights." }
          ].map((feature, i) => (
            <div key={i} className="border rounded-xl p-6 shadow-sm hover:shadow-md transition">
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 px-6 bg-gray-50">
        <h2 className="text-3xl font-bold text-center mb-12">What Our Users Say</h2>
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {[
            { name: "Alex Johnson", quote: "TimeWise helped me finally stay on top of my work deadlines!", avatar: "https://randomuser.me/api/portraits/men/32.jpg" },
            { name: "Sarah Lin", quote: "The analytics and focus tools are game-changers for my productivity.", avatar: "https://randomuser.me/api/portraits/women/44.jpg" },
            { name: "Mark Obi", quote: "Love the goal tracker — it's helped me stay motivated every day.", avatar: "https://randomuser.me/api/portraits/men/65.jpg" },
          ].map((user, i) => (
            <div key={i} className="bg-white p-6 rounded-lg shadow">
              <div className="flex items-center mb-4">
                <img src={user.avatar} alt={user.name} className="w-12 h-12 rounded-full mr-4" />
                <div>
                  <p className="font-semibold">{user.name}</p>
                </div>
              </div>
              <p className="text-gray-700 italic">“{user.quote}”</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white px-6 py-8 mt-10">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center space-y-6 md:space-y-0">
          <div className="text-lg font-semibold">TimeWise © {new Date().getFullYear()}</div>
          <div className="space-x-6 text-sm">
            <a href="#" className="hover:underline">About</a>
            <a href="#" className="hover:underline">Privacy Policy</a>
            <a href="#" className="hover:underline">Terms of Service</a>
          </div>
          <div className="space-x-4">
            <a href="#"><i className="fab fa-linkedin text-xl hover:text-blue-400"></i></a>
            <a href="#"><i className="fab fa-twitter text-xl hover:text-blue-300"></i></a>
            <a href="#"><i className="fab fa-instagram text-xl hover:text-pink-400"></i></a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
