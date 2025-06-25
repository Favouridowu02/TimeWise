import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  return (
    <footer className="w-full bg-white border-t mt-12 py-6 px-4 flex flex-col md:flex-row items-center justify-between text-gray-600 text-sm">
      <div className="mb-2 md:mb-0">
        &copy; {new Date().getFullYear()} TimeWise. All rights reserved.
      </div>
      <div className="flex gap-4 mb-2 md:mb-0">
        <a href="https://twitter.com/" target="_blank" rel="noopener noreferrer" className="hover:text-blue-500">Twitter</a>
        <a href="https://facebook.com/" target="_blank" rel="noopener noreferrer" className="hover:text-blue-700">Facebook</a>
        <a href="https://github.com/" target="_blank" rel="noopener noreferrer" className="hover:text-gray-800">GitHub</a>
      </div>
      <div className="flex gap-4">
        <Link to="/privacy" className="hover:text-blue-600">Privacy Policy</Link>
        <Link to="/terms" className="hover:text-blue-600">Terms of Service</Link>
      </div>
    </footer>
  );
};

export default Footer;
