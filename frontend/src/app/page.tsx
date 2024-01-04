"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useState } from "react";
import { Input } from "@ui/input";
import { Button } from "@ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardDescription,
  CardTitle,
  CardFooter,
} from "@ui/card";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
} from "@ui/navigation-menu";
import { Badge } from "@ui/badge";
import { AspectRatio } from "@ui/aspect-ratio";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@ui/carousel";
import Autoplay from "embla-carousel-autoplay";

export default function Home() {
  const [topCoins, setTopCoins] = useState<any[]>([]);
  const [news, setNews] = useState<any[]>([]);

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

  useEffect(() => {
    const fetchNews = async () => {
      const response = await fetch(
        `https://newsapi.org/v2/everything?q=crypto+OR+ethereum+OR+bitcoin&language=en&sortBy=publishedAt&pageSize=3&apiKey=${process.env.NEXT_PUBLIC_NEWS_API_KEY}`
      );
      const data = await response.json();
      setNews(data.articles);
    };

    fetchNews();

    const intervalId = setInterval(fetchNews, 60000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      <div className="p-4 lg:px-6 h-14 flex items-center bg-gradient-to-r from-indigo-200 via-purple-500 to-pink-200">
        <Link className="flex items-center gap-2" href="/">
          <Image
            src="/logo_without_text.svg"
            alt="CryptoTracker"
            width={50}
            height={50}
            layout="fixed"
          />
          <span className="ml-2 text-lg font-bold">Datablevn</span>
        </Link>
        <div className="ml-auto flex gap-4 sm:gap-6">
          <NavigationMenu>
            <NavigationMenuList>
              <NavigationMenuItem>
                <NavigationMenuLink
                  className="content-center pr-2 hover:underline "
                  href="/news"
                >
                  News
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <NavigationMenuLink
                  className="content-center pr-2 hover:underline "
                  href="/contact"
                >
                  Contact
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <NavigationMenuLink className="pr-2" href="/login">
                  <Button className="w-20 bg-gray-200 text-black hover:text-white">
                    Login
                  </Button>
                </NavigationMenuLink>
              </NavigationMenuItem>
              <NavigationMenuItem>
                <NavigationMenuLink className="" href="/register">
                  <Button className="w-20 bg-gray-200 text-black hover:text-white">
                    Register
                  </Button>
                </NavigationMenuLink>
              </NavigationMenuItem>
            </NavigationMenuList>
          </NavigationMenu>
        </div>
      </div>
      <div className="flex-1">
        <div className="w-full py-12 md:py-20 lg:py-26 border-y">
          <div className="px-4 md:px-6 space-y-10 xl:space-y-16">
            <div className="grid max-w-[1300px] mx-auto gap-4 px-4 sm:px-6 md:px-10 md:grid-cols-2 md:gap-16">
              <div>
                <h1 className="lg:leading-tighter text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl xl:text-[3.4rem] 2xl:text-[3.75rem] my-3 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500">
                  Track Your Cryptocurrencies Portfolio
                </h1>
                <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400">
                  Get real-time updates on the top cryptocurrencies, latest,
                  market trends, analytics, news, and more.
                </p>
              </div>
              <div className="flex flex-col items-start space-y-4">
                <AspectRatio ratio={16 / 9} className="w-full">
                  <Image
                    alt="Crypto Tracker"
                    className="mx-auto aspect-[5/3] overflow-hidden rounded-xl object-cover"
                    height="300"
                    src="/hero.png"
                    width="500"
                  />
                </AspectRatio>
              </div>
            </div>
          </div>
        </div>
        <div className="w-full py-12 md:py-24 lg:py-32 bg-gradient-to-r from-indigo-500 via-purple-400 to-pink-400 text-white">
          <div className="space-y-12 px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <Badge className="px-3 py-1 text-sm ">
                  Top Cryptocurrencies
                </Badge>
                <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl bg-clip-text">
                  Stay Updated with Market Trends
                </h2>
                <p className="max-w-[900px] text-gray-100 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                  Get the latest prices and trends of the top cryptocurrencies
                  in the market.
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
                              24h: {coin.price_change_percentage_24h.toFixed(2)}
                              %
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
          </div>
        </div>
        <div className="w-full py-12 md:py-24 lg:py-32 dark:bg-gray-800">
          <div className="grid items-center justify-center gap-4 px-4 text-center md:px-6">
            <div className="space-y-3">
              <h2 className="text-3xl font-bold tracking-tighter md:text-4xl/tight bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-500">
                Latest Cryptocurrency News
              </h2>
              <p className="mx-auto max-w-[600px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                Stay informed with the latest news and updates in the
                cryptocurrency world.
              </p>
            </div>
            <div className="mx-auto grid max-w-sm items-start gap-8 sm:max-w-4xl sm:grid-cols-2 md:gap-12 lg:max-w-7xl lg:grid-cols-3">
              {news.map((article, index) => (
                <Card
                  key={index}
                  className="flex flex-col bg-white dark:bg-gray-700 hover:shadow-xl h-full rounded-xl overflow-hidden shadow-lg transition-shadow duration-300"
                >
                  <CardHeader className="p-4 border-b dark:border-gray-600 flex flex-col justify-between flex-grow">
                    <AspectRatio
                      ratio={16 / 9}
                      className="w-full flex-shrink-0"
                    >
                      <Image
                        src={article.urlToImage || "/placeholder.svg"}
                        alt={article.title || "News"}
                        className="w-full h-48 object-cover"
                        width={500}
                        height={300}
                      />
                    </AspectRatio>
                    <CardTitle className="text-lg font-bold my-2">
                      {article.title || "Title not available"}
                    </CardTitle>
                  </CardHeader>
                  <div className="flex flex-col justify-center pt-2 px-4 flex-grow">
                    <div>
                      <CardDescription className="text-sm text-gray-700 dark:text-gray-400">
                        {article.description || "Description not available"}
                      </CardDescription>
                    </div>
                    <CardContent>
                      <a
                        href={article.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block mt-4 text-blue-600 hover:text-blue-800 transition-colors duration-300"
                      >
                        Read more
                      </a>
                      <CardFooter className="text-sm pt-4 justify-center text-gray-500 dark:text-gray-400 mt-2">
                        {article.publishedAt
                          ? new Date(article.publishedAt).toLocaleDateString(
                              "en-US",
                              {
                                year: "numeric",
                                month: "long",
                                day: "numeric",
                                hour: "2-digit",
                                minute: "2-digit",
                              }
                            )
                          : "Date not available"}
                      </CardFooter>
                    </CardContent>
                  </div>
                </Card>
              ))}
            </div>
            <Link href="/news" className="inline-block mt-8">
              <Button className="bg-pink-500 hover:bg-purple-500 text-white font-bold py-2 px-4 rounded">
                Explore All Crypto News
              </Button>
            </Link>
          </div>
        </div>
      </div>
      <div className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t bg-gray-200">
        <p className="text-xs text-gray-500 dark:text-gray-400">
          © CryptoTracker. All rights reserved.
        </p>
        <div className="sm:ml-auto flex gap-4 sm:gap-6">
          <Link className="text-xs hover:underline underline-offset-4" href="#">
            Facebook
          </Link>
          <Link className="text-xs hover:underline underline-offset-4" href="#">
            Twitter
          </Link>
          <Link className="text-xs hover:underline underline-offset-4" href="#">
            Instagram
          </Link>
        </div>
        <div className="mt-4 w-full max-w-sm mx-auto space-y-2">
          <form className="flex space-x-2">
            <Input
              className="max-w-lg flex-1"
              placeholder="Enter your email"
              type="email"
            />
            <Button type="submit">Subscribe</Button>
          </form>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Subscribe to get notified about latest updates.
          </p>
        </div>
      </div>
    </div>
  );
}
