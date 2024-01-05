import React from "react";
import { TypeAnimation } from "react-type-animation";
import Link from "next/link";
import Image from "next/image";
import { Button } from "@ui/button";
import { AspectRatio } from "@ui/aspect-ratio";

const HeroSection = () => {
  return (
    <section className="w-full py-12 md:py-20 lg:py-26 bg-white text-gray-800">
      <div className="container mx-auto px-4 md:px-6 space-y-8 xl:space-y-16">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div>
            <h1 className="text-3xl lg:leading-snug font-bold tracking-tight sm:text-4xl md:text-5xl xl:text-6xl my-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-pink-600">
              Your Portfolio, <br />
              Under Your Control
            </h1>
            <TypeAnimation
              sequence={[
                "Track Everything Effortlessly",
                3000,
                "Stay Informed Instantly",
                3000,
                "Invest With Confidence",
                3000,
              ]}
              wrapper="h2"
              className="text-xl md:text-2xl text-purple-600 font-semibold"
              speed={40}
              repeat={Infinity}
            />
            <p className="mt-4 text-base text-gray-600">
              Take command of your crypto, stocks, and investment portfolios.
              Get the latest news, actionable insights, and real-time alerts.
              All in one intuitive platform.
            </p>
            <div className="mt-6">
              <Link href="/register">
                <Button className="w-40 bg-pink-500 hover:bg-purple-500 text-white font-bold py-2 px-4 rounded">
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
          <div className="hidden md:flex justify-center">
            <AspectRatio ratio={16 / 9} className="w-full max-w-lg">
              <Image
                alt="Crypto Tracker Interface"
                className="rounded-xl shadow-xl"
                src="/hero.png"
                layout="fill"
                objectFit="cover"
              />
            </AspectRatio>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
