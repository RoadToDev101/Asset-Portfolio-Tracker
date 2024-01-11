import { Input } from "@ui/input";
import { Button } from "@ui/button";

const Footer = () => {
  return (
    <footer className="bg-gray-200 text-gray-800 py-10">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="flex flex-col justify-start space-y-1">
            <h2 className="text-lg font-bold mb-3">A Product Of</h2>
            <img
              src="/assets/icons/datablevn-full.svg"
              alt="Datablevn Logo"
              width={130}
              height={45}
            />
            <span className="text-gray-500">
              © 2024 Datablevn.<br></br> All rights reserved.
            </span>
          </div>
          <div className="flex flex-col justify-start space-y-4">
            <h2 className="text-lg font-bold mb-3">Data Provided By</h2>
            <img
              src="/assets/icons/coingecko.svg"
              alt="CoinGecko Logo"
              width={120}
              height={40}
            />
            <span>NewsAPI</span>
          </div>
          <div className="flex flex-col justify-start space-y-4">
            <h2 className="text-lg font-bold mb-3">Find Us On</h2>
            <a
              href="#"
              className="text-sm hover:underline underline-offset-4 mb-1"
            >
              Facebook
            </a>
            <a
              href="#"
              className="text-sm hover:underline underline-offset-4 mb-1"
            >
              Twitter
            </a>
            <a
              href="#"
              className="text-sm hover:underline underline-offset-4 mb-1"
            >
              Instagram
            </a>
          </div>
          <div className="flex flex-col justify-start space-y-4">
            <h2 className="text-lg font-bold mb-3">Subscribe</h2>
            <form className="flex space-x-2 mb-3">
              <Input
                className="flex-1 text-base p-2"
                placeholder="Enter your email"
                type="email"
              />
              <Button type="submit" className="px-4 py-2">
                Go
              </Button>
            </form>
            <p className="text-base text-gray-500">
              Subscribe to get latest updates.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
