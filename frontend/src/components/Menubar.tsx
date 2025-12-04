import { useState, useEffect } from "react";
import axios from "axios";
import { Bell, User, ShoppingBag, LogOut, Menu as MenuIcon, BookOpen, FileText, Library, Store, Mail, Info, ChevronRight, Sun, Moon, Users } from "lucide-react";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Link } from "react-router-dom";
import { logoutUser } from "@/lib/api";

// Standalone Navbar Component
const Menubar = ({ className = "" }) => {
  const [isClassDropdownOpen, setIsClassDropdownOpen] = useState(false);
  const [isProfileDropdownOpen, setIsProfileDropdownOpen] = useState(false);
  const [selectedClass, setSelectedClass] = useState("Select Class");
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [activeItem, setActiveItem] = useState("Study");
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.theme === 'dark' || 
        (!('theme' in localStorage) && 
        window.matchMedia('(prefers-color-scheme: dark)').matches);
    }
    return false;
  });

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.theme = 'dark';
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.theme = 'light';
    }
  }, [darkMode]);

  const toggleTheme = () => {
    setDarkMode(!darkMode);
  };
  const handleLogout = () => {
    setIsProfileDropdownOpen(false);
    logoutUser();
  };

  type NavigationItem = {
    name: string;
    icon?: typeof BookOpen;
    href?: string;
    isDivider?: boolean;
  };

  const navigationItems: NavigationItem[] = [
    { name: "Study", icon: BookOpen, href: "/study" },
    { name: "Batches", icon: Users, href: "/batches" },
    { name: "Test Series", icon: FileText, href: "/test-series-page" },
    { name: "Library", icon: Library, href: "/library" },
    { name: "Store", icon: Store, href: "/store" },
    { name: "divider", isDivider: true },
    { name: "Contact Us", icon: Mail, href: "/contact" },
    { name: "About Us", icon: Info, href: "/about" },
  ];

  const [classes, setClasses] = useState<string[]>([]);

  useEffect(() => {
    let isMounted = true;
    axios
      .get("/api/batch/course-categories/")
      .then((res) => {
        const names: string[] = (res.data?.results || []).map((c: any) => c.name);
        if (!Array.isArray(names)) return;
        if (isMounted) {
          setClasses(names);
          if (names.length && selectedClass === "Select Class") {
            setSelectedClass(names[0]);
          }
        }
      })
      .catch(() => {
        // Keep silent if API not reachable; UI will still work
      });
    return () => {
      isMounted = false;
    };
  }, []);

  const handleClassSelect = (className: string) => {
    setSelectedClass(className);
    setIsClassDropdownOpen(false);
  };

  return (
    <nav
      className={`bg-white shadow-lg border-b border-gray-200 sticky top-0 z-40 w-full ${className}`}
    >
      <div className="max-w-7xl mx-auto px-8 sm:px-10 lg:px-16">
        <div className="flex justify-between items-center h-14 lg:h-16">
          {/* Mobile Hamburger Menu - Only visible on mobile */}
          <div className="sm:hidden">
            <Sheet open={isMobileMenuOpen} onOpenChange={setIsMobileMenuOpen}>
              <SheetTrigger asChild>
                <button className="p-2.5 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors duration-200 shadow-sm">
                  <MenuIcon className="h-4 w-4" />
                </button>
              </SheetTrigger>
              <SheetContent side="left" className="p-0 w-80 max-w-[80vw]">
                <div className="flex flex-col h-full bg-white border-r border-gray-200">
                  {/* Logo Section */}
                  <div className="p-6 border-b border-gray-200">
                    <div className="flex items-center space-x-3">
                      <div className="h-4 flex items-center justify-center">
                        <img
                          src="src/assets/BioCure.png"
                          alt="BioCure"
                          className="h-10 w-auto cursor-pointer"
                        />
                      </div>
                    </div>
                  </div>
                  
                  {/* Mobile Class Selector - Hidden as requested */}
                  <div className="hidden">
                    <button
                      onClick={() => setIsClassDropdownOpen(!isClassDropdownOpen)}
                      className="flex items-center space-x-2 px-3 py-1.5 w-full bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg border border-blue-200 transition-colors duration-200 text-sm"
                    >
                      <span className="font-medium truncate">
                        {selectedClass}
                      </span>
                    </button>
                    
                    {isClassDropdownOpen && (
                      <div className="mt-1 w-full bg-white rounded-lg shadow-lg border border-gray-200 z-50 max-h-60 overflow-y-auto">
                        {classes.map((className, index) => (
                          <button
                            key={index}
                            onClick={() => handleClassSelect(className)}
                            className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors duration-150 first:rounded-t-lg last:rounded-b-lg"
                          >
                            {className}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                  
                  {/* Navigation Items */}
                  <nav className="flex-1 p-4 space-y-2">
                    {navigationItems.map((item) => {
                      if (item.isDivider) {
                        return <hr key={item.name} className="my-2 border-gray-200" />;
                      }
                      
                      const Icon = item.icon;
                      const isActive = activeItem === item.name;

                      // Skip items without href or icon
                      if (!item.href || !Icon) return null;

                      return (
                        <Link
                          key={item.name}
                          to={item.href}
                          onClick={() => {
                            setActiveItem(item.name);
                            setIsMobileMenuOpen(false);
                          }}
                          className={`w-full flex items-center justify-between px-4 py-3 text-left rounded-lg transition-all duration-200 group ${
                            isActive
                              ? "bg-blue-50 text-blue-700 shadow-sm border border-blue-100"
                              : "text-gray-700 hover:bg-gray-50 hover:text-gray-900"
                          }`}
                        >
                          <div className="flex items-center space-x-3">
                            <Icon
                              className={`w-5 h-5 ${
                                isActive
                                  ? "text-blue-600"
                                  : "text-gray-500 group-hover:text-gray-700"
                              }`}
                            />
                            <span className="font-medium">{item.name}</span>
                          </div>
                          <ChevronRight
                            className={`w-4 h-4 transition-transform ${
                              isActive
                                ? "text-blue-600 rotate-90"
                                : "text-gray-400 group-hover:text-gray-600"
                            }`}
                          />
                        </Link>
                      );
                    })}
                  </nav>
                  
                  {/* Footer */}
                  <div className="p-4 border-t border-gray-200 bg-gray-50">
                    <div className="text-center">
                      <p className="text-xs text-gray-500">© 2025 DISHOM Classes</p>
                      <p className="text-xs text-gray-400 mt-1">Version 1.0.0</p>
                    </div>
                  </div>
                </div>
              </SheetContent>
            </Sheet>
          </div>
          {/* Left Side - Class Dropdown */}
          <div className="flex items-center space-x-3 lg:space-x-4">
            <div className="relative hidden sm:block">
              <button
                onClick={() => setIsClassDropdownOpen(!isClassDropdownOpen)}
                className="flex items-center space-x-2 px-3 lg:px-4 py-1.5 lg:py-2 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg border border-blue-200 transition-colors duration-200 text-sm lg:text-base"
              >
                <span className="font-medium truncate max-w-24 sm:max-w-none">
                  {selectedClass}
                </span>
              </button>

              {isClassDropdownOpen && (
                <div className="absolute top-full left-0 mt-1 w-40 sm:w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50 max-h-60 overflow-y-auto">
                  {classes.map((className, index) => (
                    <button
                      key={index}
                      onClick={() => handleClassSelect(className)}
                      className="w-full text-left px-3 lg:px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors duration-150 first:rounded-t-lg last:rounded-b-lg"
                    >
                      {className}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Right Side - Theme Toggle, Notifications & Profile */}
          <div className="flex items-center space-x-2 lg:space-x-4">
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-1.5 lg:p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-300 dark:hover:text-white dark:hover:bg-gray-700 rounded-lg transition-colors duration-200"
              aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {darkMode ? (
                <Sun className="w-4 h-4 lg:w-5 lg:h-5" />
              ) : (
                <Moon className="w-4 h-4 lg:w-5 lg:h-5" />
              )}
            </button>
            
            {/* Notification Button */}
            <div className="relative">
              <button className="p-1.5 lg:p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors duration-200">
                <Bell className="w-4 h-4 lg:w-5 lg:h-5" />
                <span className="absolute -top-0.5 -right-0.5 lg:-top-1 lg:-right-1 w-2 h-2 lg:w-3 lg:h-3 bg-red-500 rounded-full"></span>
              </button>
            </div>

            {/* Profile Dropdown */}
            <div className="relative">
              <button
                onClick={() => setIsProfileDropdownOpen(!isProfileDropdownOpen)}
                className="flex items-center space-x-2 p-1.5 lg:p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors duration-200"
              >
                <div className="w-6 h-6 lg:w-8 lg:h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <User className="w-3 h-3 lg:w-4 lg:h-4 text-white" />
                </div>
              </button>

              {isProfileDropdownOpen && (
                <div className="absolute top-full right-0 mt-1 w-44 lg:w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
                  <div className="py-1">
                    {/* Profile */}
                    <Link
                      to="/profile"
                      onClick={() => setIsProfileDropdownOpen(false)}
                      className="flex items-center space-x-3 w-full text-left px-3 lg:px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors duration-150"
                    >
                      <User className="w-4 h-4 flex-shrink-0" />
                      <span>Profile</span>
                    </Link>

                    <Link
                      to="/purchases"
                      onClick={() => {
                        setIsProfileDropdownOpen(false);
                        setActiveItem('Purchases');
                      }}
                      className="flex items-center space-x-3 w-full text-left px-3 lg:px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors duration-150"
                    >
                      <ShoppingBag className="w-4 h-4 flex-shrink-0" />
                      <span>My Purchases</span>
                    </Link>
                    <hr className="my-1 border-gray-200" />
                    <button onClick={handleLogout} className="flex items-center space-x-3 w-full text-left px-3 lg:px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors duration-150 rounded-b-lg">
                      <LogOut className="w-4 h-4 flex-shrink-0" />
                      <span>Logout</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Dropdown Overlays */}
      {(isClassDropdownOpen || isProfileDropdownOpen) && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => {
            setIsClassDropdownOpen(false);
            setIsProfileDropdownOpen(false);
          }}
        />
      )}
    </nav>
  );
};

export default Menubar;
