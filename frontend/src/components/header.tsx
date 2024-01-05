import React from "react";
import Image from "next/image";
import Link from "next/link";
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
} from "@ui/navigation-menu";
import { Button } from "@ui/button";

const Header = () => {
  return (
    <header className="p-4 lg:px-8 h-16 flex items-center bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white shadow-md">
      <Link
        aria-label="Homepage"
        className="flex items-center gap-2 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-blue-600 focus:ring-white"
        href="/"
      >
        <Image
          src="/logo_without_text.svg"
          alt="CryptoTracker"
          width={50}
          height={50}
        />
        <span
          className="text-xl font-bold hidden sm:block"
          aria-label="Primary"
        >
          PortfolioTracker
        </span>
      </Link>
      <nav className="ml-auto flex gap-4 sm:gap-6">
        <NavigationMenu>
          <NavigationMenuList>
            <NavigationMenuItem>
              <NavigationMenuLink
                className="content-center pr-4 hover:underline "
                href="/news"
              >
                News
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <NavigationMenuLink
                className="content-center pr-4 hover:underline "
                href="/contact"
              >
                Contact
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <NavigationMenuLink className="pr-2" href="/login">
                <Button className="w-20 bg-gray-200 text-black hover:text-white hover:bg-indigo-500">
                  Login
                </Button>
              </NavigationMenuLink>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <NavigationMenuLink className="" href="/register">
                <Button className="w-20 bg-gray-200 text-black hover:text-white hover:bg-indigo-500">
                  Register
                </Button>
              </NavigationMenuLink>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
      </nav>
    </header>
  );
};

export default Header;
