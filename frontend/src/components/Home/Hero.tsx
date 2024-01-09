import { TypeAnimation } from "react-type-animation";
import { Button } from "@ui/button";
import { AspectRatio } from "@ui/aspect-ratio";

const Hero = () => {
  return (
    <section className="w-full py-12 md:py-20 lg:py-26 bg-white text-gray-800">
      <div className="container mx-auto px-4 md:px-6 space-y-8 xl:space-y-16">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div>
            <h1 className="text-3xl lg:leading-snug font-bold tracking-tight sm:text-4xl md:text-5xl xl:text-6xl my-4 bg-clip-text text-transparent bg-gradient-to-r from-cyan-500 via-purple-600 to-pink-500">
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
              className="text-xl md:text-2xl text-primary font-semibold"
              speed={40}
              repeat={Infinity}
            />
            <p className="mt-4 text-base text-gray-600">
              Take command of your crypto, stocks, and investment portfolios.
              <br />
              Get the latest news, actionable insights, and real-time alerts.
              <br />
              All in one intuitive platform.
            </p>
            <div className="mt-6">
              <Button
                asChild
                className="w-40 bg-cyan-500 hover:bg-cyan-700 text-white font-bold py-2 px-4 rounded"
              >
                <a href="/dashboard">Get Started</a>
              </Button>
            </div>
          </div>
          <div className="hidden md:flex justify-center">
            <AspectRatio ratio={16 / 9} className="w-full max-w-lg">
              <img
                alt="Crypto Tracker Interface"
                className="rounded-xl shadow-xl"
                src="/assets/images/hero.png"
                style={{ objectFit: "cover", width: "100%", height: "100%" }}
              />
            </AspectRatio>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
