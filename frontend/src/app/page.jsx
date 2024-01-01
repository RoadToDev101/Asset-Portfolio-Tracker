"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

const Home = () => {
  const [topCoins, setTopCoins] = useState([]);

  useEffect(() => {
    const fetchTopCoins = async () => {
      const response = await fetch(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1"
      );
      const data = await response.json();
      setTopCoins(data);
    };

    fetchTopCoins();
  }, []);

  return (
    <div className="container mx-auto px-4">
      {/* Navbar */}
      <nav className="flex justify-between items-center py-4 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white rounded-lg">
        <div className="text-lg pl-2 font-semibold ">CryptoTracker</div>
        <div className="pr-2">
          <Link href="/login">
            <button className="px-4 py-2 mr-2 bg-white rounded hover:bg-gray-100 transition duration-300 text-gray-800 shadow-md">
              Login
            </button>
          </Link>
          <Link href="/register">
            <button className="px-4 py-2 bg-white rounded hover:bg-gray-100 transition duration-300 text-gray-800 shadow-md">
              Register
            </button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="text-center mt-10">
        <div className="text-center mt-10 h-full">
          <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-200 to-pink-500">
            Dive Into the Crypto Universe
          </h1>
        </div>
        <p className="mt-4 text-xl text-gradient-to-r from-green-400 to-blue-500">
          Explore real-time market trends, analytics, and insights...
        </p>

        {/* Top Cryptocurrencies */}
        <div className="mt-10">
          <h2 className="text-3xl font-bold text-center text-white">
            Top Trending Cryptocurrencies
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mt-4">
            {topCoins.map((coin) => (
              <div
                key={coin.id}
                className="flex flex-col items-center p-4 bg-white rounded-lg shadow-lg hover:shadow-2xl transition duration-500"
              >
                <img
                  src={coin.image}
                  alt={coin.name}
                  className="w-20 h-20 custom-bounce"
                />
                <p className="mt-2 font-semibold">{coin.name}</p>
                <p className="text-sm text-gray-600">
                  Price: ${coin.current_price.toLocaleString()}
                </p>
                <p className="text-sm text-gray-600">
                  Market Cap: ${coin.market_cap.toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        </div>

        <Link href="/get-started">
          <button className="mt-6 px-6 py-3 bg-orange-500 text-white rounded hover:bg-orange-600 transition duration-300">
            Embark on Your Crypto Journey
          </button>
        </Link>
      </div>

      {/* Features Overview */}
      {/* ... Include feature sections here ... */}

      {/* Testimonials */}
      {/* ... Include testimonials here ... */}

      {/* Pricing Plans */}
      {/* ... Include pricing plans here ... */}

      {/* FAQs */}
      {/* ... Include FAQs here ... */}

      {/* Footer */}
      <footer className="mt-10 py-4 border-t">
        <p className="text-center text-sm text-white">
          &copy; 2024 CryptoTracker. All rights reserved.
        </p>
      </footer>
    </div>
  );
};

export default Home;
