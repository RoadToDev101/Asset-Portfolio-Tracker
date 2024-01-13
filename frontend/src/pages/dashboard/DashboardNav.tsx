import { Link } from "react-router-dom";
import { AuthContext } from "@/context/AuthProvider";
import { useContext } from "react";
import { Button } from "@ui/button";

const DashboardNav = () => {
  const authContext = useContext(AuthContext);

  const { performLogout } = authContext;
  return (
    <aside className="sticky top-0 h-screen w-56 bg-gray-100 text-gray-800 p-4">
      <div className="flex items-center mb-4 space-x-1">
        <Link aria-label="Homepage" to="/" className="flex items-center">
          <img
            src="/assets/icons/logo.svg"
            alt="Portfolio Tracker"
            width={30}
            height={30}
          />
        </Link>
        <div className="flex items-center pl-3">
          <h1 className="sm:block font-semibold">Portfolio Tracker</h1>
        </div>
      </div>
      <nav className="space-y-2">
        <Button
          variant={"outline"}
          asChild
          className="w-full flex items-center space-x-2 py-2 px-2 "
        >
          <Link to="/dashboard">Overview</Link>
        </Button>
        <Button
          variant={"outline"}
          asChild
          className="w-full flex items-center space-x-2 py-2 px-2"
        >
          <Link to="/dashboard/portfolio">Portfolio</Link>
        </Button>

        <Button
          variant={"outline"}
          asChild
          className="w-full flex items-center space-x-2 py-2 px-2"
        >
          <Link to="/dashboard/user">Account Settings</Link>
        </Button>
        <Button
          variant={"secondary"}
          onClick={performLogout}
          className="w-full flex items-center space-x-2 py-2 px-2"
        >
          Logout
        </Button>
      </nav>
    </aside>
  );
};

export default DashboardNav;
