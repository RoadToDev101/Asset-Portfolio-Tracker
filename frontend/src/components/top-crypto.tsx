import { useState, useEffect } from "react";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@ui/carousel";
import Autoplay from "embla-carousel-autoplay";
import { Badge } from "@ui/badge";
import {
  Card,
  CardContent,
  CardHeader,
  CardDescription,
  CardTitle,
  CardFooter,
} from "@ui/card";
import Image from "next/image";

const TopCryptoSection = () => {
  const [topCoins, setTopCoins] = useState<any[]>([]);

  useEffect(() => {
    const fetchTopCoins = async () => {
      const response = await fetch(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
      );
      const data = await response.json();
      setTopCoins(data);
    };

    // Call the function immediately
    fetchTopCoins();

    // Then set up the interval to call the function every 1 minute
    const intervalId = setInterval(fetchTopCoins, 60000); // 60000 milliseconds = 1 minute

    // Clear the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="w-full py-12 md:py-24 lg:py-32 bg-gradient-to-r from-indigo-500 via-purple-400 to-pink-400 text-white">
      <div className="space-y-12 px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <Badge className="px-3 py-1 text-sm ">Top Cryptocurrencies</Badge>
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl bg-clip-text">
              Stay Updated with Market Trends
            </h2>
            <p className="max-w-[900px] text-gray-100 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
              Get the latest prices and trends of the top cryptocurrencies in
              the market.
            </p>
          </div>
        </div>
        <div className="mx-auto sm:max-w-4xl lg:max-w-7xl">
          <Carousel
            className="w-full"
            plugins={[
              Autoplay({
                delay: 5000,
              }),
            ]}
          >
            <CarouselContent>
              {topCoins.map((coin) => (
                <CarouselItem
                  key={coin.id}
                  className="md:basis-1/3 lg:basis-1/5"
                >
                  <Card
                    key={coin.id}
                    className="w-full h-full flex flex-col items-center justify-center text-center"
                  >
                    <CardHeader className="flex items-center justify-center gap-2 pt-4">
                      <Image
                        src={coin.image}
                        alt={coin.name}
                        width={50}
                        height={50}
                        className="h-6 w-6"
                      />
                      <CardTitle>{coin.symbol.toUpperCase()}</CardTitle>
                      <CardDescription className="flex flex-col items-center justify-center">
                        <p className="text-sm text-gray-600">
                          High 24h: ${coin.high_24h.toLocaleString()}
                        </p>
                        <p className="text-sm text-gray-600">
                          Low 24h: ${coin.low_24h.toLocaleString()}
                        </p>
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="flex flex-col items-center justify-center">
                      <div className="mb-3">
                        <p className="text-lg font-bold">
                          ${coin.current_price.toLocaleString()}
                        </p>
                        <p
                          className={`text-sm ${
                            coin.price_change_percentage_24h > 0
                              ? "text-green-600"
                              : "text-red-600"
                          }`}
                        >
                          24h: {coin.price_change_percentage_24h.toFixed(2)}%
                        </p>
                      </div>
                      <p className="text-sm text-gray-600">
                        Market Cap: ${(coin.market_cap / 1000000000).toFixed(2)}{" "}
                        B
                      </p>
                    </CardContent>
                    <CardContent className="flex justify-center">
                      <a
                        href={`https://www.coingecko.com/en/coins/${coin.id}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline"
                      >
                        More info
                      </a>
                    </CardContent>
                  </Card>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </div>
      </div>
    </div>
  );
};

export default TopCryptoSection;
