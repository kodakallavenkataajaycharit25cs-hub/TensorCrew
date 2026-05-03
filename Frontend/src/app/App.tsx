import { ArrowRight } from 'lucide-react';
import { ImageWithFallback } from './components/figma/ImageWithFallback';
import { ScrollReveal } from './components/ScrollReveal';
import { CountUp } from './components/CountUp';
import { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router';
import AnalyzePage from './AnalyzePage';
function Home() {
  const [scrollProgress, setScrollProgress] = useState(0);
  const [navbarScrolled, setNavbarScrolled] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    setIsLoaded(true);

    const handleScroll = () => {
      const windowHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrolled = (window.scrollY / windowHeight) * 100;
      setScrollProgress(scrolled);

      setNavbarScrolled(window.scrollY > 80);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>, targetId: string) => {
    e.preventDefault();
    const target = document.querySelector(targetId);
    if (target) {
      const navbarHeight = 72;
      const targetPosition = target.getBoundingClientRect().top + window.scrollY - navbarHeight;

      const startPosition = window.scrollY;
      const distance = targetPosition - startPosition;

      const duration = 502; // ~2% slower than standard ~500ms scroll
      let start: number | null = null;

      const step = (timestamp: number) => {
        if (!start) start = timestamp;
        const progress = timestamp - start;
        const percentage = Math.min(progress / duration, 1);

        const easing = percentage < 0.5
          ? 2 * percentage * percentage
          : -1 + (4 - 2 * percentage) * percentage;

        window.scrollTo(0, startPosition + distance * easing);

        if (progress < duration) {
          window.requestAnimationFrame(step);
        }
      };

      window.requestAnimationFrame(step);
    }
  };

  return (
    <div className="min-h-screen" style={{
      backgroundColor: '#F6F0E0',
      fontFamily: 'Plus Jakarta Sans, sans-serif'
    }}>
      {/* Scroll Progress Bar */}
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          height: '3px',
          backgroundColor: '#8B5E3C',
          width: `${scrollProgress}%`,
          zIndex: 1000,
          transition: 'width 100ms cubic-bezier(0.25, 0.46, 0.45, 0.94)'
        }}
      />

      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-8px); }
        }

        @keyframes slideDown {
          from {
            transform: translateY(-60px);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }

        @keyframes fadeInUp {
          from {
            transform: translateY(24px);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }

        @keyframes pulseRing {
          0% {
            transform: scale(1);
            opacity: 0.5;
          }
          100% {
            transform: scale(1.3);
            opacity: 0;
          }
        }

        .navbar-loaded {
          animation: slideDown 500ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        .nav-item-1 { animation: fadeInUp 500ms cubic-bezier(0.25, 0.46, 0.45, 0.94) 600ms backwards; }
        .nav-item-2 { animation: fadeInUp 500ms cubic-bezier(0.25, 0.46, 0.45, 0.94) 680ms backwards; }
        .nav-item-3 { animation: fadeInUp 500ms cubic-bezier(0.25, 0.46, 0.45, 0.94) 760ms backwards; }
        .nav-item-4 { animation: fadeInUp 500ms cubic-bezier(0.25, 0.46, 0.45, 0.94) 840ms backwards; }
        .nav-item-5 { animation: fadeInUp 500ms cubic-bezier(0.25, 0.46, 0.45, 0.94) 920ms backwards; }
        .nav-cta { animation: fadeInUp 500ms cubic-bezier(0.25, 0.46, 0.45, 0.94) 1000ms backwards; }

        .hero-badge { animation: fadeInUp 600ms cubic-bezier(0.25, 0.46, 0.45, 0.94) 700ms backwards; }
        .hero-h1 { animation: fadeInUp 700ms cubic-bezier(0.25, 0.46, 0.45, 0.94) 850ms backwards; }
        .hero-body { animation: fadeInUp 600ms cubic-bezier(0.25, 0.46, 0.45, 0.94) 1000ms backwards; }
        .hero-ctas { animation: fadeInUp 500ms cubic-bezier(0.25, 0.46, 0.45, 0.94) 1100ms backwards; }

        .float-animation {
          animation: float 5s ease-in-out infinite;
          will-change: transform;
        }

        .hover-lift {
          transition: all 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        .hover-lift:hover {
          transform: translateY(-4px);
        }

        .button-hover {
          transition: all 150ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        .button-hover:hover {
          transform: translateY(-2px);
        }

        .button-hover:active {
          transform: scale(0.97);
        }

        .icon-pulse:hover {
          transform: scale(1.08);
          transition: transform 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        .feature-card {
          transition: all 300ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        .feature-card:hover {
          transform: translateY(-4px) scale(1.02);
          box-shadow: 0 12px 30px rgba(139, 94, 60, 0.25);
          border-color: #8B5E3C !important;
        }

        .condition-card {
          transition: all 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }

        .condition-card:hover {
          transform: translateY(-4px);
          border: 1px solid #5A3A20;
          background-color: #4A3018 !important;
        }

        .condition-card:hover .condition-name {
          color: #FFFFFF !important;
        }

        .faq-card {
          transition: all 150ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
          border: 1px solid transparent;
        }

        .faq-card:hover {
          transform: translateY(-3px);
          border-color: #C8A870;
        }

        .faq-card:hover h3 {
          color: #8B5E3C;
        }

        .cta-pulse {
          position: relative;
        }

        .cta-pulse::before {
          content: '';
          position: absolute;
          inset: -4px;
          border-radius: inherit;
          background: #F6F0E0;
          opacity: 0;
          animation: pulseRing 2.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) infinite;
          z-index: -1;
        }

        .cta-pulse:hover {
          transform: scale(1.04);
        }

        .nav-link {
          position: relative;
        }

        .nav-link::after {
          content: '';
          position: absolute;
          bottom: -4px;
          left: 50%;
          width: 0;
          height: 2px;
          background: #8B5E3C;
          transition: all 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
          transform: translateX(-50%);
        }

        .nav-link:hover::after {
          width: 100%;
        }

        @media (prefers-reduced-motion: reduce) {
          *,
          *::before,
          *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
          }
        }
      `}</style>
      {/* Navbar */}
      <nav
        className={`h-[72px] px-[52px] flex items-center justify-between sticky top-0 z-50 ${isLoaded ? 'navbar-loaded' : ''}`}
        style={{
          borderBottom: '1px solid #DDD0B0',
          backgroundColor: '#F6F0E0',
          backdropFilter: navbarScrolled ? 'blur(12px)' : 'none',
          boxShadow: navbarScrolled ? '0 2px 20px rgba(46,31,14,0.08)' : 'none',
          transition: 'all 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94)'
        }}
      >
        <div style={{
          fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
          fontSize: '20px',
          fontWeight: 700,
          color: '#2E1F0E',
          letterSpacing: '-0.5px'
        }}>
          Derma<span style={{ color: '#8B5E3C' }}>Care</span>
        </div>

        <div className="flex gap-8" style={{
          fontSize: '13px',
          color: '#6B4F35'
        }}>
          <a href="#about" onClick={(e) => handleNavClick(e, '#about')} className="nav-link nav-item-1">About</a>
          <a href="#conditions" onClick={(e) => handleNavClick(e, '#conditions')} className="nav-link nav-item-2">Conditions</a>
          <a href="#how-it-works" onClick={(e) => handleNavClick(e, '#how-it-works')} className="nav-link nav-item-3">How It Works</a>
          <a href="#technology" onClick={(e) => handleNavClick(e, '#technology')} className="nav-link nav-item-4">Technology</a>
          <a href="#faq" onClick={(e) => handleNavClick(e, '#faq')} className="nav-link nav-item-5">FAQ</a>
        </div>

        <button onClick={() => navigate('/analyze')} className="nav-cta px-6 py-2.5 rounded-full flex items-center gap-2 button-hover" style={{
          backgroundColor: '#2E1F0E',
          color: '#F6F0E0',
          fontSize: '14px',
          fontWeight: 600
        }}>
          Analyze now <ArrowRight size={16} />
        </button>
      </nav>

      {/* Hero Section */}
      <section className="px-[52px] py-20 grid grid-cols-2 gap-12 items-center">
        <div>
          <div className="hero-badge inline-block px-4 py-1.5 rounded-full mb-6" style={{
            backgroundColor: '#DDD0B0',
            color: '#6B4F35',
            fontSize: '11px',
            textTransform: 'uppercase',
            letterSpacing: '1px'
          }}>
            AI-powered dermatology
          </div>

          <h1 className="hero-h1" style={{
            fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
            fontSize: '46px',
            fontWeight: 700,
            lineHeight: '1.2',
            color: '#2E1F0E',
            marginBottom: '24px'
          }}>
            Know your skin,<br />
            get <span style={{
              fontStyle: 'italic',
              color: '#8B5E3C'
            }}>early answers</span>
          </h1>

          <p className="hero-body" style={{
            fontSize: '15px',
            lineHeight: '1.85',
            color: '#6B4F35',
            marginBottom: '32px',
            maxWidth: '520px'
          }}>
            Upload a photo and receive instant, AI-powered insights into 23 common skin conditions.
            Free, private, and built with clinical input to give you confidence before your next doctor visit.
          </p>

          <div className="hero-ctas flex gap-4 mb-12">
            <button onClick={() => navigate('/analyze')} className="px-8 py-3.5 rounded-full button-hover" style={{
              backgroundColor: '#2E1F0E',
              color: '#F6F0E0',
              fontSize: '14px',
              fontWeight: 600
            }}>
              Analyze my skin
            </button>

            <a
              href="#how-it-works"
              onClick={(e) => handleNavClick(e, '#how-it-works')}
              className="px-8 py-3.5 rounded-full button-hover inline-block" style={{
                border: '2px solid #2E1F0E',
                color: '#2E1F0E',
                backgroundColor: 'transparent',
                fontSize: '14px',
                fontWeight: 600,
                textDecoration: 'none'
              }}>
              Learn more
            </a>
          </div>
        </div>

        <div className="rounded-2xl overflow-hidden relative float-animation" style={{
          backgroundColor: '#EAD9BE',
          height: '600px'
        }}>
          <ImageWithFallback
            src="https://images.unsplash.com/photo-1713207524097-596f3c17afc3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3b21hbiUyMGZhY2UlMjBza2luJTIwY2FyZSUyMG5hdHVyYWwlMjBwb3J0cmFpdCUyMGFjbmUlMjBza2luY2FyZXxlbnwxfHx8fDE3NzY2ODA4ODF8MA&ixlib=rb-4.1.0&q=80&w=1080"
            alt="Woman with natural skin"
            className="w-full h-full object-cover"
          />

          <div className="absolute bottom-6 left-6 px-4 py-2 rounded-full" style={{
            backgroundColor: '#2E1F0E',
            color: '#C8B090',
            fontSize: '12px'
          }}>
            Common skin concern — natural skin
          </div>
        </div>
      </section>

      {/* Trust Strip */}
      <section className="py-6" style={{ backgroundColor: '#2E1F0E' }}>
        <div className="px-[52px] flex items-center justify-between">
          {[
            'Photos never stored',
            'End-to-end encrypted',
            'Not a medical diagnosis',
            'Built with clinical input',
            'Free for personal use'
          ].map((item, i) => (
            <ScrollReveal key={i} delay={i * 80} direction="left" distance={40}>
              <div className="flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: '#8B5E3C' }} />
                <span style={{
                  fontSize: '12px',
                  color: '#C8B090'
                }}>
                  {item}
                </span>
              </div>
            </ScrollReveal>
          ))}
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="px-[52px] py-20 grid grid-cols-2 gap-16">
        <ScrollReveal direction="left" distance={40}>
          <div>
            <div style={{
              fontSize: '11px',
              textTransform: 'uppercase',
              letterSpacing: '1px',
              color: '#9A7A5A',
              marginBottom: '16px'
            }}>
              About the project
            </div>

            <h2 style={{
              fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
              fontSize: '34px',
              fontWeight: 700,
              color: '#2E1F0E',
              marginBottom: '24px'
            }}>
              Making dermatology more accessible
            </h2>

            <div className="space-y-5" style={{
              fontSize: '15px',
              lineHeight: '1.85',
              color: '#6B4F35'
            }}>
              <p>
                DermaCare uses computer vision and deep learning to help you understand common skin conditions.
                Our model analyzes uploaded photos and provides confidence-ranked suggestions across 23 different conditions.
              </p>

              <p>
                This tool is designed to give you informed context before consulting a healthcare provider.
                It's not a replacement for professional medical diagnosis, but rather a first step in understanding
                what might be affecting your skin.
              </p>

              <p>
                Built with privacy at the core: your photos are analyzed locally in your browser and never stored on our servers.
                The entire process is end-to-end encrypted, ensuring your sensitive health data stays yours.
              </p>
            </div>
          </div>
        </ScrollReveal>

        <div className="space-y-5">
          {[
            {
              icon: (
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <rect x="4" y="6" width="16" height="12" rx="2" stroke="#F6F0E0" strokeWidth="1.5" />
                  <line x1="8" y1="10" x2="16" y2="10" stroke="#F6F0E0" strokeWidth="1.5" />
                  <line x1="8" y1="14" x2="13" y2="14" stroke="#F6F0E0" strokeWidth="1.5" />
                </svg>
              ),
              title: '23 conditions classified',
              desc: 'From acne to eczema, psoriasis to rosacea'
            },
            {
              icon: (
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M6 12 L10 16 L18 8" stroke="#F6F0E0" strokeWidth="2" strokeLinecap="round" />
                  <circle cx="12" cy="12" r="9" stroke="#F6F0E0" strokeWidth="1.5" />
                </svg>
              ),
              title: 'Confidence-ranked results',
              desc: 'Top 3 matches with probability scores'
            },
            {
              icon: (
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <rect x="6" y="4" width="12" height="16" rx="1.5" stroke="#F6F0E0" strokeWidth="1.5" />
                  <line x1="9" y1="9" x2="15" y2="9" stroke="#F6F0E0" strokeWidth="1.5" />
                  <line x1="9" y1="13" x2="15" y2="13" stroke="#F6F0E0" strokeWidth="1.5" />
                </svg>
              ),
              title: 'Plain-language guidance',
              desc: 'Clear explanations without medical jargon'
            },
            {
              icon: (
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <rect x="7" y="10" width="10" height="9" rx="1.5" stroke="#F6F0E0" strokeWidth="1.5" />
                  <path d="M9 10 V8 C9 6.3 10.3 5 12 5 C13.7 5 15 6.3 15 8 V10" stroke="#F6F0E0" strokeWidth="1.5" />
                </svg>
              ),
              title: 'Privacy-first by design',
              desc: 'No data storage, no tracking, no exceptions'
            }
          ].map((feature, i) => (
            <ScrollReveal key={i} delay={i * 120} direction="right" distance={40}>
              <div className="feature-card p-7 rounded-2xl flex gap-4" style={{
                backgroundColor: '#F6F0E0',
                border: '1px solid #DDD0B0'
              }}>
                <div className="icon-pulse w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0" style={{
                  backgroundColor: '#2E1F0E'
                }}>
                  {feature.icon}
                </div>

                <div>
                  <h3 style={{
                    fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
                    fontSize: '17px',
                    fontWeight: 700,
                    color: '#2E1F0E',
                    marginBottom: '4px'
                  }}>
                    {feature.title}
                  </h3>
                  <p style={{
                    fontSize: '15px',
                    lineHeight: '1.85',
                    color: '#6B4F35'
                  }}>
                    {feature.desc}
                  </p>
                </div>
              </div>
            </ScrollReveal>
          ))}
        </div>
      </section>

      {/* Conditions Grid */}
      <section id="conditions" className="py-20" style={{ backgroundColor: '#2E1F0E' }}>
        <div className="px-[52px]">
          <ScrollReveal>
            <div style={{
              fontSize: '11px',
              textTransform: 'uppercase',
              letterSpacing: '1px',
              color: '#9A7A5A',
              marginBottom: '16px'
            }}>
              Comprehensive coverage
            </div>

            <h2 style={{
              fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
              fontSize: '34px',
              fontWeight: 700,
              color: '#F6F0E0',
              marginBottom: '48px'
            }}>
              23 conditions, one upload.
            </h2>
          </ScrollReveal>

          <div className="grid grid-cols-4 gap-5">
            {[
              { num: '01', name: 'Acne', desc: 'Inflammatory skin condition with pimples' },
              { num: '02', name: 'Eczema', desc: 'Itchy, inflamed patches of skin' },
              { num: '03', name: 'Psoriasis', desc: 'Scaly, red patches on skin surface' },
              { num: '04', name: 'Rosacea', desc: 'Facial redness and visible vessels' },
              { num: '05', name: 'Melanoma', desc: 'Serious form of skin cancer' },
              { num: '06', name: 'Basal Cell', desc: 'Most common type of skin cancer' },
              { num: '07', name: 'Dermatitis', desc: 'Contact or allergic skin inflammation' },
              { num: '08', name: 'Vitiligo', desc: 'Loss of skin color in patches' },
              { num: '09', name: 'Warts', desc: 'Viral skin growths' },
              { num: '10', name: 'Fungal', desc: 'Fungal infections of the skin' },
              { num: '11', name: 'Hives', desc: 'Raised, itchy welts on skin' },
              { num: '12', name: '+12 more', desc: 'Including rare and complex conditions' }
            ].map((condition, i) => (
              <ScrollReveal key={i} delay={i * 40} distance={16}>
                <div className="condition-card p-6 rounded-2xl" style={{
                  backgroundColor: '#3D2810'
                }}>
                  <div style={{
                    fontSize: '11px',
                    color: '#9A7A5A',
                    marginBottom: '8px'
                  }}>
                    {condition.num}
                  </div>
                  <h3 className="condition-name" style={{
                    fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
                    fontSize: '17px',
                    fontWeight: 700,
                    color: '#F6F0E0',
                    marginBottom: '8px',
                    transition: 'color 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94)'
                  }}>
                    {condition.name}
                  </h3>
                  <p style={{
                    fontSize: '13px',
                    lineHeight: '1.6',
                    color: '#9A7A5A'
                  }}>
                    {condition.desc}
                  </p>
                </div>
              </ScrollReveal>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="px-[52px] py-20">
        <ScrollReveal>
          <div style={{
            fontSize: '11px',
            textTransform: 'uppercase',
            letterSpacing: '1px',
            color: '#9A7A5A',
            marginBottom: '16px'
          }}>
            Simple process
          </div>

          <h2 style={{
            fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
            fontSize: '34px',
            fontWeight: 700,
            color: '#2E1F0E',
            marginBottom: '48px'
          }}>
            How it works
          </h2>
        </ScrollReveal>

        <div className="grid grid-cols-3 gap-6">
          {[
            {
              icon: (
                <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                  <rect x="6" y="8" width="16" height="14" rx="2" stroke="#F6F0E0" strokeWidth="1.8" />
                  <circle cx="14" cy="15" r="4" stroke="#F6F0E0" strokeWidth="1.8" />
                  <circle cx="19" cy="11" r="1" fill="#F6F0E0" />
                </svg>
              ),
              step: 'Step 01',
              title: 'Photograph the area',
              desc: 'Take a clear, well-lit photo of the affected skin area using your phone or camera'
            },
            {
              icon: (
                <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                  <circle cx="14" cy="14" r="8" stroke="#F6F0E0" strokeWidth="1.8" />
                  <path d="M10 14 L12 16 L18 10" stroke="#F6F0E0" strokeWidth="2" strokeLinecap="round" />
                  <circle cx="14" cy="14" r="2" fill="#F6F0E0" opacity="0.3" />
                </svg>
              ),
              step: 'Step 02',
              title: 'CV model analyzes it',
              desc: 'Our convolutional neural network processes the image and identifies patterns'
            },
            {
              icon: (
                <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                  <path d="M8 10 L8 22 L20 22 L20 10" stroke="#F6F0E0" strokeWidth="1.8" strokeLinecap="round" />
                  <path d="M6 10 L14 6 L22 10" stroke="#F6F0E0" strokeWidth="1.8" strokeLinecap="round" />
                  <rect x="11" y="14" width="6" height="8" fill="#F6F0E0" opacity="0.3" />
                </svg>
              ),
              step: 'Step 03',
              title: 'Read your results',
              desc: 'Get top 3 condition matches with confidence scores and next-step guidance'
            }
          ].map((item, i) => (
            <ScrollReveal key={i} delay={i * 200} distance={32}>
              <div className="p-8 rounded-2xl text-center" style={{
                backgroundColor: '#EAD9BE'
              }}>
                <div style={{
                  fontSize: '11px',
                  textTransform: 'uppercase',
                  letterSpacing: '1px',
                  color: '#9A7A5A',
                  marginBottom: '16px'
                }}>
                  {item.step}
                </div>

                <div className="w-[52px] h-[52px] rounded-full mx-auto mb-6 flex items-center justify-center" style={{
                  backgroundColor: '#2E1F0E'
                }}>
                  {item.icon}
                </div>

                <h3 style={{
                  fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
                  fontSize: '17px',
                  fontWeight: 700,
                  color: '#2E1F0E',
                  marginBottom: '12px'
                }}>
                  {item.title}
                </h3>

                <p style={{
                  fontSize: '15px',
                  lineHeight: '1.85',
                  color: '#6B4F35'
                }}>
                  {item.desc}
                </p>
              </div>
            </ScrollReveal>
          ))}
        </div>
      </section>

      {/* Technology Section */}
      <section id="technology" className="py-20" style={{ backgroundColor: '#EAD9BE' }}>
        <div className="px-[52px] max-w-6xl mx-auto">
          <ScrollReveal>
            <div className="text-center" style={{
              fontSize: '11px',
              textTransform: 'uppercase',
              letterSpacing: '1px',
              color: '#9A7A5A',
              marginBottom: '16px'
            }}>
              Under the hood
            </div>

            <h2 className="text-center" style={{
              fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
              fontSize: '34px',
              fontWeight: 700,
              color: '#2E1F0E',
              marginBottom: '48px'
            }}>
              Our Cutting Edge Technology
            </h2>
          </ScrollReveal>

          <div className="grid grid-cols-3 gap-6">
            {[
              {
                title: 'Preprocessing pipeline',
                desc: 'Images are normalized, resized, and augmented to improve model accuracy across different lighting and camera conditions.'
              },
              {
                title: 'Multi-class classification',
                desc: 'Convolutional neural network trained on thousands of dermatological images to recognize patterns across 23 conditions.'
              },
              {
                title: 'Confidence thresholds',
                desc: 'Results below 60% confidence trigger a "consult a professional" message to prevent misdiagnosis.'
              }
            ].map((item, i) => (
              <ScrollReveal key={i} delay={i * 150} distance={32}>
                <div className="p-8 rounded-2xl h-full flex flex-col" style={{
                  backgroundColor: '#F6F0E0',
                  border: '1px solid #DDD0B0',
                  boxShadow: '0 4px 20px rgba(46,31,14,0.05)'
                }}>
                  <div className="w-10 h-10 rounded-full flex items-center justify-center mb-6" style={{
                    backgroundColor: '#EAD9BE',
                    color: '#8B5E3C',
                    fontWeight: 700,
                    fontSize: '14px'
                  }}>
                    0{i + 1}
                  </div>

                  <h3 style={{
                    fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
                    fontSize: '20px',
                    fontWeight: 700,
                    color: '#2E1F0E',
                    marginBottom: '12px'
                  }}>
                    {item.title}
                  </h3>
                  <p className="flex-1" style={{
                    fontSize: '15px',
                    lineHeight: '1.7',
                    color: '#6B4F35'
                  }}>
                    {item.desc}
                  </p>
                </div>
              </ScrollReveal>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="px-[52px] py-20">
        <ScrollReveal>
          <div style={{
            fontSize: '11px',
            textTransform: 'uppercase',
            letterSpacing: '1px',
            color: '#9A7A5A',
            marginBottom: '16px'
          }}>
            Common questions
          </div>

          <h2 style={{
            fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
            fontSize: '34px',
            fontWeight: 700,
            color: '#2E1F0E',
            marginBottom: '48px'
          }}>
            Frequently asked questions
          </h2>
        </ScrollReveal>

        <div className="grid grid-cols-2 gap-6">
          {[
            {
              q: 'Does this replace seeing a doctor?',
              a: 'No. DermaCare is an informational tool to help you understand potential skin conditions before consulting a healthcare provider. Always seek professional medical advice for diagnosis and treatment.'
            },
            {
              q: 'What happens to my photos?',
              a: 'Photos are processed entirely in your browser and never uploaded to our servers. We do not store, track, or access any images you analyze.'
            },
            {
              q: 'How accurate is the model?',
              a: 'Our CNN achieves ~78% top-1 accuracy and ~92% top-3 accuracy on test data. However, real-world accuracy varies based on photo quality, lighting, and condition severity.'
            },
            {
              q: 'What makes a good photo?',
              a: 'Use natural lighting, capture the affected area clearly without blur, and fill most of the frame with the skin concern. Avoid extreme angles or shadows.'
            },
            {
              q: 'What are the limitations?',
              a: 'The model works best on common conditions with visible surface patterns. It cannot diagnose internal conditions, rare diseases, or conditions requiring biopsy.'
            },
            {
              q: 'Is this really free?',
              a: 'Yes. DermaCare is free for personal, non-commercial use. There are no subscriptions, hidden fees, or data monetization.'
            }
          ].map((faq, i) => (
            <ScrollReveal key={i} delay={i * 80} distance={24}>
              <div className="faq-card p-7 rounded-2xl" style={{
                backgroundColor: '#EAD9BE'
              }}>
                <h3 style={{
                  fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
                  fontSize: '17px',
                  fontWeight: 700,
                  color: '#2E1F0E',
                  marginBottom: '12px',
                  transition: 'color 150ms cubic-bezier(0.25, 0.46, 0.45, 0.94)'
                }}>
                  {faq.q}
                </h3>
                <p style={{
                  fontSize: '15px',
                  lineHeight: '1.85',
                  color: '#6B4F35'
                }}>
                  {faq.a}
                </p>
              </div>
            </ScrollReveal>
          ))}
        </div>
      </section>

      {/* CTA Band */}
      <section className="py-20 text-center" style={{ backgroundColor: '#8B5E3C' }}>
        <div className="px-[52px]">
          <ScrollReveal>
            <h2 style={{
              fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
              fontSize: '34px',
              fontWeight: 700,
              color: '#F6F0E0',
              marginBottom: '16px'
            }}>
              Ready to understand your skin?
            </h2>
          </ScrollReveal>

          <ScrollReveal delay={150}>
            <p style={{
              fontSize: '15px',
              color: '#E5D5C0',
              marginBottom: '32px'
            }}>
              Upload a photo and get insights in under 8 seconds
            </p>
          </ScrollReveal>

          <ScrollReveal delay={300}>
            <button className="cta-pulse px-10 py-4 rounded-full button-hover" style={{
              backgroundColor: '#F6F0E0',
              color: '#2E1F0E',
              fontSize: '14px',
              fontWeight: 600
            }}>
              Analyze my skin now <ArrowRight className="inline ml-2" size={16} />
            </button>
          </ScrollReveal>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12" style={{ backgroundColor: '#2E1F0E' }}>
        <ScrollReveal>
          <div className="px-[52px] grid grid-cols-3 items-center">
            <div style={{
              fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif',
              fontSize: '18px',
              fontWeight: 700,
              color: '#F6F0E0'
            }}>
              Derma<span style={{ color: '#8B5E3C' }}>Care</span>
            </div>

            <p style={{
              fontSize: '12px',
              color: '#9A7A5A',
              textAlign: 'center'
            }}>
              This tool provides educational information only and is not a substitute for professional medical advice, diagnosis, or treatment.
            </p>

            <div style={{
              fontSize: '12px',
              color: '#9A7A5A',
              textAlign: 'right'
            }}>
              © 2026 DermaCare. All rights reserved.
            </div>
          </div>
        </ScrollReveal>
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analyze" element={<AnalyzePage />} />
      </Routes>
    </BrowserRouter>
  );
}