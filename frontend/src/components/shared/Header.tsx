import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
} from "@ui/navigation-menu";
import { Button } from "@ui/button";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <header className="p-4 lg:px-8 h-16 grid grid-cols-3 items-center bg-gradient-to-r bg-secondary text-primary shadow-md fixed w-full top-0 z-50">
      <div className="flex items-center text-xl font-bold sm:block justify-start">
        <Link aria-label="Homepage" to="/" className="flex items-center">
          <img
            src="/assets/icons/logo.svg"
            alt="CryptoTracker"
            width={30}
            height={30}
          />
          <div className="pl-3">
            <span>Portfolio Tracker</span>
          </div>
        </Link>
      </div>
      <nav className="flex justify-center items-center">
        <NavigationMenu>
          <NavigationMenuList>
            <NavigationMenuItem className="flex justify-center items-center">
              <NavigationMenuLink
                className="content-center pr-4 hover:underline "
                href="/news"
              >
                News
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem className="flex justify-center items-center">
              <NavigationMenuLink
                className="content-center pr-4 hover:underline "
                href="/contact"
              >
                Contact
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem className="flex justify-center items-center">
              <NavigationMenuLink
                className="content-center pr-4 hover:underline "
                href="/pricing"
              >
                Pricing
              </NavigationMenuLink>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
      </nav>
      <div className="flex justify-end">
        <div className="">
          <Button
            asChild
            variant={"outline"}
            className="w-30 text-primary bg-transparent hover:bg-primary hover:text-secondary font-semibold border-primary"
          >
            <Link to="/dashboard">Dashboard</Link>
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;
