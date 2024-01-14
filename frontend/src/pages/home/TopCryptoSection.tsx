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
} from "@ui/card";
import { Skeleton } from "@ui/skeleton";

interface Coin {
  id: string;
  name: string;
  symbol: string;
  image: string;
  current_price: number;
  high_24h: number;
  low_24h: number;
  price_change_percentage_24h: number;
  market_cap: number;
}

const TopCryptoSection = () => {
  const [topCoins, setTopCoins] = useState<Coin[]>([]);

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    const isDataStale = (timestamp: number) => {
      return new Date().getTime() - timestamp > 60000; // Data is stale if older than 60 seconds
    };

    const saveToLocalStorage = (data: Coin[]) => {
      const dataWithTimestamp = {
        timestamp: new Date().getTime(),
        data: data,
      };
      localStorage.setItem("topCoins", JSON.stringify(dataWithTimestamp));
    };

    const fetchTopCoins = async (retryCount = 0) => {
      try {
        const cachedData = localStorage.getItem("topCoins");
        const cachedObject = cachedData ? JSON.parse(cachedData) : null;
        if (cachedObject && !isDataStale(cachedObject.timestamp)) {
          setTopCoins(cachedObject.data);
          return;
        }
        const response = await fetch(
          "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1",
          { signal }
        );

        if (!response.ok) {
          if (response.status === 429 && retryCount < 3) {
            setTimeout(
              () => fetchTopCoins(retryCount + 1),
              Math.pow(2, retryCount) * 1000
            );
            return;
          }
          throw new Error("API request failed");
        }

        const data = await response.json();
        setTopCoins(data);
        saveToLocalStorage(data);
      } catch (error) {
        if (error instanceof DOMException && error.name === "AbortError") {
          return;
        }
        console.error(error);
        if (retryCount < 3) {
          setTimeout(
            () => fetchTopCoins(retryCount + 1),
            Math.pow(2, retryCount) * 1000
          );
        }
      }
    };

    fetchTopCoins();
    const intervalId = setInterval(() => fetchTopCoins(), 60000);

    return () => {
      clearInterval(intervalId);
      controller.abort();
    };
  }, []);

  return (
    <div className="w-full py-12 md:py-24 lg:py-32 bg-gradient-to-r from-cyan-500 via-purple-600 to-pink-500 text-white">
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
        {!topCoins.length ? (
          <div className="flex justify-center space-x-4 gap-4">
            {Array(5)
              .fill(0)
              .map((_, index) => (
                <div key={index} className="flex flex-col items-center">
                  <Skeleton className="h-24 w-24" />
                </div>
              ))}
          </div>
        ) : (
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
                        <img
                          src={coin.image}
                          alt={coin.name}
                          width={50}
                          height={50}
                          className="h-6 w-6"
                        />
                        <CardTitle>{coin.symbol.toUpperCase()}</CardTitle>
                        <CardDescription className="flex flex-col items-center justify-center">
                          <span className="text-sm text-gray-600">
                            High 24h: ${coin.high_24h.toLocaleString()}
                          </span>
                          <span className="text-sm text-gray-600">
                            Low 24h: ${coin.low_24h.toLocaleString()}
                          </span>
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
                          Market Cap: $
                          {(coin.market_cap / 1000000000).toFixed(2)} B
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
        )}
      </div>
    </div>
  );
};

export default TopCryptoSection;
