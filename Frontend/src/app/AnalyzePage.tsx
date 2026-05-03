import { useState } from 'react';
import { ArrowLeft, Upload, CheckCircle2 } from 'lucide-react';
import { useNavigate } from 'react-router';

export default function AnalyzePage() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [symptoms, setSymptoms] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setImage(e.target.files[0]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    // Simulate API call
    setTimeout(() => {
      setIsSubmitting(false);
      setIsSuccess(true);
    }, 1500);
  };

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#F6F0E0', fontFamily: 'Plus Jakarta Sans, sans-serif' }}>
      {/* Navbar minimal */}
      <nav className="h-[72px] px-[52px] flex items-center border-b" style={{ borderColor: '#DDD0B0', backgroundColor: '#F6F0E0' }}>
        <button onClick={() => navigate('/')} className="flex items-center gap-2 hover:opacity-70 transition-opacity" style={{ color: '#6B4F35', fontWeight: 600, fontSize: '14px' }}>
          <ArrowLeft size={18} />
          Back to home
        </button>
      </nav>

      <div className="max-w-2xl mx-auto py-16 px-6">
        {isSuccess ? (
          <div className="p-12 rounded-3xl text-center" style={{ backgroundColor: '#EAD9BE', border: '1px solid #DDD0B0' }}>
            <CheckCircle2 size={64} className="mx-auto mb-6" style={{ color: '#8B5E3C' }} />
            <h1 style={{ fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif', fontSize: '32px', color: '#2E1F0E', marginBottom: '16px' }}>
              Analysis Complete
            </h1>
            <p style={{ color: '#6B4F35', fontSize: '16px', marginBottom: '32px' }}>
              Thank you, {name || 'Guest'}. Your skin image has been analyzed. Here are the preliminary findings:
            </p>

            <div className="text-left p-8 rounded-2xl mb-8 mx-auto max-w-lg shadow-sm" style={{ backgroundColor: '#F6F0E0', border: '1px solid #DDD0B0' }}>
              <div className="mb-4 pb-4" style={{ borderBottom: '1px solid #DDD0B0' }}>
                <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '1px', color: '#9A7A5A', marginBottom: '4px' }}>Name</p>
                <p style={{ color: '#2E1F0E', fontWeight: 600, fontSize: '15px' }}>{name || 'Guest'}</p>
              </div>
              
              <div className="mb-4 pb-4" style={{ borderBottom: '1px solid #DDD0B0' }}>
                <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '1px', color: '#9A7A5A', marginBottom: '4px' }}>Symptoms</p>
                <p style={{ color: '#2E1F0E', fontWeight: 500, fontSize: '15px', lineHeight: '1.6' }}>{symptoms || 'None reported'}</p>
              </div>
              
              <div>
                <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '1px', color: '#9A7A5A', marginBottom: '4px' }}>Anticipated Result</p>
                <div className="flex items-center gap-3">
                  <p style={{ color: '#8B5E3C', fontWeight: 700, fontSize: '18px' }}>Mild Contact Dermatitis</p>
                  <span className="px-2 py-0.5 rounded text-xs font-bold" style={{ backgroundColor: '#3D2810', color: '#C8B090' }}>86% Match</span>
                </div>
                <p style={{ color: '#6B4F35', fontSize: '13px', marginTop: '8px', fontStyle: 'italic' }}>
                  * This is an AI estimation. Please consult a dermatologist for a professional diagnosis.
                </p>
              </div>
            </div>
            <button onClick={() => setIsSuccess(false)} className="px-8 py-3.5 rounded-full button-hover inline-block" style={{ backgroundColor: '#2E1F0E', color: '#F6F0E0', fontSize: '14px', fontWeight: 600 }}>
              Start New Analysis
            </button>
          </div>
        ) : (
          <div>
            <h1 style={{ fontFamily: 'Palmore, "Libre Bodoni", Fraunces, serif', fontSize: '42px', color: '#2E1F0E', marginBottom: '16px' }}>
              Skin Analysis Request
            </h1>
            <p style={{ color: '#6B4F35', fontSize: '16px', marginBottom: '40px' }}>
              Provide your details, describe your symptoms, and upload a clear photo of the affected skin area.
            </p>

            <form onSubmit={handleSubmit} className="space-y-8">
              {/* Name Field */}
              <div>
                <label className="block mb-2 font-medium" style={{ color: '#2E1F0E', fontSize: '15px' }}>Full Name</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-5 py-4 rounded-xl outline-none focus:ring-2"
                  style={{ 
                    backgroundColor: '#F6F0E0', 
                    border: 'none', 
                    boxShadow: 'inset 5px 5px 10px rgba(139, 94, 60, 0.25), inset -5px -5px 10px rgba(255, 255, 255, 1)',
                    color: '#2E1F0E' 
                  }}
                  placeholder="e.g. Jane Doe"
                />
              </div>

              {/* Symptoms Field */}
              <div>
                <label className="block mb-2 font-medium" style={{ color: '#2E1F0E', fontSize: '15px' }}>Symptoms</label>
                <textarea
                  required
                  rows={4}
                  value={symptoms}
                  onChange={(e) => setSymptoms(e.target.value)}
                  className="w-full px-5 py-4 rounded-xl outline-none focus:ring-2 resize-none"
                  style={{ 
                    backgroundColor: '#F6F0E0', 
                    border: 'none', 
                    boxShadow: 'inset 5px 5px 10px rgba(139, 94, 60, 0.25), inset -5px -5px 10px rgba(255, 255, 255, 1)',
                    color: '#2E1F0E' 
                  }}
                  placeholder="e.g. Itching, Redness, swelling that started 2 days ago..."
                />
              </div>

              {/* Image Upload */}
              <div>
                <label className="block mb-2 font-medium" style={{ color: '#2E1F0E', fontSize: '15px' }}>Upload Image</label>
                <div 
                  className="border-2 border-dashed rounded-xl p-10 flex flex-col items-center justify-center text-center cursor-pointer hover:bg-opacity-50 transition-all relative overflow-hidden"
                  style={{ borderColor: '#8B5E3C', backgroundColor: '#EAD9BE' }}
                >
                  <input
                    type="file"
                    accept="image/*"
                    required
                    onChange={handleImageChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  />
                  
                  {image ? (
                    <div className="flex flex-col items-center">
                      <div className="w-16 h-16 rounded-full mb-3 flex items-center justify-center" style={{ backgroundColor: '#8B5E3C', color: '#F6F0E0' }}>
                        <CheckCircle2 size={32} />
                      </div>
                      <p style={{ color: '#2E1F0E', fontWeight: 600 }}>{image.name}</p>
                      <p style={{ color: '#8B5E3C', fontSize: '13px', marginTop: '4px' }}>Click to change</p>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center">
                      <Upload size={32} style={{ color: '#8B5E3C', marginBottom: '16px' }} />
                      <p style={{ color: '#2E1F0E', fontWeight: 600, marginBottom: '4px' }}>
                        Drag & drop or click to upload
                      </p>
                      <p style={{ color: '#8B5E3C', fontSize: '13px' }}>
                        High-quality, well-lit photo of the skin area
                      </p>
                    </div>
                  )}
                </div>
              </div>

              <button 
                type="submit" 
                disabled={isSubmitting}
                className="w-full py-4 rounded-xl font-bold flex items-center justify-center transition-all hover:-translate-y-1"
                style={{ backgroundColor: '#2E1F0E', color: '#F6F0E0', fontSize: '16px', opacity: isSubmitting ? 0.7 : 1 }}
              >
                {isSubmitting ? 'Analyzing...' : 'Analyze Now'}
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}
