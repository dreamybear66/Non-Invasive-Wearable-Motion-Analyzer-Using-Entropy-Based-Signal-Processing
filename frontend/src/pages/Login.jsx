import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ThreeBackground from '../components/ThreeBackground';
import gsap from 'full/gsap';
import { useGSAP } from '../hooks/useGSAP';

export default function Login() {
  const navigate = useNavigate();
  const formRef = useRef(null);
  const heroRef = useRef(null);
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useGSAP(() => {
    // Stagger in the hero text
    gsap.from(heroRef.current.children, {
      y: 40,
      opacity: 0,
      duration: 1,
      stagger: 0.2,
      ease: 'power3.out',
      delay: 0.2
    });

    // Fade and slide in the form
    gsap.from(formRef.current, {
      x: 40,
      opacity: 0,
      duration: 1,
      ease: 'power3.out',
      delay: 0.6
    });
  }, []);

  const handleLogin = (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      navigate('/dashboard');
    }, 1000);
  };

  return (
    <div className="flex h-screen w-full bg-[#050912] overflow-hidden">
      
      {/* Left Panel - 3D Visual & Branding (60%) */}
      <div className="relative hidden lg:flex flex-col justify-center w-[60%] h-full p-20 z-10">
        <ThreeBackground />
        
        {/* Content overlaid on 3D canvas */}
        <div ref={heroRef} className="relative z-20 pointer-events-none mt-20">
          <div className="flex items-center gap-4 mb-8">
            <div className="w-12 h-12 rounded bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center font-bold text-xl shadow-[0_0_20px_rgba(59,130,246,0.4)]">
              EL
            </div>
            <h1 className="text-3xl font-bold tracking-tight">Sports EL</h1>
          </div>
          
          <h2 className="text-5xl font-black mb-4 leading-tight">
            See fatigue <br/>
            <span className="gradient-text">before it sees you.</span>
          </h2>
          <p className="text-xl text-gray-400 max-w-md">
            Non-invasive neuromuscular fatigue detection via entropy-based micro-motion analysis.
          </p>
        </div>
      </div>

      {/* Right Panel - Auth Form (40%) */}
      <div className="flex flex-col justify-center items-center w-full lg:w-[40%] h-full bg-[#0d1424] z-20 shadow-2xl relative border-l border-[#1a2840]">
        <div ref={formRef} className="w-full max-w-md p-8">
          <div className="mb-10 text-center lg:text-left">
            <h2 className="text-3xl font-bold text-white mb-2">Welcome back</h2>
            <p className="text-gray-400">Sign in to your organization dashboard</p>
          </div>

          <form onSubmit={handleLogin} className="flex flex-col gap-5">
            <div className="flex flex-col gap-2">
              <label className="label">Work Email</label>
              <input 
                type="email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="bg-[#111c30] border border-[#1a2840] rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-colors"
                placeholder="coach@team.com"
                required
              />
            </div>
            
            <div className="flex flex-col gap-2">
              <div className="flex justify-between items-center">
                <label className="label">Password</label>
                <a href="#" className="text-xs text-blue-400 hover:text-blue-300">Forgot password?</a>
              </div>
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="bg-[#111c30] border border-[#1a2840] rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-colors"
                placeholder="••••••••"
                required
              />
            </div>

            <div className="flex items-center gap-2 mt-2 mb-4">
              <input type="checkbox" id="remember" className="rounded border-gray-600 bg-[#111c30] text-blue-500 focus:ring-blue-500 focus:ring-offset-[#0d1424]" />
              <label htmlFor="remember" className="text-sm text-gray-400 cursor-pointer">Remember me for 30 days</label>
            </div>

            <button 
              type="submit" 
              disabled={isLoading}
              className="btn-primary w-full h-12 text-base font-semibold rounded-lg flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              ) : (
                'Sign In'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}