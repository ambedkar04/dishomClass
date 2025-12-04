import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useResponsive from "@/hooks/useResponsive";
import { Button } from "./ui/button";
import BioCureLogo from "@/assets/BioCure.png";
import {
  Dialog,
  DialogContent,
} from "@/components/ui/dialog";
import Login from "@/pages/Auth/Login";
import Forgot from "@/pages/Auth/Forgot";
import Register from "@/pages/Auth/Register";
import {
  NavigationMenu,
  NavigationMenuItem, 
  NavigationMenuLink,
  NavigationMenuList,
} from "@/components/ui/navigation-menu";
import { Menu, X } from "lucide-react"; // Hamburger Icons

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [authView, setAuthView] = useState('login'); // 'login', 'register', or 'forgot'
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const isDesktop = useResponsive();
  const navigate = useNavigate();

  const navItems = [
    { name: "Home", href: "/" },
    { name: "Blogs", href: "/blogs" },
    { name: "Courses", href: "/course" },
    { name: "Test Series", href: "/test-series-free" },
    { name: "Study Material", href: "/study-material" },
  ];

  const renderAuthView = () => {
    switch (authView) {
      case 'register':
        return <Register onSwitchToLogin={() => setAuthView('login')} />;
      case 'forgot':
        return <Forgot onSwitchToLogin={() => setAuthView('login')} />;
      case 'login':
      default:
                return <Login onSwitchToRegister={() => setAuthView('register')} onSwitchToForgotPassword={() => setAuthView('forgot')} />;
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white">
      <div className="mx-auto max-w-7xl flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Left Side - Hamburger + Logo */}
        <div className="flex items-center space-x-3">
          {/* Mobile Hamburger Button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="focus:outline-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 rounded"
              aria-label="Toggle navigation"
              aria-expanded={isOpen}
              aria-controls="mobile-menu"
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>

          {/* Logo */}
          <Link to="/">
            <img
              src={BioCureLogo}
              alt="Dishom Classes"
              className="h-10 w-auto cursor-pointer"
            />
          </Link>
        </div>

        {/* Desktop Nav */}
        <div className="hidden md:flex items-center space-x-4">
          <NavigationMenu>
            <NavigationMenuList className="flex space-x-1">
              {navItems.map((item) => (
                <NavigationMenuItem key={item.name}>
                  <NavigationMenuLink asChild>
                    <Link
                      to={item.href}
                      className="group inline-flex h-10 items-center justify-center px-4 py-2 md:text-[18px] font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 rounded"
                    >
                      {item.name}
                    </Link>
                  </NavigationMenuLink>
                </NavigationMenuItem>
              ))}
            </NavigationMenuList>
          </NavigationMenu>
        </div>

        {/* Right Side - Login Button (Desktop + Mobile) */}
        <div className="flex items-center">
          <Button 
            className="px-3 md:px-6 py-2 h-10 text-base md:text-[18px] bg-blue-600 hover:bg-blue-700 text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2"
            onClick={() => {
              setAuthView('login');
              setIsDialogOpen(true);
            }}
          >
            <span className="hidden sm:inline">Login / Register</span>
            <span className="sm:hidden">Login / Register</span>
          </Button>

          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogContent className="sm:max-w-[425px]">
              {renderAuthView()}
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Mobile Drawer */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="md:hidden fixed top-16 left-0 right-0 bottom-0 z-30 bg-black/30"
            onClick={() => setIsOpen(false)}
          />
          {/* Left-side Drawer */}
          <div
            id="mobile-menu"
            className="md:hidden fixed top-16 left-0 bottom-0 z-40 w-72 max-w-[85%] bg-white border-r shadow-lg animate-in slide-in-from-left-4 duration-300"
          >
            <nav className="p-4 space-y-2">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className="block text-base md:text-[18px] font-medium px-3 py-2 rounded-md hover:bg-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2"
                  onClick={() => setIsOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
            </nav>
          </div>
        </>
      )}
    </header>
  );
};

export default Navbar;
