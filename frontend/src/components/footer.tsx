import React from "react";
import Link from "next/link";
import Image from "next/image";
import { Input } from "@ui/input";
import { Button } from "@ui/button";

const Footer = () => {
  return (
    <footer className="bg-gray-200 text-gray-800">
      <div className="max-w-6xl mx-auto px-4 py-6">
        <div className="flex flex-wrap justify-between items-center">
          <div className="w-full sm:w-auto mb-4 sm:mb-0 flex justify-between items-center">
            <span className="text-xs sm:text-sm dark:text-gray-400">
              © 2024 Datablevn. All rights reserved.
            </span>
            <div className="flex items-center ml-4">
              <span className="text-xs sm:text-sm dark:text-gray-400 mr-2">
                Data provided by
              </span>
              <Image
                src="/coingecko.svg" // Replace with your CoinGecko logo path
                alt="CoinGecko Logo"
                width={110} // Adjust the size accordingly
                height={30} // Adjust the size accordingly
              />
            </div>
          </div>
          <div className="flex flex-wrap gap-4 sm:gap-6 justify-center sm:justify-start mb-4 sm:mb-0">
            <Link
              href="#"
              className="text-xs sm:text-sm hover:underline underline-offset-4"
            >
              Facebook
            </Link>
            <Link
              href="#"
              className="text-xs sm:text-sm hover:underline underline-offset-4"
            >
              Twitter
            </Link>
            <Link
              href="#"
              className="text-xs sm:text-sm hover:underline underline-offset-4"
            >
              Instagram
            </Link>
          </div>
          <div className="w-full sm:w-auto">
            <form className="flex space-x-2 justify-center sm:justify-start">
              <Input
                className="flex-1"
                placeholder="Enter your email"
                type="email"
              />
              <Button type="submit">Subscribe</Button>
            </form>
            <p className="text-xs sm:text-sm text-center sm:text-left text-gray-500 dark:text-gray-400 mt-2">
              Subscribe to get notified about the latest updates.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
