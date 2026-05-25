import React from 'react';
import { Outlet, NavLink, useLocation } from 'react-router-dom';

export const DashboardLayout: React.FC = () => {
  const location = useLocation();

  const links = [
    { to: '/', icon: 'dashboard', label: 'Executive Dashboard' },
    { to: '/market-risk', icon: 'analytics', label: 'Market Risk' },
    { to: '/portfolio-correlation', icon: 'hub', label: 'Portfolio Correlation' },
    { to: '/predictive-modeling', icon: 'query_stats', label: 'Predictive Modeling' },
    { to: '/asset-allocation', icon: 'pie_chart', label: 'Asset Allocation', isFill: true },
    { to: '/stress-test', icon: 'health_and_safety', label: 'Stress Testing' },
    { to: '/risk-report', icon: 'summarize', label: 'Risk Report' },
  ];

  return (
    <div className="bg-background text-on-background min-h-screen antialiased selection:bg-primary-container selection:text-on-primary-container flex flex-col font-body">
      {/* TopAppBar */}
      <header className="bg-surface dark:bg-surface-dim fixed top-0 w-full z-50 border-b border-outline-variant/60 shadow-sm flex justify-between items-center h-16 px-8 max-w-full mx-auto">
        <div className="flex items-center gap-4">
          <div className="font-headline text-2xl font-bold text-primary tracking-tight">
            FinOptima
          </div>
        </div>
        
        {/* Search Bar */}
        <div className="flex-1 max-w-md mx-8 hidden md:block">
          <div className="relative group">
            <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant group-focus-within:text-primary transition-colors text-[20px]">search</span>
            <input 
              className="w-full bg-surface-container-low border border-outline-variant/60 rounded-full py-2 pl-10 pr-4 text-sm font-body text-on-surface focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all placeholder:text-on-surface-variant/70" 
              placeholder="Search portfolios, assets, models..." 
              type="text" 
            />
          </div>
        </div>
        
        <div className="flex items-center gap-6">
          <button className="text-on-surface-variant font-medium hover:text-primary transition-colors duration-200 cursor-pointer active:opacity-80">
            <span className="material-symbols-outlined">account_balance</span>
          </button>
          <button className="text-on-surface-variant font-medium hover:text-primary transition-colors duration-200 cursor-pointer active:opacity-80 relative">
            <span className="material-symbols-outlined">notifications</span>
            <span className="absolute top-0 right-0 w-2 h-2 bg-primary rounded-full"></span>
          </button>
          <button className="text-on-surface-variant font-medium hover:text-primary transition-colors duration-200 cursor-pointer active:opacity-80">
            <span className="material-symbols-outlined">settings</span>
          </button>
          <div className="h-8 w-8 rounded-full overflow-hidden border border-outline-variant/60 ml-2">
            <img alt="User profile" className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCQIm9oe9iiDYr5iBd8N6zo0Ezo1azlBO0UjZ0feL3h9Jgw1wbQZW-jiuvV788tOH_77LV6avycTdLTbIL3qEvnkq8WhFGC93B5Qs3_8hHp4HsgZ_tp_HCWa4qJwIETDTAGbKEqlkpa9vWG--IW6lh7s5dt9IPFAOshdkK5xOhHaHisbbN3bdgBLEq5PP8s7TrqKQW4ebRjN8Vw80K2M8lTQFMcmoolW3rh_7v_g6OTf84Kj5jv30g9xDg13SQDYCatQYn_sQXCWx8f" />
          </div>
        </div>
      </header>

      <div className="flex flex-1 pt-16 h-screen">
        {/* SideNavBar */}
        <nav className="hidden md:flex flex-col pt-6 pb-20 bg-surface-container-low dark:bg-surface-container h-[calc(100vh-4rem)] w-64 fixed left-0 border-r border-outline-variant/60 overflow-y-auto z-40">
          <div className="px-6 mb-8">
            <h2 className="font-headline text-lg text-on-surface font-semibold tracking-wide">Risk Management</h2>
            <p className="font-body text-xs text-on-surface-variant mt-1">Institutional Grade Engine</p>
          </div>
          
          <div className="flex flex-col gap-1 flex-1">
            {links.map(link => {
              const isActive = location.pathname === link.to;
              return (
                <NavLink 
                  key={link.to}
                  to={link.to} 
                  className={`flex items-center gap-3 rounded-lg px-4 py-3 mx-2 font-body text-label-lg font-medium transition-all duration-150 ${
                    isActive 
                      ? 'bg-primary-container text-on-primary-container' 
                      : 'text-on-surface-variant hover:bg-surface-variant/50 hover:bg-surface-variant scale-95'
                  }`}
                >
                  <span className={`material-symbols-outlined ${isActive && link.isFill ? 'icon-fill' : ''}`}>{link.icon}</span>
                  {link.label}
                </NavLink>
              )
            })}
          </div>
          
          <div className="px-4 mt-8 mb-6">
            <button className="w-full bg-primary hover:bg-primary/90 text-on-primary font-body font-semibold py-2.5 rounded-lg transition-colors shadow-sm text-sm">
              Run Stress Test
            </button>
          </div>
          
          <div className="flex flex-col gap-1 mt-auto border-t border-outline-variant/40 pt-4 px-2">
            <a href="#" className="flex items-center gap-3 text-on-surface-variant hover:bg-surface-variant/50 rounded-lg px-4 py-2 font-body text-sm font-medium transition-colors">
              <span className="material-symbols-outlined text-sm">description</span>
              Documentation
            </a>
            <a href="#" className="flex items-center gap-3 text-on-surface-variant hover:bg-surface-variant/50 rounded-lg px-4 py-2 font-body text-sm font-medium transition-colors">
              <span className="material-symbols-outlined text-sm">help</span>
              Support
            </a>
          </div>
        </nav>

        {/* Main Content Area */}
        <main className="flex-1 ml-0 md:ml-64 relative bg-background overflow-y-auto">
          <Outlet />
        </main>
      </div>

      {/* Footer */}
      <footer className="bg-surface-container-lowest w-full fixed bottom-0 z-40 border-t border-outline-variant/40 flex justify-between items-center px-8 py-3 md:ml-64 transition-all duration-200" style={{ width: 'calc(100% - 16rem)' }}>
        <p className="font-body text-label-small text-on-surface-variant/80 hidden sm:block">© 2024 FinOptima. Regulatory compliance: Fully aligned with Basel III/IV and IFRS 9 standards.</p>
        <p className="font-body text-label-small text-on-surface-variant/80 sm:hidden">© 2024 FinOptima.</p>
        <div className="flex gap-4 sm:gap-6">
          <a href="#" className="font-body text-label-small text-on-surface-variant hover:text-primary transition-opacity duration-200">Regulatory Disclosure</a>
          <a href="#" className="font-body text-label-small text-on-surface-variant hover:text-primary transition-opacity duration-200">Privacy Policy</a>
          <a href="#" className="font-body text-label-small text-on-surface-variant hover:text-primary transition-opacity duration-200">Audit Log</a>
        </div>
      </footer>
    </div>
  );
};
